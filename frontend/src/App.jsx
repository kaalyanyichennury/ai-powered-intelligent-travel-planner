import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import HeroPlanner from './components/HeroPlanner';
import TripOverview from './components/TripOverview';
import ItineraryView from './components/ItineraryView';
import InteractiveMap from './components/InteractiveMap';
import BudgetView from './components/BudgetView';
import AttractionsCarousel from './components/AttractionsCarousel';
import AIChatDrawer from './components/AIChatDrawer';
import SavedTripsModal from './components/SavedTripsModal';
import AnalyticsModal from './components/AnalyticsModal';
import ArchitectureModal from './components/ArchitectureModal';
import LoginPage from './components/LoginPage';
import { generatePlanFromNL, generatePlanFromForm, saveTripPlan, getSavedTrips, sendChatMessage, signInUser, getCurrentUser } from './services/api';
import { Sparkles, MessageSquare, AlertCircle } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('planner');
  const [currentPlan, setCurrentPlan] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [savedCount, setSavedCount] = useState(0);
  const [errorMessage, setErrorMessage] = useState(null);
  const [showLogin, setShowLogin] = useState(true);
  const [user, setUser] = useState(null);

  // Modals state
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isSavedOpen, setIsSavedOpen] = useState(false);
  const [isAnalyticsOpen, setIsAnalyticsOpen] = useState(false);
  const [isArchOpen, setIsArchOpen] = useState(false);

  // Refresh saved trips count
  const refreshSavedCount = async () => {
    try {
      const trips = await getSavedTrips();
      setSavedCount(trips.length);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('aerovoyage_session_token');
    if (!token) {
      setShowLogin(true);
      return;
    }

    getCurrentUser(token)
      .then((userData) => {
        setUser(userData);
        setShowLogin(false);
      })
      .catch(() => {
        localStorage.removeItem('aerovoyage_session_token');
        localStorage.removeItem('aerovoyage_user');
        setUser(null);
        setShowLogin(true);
      });
  }, []);

  useEffect(() => {
    if (!showLogin) refreshSavedCount();
  }, [showLogin]);

  if (showLogin) {
    return (
      <LoginPage
        onContinueAsGuest={() => {
          localStorage.removeItem('aerovoyage_session_token');
          localStorage.removeItem('aerovoyage_user');
          setUser(null);
          setShowLogin(false);
        }}
        onSignIn={async (email, password) => {
          try {
            const session = await signInUser(email, password);
            localStorage.setItem('aerovoyage_session_token', session.token);
            localStorage.setItem('aerovoyage_user', JSON.stringify(session.user));
            setUser(session.user);
            setShowLogin(false);
          } catch (error) {
            throw error;
          }
        }}
      />
    );
  }

  // Handle plan generation
  const handlePlanTrip = async (req) => {
    setIsGenerating(true);
    setErrorMessage(null);
    try {
      let plan;
      if (req.type === 'nl') {
        plan = await generatePlanFromNL(req.query);
      } else {
        plan = await generatePlanFromForm(req.data);
      }
      setCurrentPlan(plan);
      setActiveTab('itinerary');
      refreshSavedCount();
    } catch (err) {
      console.error(err);
      setErrorMessage("Failed to generate travel plan. Please ensure the backend server is running on http://localhost:8000.");
    } finally {
      setIsGenerating(false);
    }
  };

  // Handle saving current plan to database
  const handleSaveTrip = async () => {
    if (!currentPlan) return;
    setIsSaving(true);
    try {
      await saveTripPlan(currentPlan);
      await refreshSavedCount();
      alert("✅ Itinerary successfully saved to SQLite database!");
    } catch (err) {
      console.error(err);
      alert("Could not save trip. Please check backend connection.");
    } finally {
      setIsSaving(false);
    }
  };

  // Quick swap activity from ItineraryView
  const handleQuickSwap = async (dayNumber, slot) => {
    if (!currentPlan) return;
    setIsChatOpen(true);
  };

  const currencySymbol = currentPlan?.budget_breakdown?.symbol || "$";

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenSaved={() => setIsSavedOpen(true)}
        onOpenAnalytics={() => setIsAnalyticsOpen(true)}
        onOpenArch={() => setIsArchOpen(true)}
        savedCount={savedCount}
      />

      {/* Main Content Area */}
      <main className="flex-1 pb-16">
        {errorMessage && (
          <div className="max-w-4xl mx-auto my-4 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs sm:text-sm flex items-center gap-2">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span>{errorMessage}</span>
          </div>
        )}

        {/* View Tab: Planner */}
        {activeTab === 'planner' && (
          <div>
            <HeroPlanner onPlanTrip={handlePlanTrip} isGenerating={isGenerating} />
            {currentPlan && (
              <div className="text-center pb-8">
                <button
                  onClick={() => setActiveTab('itinerary')}
                  className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-indigo-300 border border-indigo-500/30 text-xs font-bold transition-colors"
                >
                  <Sparkles className="w-4 h-4 text-cyan-400" />
                  View Generated Itinerary for {currentPlan.destination} →
                </button>
              </div>
            )}
          </div>
        )}

        {/* Generated Plan Views */}
        {currentPlan && (
          <>
            {activeTab !== 'planner' && (
              <TripOverview
                plan={currentPlan}
                onSaveTrip={handleSaveTrip}
                onOpenChat={() => setIsChatOpen(true)}
                isSaving={isSaving}
              />
            )}

            {/* Tab: Itinerary & Map */}
            {activeTab === 'itinerary' && (
              <div>
                <InteractiveMap itinerary={currentPlan.itinerary} />
                <ItineraryView
                  itinerary={currentPlan.itinerary}
                  currencySymbol={currencySymbol}
                  onQuickSwap={handleQuickSwap}
                />
              </div>
            )}

            {/* Tab: Budget */}
            {activeTab === 'budget' && (
              <BudgetView budgetBreakdown={currentPlan.budget_breakdown} />
            )}

            {/* Tab: Recommendations */}
            {activeTab === 'recommendations' && (
              <AttractionsCarousel
                attractions={currentPlan.recommended_attractions}
                currencySymbol={currencySymbol}
              />
            )}
          </>
        )}

        {/* If no plan generated yet and user clicks Itinerary/Budget/Recommendations */}
        {!currentPlan && activeTab !== 'planner' && (
          <div className="max-w-2xl mx-auto my-16 p-8 rounded-2xl bg-slate-900 border border-slate-800 text-center">
            <Sparkles className="w-12 h-12 text-indigo-400 mx-auto mb-3 opacity-60" />
            <h3 className="text-lg font-bold text-white mb-2">No Active Itinerary Yet</h3>
            <p className="text-xs sm:text-sm text-slate-400 mb-6">
              Enter your destination prompt or select a demo preset to generate a full agentic travel plan.
            </p>
            <button
              onClick={() => setActiveTab('planner')}
              className="px-6 py-2.5 rounded-xl text-xs font-bold bg-indigo-600 hover:bg-indigo-500 text-white transition-colors"
            >
              Go to Trip Planner
            </button>
          </div>
        )}
      </main>

      {/* Floating AI Assistant Chat Trigger (Visible on all screens) */}
      <button
        onClick={() => setIsChatOpen(true)}
        className="fixed bottom-6 right-6 z-30 flex items-center gap-2 px-4 py-3 rounded-full bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-600 hover:to-cyan-600 text-white font-bold text-xs sm:text-sm shadow-xl shadow-indigo-500/30 transform hover:scale-105 active:scale-95 transition-all no-print"
      >
        <MessageSquare className="w-4 h-4" />
        <span>Ask Travel AI & Modify</span>
      </button>

      {/* Modals & Drawers */}
      <AIChatDrawer
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        currentPlan={currentPlan}
        onPlanUpdated={(newPlan) => setCurrentPlan(newPlan)}
      />

      <SavedTripsModal
        isOpen={isSavedOpen}
        onClose={() => setIsSavedOpen(false)}
        onLoadTrip={(loadedPlan) => {
          setCurrentPlan(loadedPlan);
          setActiveTab('itinerary');
        }}
      />

      <AnalyticsModal
        isOpen={isAnalyticsOpen}
        onClose={() => setIsAnalyticsOpen(false)}
      />

      <ArchitectureModal
        isOpen={isArchOpen}
        onClose={() => setIsArchOpen(false)}
      />
    </div>
  );
}

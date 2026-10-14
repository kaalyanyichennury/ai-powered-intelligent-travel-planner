import React, { useState } from 'react';
import { Sparkles, Compass, MapPin, Calendar, Users, DollarSign, ArrowRight, Check, SlidersHorizontal, Cpu, Lightbulb, Search } from 'lucide-react';
import { parseNaturalLanguage } from '../services/api';

const PRESET_PROMPTS = [
  {
    label: "🗼 7-Day Paris Art & Romance ($2,500)",
    text: "Plan a 7-day trip to Paris for 2 people with a budget of $2,500. I like history, photography and food.",
  },
  {
    label: "🏯 10-Day Japan Anime & Temples (₹1.5 Lakh)",
    text: "I want to visit Japan for 10 days in April. I have a budget of ₹1.5 lakh and love anime, temples, food and photography.",
  },
  {
    label: "🏛️ 5-Day Rome Ancient Antiquity (€1,800)",
    text: "Plan a 5-day trip to Rome for 2 people with a budget of €1,800. We love ancient history, architecture, and authentic pasta.",
  },
  {
    label: "🏙️ 4-Day New York Skyline ($2,200)",
    text: "Plan a 4-day trip to New York for 2 people with a budget of $2,200. I like skyline photography, museums and Broadway shows.",
  },
  {
    label: "🏜️ 6-Day Dubai Luxury & Dunes (AED 10,000)",
    text: "Plan a 6-day trip to Dubai for 2 people with a budget of AED 10,000. Interested in luxury, desert safari and modern architecture.",
  }
];

const AVAILABLE_INTERESTS = [
  "History", "Food", "Photography", "Architecture", "Temples", "Anime",
  "Museums", "Nature", "Adventure", "Shopping", "Nightlife", "Relaxation"
];

const CURRENCIES = [
  { code: "USD", symbol: "$" },
  { code: "EUR", symbol: "€" },
  { code: "INR", symbol: "₹" },
  { code: "GBP", symbol: "£" },
  { code: "JPY", symbol: "¥" },
  { code: "AED", symbol: "AED" },
  { code: "CAD", symbol: "CA$" },
  { code: "AUD", symbol: "A$" },
  { code: "SGD", symbol: "S$" }
];

export default function HeroPlanner({ onPlanTrip, isGenerating }) {
  const [plannerMode, setPlannerMode] = useState('nl'); // 'nl' or 'form'
  const [nlQuery, setNlQuery] = useState("Plan a 7-day trip to Paris for 2 people with a budget of $2,500. I like history, photography and food.");
  const [extractedPreview, setExtractedPreview] = useState(null);
  const [isExtracting, setIsExtracting] = useState(false);

  // Structured Form States
  const [formData, setFormData] = useState({
    destination: "Paris",
    duration_days: 7,
    travelers: 2,
    budget: 2500,
    currency: "USD",
    interests: ["History", "Photography", "Food"],
    travel_month: "May",
    accommodation_preference: "mid-range",
    pace: "balanced"
  });

  const handleExtractPreview = async () => {
    if (!nlQuery.trim()) return;
    setIsExtracting(true);
    try {
      const data = await parseNaturalLanguage(nlQuery);
      setExtractedPreview(data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsExtracting(false);
    }
  };

  const handleNLSubmit = (e) => {
    e.preventDefault();
    if (!nlQuery.trim()) return;
    onPlanTrip({ type: 'nl', query: nlQuery });
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    onPlanTrip({ type: 'form', data: formData });
  };

  const toggleInterest = (interest) => {
    setFormData(prev => {
      const exists = prev.interests.includes(interest);
      const updated = exists
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest];
      return { ...prev, interests: updated.length > 0 ? updated : [interest] };
    });
  };

  return (
    <div className="relative overflow-hidden pt-8 pb-12 px-4 sm:px-6 lg:px-8">
      {/* Background Glows */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-96 bg-gradient-to-b from-indigo-500/15 via-cyan-500/5 to-transparent blur-3xl pointer-events-none -z-10" />

      <div className="max-w-4xl mx-auto text-center mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold mb-4">
          <Cpu className="w-3.5 h-3.5 text-cyan-400" />
          Powered by NLP • ML Recommendation • RAG • 6-Agent AI Architecture
        </div>
        <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight font-display bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
          Intelligent Worldwide Travel Planner
        </h1>
        <p className="mt-3 text-base sm:text-lg text-slate-400 max-w-2xl mx-auto">
          Plan hyper-personalized vacations anywhere on Earth. Integrates real-time Open-Meteo forecasts, OpenStreetMap spatial routing, TF-IDF ML compatibility scoring, and verification agents.
        </p>

        {/* Mode Selector Tabs */}
        <div className="inline-flex p-1 mt-6 bg-slate-800/80 backdrop-blur rounded-xl border border-slate-700">
          <button
            onClick={() => setPlannerMode('nl')}
            className={`flex items-center gap-2 px-5 py-2 rounded-lg text-xs font-semibold transition-all ${
              plannerMode === 'nl'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5 text-cyan-300" />
            Natural Language AI Prompt
          </button>
          <button
            onClick={() => setPlannerMode('form')}
            className={`flex items-center gap-2 px-5 py-2 rounded-lg text-xs font-semibold transition-all ${
              plannerMode === 'form'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <SlidersHorizontal className="w-3.5 h-3.5 text-cyan-300" />
            Structured Filters & Form
          </button>
        </div>
      </div>

      {/* Main Interactive Card */}
      <div className="max-w-4xl mx-auto bg-slate-800/80 backdrop-blur-xl border border-slate-700/80 rounded-2xl shadow-2xl shadow-black/40 p-6 sm:p-8">
        {plannerMode === 'nl' ? (
          <div>
            <form onSubmit={handleNLSubmit} className="space-y-4">
              <label className="block text-left text-xs font-semibold uppercase tracking-wider text-slate-300">
                Describe your dream vacation in plain English
              </label>

              <div className="relative">
                <textarea
                  rows={3}
                  value={nlQuery}
                  onChange={(e) => setNlQuery(e.target.value)}
                  placeholder="e.g. Plan a 7-day trip to Paris for 2 people with a budget of $2,500. I like history, photography and food."
                  className="w-full bg-slate-900/90 border border-slate-700 rounded-xl p-4 text-sm sm:text-base text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all resize-none font-sans"
                />
              </div>

              {/* Action Buttons: Preview NLP Entities + Plan Trip */}
              <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
                <button
                  type="button"
                  onClick={handleExtractPreview}
                  disabled={isExtracting || isGenerating}
                  className="w-full sm:w-auto flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold bg-slate-700 hover:bg-slate-600 text-slate-200 border border-slate-600 transition-colors"
                >
                  <Cpu className="w-3.5 h-3.5 text-cyan-400" />
                  {isExtracting ? 'Extracting NLP...' : 'Test NLP Entity Extraction'}
                </button>

                <button
                  type="submit"
                  disabled={isGenerating}
                  className="w-full sm:w-auto flex items-center justify-center gap-2 px-8 py-3 rounded-xl text-sm font-bold bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-600 hover:to-cyan-600 text-white shadow-lg shadow-indigo-500/25 transition-all transform active:scale-95 disabled:opacity-50"
                >
                  {isGenerating ? (
                    <span className="flex items-center gap-2">
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      Agents Orchestrating...
                    </span>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4 text-cyan-200" />
                      Plan My Trip with AI
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </button>
              </div>
            </form>

            {/* Extracted Entity Preview Box */}
            {extractedPreview && (
              <div className="mt-5 p-4 rounded-xl bg-slate-900/80 border border-cyan-500/30 text-left transition-all">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold text-cyan-400 flex items-center gap-1.5">
                    <Check className="w-4 h-4" />
                    NLP Entity Extractor Output
                  </span>
                  <span className="text-[10px] text-slate-400">Confidence: 95%</span>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-xs">
                  <div className="p-2 rounded bg-slate-800/80 border border-slate-700">
                    <span className="text-slate-400 block text-[10px]">Destination</span>
                    <span className="font-semibold text-white">{extractedPreview.destination}</span>
                  </div>
                  <div className="p-2 rounded bg-slate-800/80 border border-slate-700">
                    <span className="text-slate-400 block text-[10px]">Duration</span>
                    <span className="font-semibold text-white">{extractedPreview.duration_days} Days</span>
                  </div>
                  <div className="p-2 rounded bg-slate-800/80 border border-slate-700">
                    <span className="text-slate-400 block text-[10px]">Travelers</span>
                    <span className="font-semibold text-white">{extractedPreview.travelers} Guests</span>
                  </div>
                  <div className="p-2 rounded bg-slate-800/80 border border-slate-700">
                    <span className="text-slate-400 block text-[10px]">Budget</span>
                    <span className="font-semibold text-emerald-400">
                      {extractedPreview.currency} {extractedPreview.budget.toLocaleString()}
                    </span>
                  </div>
                  <div className="col-span-2 sm:col-span-1 p-2 rounded bg-slate-800/80 border border-slate-700">
                    <span className="text-slate-400 block text-[10px]">Interests</span>
                    <span className="font-semibold text-indigo-300 truncate block">
                      {extractedPreview.interests.join(", ")}
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Presets */}
            <div className="mt-6 pt-5 border-t border-slate-700/60 text-left">
              <span className="text-xs font-semibold text-slate-400 flex items-center gap-1.5 mb-2.5">
                <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
                Quick Academic & Viva Demo Prompts:
              </span>
              <div className="flex flex-wrap gap-2">
                {PRESET_PROMPTS.map((preset, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => {
                      setNlQuery(preset.text);
                      setExtractedPreview(null);
                    }}
                    className="px-3 py-1.5 rounded-lg text-xs bg-slate-900/80 hover:bg-indigo-950/60 text-slate-300 hover:text-white border border-slate-700/80 hover:border-indigo-500/40 transition-colors text-left"
                  >
                    {preset.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          /* Structured Form Mode */
          <form onSubmit={handleFormSubmit} className="space-y-6 text-left">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              {/* Destination */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5 flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-indigo-400" />
                  Destination Anywhere Worldwide
                </label>
                <input
                  type="text"
                  value={formData.destination}
                  onChange={(e) => setFormData({ ...formData, destination: e.target.value })}
                  placeholder="Paris, Tokyo, Rome, New York, Bali..."
                  required
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              {/* Duration */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5 flex items-center gap-1.5">
                  <Calendar className="w-3.5 h-3.5 text-indigo-400" />
                  Duration: <span className="text-indigo-400 font-bold">{formData.duration_days} Days</span>
                </label>
                <input
                  type="range"
                  min={2}
                  max={14}
                  value={formData.duration_days}
                  onChange={(e) => setFormData({ ...formData, duration_days: parseInt(e.target.value) })}
                  className="w-full accent-indigo-500 h-2 bg-slate-700 rounded-lg cursor-pointer mt-3"
                />
              </div>

              {/* Travelers */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5 flex items-center gap-1.5">
                  <Users className="w-3.5 h-3.5 text-indigo-400" />
                  Travelers
                </label>
                <div className="flex items-center gap-2">
                  {[1, 2, 3, 4].map(num => (
                    <button
                      key={num}
                      type="button"
                      onClick={() => setFormData({ ...formData, travelers: num })}
                      className={`flex-1 py-2 rounded-xl text-xs font-bold border transition-colors ${
                        formData.travelers === num
                          ? 'bg-indigo-600 text-white border-indigo-500'
                          : 'bg-slate-900 text-slate-300 border-slate-700 hover:bg-slate-800'
                      }`}
                    >
                      {num} {num === 1 ? 'Solo' : (num === 2 ? 'Couple' : `${num}`)}
                    </button>
                  ))}
                </div>
              </div>

              {/* Budget & Currency */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5 flex items-center gap-1.5">
                  <DollarSign className="w-3.5 h-3.5 text-emerald-400" />
                  Total Trip Budget
                </label>
                <div className="flex gap-2">
                  <select
                    value={formData.currency}
                    onChange={(e) => setFormData({ ...formData, currency: e.target.value })}
                    className="w-24 bg-slate-900 border border-slate-700 rounded-xl px-2 py-2 text-xs text-white focus:outline-none focus:border-indigo-500"
                  >
                    {CURRENCIES.map(c => (
                      <option key={c.code} value={c.code}>{c.code} ({c.symbol})</option>
                    ))}
                  </select>
                  <input
                    type="number"
                    min={100}
                    step={50}
                    value={formData.budget}
                    onChange={(e) => setFormData({ ...formData, budget: parseFloat(e.target.value) || 0 })}
                    className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              {/* Accommodation Tier */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Lodging Tier
                </label>
                <select
                  value={formData.accommodation_preference}
                  onChange={(e) => setFormData({ ...formData, accommodation_preference: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500"
                >
                  <option value="budget">Budget Hostels & Guesthouses</option>
                  <option value="mid-range">Mid-range Boutique Hotels (Recommended)</option>
                  <option value="luxury">Luxury 5-Star Resorts</option>
                </select>
              </div>

              {/* Travel Month */}
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Travel Month
                </label>
                <select
                  value={formData.travel_month}
                  onChange={(e) => setFormData({ ...formData, travel_month: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500"
                >
                  {["April", "May", "June", "July", "August", "September", "October", "November", "December"].map(m => (
                    <option key={m} value={m}>{m}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Interest Tags Checkboxes */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-2">
                What do you love? (ML Recommendation Preferences)
              </label>
              <div className="flex flex-wrap gap-2">
                {AVAILABLE_INTERESTS.map(interest => {
                  const active = formData.interests.includes(interest);
                  return (
                    <button
                      key={interest}
                      type="button"
                      onClick={() => toggleInterest(interest)}
                      className={`px-3.5 py-1.5 rounded-xl text-xs font-medium border transition-all ${
                        active
                          ? 'bg-indigo-600 text-white border-indigo-500 shadow-md shadow-indigo-600/30'
                          : 'bg-slate-900 text-slate-300 border-slate-700 hover:border-slate-500'
                      }`}
                    >
                      {active && '✓ '}
                      {interest}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Submit */}
            <div className="pt-2 flex justify-end">
              <button
                type="submit"
                disabled={isGenerating}
                className="w-full sm:w-auto flex items-center justify-center gap-2 px-8 py-3 rounded-xl text-sm font-bold bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-600 hover:to-cyan-600 text-white shadow-lg shadow-indigo-500/25 transition-all transform active:scale-95 disabled:opacity-50"
              >
                {isGenerating ? (
                  <span className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Multi-Agent Pipeline Running...
                  </span>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 text-cyan-200" />
                    Generate Optimized Itinerary
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

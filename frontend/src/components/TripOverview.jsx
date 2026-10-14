import React, { useState } from 'react';
import { ShieldCheck, CheckCircle2, AlertCircle, Bookmark, Printer, MessageSquare, MapPin, DollarSign, Calendar, Users, ChevronDown, ChevronUp } from 'lucide-react';

export default function TripOverview({ plan, onSaveTrip, onOpenChat, isSaving }) {
  const [showVerificationDetails, setShowVerificationDetails] = useState(false);
  const budget = plan.budget_breakdown;
  const verification = plan.verification;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
      <div className="bg-slate-800/90 border border-slate-700/80 rounded-2xl p-6 sm:p-8 backdrop-blur shadow-xl text-left">
        {/* Header row */}
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 pb-6 border-b border-slate-700">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-2">
              <span className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 flex items-center gap-1.5">
                <MapPin className="w-3.5 h-3.5 text-cyan-400" />
                {plan.cities.join(" • ")}
              </span>
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                {budget.status_label}
              </span>
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">
                {plan.country || "Worldwide"}
              </span>
            </div>

            <h2 className="text-2xl sm:text-3xl font-extrabold font-display text-white">
              {plan.duration_days}-Day Trip to {plan.destination}
            </h2>
            <p className="text-sm text-slate-400 mt-1 max-w-3xl">
              {plan.overview_description}
            </p>
          </div>

          {/* Quick Action Buttons */}
          <div className="flex flex-wrap items-center gap-2 no-print">
            <button
              onClick={onSaveTrip}
              disabled={isSaving}
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl text-xs font-bold bg-amber-500 hover:bg-amber-600 text-slate-950 transition-colors shadow-md shadow-amber-500/20"
            >
              <Bookmark className="w-4 h-4 fill-slate-950" />
              {isSaving ? 'Saving...' : 'Save Itinerary'}
            </button>

            <button
              onClick={handlePrint}
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl text-xs font-bold bg-slate-700 hover:bg-slate-600 text-slate-200 border border-slate-600 transition-colors"
            >
              <Printer className="w-4 h-4 text-slate-300" />
              Print / PDF
            </button>

            <button
              onClick={onOpenChat}
              className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-600 hover:to-cyan-600 text-white shadow-md shadow-indigo-500/25 transition-all"
            >
              <MessageSquare className="w-4 h-4" />
              Modify with AI
            </button>
          </div>
        </div>

        {/* Quick Highlights Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 py-6 border-b border-slate-700">
          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-700/60">
            <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
              <Calendar className="w-4 h-4 text-indigo-400" />
              Duration
            </div>
            <div className="text-lg font-bold text-white">{plan.duration_days} Days / {plan.duration_days - 1} Nights</div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-700/60">
            <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
              <Users className="w-4 h-4 text-indigo-400" />
              Travelers
            </div>
            <div className="text-lg font-bold text-white">{plan.travelers} Traveler(s)</div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-700/60">
            <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
              <DollarSign className="w-4 h-4 text-emerald-400" />
              User Budget
            </div>
            <div className="text-lg font-bold text-emerald-400">
              {budget.symbol}{budget.user_budget.toLocaleString()}
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-700/60">
            <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
              <DollarSign className="w-4 h-4 text-cyan-400" />
              Estimated Total
            </div>
            <div className="text-lg font-bold text-white">
              {budget.symbol}{budget.total_estimated.toLocaleString()}
            </div>
          </div>
        </div>

        {/* Multi-Agent Verification Checklist Banner */}
        <div className="mt-6 p-4 rounded-xl bg-slate-900/90 border border-indigo-500/30">
          <div 
            className="flex items-center justify-between cursor-pointer"
            onClick={() => setShowVerificationDetails(!showVerificationDetails)}
          >
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center border border-emerald-500/30">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-white">Verification Agent Audit</span>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/30">
                    {verification.score_percentage}% Feasibility Passed
                  </span>
                </div>
                <p className="text-xs text-slate-400">
                  Plan audited across 5 critical dimensions: budget limit, daily pacing, geographic proximity, weather safety, and attraction hours.
                </p>
              </div>
            </div>

            <button className="text-slate-400 hover:text-white p-1 rounded-lg">
              {showVerificationDetails ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
            </button>
          </div>

          {/* Expandable Verification Breakdown */}
          {showVerificationDetails && (
            <div className="mt-4 pt-4 border-t border-slate-800 space-y-2.5">
              {verification.checks.map((c, idx) => (
                <div key={idx} className="flex items-start gap-2.5 text-xs">
                  {c.passed ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                  ) : (
                    <AlertCircle className="w-4 h-4 text-amber-400 mt-0.5 flex-shrink-0" />
                  )}
                  <div>
                    <span className="font-semibold text-slate-200">{c.name}: </span>
                    <span className="text-slate-400">{c.details}</span>
                  </div>
                </div>
              ))}

              {verification.adjustments_made && verification.adjustments_made.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-800/80">
                  <span className="text-xs font-bold text-cyan-400 block mb-1">Automated Adjustments Made by Agents:</span>
                  <ul className="list-disc list-inside text-xs text-slate-400 space-y-1">
                    {verification.adjustments_made.map((adj, i) => (
                      <li key={i}>{adj}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

import React from 'react';
import { DollarSign, Plane, Hotel, Utensils, Ticket, Train, ShieldAlert, CheckCircle, TrendingUp, HelpCircle } from 'lucide-react';

export default function BudgetView({ budgetBreakdown }) {
  const b = budgetBreakdown;
  const sym = b.symbol;

  const categories = [
    {
      name: "Flights & Long-distance Travel",
      cost: b.flights_estimate,
      pct: Math.round((b.flights_estimate / b.total_estimated) * 100),
      icon: Plane,
      color: "bg-indigo-500",
      textColor: "text-indigo-400"
    },
    {
      name: "Hotel & Accommodations",
      cost: b.accommodation_estimate,
      pct: Math.round((b.accommodation_estimate / b.total_estimated) * 100),
      icon: Hotel,
      color: "bg-cyan-500",
      textColor: "text-cyan-400"
    },
    {
      name: "Food, Cafes & Fine Dining",
      cost: b.food_dining_estimate,
      pct: Math.round((b.food_dining_estimate / b.total_estimated) * 100),
      icon: Utensils,
      color: "bg-emerald-500",
      textColor: "text-emerald-400"
    },
    {
      name: "Attractions & Sightseeing Tickets",
      cost: b.activities_estimate,
      pct: Math.round((b.activities_estimate / b.total_estimated) * 100),
      icon: Ticket,
      color: "bg-amber-500",
      textColor: "text-amber-400"
    },
    {
      name: "Local City Transit & Metro Passes",
      cost: b.local_transit_estimate,
      pct: Math.round((b.local_transit_estimate / b.total_estimated) * 100),
      icon: Train,
      color: "bg-purple-500",
      textColor: "text-purple-400"
    },
    {
      name: "Contingency & Miscellaneous Buffer",
      cost: b.miscellaneous_estimate,
      pct: Math.round((b.miscellaneous_estimate / b.total_estimated) * 100),
      icon: HelpCircle,
      color: "bg-rose-500",
      textColor: "text-rose-400"
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-12 text-left">
      <div className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 sm:p-8 backdrop-blur shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-700">
          <div>
            <h3 className="text-xl sm:text-2xl font-bold font-display text-white flex items-center gap-2">
              <DollarSign className="w-6 h-6 text-emerald-400" />
              Budget Agent Financial Breakdown
            </h3>
            <p className="text-xs sm:text-sm text-slate-400">
              Granular expense modeling calculated in {b.currency} with live currency rates.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span className={`px-3 py-1.5 rounded-xl text-xs font-bold border flex items-center gap-1.5 ${
              b.is_within_budget
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                : 'bg-rose-500/10 text-rose-400 border-rose-500/20'
            }`}>
              {b.is_within_budget ? <CheckCircle className="w-4 h-4" /> : <ShieldAlert className="w-4 h-4" />}
              {b.status_label}
            </span>
          </div>
        </div>

        {/* Big Numbers Comparison */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 my-6">
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-700">
            <span className="text-xs text-slate-400 block mb-1">Your Total Budget</span>
            <div className="text-2xl sm:text-3xl font-extrabold text-white">
              {sym}{b.user_budget.toLocaleString()}
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-700">
            <span className="text-xs text-slate-400 block mb-1">Estimated Expenses</span>
            <div className="text-2xl sm:text-3xl font-extrabold text-indigo-300">
              {sym}{b.total_estimated.toLocaleString()}
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-700">
            <span className="text-xs text-slate-400 block mb-1">
              {b.balance >= 0 ? "Surplus Remaining" : "Estimated Deficit"}
            </span>
            <div className={`text-2xl sm:text-3xl font-extrabold ${b.balance >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
              {sym}{Math.abs(b.balance).toLocaleString()}
            </div>
          </div>
        </div>

        {/* Visual Stacked Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between text-xs text-slate-400 mb-2 font-medium">
            <span>Expense Distribution</span>
            <span>100% of Estimated Cost</span>
          </div>
          <div className="h-4 w-full bg-slate-900 rounded-full overflow-hidden flex shadow-inner">
            {categories.map((cat, idx) => (
              <div
                key={idx}
                className={`${cat.color} transition-all duration-500`}
                style={{ width: `${cat.pct}%` }}
                title={`${cat.name}: ${cat.pct}%`}
              />
            ))}
          </div>
        </div>

        {/* Detailed Category Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {categories.map((cat, idx) => {
            const Icon = cat.icon;
            return (
              <div key={idx} className="p-4 rounded-xl bg-slate-900/60 border border-slate-700/60 flex items-start gap-3">
                <div className={`p-2.5 rounded-lg bg-slate-800 ${cat.textColor}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-slate-300">{cat.name}</span>
                    <span className="text-xs text-slate-500 font-bold">{cat.pct}%</span>
                  </div>
                  <div className="text-lg font-bold text-white mt-1">
                    {sym}{cat.cost.toLocaleString()}
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Currency & Cost Saving Tips */}
        <div className="mt-8 p-4 rounded-xl bg-indigo-950/30 border border-indigo-500/20 text-xs text-indigo-300">
          <div className="flex items-center gap-2 font-bold mb-1 text-white">
            <TrendingUp className="w-4 h-4 text-cyan-400" />
            Currency & Smart Budget Tips
          </div>
          <p className="text-slate-400">
            • Conversion baseline: 1 USD ≈ {b.currency_rate_to_usd} {b.currency}.
            • To reduce expenses by 15-20%, purchase city transit multi-day passes (Navigo / Suica / Roma Pass) and pre-book museum entry slots online to avoid surcharges.
          </p>
        </div>
      </div>
    </div>
  );
}

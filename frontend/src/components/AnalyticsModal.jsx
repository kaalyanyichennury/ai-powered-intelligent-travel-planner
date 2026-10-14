import React, { useEffect, useState } from 'react';
import { X, BarChart3, TrendingUp, Globe, Sparkles, PieChart, Clock } from 'lucide-react';
import { getAnalyticsDashboard } from '../services/api';

export default function AnalyticsModal({ isOpen, onClose }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      getAnalyticsDashboard()
        .then(res => setData(res))
        .catch(err => console.error(err))
        .finally(() => setLoading(false));
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-3xl overflow-hidden shadow-2xl animate-in fade-in zoom-in-95 duration-200 text-left">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center border border-cyan-500/30">
              <BarChart3 className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">Data Science & Analytics Admin Dashboard</h3>
              <p className="text-xs text-slate-400">Statistical aggregation over all global generated trips</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 max-h-[75vh] overflow-y-auto space-y-6">
          {loading || !data ? (
            <div className="text-center py-12 text-slate-400 text-sm">
              Loading Data Science metrics from analytics engine...
            </div>
          ) : (
            <>
              {/* Metric Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="p-4 rounded-xl bg-slate-800/80 border border-slate-700">
                  <div className="flex items-center gap-2 text-xs text-slate-400 mb-1">
                    <Globe className="w-4 h-4 text-cyan-400" />
                    Total Trips Generated
                  </div>
                  <div className="text-2xl font-extrabold text-white">
                    {data.total_trips_planned}
                  </div>
                  <span className="text-[11px] text-emerald-400 font-semibold mt-1 block">
                    ↑ Continuously updating
                  </span>
                </div>

                <div className="p-4 rounded-xl bg-slate-800/80 border border-slate-700">
                  <div className="flex items-center gap-2 text-xs text-slate-400 mb-1">
                    <TrendingUp className="w-4 h-4 text-emerald-400" />
                    Average Trip Budget
                  </div>
                  <div className="text-2xl font-extrabold text-emerald-400">
                    ${data.average_trip_budget_usd.toLocaleString()}
                  </div>
                  <span className="text-[11px] text-slate-400 mt-1 block">
                    Normalized in USD
                  </span>
                </div>

                <div className="p-4 rounded-xl bg-slate-800/80 border border-slate-700">
                  <div className="flex items-center gap-2 text-xs text-slate-400 mb-1">
                    <Sparkles className="w-4 h-4 text-indigo-400" />
                    Top Requested Destination
                  </div>
                  <div className="text-2xl font-extrabold text-indigo-300">
                    {data.top_destinations[0]?.destination || "Paris"}
                  </div>
                  <span className="text-[11px] text-slate-400 mt-1 block">
                    {data.top_destinations[0]?.trips_count || 1} inquiries
                  </span>
                </div>
              </div>

              {/* Chart 1: Popular Destinations Bar Chart */}
              <div className="p-5 rounded-xl bg-slate-800/60 border border-slate-700">
                <h4 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
                  <BarChart3 className="w-4 h-4 text-indigo-400" />
                  Popular Global Destinations (Trips Count)
                </h4>
                <div className="space-y-3">
                  {data.top_destinations.map((dest, idx) => {
                    const maxVal = Math.max(...data.top_destinations.map(d => d.trips_count), 1);
                    const pct = Math.round((dest.trips_count / maxVal) * 100);
                    return (
                      <div key={idx} className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span className="font-semibold text-slate-200">{dest.destination}</span>
                          <span className="text-indigo-400 font-bold">{dest.trips_count} trips</span>
                        </div>
                        <div className="w-full h-2.5 bg-slate-900 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400 rounded-full transition-all duration-500"
                            style={{ width: `${pct}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Chart 2: Popular Travel Categories Distribution */}
              <div className="p-5 rounded-xl bg-slate-800/60 border border-slate-700">
                <h4 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
                  <PieChart className="w-4 h-4 text-cyan-400" />
                  Travel Category Preference Distribution
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {data.top_categories.map((cat, idx) => (
                    <div key={idx} className="p-3 rounded-lg bg-slate-900/60 border border-slate-700/60 flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="w-2.5 h-2.5 rounded-full bg-cyan-400" />
                        <span className="text-xs font-semibold text-slate-300">{cat.category}</span>
                      </div>
                      <div className="text-right">
                        <span className="text-xs font-bold text-white">{cat.percentage}%</span>
                        <span className="text-[10px] text-slate-500 block">({cat.count} selections)</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Chart 3: Duration Preferences */}
              <div className="p-5 rounded-xl bg-slate-800/60 border border-slate-700">
                <h4 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
                  <Clock className="w-4 h-4 text-amber-400" />
                  Preferred Trip Durations
                </h4>
                <div className="flex flex-wrap gap-2">
                  {data.popular_durations.map((dur, idx) => (
                    <div key={idx} className="px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-700 text-xs">
                      <span className="text-slate-400 block text-[10px]">Duration</span>
                      <span className="font-bold text-white">{dur.duration}</span>
                      <span className="text-[10px] text-indigo-400 ml-1.5 font-semibold">({dur.count} trips)</span>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

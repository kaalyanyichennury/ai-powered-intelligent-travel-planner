import React from 'react';
import { Star, Clock, DollarSign, Sparkles, Check, Tag } from 'lucide-react';

export default function AttractionsCarousel({ attractions, currencySymbol }) {
  if (!attractions || attractions.length === 0) return null;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-12 text-left">
      <div className="mb-6">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-semibold mb-2">
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
          TF-IDF Vector Space + Cosine Similarity Recommendation
        </div>
        <h3 className="text-xl sm:text-2xl font-bold font-display text-white">
          Machine Learning Ranked Attractions
        </h3>
        <p className="text-xs sm:text-sm text-slate-400">
          Ranked using content-based vector embeddings matching your interest profile with place metadata.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {attractions.map((place, idx) => {
          const matchPct = Math.round((place.compatibility_score || 0.85) * 100);
          return (
            <div
              key={place.place_id || idx}
              className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-5 backdrop-blur shadow-xl hover:border-indigo-500/50 transition-all flex flex-col justify-between"
            >
              <div>
                {/* Header with Match % and Category */}
                <div className="flex items-center justify-between gap-2 mb-3">
                  <span className="px-2.5 py-1 rounded-lg text-xs font-extrabold bg-gradient-to-r from-indigo-500/20 to-purple-500/20 text-indigo-300 border border-indigo-500/30">
                    {matchPct}% Compatibility
                  </span>
                  <div className="flex items-center gap-1 text-xs font-bold text-amber-400">
                    <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                    {place.rating}
                  </div>
                </div>

                <h4 className="text-lg font-bold text-white mb-1">{place.name}</h4>
                <div className="flex items-center gap-2 text-xs text-slate-400 mb-3">
                  <span>{place.category}</span>
                  <span>•</span>
                  <span>{place.indoor_outdoor}</span>
                  <span>•</span>
                  <span>{place.city}</span>
                </div>

                <p className="text-xs text-slate-400 line-clamp-3 mb-4">
                  {place.description}
                </p>
              </div>

              <div>
                {/* Match Reasons */}
                {place.match_reasons && place.match_reasons.length > 0 && (
                  <div className="mb-4 pt-3 border-t border-slate-700/70">
                    <span className="text-[11px] font-semibold text-slate-400 block mb-1">
                      Why ML Recommended This:
                    </span>
                    <div className="space-y-1">
                      {place.match_reasons.slice(0, 2).map((reason, rIdx) => (
                        <div key={rIdx} className="flex items-center gap-1.5 text-xs text-cyan-300">
                          <Check className="w-3 h-3 text-cyan-400 flex-shrink-0" />
                          <span className="truncate">{reason}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Footer specs */}
                <div className="flex items-center justify-between text-xs text-slate-400 pt-3 border-t border-slate-700/70">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5 text-indigo-400" />
                    ~{place.visit_duration_hrs}h visit
                  </span>
                  <span className="font-bold text-emerald-400">
                    {place.price === 0 ? "Free Entry" : `${currencySymbol}${place.price}`}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

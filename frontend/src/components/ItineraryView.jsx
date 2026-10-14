import React, { useState } from 'react';
import { Sun, CloudRain, Clock, MapPin, Navigation, DollarSign, ArrowDown, Utensils, Compass, Sparkles } from 'lucide-react';

export default function ItineraryView({ itinerary, currencySymbol, onQuickSwap }) {
  const [selectedDayIndex, setSelectedDayIndex] = useState(0); // 0 = Day 1, or 'all'

  const activeDays = selectedDayIndex === 'all' ? itinerary : [itinerary[selectedDayIndex]];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-12 text-left">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h3 className="text-xl sm:text-2xl font-bold font-display text-white flex items-center gap-2">
            <Compass className="w-6 h-6 text-indigo-400" />
            Day-by-Day Schedule & Spatial Route
          </h3>
          <p className="text-xs sm:text-sm text-slate-400">
            Sequenced using Nearest-Neighbor spatial routing to minimize cross-city commute times.
          </p>
        </div>

        {/* Day selector tabs */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-2 sm:pb-0 scrollbar-none">
          <button
            onClick={() => setSelectedDayIndex('all')}
            className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-colors flex-shrink-0 ${
              selectedDayIndex === 'all'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
          >
            All Days
          </button>
          {itinerary.map((d, idx) => (
            <button
              key={d.day_number}
              onClick={() => setSelectedDayIndex(idx)}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-colors flex-shrink-0 ${
                selectedDayIndex === idx
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              Day {d.day_number}
            </button>
          ))}
        </div>
      </div>

      {/* Daily Cards */}
      <div className="space-y-8">
        {activeDays.map((day) => {
          const weather = day.weather_summary || {};
          return (
            <div
              key={day.day_number}
              className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 sm:p-8 backdrop-blur shadow-xl transition-all"
            >
              {/* Day Header with Weather */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-700">
                <div>
                  <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">
                    Day {day.day_number} • {day.city}
                  </span>
                  <h4 className="text-xl font-extrabold text-white mt-0.5">{day.title}</h4>
                </div>

                {/* Weather Forecast Badge */}
                <div className="flex items-center gap-3 bg-slate-900/80 px-4 py-2.5 rounded-xl border border-slate-700">
                  <span className="text-2xl">{weather.icon || "🌤️"}</span>
                  <div>
                    <div className="text-xs font-bold text-white flex items-center gap-1.5">
                      <span>{weather.condition || "Pleasant"}</span>
                      <span className="text-slate-400 font-normal">({weather.temp_max || 22}°C / {weather.temp_min || 14}°C)</span>
                    </div>
                    <div className="text-[11px] text-slate-400 flex items-center gap-2">
                      <span className="flex items-center gap-1">
                        <CloudRain className="w-3 h-3 text-cyan-400" />
                        Rain: {weather.rain_probability || 10}%
                      </span>
                      {weather.is_rainy ? (
                        <span className="text-amber-400 font-semibold">• Indoor Plan Active</span>
                      ) : (
                        <span className="text-emerald-400 font-semibold">• Great for Outdoors</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Time Slots Timeline */}
              <div className="mt-6 space-y-4">
                {/* Morning Slot */}
                <div className="relative pl-6 sm:pl-8 border-l-2 border-indigo-500/40 pb-6">
                  <div className="absolute -left-[9px] top-1.5 w-4 h-4 rounded-full bg-indigo-600 border-2 border-slate-900" />
                  <div className="bg-slate-900/80 border border-slate-700/70 rounded-xl p-4 sm:p-5">
                    <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                      <div className="flex items-center gap-2">
                        <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {day.morning.time_range}
                        </span>
                        <span className="text-xs font-semibold uppercase text-slate-400">
                          {day.morning.time_slot}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-slate-800 text-slate-300 border border-slate-700">
                          {day.morning.category}
                        </span>
                        <span className="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-slate-800 text-slate-300 border border-slate-700">
                          {day.morning.indoor_outdoor}
                        </span>
                        <span className="text-xs font-bold text-emerald-400">
                          {currencySymbol}{day.morning.estimated_cost}
                        </span>
                      </div>
                    </div>
                    <h5 className="text-base font-bold text-white">{day.morning.title}</h5>
                    <p className="text-xs sm:text-sm text-slate-400 mt-1">{day.morning.description}</p>
                    <div className="mt-3 flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800">
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-indigo-400" />
                        {day.morning.location}
                      </span>
                      <span className="text-slate-400 text-[11px]">Duration: ~{day.morning.duration_hrs}h</span>
                    </div>
                  </div>
                </div>

                {/* Spatial Transit Route Leg: Morning -> Afternoon */}
                <div className="relative pl-6 sm:pl-8 border-l-2 border-indigo-500/40 pb-6">
                  <div className="p-2.5 rounded-lg bg-indigo-950/40 border border-indigo-500/20 text-xs text-indigo-300 flex items-center gap-2">
                    <Navigation className="w-4 h-4 text-cyan-400 flex-shrink-0" />
                    <span>
                      <strong className="text-white">Route Transfer:</strong> {day.afternoon.transit_info || "Short transit hop"}
                    </span>
                  </div>
                </div>

                {/* Afternoon Slot */}
                <div className="relative pl-6 sm:pl-8 border-l-2 border-indigo-500/40 pb-6">
                  <div className="absolute -left-[9px] top-1.5 w-4 h-4 rounded-full bg-cyan-500 border-2 border-slate-900" />
                  <div className="bg-slate-900/80 border border-slate-700/70 rounded-xl p-4 sm:p-5">
                    <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                      <div className="flex items-center gap-2">
                        <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {day.afternoon.time_range}
                        </span>
                        <span className="text-xs font-semibold uppercase text-slate-400">
                          {day.afternoon.time_slot}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-slate-800 text-slate-300 border border-slate-700">
                          {day.afternoon.category}
                        </span>
                        <span className="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-slate-800 text-slate-300 border border-slate-700">
                          {day.afternoon.indoor_outdoor}
                        </span>
                        <span className="text-xs font-bold text-emerald-400">
                          {currencySymbol}{day.afternoon.estimated_cost}
                        </span>
                      </div>
                    </div>
                    <h5 className="text-base font-bold text-white">{day.afternoon.title}</h5>
                    <p className="text-xs sm:text-sm text-slate-400 mt-1">{day.afternoon.description}</p>
                    <div className="mt-3 flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800">
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-cyan-400" />
                        {day.afternoon.location}
                      </span>
                      <button
                        onClick={() => onQuickSwap(day.day_number, "afternoon")}
                        className="text-[11px] font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
                      >
                        <Sparkles className="w-3 h-3" />
                        Swap Activity
                      </button>
                    </div>
                  </div>
                </div>

                {/* Spatial Transit Route Leg: Afternoon -> Evening */}
                <div className="relative pl-6 sm:pl-8 border-l-2 border-indigo-500/40 pb-6">
                  <div className="p-2.5 rounded-lg bg-indigo-950/40 border border-indigo-500/20 text-xs text-indigo-300 flex items-center gap-2">
                    <Navigation className="w-4 h-4 text-cyan-400 flex-shrink-0" />
                    <span>
                      <strong className="text-white">Route Transfer:</strong> {day.evening.transit_info || "Short transit hop"}
                    </span>
                  </div>
                </div>

                {/* Evening Slot */}
                <div className="relative pl-6 sm:pl-8 border-l-2 border-indigo-500/40 pb-6">
                  <div className="absolute -left-[9px] top-1.5 w-4 h-4 rounded-full bg-amber-500 border-2 border-slate-900" />
                  <div className="bg-slate-900/80 border border-slate-700/70 rounded-xl p-4 sm:p-5">
                    <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                      <div className="flex items-center gap-2">
                        <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30 flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {day.evening.time_range}
                        </span>
                        <span className="text-xs font-semibold uppercase text-slate-400">
                          {day.evening.time_slot}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-slate-800 text-slate-300 border border-slate-700">
                          {day.evening.category}
                        </span>
                        <span className="text-xs font-bold text-emerald-400">
                          {currencySymbol}{day.evening.estimated_cost}
                        </span>
                      </div>
                    </div>
                    <h5 className="text-base font-bold text-white">{day.evening.title}</h5>
                    <p className="text-xs sm:text-sm text-slate-400 mt-1">{day.evening.description}</p>
                  </div>
                </div>

                {/* Dinner Slot */}
                <div className="relative pl-6 sm:pl-8">
                  <div className="absolute -left-[9px] top-1.5 w-4 h-4 rounded-full bg-rose-500 border-2 border-slate-900" />
                  <div className="bg-slate-900/80 border border-slate-700/70 rounded-xl p-4 sm:p-5">
                    <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                      <div className="flex items-center gap-2">
                        <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30 flex items-center gap-1">
                          <Utensils className="w-3 h-3" />
                          {day.dinner.time_range}
                        </span>
                        <span className="text-xs font-semibold uppercase text-slate-400">
                          Dinner & Culinary Experience
                        </span>
                      </div>
                      <span className="text-xs font-bold text-emerald-400">
                        {currencySymbol}{day.dinner.estimated_cost}
                      </span>
                    </div>
                    <h5 className="text-base font-bold text-white">{day.dinner.title}</h5>
                    <p className="text-xs sm:text-sm text-slate-400 mt-1">{day.dinner.description}</p>
                  </div>
                </div>
              </div>

              {/* Day Total Footer */}
              <div className="mt-6 pt-4 border-t border-slate-700/80 flex items-center justify-between text-xs text-slate-400">
                <span>Estimated Activity & Dining Cost for Day {day.day_number}:</span>
                <span className="font-bold text-emerald-400 text-sm">{currencySymbol}{day.day_cost_estimate}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

import React, { useEffect, useState } from 'react';
import { X, Bookmark, Trash2, Calendar, Users, DollarSign, ArrowRight, FolderOpen } from 'lucide-react';
import { getSavedTrips, deleteSavedTrip } from '../services/api';

export default function SavedTripsModal({ isOpen, onClose, onLoadTrip }) {
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchTrips = async () => {
    setLoading(true);
    try {
      const data = await getSavedTrips();
      setTrips(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchTrips();
    }
  }, [isOpen]);

  const handleDelete = async (tripId, e) => {
    e.stopPropagation();
    try {
      await deleteSavedTrip(tripId);
      setTrips(prev => prev.filter(t => t.trip_id !== tripId));
    } catch (err) {
      console.error(err);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl animate-in fade-in zoom-in-95 duration-200 text-left">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center border border-amber-500/30">
              <Bookmark className="w-5 h-5 fill-amber-400" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">Saved Trips & Itineraries</h3>
              <p className="text-xs text-slate-400">Persisted in SQLite database</p>
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
        <div className="p-5 max-h-[60vh] overflow-y-auto space-y-3">
          {loading ? (
            <div className="text-center py-12 text-slate-400 text-sm">
              Loading saved trips from SQLite database...
            </div>
          ) : trips.length === 0 ? (
            <div className="text-center py-12 text-slate-500">
              <FolderOpen className="w-12 h-12 mx-auto mb-3 opacity-40" />
              <p className="text-sm font-semibold">No saved trips found yet</p>
              <p className="text-xs mt-1">Generate a travel plan and click "Save Itinerary" to persist it here.</p>
            </div>
          ) : (
            trips.map(trip => (
              <div
                key={trip.trip_id}
                onClick={() => {
                  onLoadTrip(trip.plan_data);
                  onClose();
                }}
                className="group p-4 rounded-xl bg-slate-800/80 hover:bg-slate-800 border border-slate-700/80 hover:border-indigo-500/50 cursor-pointer transition-all flex items-center justify-between gap-4"
              >
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-bold text-white text-sm group-hover:text-indigo-300 transition-colors">
                      {trip.title}
                    </span>
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-indigo-500/20 text-indigo-300">
                      {trip.destination}
                    </span>
                  </div>
                  <div className="flex items-center gap-3 text-xs text-slate-400">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5" />
                      {trip.duration_days} Days
                    </span>
                    <span className="flex items-center gap-1">
                      <Users className="w-3.5 h-3.5" />
                      {trip.travelers} Guests
                    </span>
                    <span className="flex items-center gap-1 text-emerald-400 font-semibold">
                      <DollarSign className="w-3.5 h-3.5" />
                      {trip.currency} {trip.budget.toLocaleString()}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={(e) => handleDelete(trip.trip_id, e)}
                    className="p-2 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
                    title="Delete saved trip"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                  <span className="p-2 rounded-lg text-slate-400 group-hover:text-indigo-400 group-hover:translate-x-1 transition-all">
                    <ArrowRight className="w-4 h-4" />
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

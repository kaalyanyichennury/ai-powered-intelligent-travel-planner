import React from 'react';
import { X, BookOpen, Cpu, Layers, Database, Globe, ShieldCheck, Compass, CheckCircle } from 'lucide-react';

export default function ArchitectureModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-4xl overflow-hidden shadow-2xl animate-in fade-in zoom-in-95 duration-200 text-left">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-indigo-500/20 text-indigo-400 flex items-center justify-center border border-indigo-500/30">
              <BookOpen className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">B.E. Final Year Project System Architecture</h3>
              <p className="text-xs text-slate-400">
                Machine Learning • LLM • RAG • 6-Agent AI Architecture
              </p>
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
          {/* Architecture Pipeline Flow */}
          <div className="p-5 rounded-xl bg-slate-800/80 border border-slate-700">
            <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-400 mb-3">
              1. End-to-End System Pipeline
            </h4>
            <div className="font-mono text-[11px] sm:text-xs text-slate-300 bg-slate-950 p-4 rounded-xl border border-slate-800 overflow-x-auto leading-relaxed whitespace-pre">
{`USER REQUEST ("Plan a 7-day trip to Paris for 2 people with $2,500 budget...")
      │
      ▼
┌────────────────────────────────────────────────────────┐
│  FASTAPI BACKEND & INTENT PARSER                       │
│  • Rule-Based Regex & LLM Entity Extractor             │
│  • Output: { destination, days, travelers, budget, interests }
└───────────────────────────┬────────────────────────────┘
                            │
      ┌─────────────────────┼─────────────────────┐
      ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────────┐
│ GLOBAL DATA   │   │ WEATHER API   │   │ CURRENCY SERVICE  │
│ OpenStreetMap │   │ Open-Meteo    │   │ Live Exchange API │
│ Geocoding     │   │ Real-time Rain│   │ USD, EUR, INR...  │
└───────┬───────┘   └───────┬───────┘   └─────────┬─────────┘
        │                   │                     │
        └───────────────────┼─────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  MACHINE LEARNING LAYER (Scikit-Learn)                 │
│  • TF-IDF Vectorizer + Cosine Similarity               │
│  • Ranks attractions matching user preference vector   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  RETRIEVAL-AUGMENTED GENERATION (RAG SYSTEM)           │
│  • In-Memory Vector Store + TF-IDF/Dense Embeddings   │
│  • Grounded destination guides & travel etiquette      │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  MULTI-AGENT AI ORCHESTRATOR                           │
│  1. Destination Agent  ──> Resolves multi-city splits  │
│  2. Weather Agent      ──> Rain advisories & indoors   │
│  3. Recommender Agent  ──> ML Scoring & Diversity      │
│  4. Budget Agent       ──> Flights, hotels, activities │
│  5. Itinerary Agent    ──> Spatial nearest-neighbor    │
│  6. Verification Agent ──> Audits 5 feasibility rules  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  REACT FRONTEND (Leaflet Map + Timeline + Chatbot)     │
└────────────────────────────────────────────────────────┘`}
            </div>
          </div>

          {/* 6 Specialized Agents Breakdown */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-slate-800/60 border border-slate-700/80">
              <div className="flex items-center gap-2 text-xs font-bold text-indigo-400 mb-1">
                <Compass className="w-4 h-4" />
                1. Destination Agent
              </div>
              <p className="text-xs text-slate-300">
                Determines multi-city route distribution (e.g. 7-day Italy split into Rome, Florence, Venice) and geocodes coordinates.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-800/60 border border-slate-700/80">
              <div className="flex items-center gap-2 text-xs font-bold text-cyan-400 mb-1">
                <Globe className="w-4 h-4" />
                2. Weather Agent
              </div>
              <p className="text-xs text-slate-300">
                Pulls forecast from Open-Meteo API. Automatically tags rainy days and shifts outdoor sights to indoor museums.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-800/60 border border-slate-700/80">
              <div className="flex items-center gap-2 text-xs font-bold text-purple-400 mb-1">
                <Cpu className="w-4 h-4" />
                3. Recommendation Agent (ML)
              </div>
              <p className="text-xs text-slate-300">
                Constructs TF-IDF vector spaces over destination places. Computes cosine similarity against user interests and tags compatibility scores.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-800/60 border border-slate-700/80">
              <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 mb-1">
                <Layers className="w-4 h-4" />
                4. Budget Agent
              </div>
              <p className="text-xs text-slate-300">
                Models flights, lodging, transit passes, food, and attractions. Converts across currencies and validates financial boundaries.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-800/60 border border-slate-700/80">
              <div className="flex items-center gap-2 text-xs font-bold text-amber-400 mb-1">
                <Compass className="w-4 h-4" />
                5. Itinerary Agent
              </div>
              <p className="text-xs text-slate-300">
                Assembles morning, afternoon, evening, and dining slots. Employs Nearest-Neighbor spatial routing to optimize transit times.
              </p>
            </div>

            <div className="p-4 rounded-xl bg-slate-800/60 border border-slate-700/80">
              <div className="flex items-center gap-2 text-xs font-bold text-rose-400 mb-1">
                <ShieldCheck className="w-4 h-4" />
                6. Verification Agent
              </div>
              <p className="text-xs text-slate-300">
                Audits the final schedule against 5 rules: budget ceiling, daily fatigue pacing, geographic cluster feasibility, rain suitability, and opening hours.
              </p>
            </div>
          </div>

          {/* Academic Highlights */}
          <div className="p-4 rounded-xl bg-indigo-950/40 border border-indigo-500/30 text-xs text-indigo-300">
            <h5 className="font-bold text-white mb-2 flex items-center gap-1.5">
              <CheckCircle className="w-4 h-4 text-emerald-400" />
              What makes this a genuine B.E. / Academic-level System?
            </h5>
            <ul className="list-disc list-inside space-y-1 text-slate-300">
              <li><strong>Not a basic wrapper:</strong> Uses an actual Scikit-learn TF-IDF Machine Learning model for content-based recommendations.</li>
              <li><strong>RAG System:</strong> Vector embeddings index destination guides and enforce factual grounded responses with citations.</li>
              <li><strong>Agentic AI Architecture:</strong> Separates responsibilities across 6 autonomous agents coordinated by an orchestrator.</li>
              <li><strong>Real-World Global APIs:</strong> Integrates OpenStreetMap Nominatim, Open-Meteo forecasts, and live exchange rate APIs.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

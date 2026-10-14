import React, { useEffect, useRef, useState } from 'react';
import { MapPin, Navigation, Compass, Layers } from 'lucide-react';

export default function InteractiveMap({ itinerary, selectedDayNumber }) {
  const mapContainerRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const layerGroupRef = useRef(null);
  const [activeDay, setActiveDay] = useState(selectedDayNumber || 1);

  useEffect(() => {
    if (selectedDayNumber) {
      setActiveDay(selectedDayNumber);
    }
  }, [selectedDayNumber]);

  useEffect(() => {
    if (!mapContainerRef.current || !window.L) return;

    // Initialize Leaflet map if not already done
    if (!mapInstanceRef.current) {
      const map = window.L.map(mapContainerRef.current, {
        zoomControl: true,
        scrollWheelZoom: false,
      }).setView([48.8566, 2.3522], 13);

      window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19,
      }).addTo(map);

      layerGroupRef.current = window.L.layerGroup().addTo(map);
      mapInstanceRef.current = map;
    }

    const map = mapInstanceRef.current;
    const layerGroup = layerGroupRef.current;
    layerGroup.clearLayers();

    // Determine which stops to render
    const currentDay = itinerary.find(d => d.day_number === activeDay) || itinerary[0];
    if (!currentDay) return;

    const stops = [
      { slot: 'Morning', data: currentDay.morning, color: '#6366f1', label: '1' },
      { slot: 'Afternoon', data: currentDay.afternoon, color: '#06b6d4', label: '2' },
      { slot: 'Evening', data: currentDay.evening, color: '#f59e0b', label: '3' },
      { slot: 'Dinner', data: currentDay.dinner, color: '#f43f5e', label: '4' }
    ].filter(s => s.data && s.data.latitude && s.data.longitude);

    if (stops.length === 0) return;

    const latLngs = [];

    stops.forEach((stop) => {
      const { latitude, longitude, title, category, location, time_range } = stop.data;
      const point = [latitude, longitude];
      latLngs.push(point);

      // Custom HTML Marker Icon
      const customIcon = window.L.divIcon({
        className: 'custom-map-marker',
        html: `
          <div style="
            background-color: ${stop.color};
            width: 32px;
            height: 32px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 800;
            font-size: 13px;
          ">
            ${stop.label}
          </div>
        `,
        iconSize: [32, 32],
        iconAnchor: [16, 16],
        popupAnchor: [0, -18],
      });

      const popupContent = `
        <div style="font-family: sans-serif; padding: 4px; min-width: 180px;">
          <div style="font-size: 10px; font-weight: bold; text-transform: uppercase; color: ${stop.color};">
            ${stop.slot} (${time_range})
          </div>
          <div style="font-size: 14px; font-weight: bold; color: #0f172a; margin: 2px 0;">
            ${title}
          </div>
          <div style="font-size: 11px; color: #64748b;">
            ${category} • ${location || ''}
          </div>
        </div>
      `;

      window.L.marker(point, { icon: customIcon })
        .bindPopup(popupContent)
        .addTo(layerGroup);
    });

    // Draw route polyline
    if (latLngs.length > 1) {
      window.L.polyline(latLngs, {
        color: '#6366f1',
        weight: 4,
        opacity: 0.8,
        dashArray: '8, 8',
      }).addTo(layerGroup);
    }

    // Fit map bounds
    if (latLngs.length > 0) {
      const bounds = window.L.latLngBounds(latLngs);
      map.fitBounds(bounds, { padding: [50, 50], maxZoom: 15 });
    }
  }, [itinerary, activeDay]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-12 text-left">
      <div className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 backdrop-blur shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
          <div>
            <h3 className="text-xl font-bold font-display text-white flex items-center gap-2">
              <Navigation className="w-5 h-5 text-indigo-400" />
              Interactive Geographic Route Map
            </h3>
            <p className="text-xs text-slate-400">
              Real-time OpenStreetMap rendering with sequenced transit pins (1: Morning, 2: Afternoon, 3: Evening, 4: Dinner).
            </p>
          </div>

          {/* Day Filter Chips */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0 scrollbar-none">
            {itinerary.map((d) => (
              <button
                key={d.day_number}
                onClick={() => setActiveDay(d.day_number)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-colors ${
                  activeDay === d.day_number
                    ? 'bg-indigo-600 text-white'
                    : 'bg-slate-900 text-slate-400 hover:text-white'
                }`}
              >
                Day {d.day_number}
              </button>
            ))}
          </div>
        </div>

        {/* Map Container */}
        <div className="relative w-full h-96 sm:h-[460px] rounded-xl overflow-hidden border border-slate-700 shadow-inner">
          <div ref={mapContainerRef} className="w-full h-full z-10" />

          {/* Floating Map Legend */}
          <div className="absolute bottom-4 left-4 z-20 bg-slate-900/90 backdrop-blur-md border border-slate-700/80 rounded-xl p-3 shadow-lg flex items-center gap-3 text-xs">
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded-full bg-indigo-500" />
              <span className="text-slate-300">1: Morning</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded-full bg-cyan-400" />
              <span className="text-slate-300">2: Afternoon</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded-full bg-amber-400" />
              <span className="text-slate-300">3: Evening</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-3 h-3 rounded-full bg-rose-500" />
              <span className="text-slate-300">4: Dinner</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

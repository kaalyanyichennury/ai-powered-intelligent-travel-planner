# 🌎 AI-Powered Intelligent Travel Planner
### Using Machine Learning, LLM, RAG, and Agentic AI

An intelligent worldwide travel-planning web application designed as a production-ready, global platform. Instead of relying on a static, manual dataset, it unites **global databases, live external APIs, Machine Learning recommendation models, Retrieval-Augmented Generation (RAG), and a 6-Agent AI Orchestration architecture**.

---

## 📌 Main Objective
A user can enter free-form natural language queries such as:
> *"Plan a 7-day trip to Paris for 2 people with a budget of $2,500. I like history, photography and food."*
>
> or:
>
> *"I want to visit Japan for 10 days in April. I have a budget of ₹1.5 lakh and love anime, temples, food and photography."*

The system automatically:
1. **Understands the Request** via NLP / LLM entity extraction (destination, duration, budget, currency, interests, travelers, travel month).
2. **Geocodes Destination Worldwide** via OpenStreetMap Nominatim and multi-city spatial allocation.
3. **Retrieves Live Weather Forecasts** via Open-Meteo API (temperature, precipitation chance, rain alerts).
4. **Calculates Currency Conversion** using live exchange rates (supporting USD, EUR, INR, GBP, JPY, AED, etc.).
5. **Ranks Attractions via Machine Learning** using TF-IDF Vectorization and Cosine Similarity matching user interest profiles.
6. **Grounds Travel Knowledge via RAG** with vector search over curated guides and cultural etiquette facts.
7. **Orchestrates 6 Specialized Agents** (Destination, Weather, Recommendation, Budget, Itinerary, Verification).
8. **Enforces Verification Audits** checking budget ceilings, daily pacing fatigue, geographic clustering, and rain adaptation.
9. **Renders Day-by-Day Schedules & Interactive Map** with transit durations and route polylines.
10. **Permits Conversational Itinerary Modification** through an interactive AI Travel Concierge chatbot (*"Can you replace the museum on Day 2 with something outdoors?"*).
11. **Persists Plans & Generates Analytics** in SQLite database for an interactive Data Science admin dashboard.

---

## 🏗️ System Architecture

```
USER
 │
 ▼
┌────────────────────────────────────────────────────────┐
│  REACT FRONTEND (Vite + Tailwind CSS + Leaflet.js)     │
└───────────────────────────┬────────────────────────────┘
                            │ (REST API / JSON)
                            ▼
┌────────────────────────────────────────────────────────┐
│  FASTAPI BACKEND & INTENT PARSER                       │
│  • Regex Rule Heuristics & LLM Entity Extractor        │
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
│  • TF-IDF Vector Space Representation                  │
│  • Cosine Similarity Scoring & Ranking                 │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  RAG SYSTEM (Retrieval-Augmented Generation)           │
│  • In-Memory Vector Store + Text Chunks                │
│  • Grounded Travel Q&A with Source Citations           │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  AGENTIC AI ORCHESTRATOR                               │
│  ├── Destination Agent  (multi-city splits & coords)   │
│  ├── Weather Agent      (rain advisories & indoors)    │
│  ├── Recommendation Agt (ML scoring & diversity)       │
│  ├── Budget Agent       (flights, hotels, transport)   │
│  ├── Itinerary Agent    (spatial nearest-neighbor)     │
│  └── Verification Agent (audits 5 feasibility rules)   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  VERIFIED TRAVEL PLAN & INTERACTIVE WEB UI             │
│  • Day-by-Day Timeline • Leaflet Map • Budget Visuals  │
│  • AI Chatbot Assistant • PDF Print Export             │
└────────────────────────────────────────────────────────┘
```

---

## 🤖 The 6 Specialized AI Agents

| Agent | Responsibility |
|---|---|
| **1. Destination Agent** | Analyzes country/region and splits into logical multi-city legs (e.g. 7-day Italy -> Rome, Florence, Venice) and geocodes coordinates. |
| **2. Weather Agent** | Queries Open-Meteo API for target dates; identifies precipitation risk and instructs downstream agents to substitute outdoor sites with indoor cultural backups. |
| **3. Recommendation Agent** | Executes Scikit-learn TF-IDF + Cosine Similarity algorithms to compute compatibility percentages (e.g. *94% Match for History & Photography*) and enforces category diversity. |
| **4. Budget Agent** | Models multi-category expenses (flights, lodging, transit passes, dining, ticket admissions, miscellaneous contingency buffer), validates budget limits, and converts currencies. |
| **5. Itinerary Agent** | Assembles morning, afternoon, evening, and dining slots using Nearest-Neighbor spatial routing to optimize transit times and distance between consecutive attractions. |
| **6. Verification Agent** | Audits the generated plan across 5 dimensions: budget cap, pacing fatigue (< 11.5 active hours/day), spatial cluster proximity, rain safety, and operating hours compatibility. |

---

## 🧠 Machine Learning & Data Science Components

### 1. Content-Based Recommendation (TF-IDF + Cosine Similarity)
- **Document Vectors**: Attraction categories, tags, descriptions, and indoor/outdoor flags are vectorized into TF-IDF n-gram feature spaces.
- **User Preference Vector**: User interest keywords (e.g. *History, Architecture, Food, Photography*) are mapped into the same vector space.
- **Similarity Metric**:
  $$\text{Cosine Similarity}(u, p) = \frac{u \cdot p}{\|u\| \|p\|}$$
- Scaled into a normalized compatibility percentage ($65\% - 99\%$) with human-readable rationale explanations.

### 2. Retrieval-Augmented Generation (RAG)
- Curated vector store indexing destination cultural guides, tipping etiquette, dress codes, transit passes, and visa basics.
- Returns grounded responses with explicit source file citations (e.g. `[Source: paris_guide.txt - Tipping & Etiquette]`).

### 3. Data Science Analytics Dashboard
- Dynamic tracking of:
  - Total trips generated
  - Average trip budget in USD
  - Popular worldwide destinations (interactive bar chart)
  - Travel category preference distribution (pie/breakdown metrics)
  - Most requested trip durations

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI, Pydantic V2, SQLAlchemy, Uvicorn
- **Machine Learning & NLP**: Scikit-learn, NumPy, Pandas, Regex Entity Extractor, Configurable Google Gemini API
- **Frontend**: React 19, Vite, Tailwind CSS, Lucide React, Leaflet.js
- **Database**: SQLite (SQLAlchemy ORM) / PostgreSQL compatible
- **External Global APIs**:
  - Open-Meteo API (Free real-time multi-day weather forecasts & rain probability)
  - OpenStreetMap Nominatim (Worldwide geocoding)
  - Open Exchange Rates API (Live worldwide currency conversion)
- **DevOps**: Docker, Docker Compose, Pytest

---

## 🚀 Quick Start Guide

### Configure the Gemini LLM

The natural-language parser and travel Q&A use Google Gemini when configured. Create a Gemini API key at [Google AI Studio](https://aistudio.google.com/apikey), copy `.env.example` to `.env`, and set `GEMINI_API_KEY` in `.env`. The default model is `gemini-2.5-flash`; set `GEMINI_MODEL` to use another supported Gemini model.

Without an API key, the application keeps its local rule-based NLP and retrieval-formatted answers. When a key is present, Gemini API/configuration errors are returned instead of silently replacing failed model responses with local output. The itinerary's geospatial, budget, and verification steps remain deterministic.

### 1. Clone & Set Up Backend
```bash
# Navigate to project directory
cd "c:/ai powdered intelligent travel planner"

# Install backend dependencies
python -m pip install -r backend/requirements.txt

# Run pytest unit & integration test suite
python -m pytest tests

# Start FastAPI backend server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be live at: `http://localhost:8000/docs`

### 2. Set Up & Launch Frontend
```bash
# Open a new terminal
cd "c:/ai powdered intelligent travel planner/frontend"

# Install node packages (if not already installed)
npm install

# Start Vite React development server
npm run dev
```
Web application will be live at: `http://localhost:5173`

---

## 🐳 Docker Deployment

Run the complete frontend and backend in a single reproducible container:
```bash
docker-compose up --build
```
Access the application at `http://localhost:8000`.

---

## 🎓 Academic Viva & Project Presentation Highlights

1. **Why is this stronger than a basic ChatGPT wrapper?**
   - It incorporates a real Python Machine Learning recommendation engine (TF-IDF + Cosine Similarity) that computes mathematical compatibility scores.
   - It employs autonomous Agentic AI principles: 6 specialized agents collaborate and verify the output rather than relying on a single static LLM prompt.
   - It performs real-time verification against real-world constraints (budget ceilings, weather clashes, transit distance feasibility).

2. **How does worldwide support work without manual data entry?**
   - Combines dynamic geocoding (OpenStreetMap Nominatim), real-time global weather APIs (Open-Meteo), live foreign exchange rates, and spatial route chaining.

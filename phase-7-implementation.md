# SANKALP — Phase 7 Implementation Guide
## Intelligence, Analytics & Decision Support

**Project:** SANKALP  
**Phase:** 7  
**Repository Root:** `C:\Users\Soumen Pore\Desktop\SANKALP`  
**Backend:** `C:\Users\Soumen Pore\Desktop\SANKALP\apps\api`  
**Frontend:** `C:\Users\Soumen Pore\Desktop\SANKALP\apps\web`  

---

## 1. Purpose & Vision

Phase 7 transforms the secured SANKALP platform from a CRUD/dashboard application into a comprehensive **Development-Intelligence System**.

Rather than serving static charts or raw CRUD records, SANKALP will generate unified regional intelligence by synthesizing:
1. **Citizen Intelligence** (requests, category demand, temporal trends, spatial clusters)
2. **Government Infrastructure Data** (coverage, quality scores, operational status, capacity)
3. **Government Project Records** (planned, ongoing, completed, cancelled projects)

### Core Design Principles

1. **Human-in-the-Loop Decision Support**: SANKALP does **not** make automated policy or allocation decisions. It provides measurable indicators, empirical evidence, trends, comparisons, geographic patterns, data quality warnings, and explanations to assist administrative decision-makers.
2. **Transparent, Multi-Metric Indicators**: Avoid misleading "single black-box priority scores". Keep underlying metrics visible and disaggregated (e.g., demand score, coverage percentage, active project count, data missingness).
3. **Privacy-Preserving Spatial Analytics**: Geographic hotspot detection utilizes aggregated spatial grouping and approximate area representations to protect exact citizen location privacy.
4. **Deterministic Analytics First, AI Narratives Second**: AI is strictly restricted to summarizing and explaining deterministic calculation outputs. AI will never invent facts, override scores, or fabricate evidence.

---

## 2. Architecture Overview

```text
                                  SANKALP
                                     │
                  ┌──────────────────┴──────────────────┐
                  │                                     │
           Citizen Intelligence                  Government Data
                  │                                     │
                  ▼                                     ▼
           Citizen Requests                     Infrastructure
                  │                             Government Projects
                  │                             Demographics
                  └───────────────┬─────────────────────┘
                                  ▼
                         INTELLIGENCE ENGINE
                                  │
               ┌──────────────────┼──────────────────┐
               ▼                  ▼                  ▼
            Demand          Infrastructure         Trends
           Analysis             Gaps              Analysis
               │                  │                  │
               └──────────────────┼──────────────────┘
                                  ▼
                          REGIONAL INSIGHTS
                                  │
                  ┌───────────────┴───────────────┐
                  ▼                               ▼
              Dashboard                     AI Explanation
                  │                               │
                  └───────────────┬───────────────┘
                                  ▼
                             HUMAN REVIEW
```

---

## 3. Phase 7 Roadmap

```text
PHASE 7 — INTELLIGENCE, ANALYTICS & DECISION SUPPORT

[x] 7.1  Regional Intelligence Engine
[x] 7.2  Multi-Region Comparison
[x] 7.3  Development Priority Analysis
[x] 7.4  Trend & Time-Series Analysis
[x] 7.5  Citizen Demand Trends
[x] 7.6  Infrastructure Performance Analytics
[x] 7.7  Government Project Effectiveness
[x] 7.8  Geographic Hotspot Detection
[x] 7.9  Need vs Development Analysis
[x] 7.10 AI Intelligence Summary
[x] 7.11 Explainable Analytics
[x] 7.12 Analytics Dashboard
[x] 7.13 Export & Reporting
[x] 7.14 Intelligence API
[x] 7.15 Phase 7 Testing
```

---

## 4. Implementation Details

### 7.1 — Regional Intelligence Engine

Create a unified backend intelligence service layer that replaces or synthesizes standalone endpoints (`/demand/regions/{id}`, `/infrastructure-gap/regions/{id}`, `/development-insights/regions/{id}`).

**Directory Structure:**
```text
apps/api/app/services/
└── intelligence/
    ├── __init__.py
    ├── regional_intelligence_service.py
    ├── demand_analysis.py
    ├── infrastructure_analysis.py
    ├── project_analysis.py
    ├── trend_analysis.py
    └── hotspot_analysis.py
```

**Schemas:** `apps/api/app/schemas/intelligence.py`

**Core Response Format:**
```json
{
  "region_id": 1,
  "region_name": "North Region",
  "request_metrics": {
    "total_requests": 120,
    "categories": [
      { "category": "Water & Sanitation", "count": 45, "percentage": 37.5 },
      { "category": "Healthcare", "count": 32, "percentage": 26.7 }
    ]
  },
  "infrastructure_metrics": {
    "average_coverage": 72.4,
    "average_quality": 0.71,
    "total_units": 15,
    "operational_units": 13
  },
  "project_metrics": {
    "total_projects": 6,
    "planned": 2,
    "ongoing": 3,
    "completed": 1,
    "cancelled": 0
  },
  "development_signals": [
    {
      "category": "Healthcare",
      "demand_score": 64.2,
      "infrastructure_coverage": 42.0,
      "infrastructure_quality": 0.61,
      "gap_score": 37.3,
      "project_count": 2,
      "data_warnings": []
    }
  ],
  "data_quality": {
    "warnings": ["Demographic coverage data incomplete for Sub-district B"]
  }
}
```

---

### 7.2 — Multi-Region Comparison

Enable cross-regional comparison for comparative analysis without relying on a single deceptive ranking number.

**API Endpoint:** `GET /api/v1/intelligence/regions/compare`

**Metrics Breakdown:**
- Requests count per region & dominant categories
- Average Infrastructure Coverage (%) & Quality Index
- Total & Active Project counts
- Unmet Need Indicators per category

---

### 7.3 — Development Priority Analysis

Implement transparent development priority signal calculations where every component remains visible to analysts and decision-makers:

```text
Demand Score (0-100)
   +
Infrastructure Coverage (%) & Quality (0-1)
   +
Active Government Projects Count
   +
Data Quality / Missingness Warnings
   ↓
Category Development Signal
```

No black-box or opaque AI scores replace raw empirical measurements.

---

### 7.4 — Trend & Time-Series Analysis

Add temporal analysis capabilities using `created_at` timestamps from requests and project records.

**API Endpoint:** `GET /api/v1/intelligence/regions/{region_id}/trends`  
**Query Parameters:** `interval` (`daily`, `weekly`, `monthly`), `category` (optional), `start_date`, `end_date`

**Metrics:**
- Request volume trajectory (growth rate %, moving average)
- Status resolution velocity over time
- Project milestone progression over time

---

### 7.5 — Citizen Demand Trends

Category-level breakdown of temporal request spikes and emerging demand signals.

**Key Analytical Features:**
- Category growth velocity (% change week-over-week / month-over-month)
- Seasonality / sudden request surge detection
- Recent request feed with status tracking

---

### 7.6 — Infrastructure Performance Analytics

Deep analysis of physical infrastructure assets within each region.

**Metrics Analyzed:**
- Operational vs Non-operational asset count
- Average Coverage (%) vs Target Population
- Asset Quality Score distribution
- Asset Capacity Utilization rates

**API Endpoint:** `GET /api/v1/intelligence/regions/{region_id}/infrastructure`

---

### 7.7 — Government Project Effectiveness

Evaluation of government project distribution against citizen request sectors.

**Key Analytics:**
- Status breakdown: Planned, Ongoing, Completed, Cancelled
- Project investment alignment (matching high-demand sectors with planned/ongoing projects)
- Gaps where high citizen demand has zero assigned active projects

**API Endpoint:** `GET /api/v1/intelligence/regions/{region_id}/projects`

---

### 7.8 — Geographic Hotspot Detection

Spatial clustering of citizen requests to identify high-density issue clusters.

**Methodology:**
- Spatial clustering algorithm (e.g., Grid-based aggregation or DBSCAN clustering on request coordinates)
- Generation of approximate cluster centers & cluster radiuses
- Privacy preservation: Hide precise citizen coordinates in public cluster representations

**API Endpoint:** `GET /api/v1/intelligence/regions/{region_id}/hotspots`

---

### 7.9 — Need vs Development Analysis

Direct comparative matrix correlating:
- **Citizen Demand** (Request volume & surge signals)
- **Infrastructure Gap** (Low coverage / low quality)
- **Government Action** (Active / planned project count)

Exposes misalignments (e.g., High Demand + High Infrastructure Gap + 0 Projects).

---

### 7.10 — AI Intelligence Summary

Generates contextual narratives strictly derived from deterministic engine outputs.

**API Endpoint:** `POST /api/v1/intelligence/explanation` or `GET /api/v1/intelligence/regions/{id}/ai-summary`

**Strict AI Guardrails:**
- ❌ No invented facts, figures, or locations
- ❌ No modification of calculated scores
- ❌ No automated policy mandates
- ✅ Mandatory output structure: Summary, Key Evidence, Observed Trends, Data Limitations, Questions for Human Review

---

### 7.11 — Explainable Analytics

Standardized decision rationale component attached to every development signal card.

**5-Point Explanation Framework:**
1. **What?** (The signal/finding)
2. **Why?** (Underlying calculation formula)
3. **Based on what data?** (Specific request/infra/project counts)
4. **How reliable is the data?** (Data quality score)
5. **What is missing?** (Explicit data warnings)

---

### 7.12 — Analytics Dashboard

Re-architect `apps/web/src/pages/Dashboard.tsx` into a modern, modular Intelligence Hub:
- Unified Filter Bar (Region, Time Period, Category)
- Metric Summary Ribbon
- Temporal Trend Viewer (Recharts / ChartJS)
- Infrastructure & Project Effectiveness Widgets
- Need vs Development Matrix
- Geographic Hotspot Map View
- AI Intelligence & Explanation Drawer

---

### 7.13 — Export & Reporting

Provide formatted data exports and printable/downloadable regional intelligence reports.

**Supported Formats:**
- `CSV` Export (Raw metrics & category breakdowns)
- `JSON` Export (Full engine response)
- `Markdown / PDF` Regional Intelligence Summary Report

---

### 7.14 — Intelligence API

Full RESTful API specification secured via Phase 6 JWT Authentication & Role-Based Access Control (`admin`, `reviewer`, `analyst`, `viewer`).

| Method | Endpoint | Allowed Roles | Description |
|---|---|---|---|
| GET | `/api/v1/intelligence/regions/{id}` | All Authenticated | Unified regional intelligence payload |
| GET | `/api/v1/intelligence/regions/compare` | All Authenticated | Multi-region metrics comparison |
| GET | `/api/v1/intelligence/regions/{id}/trends` | All Authenticated | Time-series trend analysis |
| GET | `/api/v1/intelligence/regions/{id}/infrastructure` | All Authenticated | Asset coverage & quality analytics |
| GET | `/api/v1/intelligence/regions/{id}/projects` | All Authenticated | Project status & sector alignment |
| GET | `/api/v1/intelligence/regions/{id}/hotspots` | All Authenticated | Aggregated spatial hotspots |
| POST | `/api/v1/intelligence/explanation` | All Authenticated | AI explainability narrative |
| GET | `/api/v1/intelligence/export` | Analyst, Reviewer, Admin | Export report data (CSV/JSON) |

---

### 7.15 — Phase 7 Testing

Comprehensive verification across backend engines and frontend components:

- [ ] Backend Pytest unit tests for `regional_intelligence_service`
- [ ] Multi-region comparison aggregation correctness
- [ ] Trend time-series date math & zero-filling correctness
- [ ] Spatial clustering & privacy coordinate masking
- [ ] AI guardrails & fallback test (handling null AI API keys gracefully)
- [ ] RBAC enforcement tests on all `/api/v1/intelligence/*` routes
- [ ] Frontend build verification (`npm run build`) and clean browser rendering

---

## 5. Immediate Execution Step: Phase 7.1

We begin implementation with **Phase 7.1 — Regional Intelligence Engine**.

### Files to create:
1. `apps/api/app/schemas/intelligence.py`
2. `apps/api/app/services/intelligence/__init__.py`
3. `apps/api/app/services/intelligence/regional_intelligence_service.py`
4. `apps/api/app/api/routes/intelligence.py`
5. `apps/api/tests/test_regional_intelligence.py`

### Step-by-Step Action Plan:
1. Define PyDantic response schemas for unified regional intelligence.
2. Build `RegionalIntelligenceService` synthesizing data from existing DB models (`CitizenRequest`, `Infrastructure`, `Project`, `Region`).
3. Register the new `/api/v1/intelligence` router in `apps/api/app/main.py`.
4. Run backend tests to verify response accuracy and missing data handling.

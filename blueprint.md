SANKALP --- System Blueprint v1.0

AI-Powered Citizen-to-Development Intelligence Platform

Tagline Listen. Understand. Prioritize. Develop.

1. Project Overview

SANKALP is a multilingual, AI-assisted Digital Public Good concept that
transforms fragmented citizen development requests into structured,
geographically grounded development intelligence.

The platform connects four information layers

Citizen voice --- text, voice, and messaging-style submissions.

Demographic context --- population and population-related
indicators.

Infrastructure context --- availability, coverage, quality, and
capacity.

Public investment context --- existing and planned government
projects.

The system analyzes these layers to identify demand concentrations,
infrastructure gaps, and evidence-backed potential development
interventions for policymakers.

SANKALP is a decision-support platform, not an autonomous
public-spending decision maker. Human officials remain responsible for
verification, feasibility assessment, budgeting, and final decisions.

2. Product Vision

Vision

Create an inclusive digital intelligence layer that helps governments
understand citizen needs and make better-informed
infrastructure-development decisions.

Mission

Convert fragmented citizen voices into structured, explainable, and
geographically grounded development intelligence.

Core Value Proposition

SANKALP converts What citizens are asking for into Where
development gaps may exist and why they deserve attention.

3. Problem Definition

3.1 Fragmented citizen feedback

Requests can arrive through different channels and remain disconnected.

3.2 Unstructured information

Citizens describe the same need in different languages, formats, and
terminology.

3.3 Limited context

A request count alone does not reveal whether infrastructure is actually
deficient.

3.4 Geographic blindness

Aggregated requests without geographic context make it difficult to
identify local demand concentrations.

3.5 Weak evidence chains

Decision-makers need to understand not only what the system recommends,
but why.

4. Target Users

Citizen

Purpose - Submit a development request. - Use local language. - Use
text or voice. - Confirm location. - Track submitted requests.

Government Analyst  Policymaker

Purpose - Monitor development demand. - Explore geographic hotspots. -
Compare citizen demand with infrastructure. - Inspect evidence. - Review
potential interventions.

System Administrator  Data Manager

Purpose - Manage reference data. - Import datasets. - Maintain
categories and regions. - Monitor system health. - Manage authorized
data sources.

5. MVP Scope

Must Have

Citizen text request submission.

Voice-to-text input.

Multilingual request processing.

AI category and intent classification.

Locationregion association.

PostgreSQL persistence.

PostGIS-ready geographic model.

Demographic dataset.

Infrastructure dataset.

Government project dataset.

Demand aggregation.

Infrastructure-gap analysis.

Hotspot visualization.

Government dashboard.

Explainable recommendation cards.

Basic authentication and role separation.

API health monitoring.

Seeddemo data.

Should Have

Request history.

Request status.

Multiple language UI.

Regioncategory filters.

Evidence drill-down.

Recommendation review workflow.

CSV dataset import.

API documentation.

Docker-based local development.

Future

Direct messaging-platform integrations.

Advanced GIS layers.

Satelliteopen geospatial data.

More BRICS languages.

Streaming ingestion.

Advanced ML forecasting.

Government identity integration.

Large-scale distributed deployment.

Offlinelow-connectivity citizen submission.

6. Core Categories

Initial domains

Healthcare

Transport

Water & Sanitation

Education

Digital Connectivity

The category system must be extensible.

7. High-Level Architecture

                         SANKALP
                            
              +-------------+-------------+
                                         
          CITIZEN PORTAL             GOVERNMENT PORTAL
                                         
              +-------------+-------------+
                            
                         API Layer
                            
                         FastAPI
                            
       +--------------------+--------------------+
                                               
       v                    v                    v
  AI Services          Data Services       Geo Services
                                               
       +--------------------+--------------------+
                            
                    PostgreSQL + PostGIS
                            
        +-------------------+-------------------+
                                              
        v                   v                   v
     Requests          Demographics       Infrastructure
                                                
                                                v
                                      Government Projects
                            
                            v
                   Intelligence Engine
                            
              +-------------+-------------+
                                        
              v             v             v
           Demand        Gap Analysis   Hotspots
              +-------------+-------------+
                            
                            v
                    Recommendations
                            
                            v
                    Government Portal

8. Technology Stack

Frontend

React

TypeScript

Vite

Tailwind CSS

React Router

Recharts

Leaflet  React-Leaflet

Backend

Python

FastAPI

Pydantic

SQLAlchemy

Alembic

Database

PostgreSQL

PostGIS

AI Layer

Provider-agnostic service interface supporting - LLM-based structured
extractionclassification. - Speech-to-text. - Translation. - Optional
embeddingsearch services.

DevOps

Git

GitHub

Docker

Docker Compose

Environment variables

Vercel for frontend

Render or equivalent for backend

9. Repository Structure

sankalp
├── apps
│   ├── web
│   │   ├── src
│   │   │   ├── components
│   │   │   ├── layouts
│   │   │   ├── pages
│   │   │   ├── services
│   │   │   ├── hooks
│   │   │   ├── types
│   │   │   ├── data
│   │   │   ├── lib
│   │   │   ├── App.tsx
│   │   │   └── main.tsx
│   │   ├── public
│   │   ├── package.json
│   │   └── vite.config.ts
│   │
│   └── api
│       ├── app
│       │   ├── api
│       │   │   └── routes
│       │   ├── core
│       │   ├── db
│       │   ├── models
│       │   ├── schemas
│       │   ├── services
│       │   ├── main.py
│       │   └── __init__.py
│       ├── tests
│       ├── alembic
│       ├── requirements.txt
│       └── Dockerfile
│
├── data
│   ├── seed
│   └── README.md
│
├── docs
│   ├── blueprint.md
│   └── implementation.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md

10. Core Database Entities

users

id
email
password_hash
role
created_at

regions

id
code
name
country_code
parent_region_id
geometry
created_at

citizen_requests

id
anonymous_reference
raw_text
language
category
intent
issue
region_id
latitude
longitude
status
source
created_at
updated_at

demographics

id
region_id
population
population_density
income_index
growth_rate
age_distribution
updated_at

infrastructure

id
region_id
category
facility_count
coverage_index
quality_index
capacity_index
updated_at

government_projects

id
region_id
category
project_name
status
budget
planned_capacity
start_date
expected_completion
created_at

development_insights

id
region_id
category
request_count
demand_score
infrastructure_gap
priority_score
evidence
recommendation
status
created_at

11. AI Processing Pipeline

Input
 
 +-- Voice -- Speech-to-Text
 
 +-- Text ---------------------+
                                 
                                 v
                         Language Detection
                                 
                                 v
                         TranslationNormalize
                                 
                                 v
                         Structured Extraction
                                 
              +------------------+------------------+
                                                  
              v                  v                  v
           Intent            Category           Location
                                                  
              +------------------+------------------+
                                 
                                 v
                         Validation Layer
                                 
                                 v
                           Database Record

The AI service should return structured data, not uncontrolled prose.

Example

{
  language bn,
  category water_sanitation,
  intent infrastructure_request,
  issue drinking_water,
  region R001,
  confidence 0.94
}

12. Intelligence Engine

12.1 Demand score

A configurable normalized score based on - Number of relevant
requests. - Request density relative to population. - Recent demand
trend.

12.2 Infrastructure gap

A configurable score based on - Existing coverage. - Quality. -
Capacity. - Population need.

12.3 Project coverage

Existingplanned public projects reduce uncertainty about whether a need
is already being addressed.

12.4 Composite insight score

For the MVP

Insight Score =
    weighted demand
  + weighted infrastructure gap
  + weighted population need
  - weighted project coverage

All weights must be configurable and documented.

The score is an analytical aid, not a definitive policy decision.

13. Hotspot Detection

The MVP can use two complementary methods

Regional aggregation

Group requests by administrative region and category.

Geographic clustering

Use PostGIS spatial functions or a client-side clustering method to
identify concentrated request locations.

Output

Region
Category
Request Count
Demand Score
Gap Score
Insight Score

14. Explainability Model

Every development insight must expose

WHAT

Potential development need.

WHERE

Region and geographic area.

WHY

Evidence used by the system.

DATA

Underlying request, demographic, infrastructure, and project indicators.

REVIEW

Human validation status.

Example

Healthcare — Sonapur

12,482 related requests
Population 182,000
Healthcare coverage 41%
Existing facilities 1
Planned projects 0

Potential intervention
Healthcare infrastructure expansion

Reason
High citizen demand combined with limited
existing service coverage.

15. Government Dashboard

Primary modules

Overview

Development Map

Demand Analytics

Hotspots

Recommendations

Region Details

Data Sources

Review Queue

Key KPIs

Total citizen requests.

Requests this period.

Regions analyzed.

Active demand hotspots.

Categories tracked.

Insights awaiting review.

16. Citizen Experience

Request flow

Start
 ↓
Select language  auto-detect
 ↓
Speak or type
 ↓
AI interprets
 ↓
Review extracted information
 ↓
Confirm location
 ↓
Submit
 ↓
Request ID

The confirmation screen should allow the citizen to correct AI-extracted
fields before submission.

17. Privacy & Security Principles

Minimize personally identifiable information.

Store anonymous references for analytical records.

Separate authentication identity from analytical request data.

Validate all API inputs.

Never expose database credentials to the frontend.

Use environment variables for secrets.

Apply role-based authorization.

Log administrative actions.

Use HTTPS in production.

Apply rate limiting to public submission endpoints.

Document data retention and deletion policies.

18. Digital Public Good Principles

SANKALP should be designed around

Interoperability.

Open API contracts.

Modular services.

Configurable categories.

Countryregion abstraction.

Reusable data schemas.

Transparent analytical methodology.

Documentation.

Human oversight.

19. Evaluation Framework

AI

Language detection accuracy.

Classification accuracy.

Structured extraction accuracy.

Location association accuracy.

Analytics

Correct request aggregation.

Correct regional grouping.

Correct infrastructure-gap calculation.

Hotspot consistency.

Explainability

Every insight should have an evidence trail.

Performance

API latency.

Database query latency.

Concurrent submissions.

Dashboard load time.

UX

Citizen request completion target - Under 1 minute for normal text
submission.

Policymaker discovery target - Identify a relevant hotspot within 30
seconds during the demo.

These are product test targets, not real-world outcome claims.

20. Final Demonstration Scenario

Citizen speaks in Bengali
        ↓
আমাদের এলাকায় পানীয় জলের সমস্যা হচ্ছে
        ↓
SANKALP detects Bengali
        ↓
Category Water & Sanitation
Issue Drinking Water
        ↓
Request stored
        ↓
Similar requests aggregated
        ↓
Region becomes a demand hotspot
        ↓
Demographic + infrastructure data loaded
        ↓
Gap detected
        ↓
Evidence-backed insight generated
        ↓
Government dashboard displays the insight
        ↓
Policymaker reviews evidence

21. Phase Roadmap

Phase 1 --- Foundation

Repository

Frontend

Backend

Database

Docker

Environment configuration

Health endpoints

Phase 2 --- Citizen Intelligence

Request submission

Voice input

AI extraction

Multilingual support

Request history

Phase 3 --- Data Fusion

Demographics

Infrastructure

Projects

Data ingestion

Phase 4 --- Geo Intelligence

PostGIS

Hotspots

Map layers

Geographic analytics

Phase 5 --- Recommendations

Gap engine

Insight engine

Explainability

Review workflow

Phase 6 --- Government Portal

Dashboard

Analytics

Map

Recommendations

Phase 7 --- Scale & Hardening

Security

Performance

More languages

Data-source adapters

Deployment

22. Definition of Done

SANKALP MVP is considered complete when a reviewer can

Submit a citizen request.

See AI-structured request information.

Store the request in PostgreSQL.

Aggregate multiple requests.

Compare demand with infrastructure data.

View a geographic hotspot.

Open the hotspot.

See supporting evidence.

See a potential intervention.

Understand how the insight was generated.

SANKALP --- End State

The project should feel like a government development intelligence
platform, not a complaint form.
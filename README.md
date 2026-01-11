# Milk Market Intelligence API

Data scraping and analytics platform for large-scale retail market analysis, focused on the Russian milk and dairy segment.

This project is designed as a modular, production-oriented backend with an analytical layer and a lightweight frontend for data exploration and visualization.

---

## Overview

Milk Market Intelligence is a data pipeline that collects, normalizes, stores, and analyzes retail and marketplace data.  
The system is built to support continuous data ingestion, regional mapping, and analytical outputs suitable for BI tools or custom dashboards.

The project emphasizes:
- deterministic data processing
- clean separation of scraping, analytics, and presentation
- testability and CI integration

---

## Architecture

Data Sources (Web / Marketplaces)  
→ Scraping Layer (providers, parsers)  
→ Normalization & Region Mapping  
→ Database (PostgreSQL / SQLite for dev)  
→ Analytics Layer (pandas)  
→ API (FastAPI)  
→ Frontend / BI exports (Plotly, JSON, CSV)

---

## Backend

Tech stack:
- Python 3.11+
- FastAPI
- SQLAlchemy
- pandas
- Alembic
- pytest
- Docker

Responsibilities:
- Modular scraping providers
- Region detection and normalization (Yandex Suggest API–based mapping)
- Structured data storage
- Analytical computations over collected datasets
- REST API for analytics and exports

Testing & CI:
- Unit and integration tests with pytest
- GitHub Actions CI pipeline
- Explicit PYTHONPATH handling for reliable test execution

---

## Frontend

Purpose:
- Lightweight analytical UI (not a full BI system)
- Visualization of precomputed analytics
- Export-ready plots

Tech:
- React
- Plotly

All analytical computations are performed server-side to keep results deterministic and reproducible.

---

## Analytics

- Data cleaning and transformation using pandas
- Aggregations by region, product group, and source
- BI-style outputs:
  - Interactive Plotly charts
  - JSON / CSV exports for external BI tools (Power BI, Tableau)

---

## Configuration & Security

- No secrets committed to the repository
- All credentials and API keys handled via environment variables
- Database files and local artifacts excluded via .gitignore

---

## Repository Structure

backend/ – core application logic, modules, analytics, tests  
frontend/ – React analytical UI  
.github/workflows/ – CI pipelines  
README.md

---

## Project Status

Active development.

Planned extensions:
- Additional data providers
- Scheduled ingestion pipelines
- Advanced analytics modules
- Role-based access for analytical endpoints

---

## Author

Developed and maintained by Lukas Krumpach  
Backend / Data-focused Python developer

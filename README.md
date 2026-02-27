# OSINT Fusion Platform Abu Jamal 

## Overview
A professional-grade OSINT tool that aggregates public data from multiple sources. Designed for security researchers and ethical use only.

## Features
- User authentication (JWT)
- Email breach checking (HaveIBeenPwned)
- Email reputation analysis (EmailRep.io)
- Phone number validation & carrier lookup (AbstractAPI)
- Username search (simulated – extend with Sherlock API)
- Search history & audit logging
- Admin log viewer

## Installation
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r backend/requirements.txt`
5. Create a `.env` file in the root with your API keys:

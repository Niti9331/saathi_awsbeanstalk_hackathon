# Saathi (साथी) - Mental Health First-Aid Guide

A small, privacy-first guide that helps people in India find free mental health
helplines in their own language. It does not diagnose or treat, and it does not
replace a mental health professional. No login, no accounts, no stored user data.

## Features
- Six languages: English, Hindi, Bengali, Marathi, Tamil, Telugu
- Helplines page and a "need help now" crisis page
- Calm page: guided breathing and 5-4-3-2-1 grounding
- Light and dark mode, mobile-first, quick-exit button
- Health check endpoint at `/health`

## Tech stack
Python (Flask), Gunicorn, HTML/CSS, JSON data files, pytest.
Deployed on AWS Elastic Beanstalk.

## Run locally
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements-dev.txt
    python application.py        # http://127.0.0.1:5000
    pytest -q

If port 5000 is busy (macOS AirPlay): `flask --app application run --port 5001`

## Project layout
- `application.py` - Flask app (Elastic Beanstalk looks for `application`)
- `data/translations.json`, `data/helplines.json` - all text and helpline data
- `templates/`, `static/` - pages and styling
- `tests/` - pytest suite (pages, languages, helplines, translations)
- `Procfile`, `.ebextensions/` - Elastic Beanstalk configuration

## Translation status
Wording reviewed by native speakers in English, Hindi and Bengali.
Marathi, Tamil and Telugu are awaiting native-speaker review.

## Notes
Helpline numbers should be re-verified against official sources before use
(see `verified_on` in `data/helplines.json`).

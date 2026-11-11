# RoboChapta — CAPTCHA QA Lab

A safe, local-first CAPTCHA quality-assurance harness. It classifies challenge metadata, benchmarks OCR only on synthetic/owned test fixtures, and routes real third-party verification to a human or the provider's official flow. It does not automate solving, clicking, or bypassing third-party CAPTCHA protections.

## Features
- Challenge metadata classification: text, image, audio, checkbox, interactive, unknown.
- OCR benchmark for a controlled local dataset with ground-truth labels.
- Human-review handoff marker for interactive or externally hosted challenges.
- FastAPI health and classification endpoints.
- Docker and GitHub Actions CI.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs.

## API
- `GET /health`
- `POST /detect` JSON: `{"type":"image"}`
- `POST /review` JSON: `{"provider":"example","challenge_id":"local-test-1"}`

The review endpoint only creates a handoff record; it does not submit an answer to a CAPTCHA provider.

## OCR benchmark (controlled fixtures only)
Install Tesseract OCR, then create a CSV with columns `image_path,expected_text`. Use only synthetic or owned images. Run:
```bash
python -m app.benchmark --csv datasets/fixtures.csv
```
This benchmark evaluates OCR quality; it is not an external CAPTCHA-solving service.

## Safety
Do not use this project to defeat access controls, automate account creation, scrape protected services, or bypass CAPTCHA challenges. For production services, use the provider's documented test keys, accessibility flow, or human verification.

## Tests
```bash
pytest -q
```

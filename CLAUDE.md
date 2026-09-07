# PROJECT CONTEXT — KiranaBot

## Problem Statement
Kirana store owners waste hours manually filing GST returns
because they cannot extract data from paper invoices easily.

## Solution
WhatsApp-style chat interface where owners upload invoice photos.
Gemini Vision extracts all fields automatically.
System validates GST math and generates GSTR-1 CSV export.

## Architecture
Invoice Photo → Gemini Vision OCR → Validation → Supabase → GSTR-1 CSV

## Team Roles
- Person 1 (Backend) → /backend/api/ and /backend/core/
- Person 2 (AI)      → /backend/core/extraction.py and /backend/prompts/
- Person 3 (Frontend)→ /frontend/src/ only
- Person 4 (Docs)    → /presentation/ and /docs/

## Tech Stack
- OCR: Gemini Vision (google-generativeai)
- Chat: Groq llama3-8b-8192
- Backend: FastAPI
- Frontend: React + Vite
- Database: Supabase
- Deploy: Render (backend) + Vercel (frontend)

## Current Phase
Phase: INTEGRATION COMPLETE

## DONE
- [x] T01 Environment setup
- [x] T05 FastAPI skeleton
- [x] T08 GSTIN validation
- [x] T13 Preflight checks
- [x] T12 Tax math + classification
- [x] T06 Gemini Vision extraction
- [x] T11 Full extraction pipeline
- [x] T16 Supabase read/write
- [x] T18 Backend integration
- [x] T21 Demo data seeded

## IN PROGRESS
- [ ] T22 E2E testing with frontend
- [ ] T23 Render deployment

## BLOCKED
- Nothing

## DO NOT TOUCH
- .github/workflows/
- main branch directly
- Another person's folder
- .env files

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
SETUP — Waiting for hackathon to start

## DONE
- [x] Repo setup
- [x] Folder structure
- [x] Branch structure
- [x] Templates ready

## IN PROGRESS
- [ ] Nothing yet

## BLOCKED
- Nothing

## DO NOT TOUCH
- .github/workflows/
- main branch directly
- Another person's folder
- .env files

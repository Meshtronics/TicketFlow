# 🚧  Ticket 2025-06-17-001 — Restructure Repo for Non-Template Use

---
id: 2025-06-17-001
parent: 0000-00-00-000          # ← keeps lineage with the sample ticket
title: "Repo refactor: convert template layout to single‑folder drop‑in (Option A)"
status: open
type: chore
priority: medium
author: @Mikah
created: 2025‑06‑17
tags: [repo‑structure, tech‑debt, Option‑A]
---

## 📝 Summary  
Move **all** TicketFlow code and assets into a dedicated `/TicketFlow/` directory so the project can be checked out as a one‑folder component inside an existing codebase. This implements the Option A decision (see design discussion in ticket 0000‑00‑00‑000).

## 🔨 Tasks  
- [ ] **Create target folder**  
  - `mkdir TicketFlow` at repo root.
- [ ] **Move application files** now in repo root into the new folder:  
  - Source (`src/`, `app/`, etc.)  
  - Config/build files (`package.json`, `pnpm-lock.yaml`, `tsconfig*.json`, `.eslintrc*`, Vite/Webpack configs, etc.)  
  - Assets (`public/`, `.env.example`, docs, etc.).  
- [ ] **Relocate license & docs**  
  - Move `LICENSE` and existing detailed `README.md` into `/TicketFlow/`.  
  - Add a _minimal_ root `README.md` that explains embed workflow and points to `/TicketFlow/README.md`.  
- [ ] **Update relative imports & paths**  
  - Search for hard‑coded relative paths that assume project root (`import "../src/..."`, workflow paths, Dockerfiles, etc.).  
  - Adjust package‐manager scripts (`npm run dev`, test, lint) to prepend `cd TicketFlow && …`.  
- [ ] **Update GitHub Actions**  
  - Change `working-directory:` keys or path expressions so CI jobs still build/test from inside `TicketFlow/`.  
- [ ] **Run automated & manual tests** from repo root to confirm nothing breaks.  
- [ ] **Documentation sweep**  
  - Fix any links in markdown or comments that point to now‑moved paths.  
- [ ] **Commit & PR**  
  - Title: “feat(repo): move code into /TicketFlow (implements Option A)”  
  - Request review from @Mikah and at least one other maintainer.  

## ✅ Definition of Done  
- Repository root contains only `/TicketFlow/`, a stub `README.md`, and `.gitignore`.  
- `pnpm install && pnpm test` (or equivalent) succeed from either repo root **or** `TicketFlow/`.  
- GitHub Actions workflow passes on the PR branch and on `main` after merge.  
- No broken import paths or relative links identified by linter, TypeScript compiler, or test suite.  

## 🔗 References  
- Decision rationale: ticket 0000‑00‑00‑000  
- Design doc: _One folder → one source of truth_ (in `/docs/architecture.md`)  

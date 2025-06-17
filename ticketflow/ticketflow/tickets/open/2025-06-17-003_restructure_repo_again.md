---
id: 2025-06-17-002
parent: 0000-00-00-000            # maintains lineage with the original design discussion
title: "Repo restructure: remove nested *ticketflow* dirs & establish clean top‑level layout"
status: open
type: chore
priority: high
author: @Mikah
created: 2025‑06‑17
tags: [repo‑structure, tech‑debt, cleanup]
---

## 📝 Summary  
During the Option A migration we unintentionally ended up with **three nested `ticketflow` directories**.  
This ticket tracks the full clean‑up so that:

* “TicketFlow” exists **only as the repository name** (no sub‑folders named the same).  
* `tickets/` sits at repo root (`tickets/open`, `tickets/closed`, etc.).  
* Application code, configuration and docs live in logical, conventional locations (e.g. `/src`, `/public`, `/docs`).  
* All relative paths, imports, scripts, CI workflows and docs reflect the new structure.

## 📁 Target directory layout (proposed)
.
├── tickets/
│ ├── open/
│ └── closed/
├── src/ # app source (front‑end + back‑end, if monorepo)
├── public/ # static assets exposed by the web server / bundler
├── scripts/ # one‑off CLI helpers, DB migrations, etc.
├── docs/ # architecture, ADRs, diagrams
├── tests/ # automated test suites
├── package.json
├── pnpm-lock.yaml
├── tsconfig.json
├── .eslintrc.cjs
├── .github/ # workflows, issue templates, PR templates
├── .env.example
├── LICENSE
└── README.md

> Adjust as needed if the current code base has additional layer separations (e.g. `/api`, `/ui`, `/server`, `/client`).  
> The **key rule** is: **no path may include another `ticketflow` component.**

## 🔨 Tasks  

- [ ] **Create working branch**  
  - `git checkout -b chore/repo-flatten`
- [ ] **Move `tickets/` directory**  
  - From deepest nested path to root: `git mv <old>/tickets ./tickets`
  - Verify links inside ticket markdown still resolve.
- [ ] **Flatten nested `ticketflow` folders**  
  - Identify the two inner `ticketflow/` directories.  
  - Move their contents to appropriate root‑level folders (see above).  
  - Remove the now‑empty directories: `git rm -r <inner>/ticketflow`.
- [ ] **Normalize application code paths**  
  - If code currently lives in `<root>/ticketflow/src/*`, move to `src/`.  
  - Update any bundler/build configs (`vite.config.ts`, `webpack.config.js`, `tsconfig.json` paths, Jest config, etc.).
- [ ] **Adjust package‑manager scripts**  
  - Edit `package.json` and any `Makefile` or shell scripts so commands run from repo root (no `cd ticketflow` prefixes).
- [ ] **Update imports & path aliases**  
  - **Search & replace**  
    - `import ... from "ticketflow/...";` or `../ticketflow/...`  
  - Update `tsconfig.json` `compilerOptions.paths` if using path aliases.
- [ ] **Revise GitHub Actions**  
  - Remove `working-directory:` overrides that pointed into nested folders.  
  - Confirm `checkout` step runs from root and subsequent build/test steps succeed.
- [ ] **Remove stale artifacts**  
  - Delete any duplicated lockfiles, config files or `.env.example` that were inside nested dirs.
- [ ] **Rewrite root README.md**  
  - Reflect the new structure.  
  - Clarify “one folder → one source of truth” now refers to **this repo as a component** rather than a nested sub‑folder.  
  - Fix badge paths, absolute/relative links and code block paths.
- [ ] **Documentation sweep**  
  - Update diagrams or docs in `/docs/` that embed old paths.  
  - Search markdown for “ticketflow/ticketflow” or similar.
- [ ] **Run full QA pass**  
  - `pnpm install && pnpm run lint && pnpm test` from repo root.  
  - Manual smoke test: start dev server, run a production build, execute CLI tools.
- [ ] **Commit & PR**  
  - Squash commits; PR title: `chore(repo): flatten structure & remove nested ticketflow dirs`.  
  - Request review from at least one maintainer.

## ✅ Definition of Done  

* No folder inside the repo is named `ticketflow`.  
* `tickets/` is at repo root and sample ticket renders correctly in GitHub web UI.  
* `pnpm run build` (or equivalent) and all CI checks pass from root.  
* All tests green; linter finds no broken import paths.  
* README displays correct directory tree and updated instructions.  
* `git grep -i "ticketflow/"` returns only expected code references (e.g., package name, not paths).  

## 🔗 References  

* Ticket template & discussion – `0000‑00‑00‑000` in `tickets/open`  
* Previous migration ticket – `2025‑06‑17‑001`  
* Guide: *Standard JS/TS project structure* (see `/docs/architecture.md`)  

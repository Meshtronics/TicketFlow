<!--
Rename this file to YYYY‑MM‑DD‑###_forward-reverse-merge.md
YYYY‑MM‑DD = date created
###        = incremental counter for that day (001, 002…)
-->

# 🚧  Ticket 2025‑06‑22‑001 — *Forward / Reverse Run Fusion*

**Goal / Definition of Done**  
We can load **two single‑direction CSV files (one forward, one reverse)** via the existing file‑picker or CLI; the script:
1. Automatically registers the runs on the shim‑marker peaks.  
2. Aligns both distance axes so *x = 0 … L* maps to the same physical rail span.  
3. Produces:
   * An **averaged vertical profile** and **averaged lateral profile** (`y_avg_v`, `y_avg_l`).
   * A **per‑point residual** (`y_res_v`, `y_res_l`) plus global RMS and Pearson r printed to console.
4. Plots four traces in one window (fwd, rev, avg, residual), preserves current styling, **still uses the Tk file‑picker UI** when the user omits CLI args.
5. Exports a CSV `*_fwd‑rev‑fusion.csv` containing `distance_mm`, `y_avg_v`, `y_avg_l`, `y_res_v`, `y_res_l`.

All unit tests pass, and manual shop check shows the macro‑scale shape is retained (our second‑order drift filter no longer hides true long‑wavelength deviations).

**Context / Motivation**  
A dual‑direction scan cancels most sensor drift and human‑push artefacts.  
Combining them in‑code avoids having to eyeball two plots or export to Excel.  
This ticket builds on the current **`genesis_process2.py`** pipeline that already supports single‑file processing and segmentation logic :contentReference[oaicite:1]{index=1}.

**Deliverables**  
- [ ] `genesis_process2.py` refactored:
  - [ ] new `process_pair(fwd_path, rev_path, cfg)` orchestrator  
  - [ ] helper `register_runs(df_f, df_r) -> grid, y_f, y_r` implementing:  
    - peak detection (`scipy.signal.find_peaks`) on `D_mm_V` to find shim markers  
    - linear rescaling of encoder columns  
    - inversion of reverse distances  
    - interpolation onto common 1 mm grid  
  - [ ] averaging & residual calc (`y_avg = 0.5*(y_f + y_r[::-1])`, etc.)  
  - [ ] plotting function `plot_fwd_rev_combo(...)` keeping dual‑axis style  
  - [ ] CSV writer `export_fusion_csv(...)`
- [ ] UI: if no CLI args → Tk file dialog that allows **multi‑select (two files)**; still supports single‑file mode unchanged.
- [ ] `tests/test_fwd_rev_fusion.py` with small synthetic datasets exercising:
  * correct shim detection
  * correct inversion of reverse run
  * identical output when files are passed in swapped order
- [ ] Updated `README.md` usage section.
- [ ] Docstring examples for every new public function.

**Relevant files / locations**  
`genesis_process2.py`, `tests/`, `docs/README.md#dual-run`, existing helper functions in the same module.

**Notes for AI agents**  
* Coding style: PEP 8, type hints where reasonable.  
* Use `numpy.interp` for resampling; don’t pull in heavy libs beyond SciPy already present.  
* Edge cases:  
  * duplicate encoder values → drop duplicates before interpolation (already done).  
  * only one shim detected → raise a clear `ValueError` with advice.  
  * forward file accidentally shorter than reverse → truncate longer grid to overlap.  
* Keep all existing command‑line options backward‑compatible; add `-o / --output` optional flag for custom CSV name but default to auto‑suffix.

---

_Status: open_  
_Assignee: unassigned_

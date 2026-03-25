# nle7-char3-del-pezzo

GitHub repository for the paper **"A Computer-Assisted Bound of Seven Singular Points for Rank-One klt del Pezzo Surfaces in Characteristic Three"**.

Public repository URL: <https://github.com/HiroSakuraba/DelPezzo7>

This repository is organized for two audiences at once:
1. a human referee who wants the exact computational dependencies of the final theorem, and
2. a future AI agent who needs the broader historical search record without confusing exploratory dead ends for load-bearing proof steps.

## Core rule for reading this repository

The paper depends only on the **corrected final chain** recorded in `paper/`, `scripts/`, and `results/`.
The `exploratory/` tree is preserved for provenance, method transfer, and future AI handoff, but it is **not** part of the logical core of the theorem unless the paper explicitly cites it.

## Repository layout

- `paper/` - current LaTeX drafts and PDFs.
- `scripts/` - Python programs for the load-bearing computational steps used in the final argument.
- `results/json/` - machine-readable summaries for those steps.
- `results/notes/` - human-readable notes explaining each computation and its mathematical role.
- `docs/` - repository guide, AI-agent entrypoint, historical no-go ledger, and publishing notes.
- `exploratory/` - earlier lanes retained for provenance.

## Final proof chain represented here

1. Basket / lattice screening: `scripts/i0iv_v79_odd_lattice_bilinear_anticanonical_screen.py`
2. Exotic basket global closures: `scripts/i0iv_v94_exotic_baskets_global_closure.py`
3. Mixed basket reduction to polarization orbits: `scripts/i0iv_v95_mixed_basket_polarization_orbit_reduction.py`
4. Mixed basket grouped orbit reduction: `scripts/i0iv_v96_L2_orbit_combinatorics_reduction.py`
5. Mixed basket global normalization theorem: `scripts/i0iv_v98_mixed_basket_global_normalization_theorem.py`
6. Pure `8A1` degree-1 branch-node closure: `scripts/i0iv_v72_singular_base_degree1_double_cover.py` together with `results/notes/v99.md`

## Minimal rerun commands

```bash
python scripts/i0iv_v79_odd_lattice_bilinear_anticanonical_screen.py
python scripts/i0iv_v94_exotic_baskets_global_closure.py
python scripts/i0iv_v95_mixed_basket_polarization_orbit_reduction.py
python scripts/i0iv_v96_L2_orbit_combinatorics_reduction.py
python scripts/i0iv_v98_mixed_basket_global_normalization_theorem.py
```

## Current draft

The current referee-facing paper version in this repository is:
- `paper/N_le_7_char3_paper_draft_v11.tex`
- `paper/N_le_7_char3_paper_draft_v11.pdf`

This version includes the corrected mixed-basket grouped normalization, the corrected exotic-chain root counts, and the direct public GitHub URL.

## Exploratory lanes preserved for AI handoff

- `exploratory/ambient_deformation_lanes/v30_picard_merge/`
  Early projective/high-dimensional tooling, including the matroid, circuit, and constraint-solver lane.
- `exploratory/quasi_elliptic_global_probe/v50/`
  Later ambient/deformation and quasi-elliptic scans.
- `exploratory/wild_alpha3/v20/`
  Wild/additive-action and Artin-Schreier search lane, plus its no-go ledger.
- `exploratory/historical_notes/`
  Short handoff notes that explain why older branches were pursued and how they were closed or superseded.

## Additional historical documents

A separate historical-document layer is preserved in:
- `exploratory/historical_documents/older_drafts/`

These files are older papers / handoff drafts that are useful for provenance and for future AI agents, but they are **not** part of the logical core of the theorem unless explicitly cited in the paper. See:
- `docs/HISTORICAL_DOCUMENTS_INDEX.md`
- `docs/HISTORICAL_NO_GO_LEDGER.md`

## Why keep the exploratory material?

Because the paper is also evidence that AI can solve difficult problems through a long correction-driven search. Another agent should be able to see:
- which branches were genuinely dead,
- which branches were only provisional and later corrected,
- which tools (including matroid-style structural screens) were useful search accelerators even though they are not final theorem ingredients.

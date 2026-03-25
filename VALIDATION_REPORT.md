# Repository validation report

Date: 2026-03-25

## Structural fixes applied

- Replaced the placeholder/public-note repository URL with the direct GitHub URL `https://github.com/HiroSakuraba/DelPezzo7` in the current paper source (`v11`), README, and citation metadata.
- Corrected the stale exotic-chain counts in the current repository-facing artifacts:
  - `7A1 + 1/7(1,2)` now recorded as `48` orthogonal real roots with maximal pairwise orthogonal size `4`.
  - `7A1 + 1/11(1,2)` now recorded as `32` orthogonal real roots with maximal pairwise orthogonal size `4`.
- Removed hard-coded private working-directory paths from the core mixed-basket scripts:
  - `scripts/i0iv_v96_L2_orbit_combinatorics_reduction.py`
  - `scripts/i0iv_v98_mixed_basket_global_normalization_theorem.py`
- Added a repository-relative fallback for `scripts/i0iv_v91_mixed_rational_nonrational_F9_slice_scan.py` so it runs from the packaged repository even when the old intermediate `v90` chunk files are absent.
- Repaired additional absolute-path issues in non-core helper scripts where feasible.

## Runtime checks performed

### 1. Basket screen
Command:
```bash
python scripts/i0iv_v79_odd_lattice_bilinear_anticanonical_screen.py
```
Status: ran successfully.
Headline output: the exact survivor list has 5 baskets.

### 2. Standard complement correction
Command:
```bash
python scripts/i0iv_v84_exact_standard_complement_correction.py
```
Status: ran successfully.
Headline output:
- exact grouped effective classes count = `64`
- max pairwise orthogonal subset size = `5`

### 3. Exotic basket closure script
Command:
```bash
python scripts/i0iv_v94_exotic_baskets_global_closure.py
```
Status: ran successfully.
Headline output now records corrected root counts from v80:
- `7A1_plus_1_7_11` -> `56`
- `7A1_plus_1_7_2` -> `48`
- `7A1_plus_1_11_2` -> `32`

### 4. Mixed-basket polarization reduction
Command:
```bash
python scripts/i0iv_v95_mixed_basket_polarization_orbit_reduction.py
```
Status: ran successfully.
Headline output:
- `L1 sizes 90 210`
- `L2 sizes 128 177`
- `L1 config None`
- `L2 config ((0, 31, 62, 169, 170), (46, 80, 58, 66, 63))`

### 5. Mixed rational/non-rational F9 slice scan
Command:
```bash
python scripts/i0iv_v91_mixed_rational_nonrational_F9_slice_scan.py
```
Status: ran successfully in repository mode.
Note: because the historical intermediate `v90` chunk files are not packaged, the script falls back to the cached final summary in `results/json/v91.json`.

### 6. L2 orbit combinatorics reduction
Command:
```bash
python scripts/i0iv_v96_L2_orbit_combinatorics_reduction.py
```
Status: ran successfully.
Result: output matches `results/json/v96.json` exactly.

### 7. L2 global normalization theorem
Command:
```bash
python scripts/i0iv_v98_mixed_basket_global_normalization_theorem.py
```
Status: ran successfully.
Result: output matches `results/json/v98.json` exactly.

### 8. Current paper build
Command:
```bash
cd paper
pdflatex -interaction=nonstopmode -halt-on-error N_le_7_char3_paper_draft_v11.tex
pdflatex -interaction=nonstopmode -halt-on-error N_le_7_char3_paper_draft_v11.tex
```
Status: compiled successfully.
Output: `paper/N_le_7_char3_paper_draft_v11.pdf`

## Scope note

This validation pass focused on the current theorem-facing repository chain and the immediate portability problems in the packaged scripts. It does **not** certify every exploratory or historical script in `exploratory/`.

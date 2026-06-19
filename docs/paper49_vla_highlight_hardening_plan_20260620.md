# Paper 49 VLA Highlight Hardening Plan

Date: 2026-06-20

## Objective

Harden the visual highlight/link-box styling in Paper 49 so it matches the VLA-v4 role-model PDF's professional red and green boxed callouts while preserving the final full-scale robot self-shadow manuscript, results, page count, and scientific claims.

## Current Evidence

- Canonical PDF: `C:/Users/wangz/Downloads/49.pdf`.
- Current page count: 25.
- Current affected link pages: 3, 4, 6, 7, 8, and 9.
- Current link annotations: 13 green citation/link boxes and 6 red internal-reference boxes.
- Current border state: all 19 link annotations use border `(0, 0, 0)`, so the boxes are invisible.
- Current LaTeX source uses `\hypersetup{colorlinks=true,linkcolor=black,citecolor=black,urlcolor=black}` in root `main.tex`.
- Current final result remains the full-scale robot self-shadow benchmark: 302,400 compact condition rows, 37,013,760,000 represented trajectory evaluations, and 2,664,990,720,000 represented frame decisions.

## Role-Model Style Target

Match the VLA-v4 role model's link annotation style:

```tex
\hypersetup{
  colorlinks=false,
  pdfborder={0 0 1},
  citebordercolor={0 1 0},
  linkbordercolor={1 0 0},
  urlbordercolor={0 1 0}
}
```

Expected Paper 49 result after rebuild:

- Page count remains 25.
- All 13 citation/link annotations remain green.
- All 6 internal-reference link annotations remain red.
- All 19 link annotations use border `(0, 0, 1)`.
- No scientific content, benchmark data, or claim is changed.

## Execution Plan

1. Render the affected pre-change pages to `C:/Users/wangz/highlight_box_hardening/tmp/pdfs/paper49_before` for baseline visual comparison.
2. Replace the current black color-link `\hypersetup` in root `main.tex` with the VLA-v4 hyperref settings above.
3. Rebuild using `scripts/build_pdf.ps1`, which exports only the canonical PDF to Downloads, records build metadata, and removes root `main.pdf`.
4. Verify with `pypdf` that the rebuilt PDF has 25 pages, 13 green link annotations, 6 red link annotations, and 19 `(0, 0, 1)` borders.
5. Render the affected post-change pages to `C:/Users/wangz/highlight_box_hardening/tmp/pdfs/paper49_after` and visually inspect the highlight pages for professional box weight, alignment, spacing, and legibility.
6. Update README, child status, and tracked audit metadata if needed so the canonical PDF hash and visual hardening evidence match the actual output.
7. Remove Paper 49 temporary render folders after QA.
8. Commit and push the clean repo before moving to the next paper.

## Non-Goals

- Do not rerun the benchmark.
- Do not pad content or alter the 25-page manuscript to chase page count.
- Do not revise claims, tables, captions, or results unless a visual/layout defect requires a tiny local wording adjustment.

## Final QA Result

- Rebuilt canonical PDF: `C:/Users/wangz/Downloads/49.pdf`.
- Final page count: 25.
- Final size: 296244 bytes.
- Final SHA256: `41D52D6E629156AD7C22D0706DBA2A618E95225936C5A016E94D9C34FC41D120`.
- Verified annotations: 13 green citation boxes, 6 red internal-reference boxes, and 19 visible `(0, 0, 1)` borders.
- Rendered pages 3, 4, 6, 7, 8, and 9 at 160 dpi; the boxes match the VLA-v4 role model's thin, professional style and do not create layout collisions.

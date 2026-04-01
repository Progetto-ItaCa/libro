
# Project TODO

This file tracks two long-running maintenance tracks:

- Task A: make local iteration fast (CI can keep doing the full build).
- Task B: turn `itaca.dtx`/`itaca.sty` into a readable, documented, maintainable shared package.


## Task A - Speed Up Common Local Builds (DO THIS FIRST)

Goal: optimize the day-to-day loop (edit -> compile -> repeat) without requiring full local builds.

### A1. Provide "fast" local targets

- Add `make dev` that:
  - disables expensive editorial overlays (`showkeys`, `todonotes`) by passing package options to `itaca`.
  - disables `bibtex` and `makeindex` runs (use existing `.bbl`/`.ind` if present).
  - avoids `-shell-escape` by default.
- Add `make chap CH=cap/02-limiti` that:
  - compiles `main.tex` with an injected `\includeonly{...}` (no editing `main.tex`).
  - uses the same fast settings as `make dev`.
- Add `watch` variants (`make watch-dev`, `make watch-chap CH=...`).

### A2. Make `itaca` configurable for local speed

- Add lightweight package options to `itaca`:
  - `fast` (implies `noshowkeys` + `notodos`)
  - `showkeys`/`noshowkeys`
  - `todos`/`notodos` (use `todonotes` with `disable` when off)
  - (optional later) `cjk`/`nocjk`

### A3. Cache the real offenders

- Enable TikZ externalization behind an opt-in switch (first build slower, subsequent local builds much faster).
- Keep CI building without externalization artifacts (or ensure externalization cache is deterministic).


## Task B - Document + Streamline `itaca.dtx` (PLAN ONLY FOR NOW)

Goal: collaborators can understand and safely extend the package; `itaca.pdf` becomes the canonical reference.

### B1. Define and document the public API

- Decide what is *public/stable* vs *internal/legacy*.
- Create a "User Guide" section in `itaca.dtx`:
  - how to load the package (options, expected document class assumptions)
  - conventions (naming, semantics)
  - examples of the most used macros/environments.
- Use `l3doc` markup (`\DescribeMacro`, `macro` environments) so the generated `itaca.pdf` includes a macro index.

### B2. Inventory + usage-driven pruning

- Extract a list of all commands/environments defined in `itaca.dtx`.
- Cross-check against actual usage in `cap/**/*.tex`.
- Classify each item:
  - keep as-is
  - rename (new name + compatibility alias)
  - deprecate (compat alias + warning + planned removal date)
  - remove (unused)

### B3. Make the implementation idiomatic and modular

- Introduce `l3keys2e` options for feature toggles (dev tooling, diagrams, fonts/CJK, etc.).
- Separate concerns:
  - *package-level reusable macros* vs *document-level configuration*
  - avoid doing global document configuration unconditionally inside the package (e.g. `hyperref` setup, `babel`, `showkeys`).
- Group code into clear sections (abbreviations, categories/operators, theorem envs, diagram helpers, utilities).
- Replace brittle `\def` with `xparse`/expl3 where it improves safety (without breaking existing markup).

### B4. Definition of done

- `make itaca.pdf` produces readable documentation (with examples) and a usable macro index.
- `make main.pdf` matches current output by default (or changes are explicitly intended and recorded).

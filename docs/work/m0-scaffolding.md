# M0: Scaffolding

## Intent

### Goal
An installable, empty `qanat` package with lint, tests and a CI workflow, so that M1 (the framework, circular shaft SOE and basal heave) can start writing code straight away.

### Why
- M0 is the first run through the loop ("Starting from zero" in the spec-driven-development skill; SPEC §11.4).
- Every later milestone assumes there is a package to import, a test runner, a linter and a CI matrix.

### Constraints
- SPEC §11.1:
  - 🟡 Python ≥ 3.12 and `uv`, matching hangtu, so both install in one environment.
  - MIT license.
  - CI on Windows, macOS and Linux × Python 3.12–3.14, running ruff and pytest.
- SPEC §11.2: `src/` layout, package `qanat`, tests mirroring the package.
- SPEC §1.2, §3: **no dependency on hangtu** or any other ecosystem package.
- SPEC §10: pytest and hypothesis; warnings are errors.
- SPEC §11.4: M0 is done when CI is green.
- Follow hangtu's M0 where nothing here says otherwise (`../hangtu/docs/work/m0-scaffolding.md`): `uv_build`, ruff with numpy-style docstrings, strict pytest options, and a CI job that tests the oldest allowed dependency versions.

### Out of scope
- Any M1 code: inputs, results, units, `qn.sweep`, analyses.
- A PyPI release workflow and the first upload. They come once the distribution name is settled (decision 2).
- A docs site (SPEC §11.3).
- Creating the GitHub repo and pushing. The workflow is written and checked locally; a TODO item tracks confirming CI on GitHub.

### SPEC sections touched
- §1.1: the PyPI name (decision 1).
- §6: pint first (decision 2).
- §11.1: the Python floor and the dependencies M0 installs (decisions 2, 3).
- §12: Q2 resolved.

### Decisions (intent review, 2026-10-23)
1. **Published on PyPI as `qanat-design`, imported as `qanat`.** The bare `qanat` belongs to an abandoned Python 2 game (version 0.5, no files uploaded). The author is requesting a PEP 541 transfer; that can take months, so the distribution name can't wait for it. The import name is what users type, and it doesn't change. `qanat-design` should be claimed with a 0.0.1 placeholder upload soon, as hangtu was (hangtu SPEC §12.1); that upload is its own small unit, after M0, since the release workflow is out of scope here.
2. **Pint first, and `pint` is the one runtime dependency at M0.** Inputs are written as pint quantities; a plain float is accepted as the documented SI unit (SPEC §6, resolving Q2). pint is certain, so M0 adds it with its floor, and the lowest-versions CI job has a real floor to prove from the start. `numpy` and `pandas` wait for M1, when code first uses them.
3. **Python ≥ 3.12**, matching hangtu, so both install in one environment.
4. 🟡 **`__init__` exports only `__version__`** (from the `qanat-design` distribution's metadata). The rest of the API starts at M1.


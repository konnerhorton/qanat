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

## Plan

There is no separate `## Spec`; SPEC §11 is the spec for scaffolding. Three build commits, each with ruff and pytest passing.

### 1. `M0: add package skeleton, dependencies and tool config`
- `pyproject.toml`:
  - `name = "qanat-design"`, `version = "0.1.0.dev0"`, `requires-python = ">=3.12"`, `license = "MIT"`, keywords, classifiers (Pre-Alpha, Python 3.12–3.14) and project URLs (GitHub `konnerhorton/qanat`, assumed until the repo exists).
  - `dependencies = ["pint>=0.24.4"]`. hangtu's floor: 0.24.0–0.24.3 fail to import with current `flexparser`. Re-checked here by the lowest-versions run.
  - `[dependency-groups] dev = ["pytest>=8.0", "ruff>=0.17", "hypothesis>=6.100"]`. They need floors too, because `lowest-direct` also lowers dev dependencies.
  - `[build-system]` uses `uv_build>=0.9.9,<0.10`, with `[tool.uv.build-backend] module-name = "qanat"`, since the distribution name would otherwise map to `qanat_design`.
  - `[tool.ruff]`: `target-version = "py312"`; format excludes `*.md`; lint `select = ["E", "F", "W", "I", "UP", "B", "SIM", "RUF", "D"]` with numpy docstrings; `D` ignored in `tests/**`.
  - `[tool.pytest.ini_options]`: `testpaths = ["tests"]`, `addopts = ["-ra", "--strict-markers", "--strict-config", "--import-mode=importlib"]`, `xfail_strict = true`, `filterwarnings = ["error"]`.
- `.python-version` (`3.12`), `.gitignore` (hangtu's, without its project-specific entries) and `LICENSE` (MIT).
- `src/qanat/__init__.py`: a module docstring, and `__version__` from the `qanat-design` distribution's metadata.
- `tests/test_package.py`: `__version__` equals the installed metadata version; `pint` imports.
- `uv.lock` from `uv lock`. SPEC §11.1 records the floors, in the same commit.

### 2. `M0: add CI workflow`
- `.github/workflows/ci.yml`, from hangtu's without `MPLBACKEND` or the docs job. Runs on push to `main` and on pull requests.
  - **`test`:** `ubuntu-latest`, `windows-latest`, `macos-latest` × Python 3.12, 3.13, 3.14, `fail-fast: false`: `uv sync --locked`, `ruff check`, `ruff format --check`, `pytest`.
  - **`lowest`:** ubuntu, Python 3.12, `UV_RESOLUTION: lowest-direct`, `uv sync`, `pytest`. This proves the floors.

### 3. `M0: record commands and close out scaffolding`
- `CLAUDE.md`: the status paragraph, and the Commands section.
- `README.md`: M0's docs (SPEC §11.3): installing from source until the first PyPI upload, and the development commands.
- New `docs/TODO.md`: #1 create the GitHub repo, push and confirm CI is green (SPEC §11.1, §11.4); #2 claim `qanat-design` with a 0.0.1 placeholder and a release workflow, and track the PEP 541 request for `qanat` (SPEC §1.1).

### Verification (local, since there's no remote)
- `uv sync && uv run ruff check . && uv run ruff format --check . && uv run pytest` on 3.12, and `uv run --isolated --python 3.13 pytest` and `--python 3.14`.
- The lowest floors in a scratch environment: `UV_RESOLUTION=lowest-direct UV_PROJECT_ENVIRONMENT=<scratch> uv run --python 3.12 pytest`, then restore `uv.lock`. If a floor fails, raise it and update SPEC §11.1 in that commit.
- The workflow schema: `uvx check-jsonschema --builtin-schema vendor.github-workflows .github/workflows/ci.yml`.
- `uv build`: the wheel is `qanat_design-*.whl`, contains `qanat/__init__.py`, and `import qanat` works from it in an isolated environment.
- Windows and macOS can't be checked locally. That stays open in TODO #1.

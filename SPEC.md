# qanat — Product Specification

**Status:** Draft.

**What belongs here:** decisions that constrain more than one feature, plus scope and phasing. Per-feature detail lives in that feature's spec (the `## Spec` section of `docs/work/<id>.md`, or a topic doc under `docs/`). Detail for later phases is held in `docs/drafts/` until those phases start. Update this file in the same commit as any change that alters a decision. How the process works: the `spec-driven-development` skill.

**Conventions**
- **Decided**: agreed in review.
- 🟡 **Proposed**: Claude's proposed default, awaiting review.
- ❓ **Open**: needs input (collected in §12).
- 🔬 **Research**: tracked in [TODO.md](docs/TODO.md).

**Document map**
| Document | Contents |
|---|---|
| `SPEC.md` (this file) | Scope, phasing, cross-cutting decisions |
| `docs/work/<id>.md` | Intent, spec and plan for each unit of work |
| [`docs/drafts/`](docs/drafts/) | Notes for later work, including the scope discussion this spec came from |
| `docs/TODO.md` | Research items and pending decisions (created with the first item) |
| [`CLAUDE.md`](CLAUDE.md) | Working conventions and commands |

---

## 1. Scope and phasing

**Purpose (decided 2026-10-23):** qanat is a design library for tunnels and shafts, and for closely related excavations such as support of excavation for deep foundations. It does the closed-form and empirical calculations that get a project to a 60% design quickly, and every result can be traced back to its inputs, its method and its source. It does not replace numerical analysis. It tells the engineer **where numerical analysis is needed**: a result outside a method's validity, or close to its limit, says so (§5).

### 1.1 Users and distribution
- **Persona (decided):** a geotechnical or tunnel engineer with beginner-to-intermediate Python, as for hangtu.
  - They think in **scripts and functions** more than objects, so every analysis is a plain function.
  - **The engineer who checks a calculation is often not the one who ran it** (or is the same one, months later). So every result carries what it took to check it: its inputs, method, source and validity (§4, §5). A plausible wrong answer should never pass without a trace.
- **Distribution (decided):** open source, MIT license, published on PyPI and public GitHub, developed independently. No project data is used in development or testing: real project documents stay on the machine where the work is done.
- **Name (decided 2026-10-23):** published on PyPI as **`qanat-design`**, imported as `import qanat as qn`. The bare `qanat` name on PyPI belongs to an abandoned project; a PEP 541 transfer is being requested, and the import name doesn't change either way.

### 1.2 The ecosystem
qanat is one package in a set of independent open-source libraries (decided 2026-10-23):

| Package | Role | Relation to qanat |
|---|---|---|
| **hangtu** | Derives ground parameters from test data | Upstream: its selected parameters are qanat's ground inputs |
| **qanat** | Tunnel and shaft design calculations | — |
| Settlement library (unnamed) | Ground deformation, utility and structure impact assessment | Downstream: takes qanat's volume loss and geometry |
| Alignment and object builder (unnamed) | Builds alignments and the other objects shared across the ecosystem (shafts, tunnels, structures, utilities) | Upstream: qanat takes its stations, cover and geometry as plain data (§3) |
| Project library (unnamed) | Project decisions, judgments, workflows and reporting | Connects the others (§3) |

- **No package depends on another analysis package.** qanat never imports hangtu or the settlement library, and they never import qanat. They exchange plain data (numbers, DataFrames, documented dicts).
- **qanat owns volume loss** (decided 2026-10-23): estimating it, from face pressure or empirical ranges, is a qanat calculation; turning it into settlement troughs and impacts is the settlement library's.
- **Reports, figures and deliverables are formatted outside qanat** (decided 2026-10-23), probably in the project library. qanat returns results that are complete enough to report from (§5).

### 1.3 Scope
In scope (decided 2026-10-23; the order is set by the milestones, §11.4):

| Area | Examples |
|---|---|
| **Shaft support of excavation (SOE), circular** | Empirical design of secant piles, sheet piles, liner plate, diaphragm walls; earth pressure with arching for circular shafts; hoop compression; toe embedment |
| **Shaft base and stability checks** | Basal heave, hydraulic uplift and piping (blow-in), base plug thickness (tremie, jet grout), flotation |
| **Tunnel ground support** | Liner plate, steel sets, rock bolts, shotcrete; rock loads; support selection from rock mass classification |
| **Segmental lining** | Closed-form ring forces, segment jacking loads, handling and stacking cases |
| **Face stability and face pressure** | EPB, slurry and MTBM support pressure; open-face stability and stand-up time |
| **Convergence–confinement** | Ground reaction curve, support characteristic curve, longitudinal displacement profile, squeezing assessment |
| **Groundwater** | Tunnel and shaft inflow, dewatering wells, seepage around cutoffs |
| **TBM and MTBM** | Thrust and torque, pipe jacking force and intermediate jacking stations, penetration rate and cutter wear |
| **Ground improvement and pre-support** | Ground freezing, groutability, jet grout columns, spiling, pipe canopies |
| **Volume loss** | Estimates passed to the settlement library (§1.2) |
| **Later** | Non-circular shafts and excavations, seismic ovaling and racking, portals, cross passages |

### 1.4 Non-goals
- **Deriving ground parameters** from test data. That's hangtu. qanat takes parameters as given and records where they came from (§4).
- **Settlement, ground deformation and impact assessment.** That's the settlement library.
- **Numerical analysis** (FE, FD, DEM). qanat flags where it's needed.
- **Full structural code compliance.** qanat does simple capacity checks (§7). The structural engineer does code design.
- **Reports and figures** (§1.2).
- **Reading project files or judgments files.** 🟡 The project library does that and passes values in (§3).

## 2. Sources and verification

### 2.1 Governing sources
🔬 None verified yet. Each unit of work adds the sources it relies on, verified against the source itself, to the bibliography (§2.2). Candidates from the scope discussion (`docs/drafts/scope-discussion.md`) are not citations until verified.

### 2.2 Citation format
- 🟡 **In docstrings:** `Source: <author or body> (<year>), <document>, Eq. <n> / Table <n> / Fig. <n> / p. <n>`. Always the edition or year and the equation, table, figure or page.
- 🟡 **Bibliography:** `docs/reference/sources.md`, one entry per source, with its short key and the date it was verified.
- **Never cite from memory** (decided, skill rule). An unverified citation is marked 🔬 and tracked in `docs/TODO.md`.

### 2.3 Conflicts between sources
- 🟡 The unit's spec says which source governs and why. qanat doesn't pick between methods silently: where practice uses more than one (several face pressure methods, several inflow equations), the method is a **required argument**, as hangtu does for C_N.

### 2.4 Verification
- **Golden values** come from a worked example in the source, or a hand calculation written out in the unit's spec with its inputs, steps and source. Never from running the code.
- 🟡 **Tolerance:** 0.5 % relative by default. A test that needs another states why (a value read from a chart, a source that rounds).

### 2.5 Validity limits
- 🟡 **Outside a method's range, the result is flagged, not raised** (§5.2). A screen along an alignment needs every section's result, including the ones that need numerical analysis. qanat raises only for inputs that are physically impossible or inconsistent (a negative depth, a water table above a ponded surface when that isn't allowed).
- The limits for each method, and what counts as "marginal", are in its spec and docstring, with their source.

## 3. Ecosystem contract

- **A small shared package will hold the project-level conventions** (decided 2026-10-23, subject to change): the format for project decisions and judgments, and the workflows that run hangtu, qanat and the settlement library together. It is likely the same package as the project library (§1.2).
- 🟡 **qanat doesn't depend on it.** qanat functions take every input as an explicit argument and return results that record every input (§4, §5). The project library reads the judgments file, calls qanat and keeps the provenance. This keeps qanat usable on its own, from a script, with no project file.
- 🟡 **qanat follows hangtu's naming and unit conventions** (§6, §8) so that hangtu output passes into qanat without renaming, and users see one style across the ecosystem. Where qanat needs a name hangtu also has, it uses hangtu's.
- **The project library comes after at least M1** (decided 2026-10-23), maybe later, so qanat's result shape is tried on real analyses before the project library's format is set around it.
- 🟡 **Alignments and shared objects come from the builder** (§1.2). qanat doesn't define alignment geometry of its own: a reaches table (§8.3) takes stations, cover and section geometry as plain data, in a documented shape that the builder's output can fill. The builder doesn't need to exist for qanat to work; a reaches table can be written by hand.

## 4. Inputs

Every input to a calculation is one of three kinds. They are treated differently because each goes wrong in a different way, and a forgotten judgment is the one most likely to turn into a plausible, unexamined default.

| Kind | Examples | Rule |
|---|---|---|
| **Ground parameter** | Unit weight, undrained strength, friction angle, hydraulic conductivity, GSI | Required argument. No default. |
| **Design judgment** | Design method, target factor of safety, surcharge, groundwater level, construction stage, overbreak allowance | Required, keyword-only argument. **No default** (decided, as hangtu SPEC §4). |
| **Constant or setting** | Unit weight of water, gravity | Defaulted, documented, overridable. Recorded on the result. |

- **No judgment has a default.** A missing judgment is an error that names it, says what it depends on, and how to set it. This is the main protection against a plausible value standing in for a decision nobody made.
- 🟡 **Provenance is optional on input and always kept on output.** An argument can be a plain value or a value with a source (for example a hangtu characteristic value with its file and hash; format in the first analysis milestone's spec). Either way the result records the value used, its kind, and its source when one was given.
- 🟡 **Method choice is a judgment** where practice uses more than one method (§2.3).

## 5. Results

### 5.1 One result shape
🟡 Every analysis returns a result object with the same parts:
- **values:** the computed quantities, with units;
- **checks:** each demand–capacity or stability check, with its factor of safety or utilization and the required value;
- **method:** the method, its source and the equations used;
- **inputs:** every input used, with its kind and source (§4);
- **validity:** the verdict (§5.2), with the limit that set it;
- **warnings:** everything that was flagged.

🟡 **One calculation, many views** (as hangtu SPEC §5): `.to_dict()` (JSON-ready, for the project library and other tools), `.to_frame()` and a short text summary. Views never recalculate, so two views can't disagree.

### 5.2 Validity verdict
🟡 Each result has one of three verdicts, the worst over its checks and inputs:
- **`within`:** every input is inside the method's stated range.
- **`marginal`:** within range but near a limit, by a margin set in the method's spec.
- **`outside`:** at least one input outside the range. The result is still computed, and says which input and which limit. **This is the flag for numerical analysis.**

Pass/fail on a check (FS below the target) is separate from validity: a method can be valid and fail, or pass outside its range.

### 5.3 Sensitivity runs
**Every calculation can be run many times over arrays of one to three of its inputs** (decided 2026-10-23), to see how the results vary across the distributions of uncertain parameters and judgments. This is a design constraint on every analysis, not a later feature.

- 🟡 **One sweep function for every analysis:** `qn.sweep(analysis, inputs, vary={name: array, ...}, mode=...)`. `inputs` holds the fixed values; `vary` holds one to three arrays. Analyses don't each grow their own array handling.
  - **`mode="grid"`:** every combination (a full factorial), for "how does FS change with s_u and wall embedment".
  - **`mode="paired"`:** the arrays are the same length and row *i* takes element *i* of each, for samples drawn from distributions (Monte Carlo). Drawing the samples, including any correlation between them, is the user's; qanat takes the arrays.
- 🟡 **The output is a tidy table:** one row per run, with the varied inputs, the main values, each check's FS or utilization, pass/fail and the validity verdict (§5.2). So "what fraction of runs fail" and "where does the method go out of range" are a filter on one table. The fixed inputs and their sources are recorded once, in `df.attrs`.
- 🟡 **A run that raises doesn't stop the sweep.** Its row records the error, by §9 (never drop data silently).
- 🟡 **Any input can be varied, including ones inside a ground profile**, addressed by name (for example a layer's parameter, `("clay", "undrained_shear_strength")`). The addressing is set in M1.
- 🟡 **What this asks of each analysis:** a pure function of its arguments (no hidden state, no reading files), cheap enough to call thousands of times, and a result whose `.to_dict()` flattens into a row. Varying a categorical judgment (the method) is allowed in `grid` mode, so methods can be compared on the same inputs.
- **Array inputs are decided per analysis** (decided 2026-10-23). By default `qn.sweep` calls the analysis once per run. An analysis's spec decides whether it also accepts numpy arrays directly, weighing the speed gained against the build and review cost: broadcasting turns every branch in a method (active vs passive, a regime change at a limit) into an `np.where`, which is harder to read and to check against the source. Either way the `qn.sweep` interface is the same.

## 6. Units

- **SI is the preferred system** (decided 2026-10-23): kN, kPa, m, kN/m³, as hangtu.
- **Code-neutral** (decided): qanat isn't written to one design code; the method and its source are named on every result (§7).
- **Empirical equations in US units** (decided): the conversion happens inside the function, once, at the equation, and is shown in the result's method. The user never converts by hand.
- **Never guess a unit** (as hangtu SPEC §2.6).
- **Pint first** (decided 2026-10-23): a scalar input is a pint quantity, and the docs, examples and docstrings write inputs that way, so the unit is explicit at the call. **A plain float is accepted and read as the documented SI unit.** The result's input echo (§5.1) records which it was, so a float in the wrong unit can be caught on review.
  - 🟡 Any pint quantity is accepted, whatever registry made it (hangtu has its own), by reading its magnitude and unit. qanat uses pint's application registry for the quantities it returns.
  - 🟡 Result values are pint quantities; `.to_dict()` and `.to_frame()` give SI magnitudes with the units recorded (in `df.attrs["units"]` for a frame). Set in M1.
- DataFrames carry units in `df.attrs["units"]`, as hangtu.
- **Units never appear in names** (`depth`, not `depth_m`), as hangtu.

## 7. Design codes and structural checks
- **Factors of safety only, for now** (decided 2026-10-23). Checks report a factor of safety against a target FS, and the target is a judgment (§4). Many empirical shaft and tunnel methods are written this way.
- **Each milestone evaluates LRFD** for its own analyses (decided 2026-10-23), starting with M1: whether the methods it builds have published load and resistance factors, and whether a factored check would change a design decision. The findings go in the milestone's spec. If LRFD is adopted, it becomes a decision in this file, and code factor sets come as named, cited presets.
- 🟡 **Structural checks are simple capacity checks** (axial, bending, shear, hoop, buckling where the method gives it) against capacities computed from cited formulas or given by the user. Code compliance is out of scope (§1.4).

## 8. Conventions

### 8.1 Geometry and signs
- 🟡 **Depth is positive downward** from the ground surface at the section; elevations, where used, carry their datum, as hangtu SPEC §8.
- 🟡 **Compression is positive** for soil stresses and earth pressures (geotechnical convention). Structural member forces state their sign convention in the result.
- 🟡 **Circular shafts first** (decided for scope, §1.3): a shaft is its inside diameter, wall thickness and excavation depth.

### 8.2 Ground profile
- 🟡 A section's ground is a **layered profile**: a table of layers (top and bottom depth, a ground unit name, the parameters each analysis needs) plus a groundwater level. Its exact columns are set in the first analysis milestone and use hangtu's column names (§3).

### 8.3 Sections and alignments
- 🟡 **Every analysis works on one section or one shaft.** A thin table of reaches (stations, ground class, cover, groundwater) applies analyses along an alignment and collects the verdicts. The reaches table comes after the first single-section analyses, and its shape is one the alignment builder can fill (§3).

### 8.4 Naming and API
- **Plain functions on plain data**; keep objects thin (as hangtu).
- **Names are explicit** (as hangtu): `undrained_shear_strength`, not `su`; `excavation_depth`, not `h`. Symbols belong in docstrings and labels.
- **Judgment arguments are keyword-only.**
- **Error messages** say what is wrong, where, and what to do.
- **A public calculation's docstring is its reference entry:** equation, inputs and outputs with units, validity range, assumptions, source.
- Use American spelling.

## 9. Data quality
- **Never drop data silently.** A layer or section that can't be computed is reported in the result with the reason, not skipped.

## 10. Testing
- pytest; golden values per §2.4; behavior at and beyond each validity limit is tested.
- 🟡 Property-based tests (hypothesis) for monotonic behavior where the physics requires it (more cover, more required face pressure; deeper excavation, lower basal heave FS).
- 🟡 Every analysis has a test that a `qn.sweep` row equals a direct call with the same inputs (§5.3).

## 11. Engineering

### 11.1 Environment and distribution
- **Python ≥ 3.12** (decided 2026-10-23) and `uv`, matching hangtu, so both install in one environment. CI on Windows, macOS and Linux × Python 3.12–3.14.
- **Dependencies:** `pint>=0.24.4` (from M0, §6; 0.24.0–0.24.3 fail to import with current `flexparser`). Dev: `pytest>=8.0`, `ruff>=0.17`, `hypothesis>=6.100`, floored too because the lowest-versions job lowers them as well. 🟡 `numpy` and `pandas` (profiles, reach tables, sweep output) are added by M1, when code first uses them. Each dependency has a floor, proven by a CI job on the oldest allowed versions. Adding another needs a decision here.
- MIT license.

### 11.2 Package layout
- 🟡 `src/` layout, package `qanat`, tests mirroring the package. Modules by area (`qanat.shaft`, `qanat.tunnel_support`, `qanat.face`, `qanat.groundwater`, `qanat.tbm`, …), set as each area is built.

### 11.3 Docs
- **Docs are written as we go** (decided 2026-10-23): each milestone's close-out writes the user docs for what it built (a page per analysis, an example, the API reference from docstrings), so the docs are never a backlog.
- 🟡 The docs site is set up in M1, with the first public API, using the same tooling as hangtu (Zensical, with the API reference from docstrings). M0's docs are the README.

### 11.4 Milestones
| ID | Scope | Done when |
|---|---|---|
| M0 | Scaffolding: package, lint, tests, CI | CI green |
| M1 | Framework and the first shaft checks: inputs (§4), the result shape, validity verdict and `qn.sweep` (§5), units (§6), the ground profile (§8.2), and circular shaft SOE plus basal heave (decided 2026-10-23 as the first analysis) | Golden values from verified sources; each validity limit tested; LRFD evaluated (§7); docs site with a page per analysis |
| — | Later milestones are set after M1, from §1.3 | — |

🟡 M1 builds the framework together with real analyses rather than on its own, so the result shape is tested against real checks. If it's too big for one unit, it splits into the framework with basal heave first, then the SOE wall types.

## 12. Open questions
1. Project library timing: decided 2026-10-23, after at least M1 (§3).
2. Units on scalar inputs: decided 2026-10-23, pint first with SI floats accepted (§6).
3. Check framing: decided 2026-10-23, factors of safety only for now, with LRFD evaluated in each milestone (§7).
4. Array inputs: decided 2026-10-23, per analysis (§5.3).

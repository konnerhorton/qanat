# qanat

Open-source Python library of closed-form and empirical design calculations for tunnels and shafts, to get a project to a 60% design quickly and traceably, and to show where numerical analysis is needed (SPEC §1). One package in an ecosystem with hangtu (ground parameters, upstream) and a settlement library (downstream); none depends on another (SPEC §1.2, §3). Status: `SPEC.md` is in draft. Next: M0 scaffolding, then M1 (framework, circular shaft SOE and basal heave).

## Where things are
- `SPEC.md`: product spec and cross-cutting decisions. Read the relevant section before designing anything.
- `docs/work/<id>.md`: intent, spec and plan for each unit of work (the spec-driven-development skill). Files for merged units are history.
- `docs/drafts/`: notes for later work, including `scope-discussion.md`. Not decisions unless marked "decided".
- `docs/TODO.md`: research items and pending decisions, referenced as "TODO #n".
- hangtu (`../hangtu`) is the model for conventions, but qanat never imports it.

## Commands
- Set by M0.

## Conventions
- **Judgments have no defaults.** A judgment input is a required keyword-only argument (SPEC §4).
- **Every result has the same shape** and a validity verdict; outside a method's range it is flagged, not raised (SPEC §2.5, §5).
- **Every analysis must work under `qn.sweep`:** pure, no hidden state, no file reading (SPEC §5.3).
- **Names follow hangtu:** written out in full, no units in names, American spelling (SPEC §8.4).

## Git and commits
- Defaults from the spec-driven-development skill: a branch per unit off `main`, merged with `--no-ff`; a commit per loop step; stage files by name; `<scope>: <imperative summary>`.
- **Approval:** Claude commits intermediate build steps of an approved plan without asking. Intent, spec and plan commits, docs-only commits, branches, merges and pushes need approval first.
- **The repo is public.** No project data, client names or private sources in code, docs or commits.

## Workflow rules
- If a change alters a decision recorded in `SPEC.md` or a feature spec, update that file in the same commit.
- Don't renumber `SPEC.md` sections.
- Test against the acceptance criteria in the feature's spec.
- **Docs as we go:** each milestone's close-out writes the user docs for what it built (SPEC §11.3).
- **Evaluate LRFD in each milestone:** checks are factors of safety for now; each milestone's spec records whether LRFD would apply to its analyses (SPEC §7).
- Cite sources as `SPEC.md` §2 says, checked against the source itself. Never cite from memory.

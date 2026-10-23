# TODO

Items to think through or research. Each item notes who owns it and the SPEC section it affects.

- **Owner key:** **You** = judgment or research the author does. **Claude** = verification or build-time work.
- When an item is resolved, move the decision into SPEC.md and delete it here.

---

## Release and infrastructure

### 1. GitHub repo and CI · You and Claude · SPEC §11.1, §11.4
- Create the public GitHub repo (`konnerhorton/qanat`, as `pyproject.toml`'s URLs assume), push, and confirm CI is green on the full matrix and the lowest-versions job.
- M0 was checked locally on Linux only (Python 3.12–3.14, the lowest floors, the workflow schema and the wheel). Windows and macOS are unchecked until then.

### 2. PyPI names · You and Claude · SPEC §1.1
- **Claim `qanat-design`** with a 0.0.1 placeholder upload, as hangtu was claimed. Its own small unit: a release workflow with trusted publishing, as hangtu's `.github/workflows/release.yml`.
- **PEP 541 request for `qanat`** (abandoned Python 2 game, version 0.5, no files). You file it. If it succeeds, decide whether to move the distribution to `qanat`; the import name doesn't change.

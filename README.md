# qanat

Closed-form and empirical design calculations for tunnels and shafts: support of excavation, ground support, segmental linings, face pressure, groundwater inflow, basal heave, TBM and MTBM thrust. Every result is traceable to its inputs, method and source, and flags where numerical analysis is needed.

In early design: there are no calculations yet. See [`SPEC.md`](SPEC.md) for the scope and roadmap.

## Install

qanat isn't on PyPI yet. It will be published as `qanat-design` and imported as `qanat`:

```python
import qanat as qn
```

Until then, install from source with [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/konnerhorton/qanat.git
cd qanat
uv sync
```

Python 3.12 or later.

## Development

```bash
uv sync                                                            # install, with the dev tools
uv run pytest                                                      # tests
uv run ruff check . && uv run ruff format --check . && uv run pytest  # what CI runs
```

## License

MIT.

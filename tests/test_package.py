import importlib
from importlib.metadata import version

import pytest

import qanat


def test_version_matches_installed_metadata():
    assert qanat.__version__ == version("qanat-design")


@pytest.mark.parametrize("module", ["pint"])
def test_runtime_dependency_imports(module):
    importlib.import_module(module)

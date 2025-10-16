import os
import sys
import pytest

# make "from app.*" work when running pytest from repo root
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))

from app.storage.orders import _reset_for_tests  # noqa: E402


@pytest.fixture(autouse=True)
def reset_store() -> None:
    _reset_for_tests()
    yield

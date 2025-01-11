from __future__ import annotations

import os.path

pytest_plugins = ["git-camus.test.data"]


def pytest_configure(config):
    source_root = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != source_root:
        os.chdir(source_root)


# This function name is special to pytest.  See
# https://doc.pytest.org/en/latest/how-to/writing_plugins.html#initialization-command-line-and-configuration-hooks
def pytest_addoption(parser) -> None:
    parser.addoption(
        "--bench", action="store_true", default=False, help="Enable the benchmark test runs"

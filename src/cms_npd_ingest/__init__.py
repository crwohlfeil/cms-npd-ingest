"""Ingest CMS National Provider Directory bulk files into DuckDB."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("cms-npd-ingest")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

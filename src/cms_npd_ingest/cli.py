import argparse
import logging
import sys
from pathlib import Path

from cms_npd_ingest import __version__

log = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cms-npd-ingest",
        description="Ingest CMS National Provider Directory bulk files into DuckDB.",
    )
    parser.add_argument("files", nargs="+", type=Path, help="NDJSON+zstd files to ingest")
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("data/npd.duckdb"),
        help="DuckDB database path (default: %(default)s)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10_000,
        help="records per insert batch (default: %(default)s)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="debug logging")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    missing = [p for p in args.files if not p.is_file()]
    if missing:
        for p in missing:
            log.error("not a file: %s", p)
        return 1

    try:
        for path in args.files:
            log.info("%s", path.name)
    except KeyboardInterrupt:
        log.warning("interrupted")
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())

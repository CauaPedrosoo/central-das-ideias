from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from central_das_ideias.sheets_store import SheetsStore


WORKSHEETS = {
    "news_intake": {
        "csv": ROOT / "data" / "news_intake.csv",
        "key": "article_url",
    },
    "context_enrichment": {
        "csv": ROOT / "data" / "context_enrichment.csv",
        "key": "context_id",
    },
    "creative_outputs": {
        "csv": ROOT / "data" / "creative_outputs.csv",
        "key": "creative_id",
    },
    "content_ideas": {
        "csv": ROOT / "data" / "content_ideas.csv",
        "key": "idea_id",
    },
    "lead_assets": {
        "csv": ROOT / "data" / "lead_assets.csv",
        "key": "asset_id",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync local seed data with Google Sheets.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("bootstrap", help="Create worksheets and replace them with seed CSV data.")
    subparsers.add_parser("snapshot", help="Download current worksheets to data/runtime.")
    subparsers.add_parser(
        "upsert-runtime",
        help="Upsert CSVs from data/runtime into matching worksheets.",
    )

    upsert = subparsers.add_parser("upsert", help="Upsert all local CSVs into matching worksheets.")
    upsert.add_argument(
        "--worksheet",
        choices=list(WORKSHEETS.keys()),
        help="Limit upsert to a specific worksheet.",
    )

    return parser.parse_args()


def main() -> None:
    load_dotenv(ROOT / ".env")

    spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "").strip()
    store = SheetsStore(spreadsheet_id=spreadsheet_id)
    args = parse_args()

    if args.command == "bootstrap":
        bootstrap(store)
        return

    if args.command == "snapshot":
        snapshot(store)
        return

    if args.command == "upsert":
        upsert(store, args.worksheet)
        return

    if args.command == "upsert-runtime":
        upsert_runtime(store)
        return

    raise RuntimeError(f"Comando nao suportado: {args.command}")


def bootstrap(store: SheetsStore) -> None:
    for worksheet, config in WORKSHEETS.items():
        headers = _read_headers(config["csv"])
        store.ensure_worksheet(worksheet, headers)
        store.replace_with_csv(worksheet, config["csv"])
        print(f"[bootstrap] {worksheet} inicializada com {config['csv'].name}")


def snapshot(store: SheetsStore) -> None:
    runtime_dir = ROOT / "data" / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)

    for worksheet in WORKSHEETS:
        output_path = runtime_dir / f"{worksheet}.csv"
        store.export_csv(worksheet, output_path)
        print(f"[snapshot] {worksheet} -> {output_path}")


def upsert(store: SheetsStore, worksheet: str | None) -> None:
    targets = [worksheet] if worksheet else list(WORKSHEETS.keys())
    for name in targets:
        config = WORKSHEETS[name]
        headers = _read_headers(config["csv"])
        store.ensure_worksheet(name, headers)
        store.upsert_csv(name, config["csv"], config["key"])
        print(f"[upsert] {name} sincronizada com {config['csv'].name}")


def upsert_runtime(store: SheetsStore) -> None:
    runtime_dir = ROOT / "data" / "runtime"
    for name, config in WORKSHEETS.items():
        runtime_csv = runtime_dir / f"{name}.csv"
        if not runtime_csv.exists():
            print(f"[upsert-runtime] ignorando {name}: {runtime_csv} nao existe")
            continue
        headers = _read_headers(config["csv"])
        store.ensure_worksheet(name, headers)
        store.upsert_csv(name, runtime_csv, config["key"])
        print(f"[upsert-runtime] {name} sincronizada com {runtime_csv.name}")


def _read_headers(csv_path: Path) -> list[str]:
    first_line = csv_path.read_text(encoding="utf-8").splitlines()[0]
    return first_line.split(",")


if __name__ == "__main__":
    main()

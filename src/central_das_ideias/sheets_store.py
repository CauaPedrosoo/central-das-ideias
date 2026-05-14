from __future__ import annotations

import csv
import io
import json
import os
from pathlib import Path
from typing import Iterable

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class SheetsStore:
    def __init__(self, spreadsheet_id: str) -> None:
        if not spreadsheet_id:
            raise ValueError("GOOGLE_SHEETS_SPREADSHEET_ID nao configurado.")
        self.spreadsheet_id = spreadsheet_id
        self.service = build("sheets", "v4", credentials=_load_credentials())

    def ensure_worksheet(self, title: str, headers: list[str]) -> None:
        metadata = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        existing_titles = {
            sheet["properties"]["title"] for sheet in metadata.get("sheets", [])
        }

        if title not in existing_titles:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={
                    "requests": [
                        {
                            "addSheet": {
                                "properties": {
                                    "title": title,
                                }
                            }
                        }
                    ]
                },
            ).execute()

        values = self._get_values(title)
        if not values:
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f"{title}!A1",
                valueInputOption="RAW",
                body={"values": [headers]},
            ).execute()

    def read_rows(self, title: str) -> list[dict[str, str]]:
        values = self._get_values(title)
        if not values:
            return []

        headers = values[0]
        rows: list[dict[str, str]] = []
        for row in values[1:]:
            padded = row + [""] * (len(headers) - len(row))
            rows.append(dict(zip(headers, padded)))
        return rows

    def replace_with_csv(self, title: str, csv_path: Path) -> None:
        rows = _csv_to_rows(csv_path)
        if not rows:
            raise ValueError(f"CSV vazio: {csv_path}")

        self.service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheet_id,
            range=title,
        ).execute()
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=f"{title}!A1",
            valueInputOption="RAW",
            body={"values": rows},
        ).execute()

    def upsert_csv(self, title: str, csv_path: Path, key_column: str) -> None:
        incoming = _csv_to_dict_rows(csv_path)
        if not incoming:
            return

        existing = self.read_rows(title)
        headers = list(incoming[0].keys())
        merged: dict[str, dict[str, str]] = {}

        for row in existing:
            merged[row.get(key_column, "")] = {header: row.get(header, "") for header in headers}

        for row in incoming:
            row_key = row.get(key_column, "")
            if not row_key:
                continue
            merged[row_key] = row

        final_rows = [headers] + [[row.get(header, "") for header in headers] for row in merged.values()]
        self.service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheet_id,
            range=title,
        ).execute()
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=f"{title}!A1",
            valueInputOption="RAW",
            body={"values": final_rows},
        ).execute()

    def export_csv(self, title: str, output_path: Path) -> None:
        rows = self._get_values(title)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerows(rows)

    def _get_values(self, title: str) -> list[list[str]]:
        response = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=title,
        ).execute()
        return response.get("values", [])


def _load_credentials() -> Credentials:
    raw_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    file_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "").strip()

    if raw_json:
        info = json.loads(raw_json)
        return Credentials.from_service_account_info(info, scopes=SCOPES)

    if file_path:
        return Credentials.from_service_account_file(file_path, scopes=SCOPES)

    raise ValueError(
        "Configure GOOGLE_SERVICE_ACCOUNT_JSON ou GOOGLE_SERVICE_ACCOUNT_FILE."
    )


def _csv_to_rows(csv_path: Path) -> list[list[str]]:
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.reader(handle))


def _csv_to_dict_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


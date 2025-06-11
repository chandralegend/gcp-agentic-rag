"""Index Markdown documents with metadata into Google Cloud Datastore."""

import argparse
import json
import os
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv
from google.cloud import datastore


def load_entries(md_dir: Path, metadata_file: Path) -> List[Dict[str, Any]]:
    """Load markdown content and metadata."""
    with metadata_file.open("r", encoding="utf-8") as f:
        items = json.load(f)

    entries: List[Dict[str, Any]] = []
    for item in items:
        file_path = md_dir / item["filename"]
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()
        entries.append(
            {
                "id": item["filename"],
                "content": content,
                "metadata": item.get("metadata", {}),
            }
        )
    return entries


def index_to_datastore(project: str, kind: str, entries: List[Dict[str, Any]]) -> None:
    """Write the entries to Datastore."""
    client = datastore.Client(project=project)
    for entry in entries:
        key = client.key(kind, entry["id"])
        entity = datastore.Entity(key=key)
        entity["content"] = entry["content"]
        for k, v in entry["metadata"].items():
            entity[k] = v
        client.put(entity)
    print(f"Indexed {len(entries)} documents to Datastore kind '{kind}'")


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Index markdown files into Datastore")
    parser.add_argument("--markdown-dir", type=Path, default=Path("docs"), help="Directory containing markdown files")
    parser.add_argument("--metadata-file", type=Path, required=True, help="JSON file with metadata")
    parser.add_argument("--project", default=os.getenv("GOOGLE_CLOUD_PROJECT"), help="GCP project id")
    parser.add_argument("--kind", default=os.getenv("DATASTORE_KIND", "Document"), help="Datastore kind")
    args = parser.parse_args()

    entries = load_entries(args.markdown_dir, args.metadata_file)
    if not args.project:
        raise ValueError("GCP project must be specified via --project or environment variable")
    index_to_datastore(args.project, args.kind, entries)


if __name__ == "__main__":
    main()

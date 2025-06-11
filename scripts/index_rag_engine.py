"""Upload markdown documents with metadata to a Vertex AI RAG Engine corpus."""

import argparse
import json
import os
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv
import vertexai
from vertexai.preview import rag


def load_entries(md_dir: Path, metadata_file: Path) -> List[Dict[str, Any]]:
    """Load file paths and metadata."""
    with metadata_file.open("r", encoding="utf-8") as f:
        items = json.load(f)

    entries: List[Dict[str, Any]] = []
    for item in items:
        file_path = md_dir / item["filename"]
        entries.append(
            {
                "path": file_path,
                "display_name": item["filename"],
                "metadata": item.get("metadata", {}),
            }
        )
    return entries


def upload_to_rag(corpus: str, project: str, location: str, entries: List[Dict[str, Any]]) -> None:
    """Upload the files to an existing RAG corpus."""
    vertexai.init(project=project, location=location)
    for entry in entries:
        description = json.dumps(entry["metadata"])
        rag.upload_file(
            corpus_name=corpus,
            path=str(entry["path"]),
            display_name=entry["display_name"],
            description=description,
        )
    print(f"Uploaded {len(entries)} files to corpus '{corpus}'")


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Upload markdown files to a RAG corpus")
    parser.add_argument("--markdown-dir", type=Path, default=Path("docs"), help="Directory with markdown files")
    parser.add_argument("--metadata-file", type=Path, required=True, help="JSON file with metadata")
    parser.add_argument("--corpus", default=os.getenv("RAG_CORPUS"), help="RAG corpus name")
    parser.add_argument("--project", default=os.getenv("GOOGLE_CLOUD_PROJECT"), help="GCP project id")
    parser.add_argument("--location", default=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"), help="GCP region")
    args = parser.parse_args()

    if not args.corpus:
        raise ValueError("RAG corpus must be specified via --corpus or environment variable")
    if not args.project:
        raise ValueError("GCP project must be specified via --project or environment variable")

    entries = load_entries(args.markdown_dir, args.metadata_file)
    upload_to_rag(args.corpus, args.project, args.location, entries)


if __name__ == "__main__":
    main()

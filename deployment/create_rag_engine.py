"""Create a Vertex AI RAG Engine corpus from local Markdown files."""
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv, set_key
from google.cloud import storage
import vertexai
from vertexai.preview import rag


def upload_markdown_files(bucket_name: str, md_dir: Path) -> List[str]:
    """Upload all markdown files in a directory to GCS and return their URIs."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    gcs_uris: List[str] = []
    for md_path in md_dir.glob("*.md"):
        blob = bucket.blob(md_path.name)
        blob.upload_from_filename(md_path)
        gcs_uris.append(f"gs://{bucket_name}/{md_path.name}")
    return gcs_uris


def main() -> None:
    load_dotenv()
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    bucket = os.getenv("STAGING_BUCKET")
    md_dir = Path(os.getenv("MARKDOWN_DIR", "docs"))
    corpus_display_name = os.getenv("RAG_CORPUS_DISPLAY", "markdown_corpus")
    corpus_description = os.getenv("RAG_CORPUS_DESCRIPTION", "Markdown files corpus")
    env_file = Path(__file__).resolve().parent.parent / ".env"

    vertexai.init(project=project, location=location)

    embedding_model = rag.EmbeddingModelConfig(publisher_model="publishers/google/models/text-embedding-004")
    corpus = rag.create_corpus(
        display_name=corpus_display_name,
        description=corpus_description,
        embedding_model_config=embedding_model,
    )

    gcs_uris = upload_markdown_files(bucket, md_dir)
    for uri in gcs_uris:
        rag.upload_file(corpus_name=corpus.name, path=uri, display_name=Path(uri).name)

    set_key(env_file, "RAG_CORPUS", corpus.name)
    print(f"Created RAG corpus: {corpus.name}")


if __name__ == "__main__":
    main()

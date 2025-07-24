import json
from tqdm import tqdm
from typing import List
from pprint import pprint
from config import INDEX_NAME
from utils import get_es_client
from elasticsearch import Elasticsearch
from pathlib import Path


def index_data(documents: List[dict]):
    es = get_es_client(max_retries=5, sleep_time=5)
    _ = _create_index(es=es)
    _ = _insert_documents(es=es, documents=documents)
    pprint(f'Indexed {len(documents)} documents into Elasticsearch index "{INDEX_NAME}"')


def _create_index(es: Elasticsearch) -> dict:
    es.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
    return es.indices.create(index=INDEX_NAME)


def _insert_documents(es: Elasticsearch, documents: List[dict]) -> dict:
    operations = []
    for document in tqdm(documents, total=len(documents), desc="Indexing documents"):
        operations.append({"index": {"_index": INDEX_NAME}})
        operations.append(document)
    return es.bulk(operations=operations)

if __name__ == "__main__":
    data_path = Path(__file__).resolve().parents[1] / "data" / "apod.json"
    with open(data_path, "r") as f:
        documents = json.load(f)

    index_data(documents=documents)

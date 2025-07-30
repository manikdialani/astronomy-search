import json
from tqdm import tqdm
from typing import List
from pprint import pprint
from config import INDEX_NAME_RAW
from utils import get_es_client
from elasticsearch import Elasticsearch
from elastic_transport import ObjectApiResponse
from pathlib import Path


def index_data(documents: List[dict]) -> None:
    pipeline_id = 'apod_pipeline'
    es = get_es_client(max_retries=5, sleep_time=5)

    _ = _create_pipeline(es=es, pipeline_id=pipeline_id)
    _ = _create_index(es=es)
    _ = _insert_documents(es=es, documents=documents, pipeline_id=pipeline_id)
    pprint(f'Indexed {len(documents)} documents into Elasticsearch index "{INDEX_NAME_RAW}"')

# This function creates an ingest pipeline that removes HTML tags from apod_raw.json
def _create_pipeline(es: Elasticsearch, pipeline_id: str) -> dict:
    pipeline_body = {
        "description": "Pipeline that strips HTML tags from the explanation and title fields",
        "processors": [
            {
                "html_strip": {
                    "field": "explanation"                
                    }
            },
            {
                "html_strip": {
                    "field": "title"
                }
            }
        ]
    }
    return es.ingest.put_pipeline(id=pipeline_id, body=pipeline_body)

def _create_index(es: Elasticsearch) -> dict:
    _ = es.indices.delete(index=INDEX_NAME_RAW, ignore_unavailable=True)
    return es.indices.create(index=INDEX_NAME_RAW)

def _insert_documents(es: Elasticsearch, documents: List[dict], pipeline_id: str) -> dict:
    operations = []
    for document in tqdm(documents, total=len(documents), desc="Indexing documents"):
        operations.append({"index": {"_index": INDEX_NAME_RAW}})
        operations.append(document)
    return es.bulk(operations=operations, pipeline=pipeline_id)

if __name__ == "__main__":
    data_path = Path(__file__).resolve().parents[3] / "data" / "apod_raw.json"
    with open(data_path, "r") as f:
        documents = json.load(f)

    index_data(documents=documents)

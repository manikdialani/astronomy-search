import json
import torch
from tqdm import tqdm
from typing import List
from pprint import pprint
from config import INDEX_NAME_EMBEDDING
from utils import get_es_client
from elasticsearch import Elasticsearch
from elastic_transport import ObjectApiResponse
from pathlib import Path
from sentence_transformers import SentenceTransformer


def index_data(documents: List[dict], model: SentenceTransformer) -> None:
    es = get_es_client(max_retries=5, sleep_time=5)
    _ = _create_index(es=es)
    _ = _insert_documents(es=es, documents=documents, model=model)
    pprint(f'Indexed {len(documents)} documents into Elasticsearch index "{INDEX_NAME_EMBEDDING}"')

# This function creates an index uses dense vector type for embedding
def _create_index(es: Elasticsearch) -> ObjectApiResponse:
    index_name =  INDEX_NAME_EMBEDDING

    _ = es.indices.delete(index=index_name, ignore_unavailable=True)
    return es.indices.create(
        index=index_name,
        mappings={
            "properties": {
                "embedding": {
                    "type": "dense_vector",
                }
            }
        }
    )


def _insert_documents(es: Elasticsearch, documents: List[dict], model: SentenceTransformer) -> dict:
    operations = []
    for document in tqdm(documents, total=len(documents), desc="Indexing documents"):
        operations.append({"index": {"_index": INDEX_NAME_EMBEDDING}})
        operations.append({
            **document,
            "embedding": model.encode(document['explanation']).tolist() if hasattr(model.encode(document['explanation']), "tolist") else list(model.encode(document['explanation']))
        })
    return es.bulk(operations=operations)

if __name__ == "__main__":
    data_path = Path(__file__).resolve().parents[3] / "data" / "apod.json"
    with open(data_path, "r") as f:
        documents = json.load(f)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SentenceTransformer("all-MiniLM-L6-v2").to(device)
    index_data(documents=documents, model=model)

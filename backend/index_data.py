import json
from tqdm import tqdm
from typing import List
from pprint import pprint
from config import INDEX_NAME_DEFAULT, INDEX_NAME_N_GRAM
from utils import get_es_client
from elasticsearch import Elasticsearch
from pathlib import Path


def index_data(documents: List[dict], use_n_gram_tokenizer: bool = False) -> None:
    es = get_es_client(max_retries=5, sleep_time=5)
    _ = _create_index(es=es, use_n_gram_tokenizer=use_n_gram_tokenizer)
    _ = _insert_documents(es=es, documents=documents, use_n_gram_tokenizer=use_n_gram_tokenizer)
    index_name = INDEX_NAME_N_GRAM if use_n_gram_tokenizer else INDEX_NAME_DEFAULT
    pprint(f'Indexed {len(documents)} documents into Elasticsearch index "{index_name}"')


def _create_index(es: Elasticsearch, use_n_gram_tokenizer: bool) -> dict:
    tokenizer = 'n_gram_tokenizer' if use_n_gram_tokenizer else 'standard'
    index_name = INDEX_NAME_N_GRAM if use_n_gram_tokenizer else INDEX_NAME_DEFAULT

    _ = es.indices.delete(index=index_name, ignore_unavailable=True)

    return es.indices.create(
        index=index_name,
        settings={
            "analysis": {
                "analyzer": {
                    "n_gram_analyzer": {
                        "type": "custom",
                        "tokenizer": "n_gram_tokenizer",
                        "filter": ["lowercase"],
                    },
                    "n_gram_search_analyzer": {
                        "type": "custom",
                        "tokenizer": 'standard',
                        "filter": ["lowercase"],
                    },
                },
                "tokenizer": {
                    "n_gram_tokenizer": {
                        "type": "edge_ngram",
                        "min_gram": 1,
                        "max_gram": 30,
                        "token_chars": ["letter", "digit"],
                    },
                },
            },
        },
        mappings={
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "n_gram_analyzer",  # or your n-gram analyzer name
                    "search_analyzer": "n_gram_search_analyzer"  # or "standard"
                },
                "explanation": {
                    "type": "text",
                    "analyzer": "n_gram_analyzer",  # or your n-gram analyzer name
                    "search_analyzer": "n_gram_search_analyzer"  # or "standard"
                },
                "date": {
                    "type": "date",
                    "format": "yyyy-MM-dd"
                },
            },
        },
    )


def _insert_documents(es: Elasticsearch, documents: List[dict], use_n_gram_tokenizer: bool) -> dict:
    operations = []
    index_name = INDEX_NAME_N_GRAM if use_n_gram_tokenizer else INDEX_NAME_DEFAULT
    for document in tqdm(documents, total=len(documents), desc="Indexing documents"):
        operations.append({"index": {"_index": index_name}})
        operations.append(document)
    return es.bulk(operations=operations)

if __name__ == "__main__":
    data_path = Path(__file__).resolve().parents[3] / "data" / "apod.json"
    with open(data_path, "r") as f:
        documents = json.load(f)

    index_data(documents=documents, use_n_gram_tokenizer=True)

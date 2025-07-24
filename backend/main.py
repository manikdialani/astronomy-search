from config import INDEX_NAME
from elastic_transport import ObjectApiResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
# from sentence_transformers import SentenceTransformer
from utils import get_es_client
'''

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/search/")
async def search(
    search_query: str,
    skip: int = 0,
    limit: int = 10,
) -> dict:
    es = get_es_client(max_retries=5, sleep_time=5)
    response = es.search(
        index=INDEX_NAME,
        body={
            "query": {
                "multi_match": {
                    "query": search_query,
                    "fields": ["title", "explanation"]
                }
            },
            "from": skip,
            "size": limit
        },
        filter_path=["hits.hits._source, hits.hits._score"]

    )
    hits = response["hits"]["hits"]
    return {"hits": hits}

'''


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/regular_search")
async def regular_search(
    search_query: str,
    skip: int = 0,
    limit: int = 10,
    year: str = "",
    tokenizer: str = "Standard"
) -> dict:
    es = get_es_client(max_retries=5, sleep_time=5)
    query = {
        "multi_match": {
            "query": search_query,
            "fields": ["title", "explanation"],
        }
    }
    # If you want to filter by year, add a filter here
    if year:
        query = {
            "bool": {
                "must": [query],
                "filter": [{"term": {"year": year}}]
            }
        }

    response = es.search(
        index=INDEX_NAME,
        body={
            "query": query,
            "from": skip,
            "size": limit
        },
        filter_path=["hits.hits._source, hits.hits._score"]
    )
    hits = response["hits"]["hits"]
    return {"hits": hits}

@app.get("/api/v1/get_docs_per_year_count")
async def get_docs_per_year_count(
    search_query: str,
    tokenizer: str = "Standard"
) -> dict:
    es = get_es_client(max_retries=5, sleep_time=5)
    response = es.search(
        index=INDEX_NAME,
        body={
            "size": 0,
            "query": {
                "multi_match": {
                    "query": search_query,
                    "fields": ["title", "explanation"]
                }
            },
            "aggs": {
                "years": {
                    "terms": {"field": "year"}
                }
            }
        }
    )
    buckets = response["aggregations"]["years"]["buckets"]
    return {"year_counts": buckets}

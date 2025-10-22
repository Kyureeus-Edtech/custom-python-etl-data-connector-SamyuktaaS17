import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# MongoDB URI from .env (or default to localhost)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "etl_db"
COLLECTION_NAME = "ipapi_raw"

def fetch_single_ip(ip):
    url = f"http://ip-api.com/json/{ip}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        data["endpoint"] = "json"
        data["query"] = ip
        return data
    else:
        return {"error": r.text, "query": ip}

def fetch_batch(ips):
    url = "http://ip-api.com/batch"
    r = requests.post(url, json=ips)
    if r.status_code == 200:
        datas = r.json()
        for data, ip in zip(datas, ips):
            data["endpoint"] = "batch"
            data["query"] = ip
        return datas
    else:
        return [{"error": r.text, "endpoint": "batch"}]

def fetch_csv(ip):
    url = f"http://ip-api.com/csv/{ip}"
    r = requests.get(url)
    if r.status_code == 200:
        line = r.text.strip()
        fields = line.split(",")
        return {
            "endpoint": "csv",
            "query": ip,
            "fields": fields
        }
    else:
        return {"error": r.text, "endpoint": "csv", "query": ip}

def ingest_to_mongo(data_list):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    col = db[COLLECTION_NAME]
    now = datetime.utcnow().isoformat()
    docs = []
    for data in data_list:
        data["ingested_at"] = now
        docs.append(data)
    if docs:
        col.insert_many(docs)
        print(f"Inserted {len(docs)} documents")
    else:
        print("No documents to insert")

if __name__ == "__main__":
    ips = ["8.8.8.8", "1.1.1.1", "208.80.152.201"]

    # Extract: fetch from three endpoints
    data_single = [fetch_single_ip(ip) for ip in ips]
    data_batch = fetch_batch(ips)
    data_csv = [fetch_csv(ip) for ip in ips]

    # Combine all for this assignment example
    all_data = data_single + data_batch + data_csv

    # Load: insert to MongoDB
    ingest_to_mongo(all_data)

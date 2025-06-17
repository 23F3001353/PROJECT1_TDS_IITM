from fastapi import FastAPI, HTTPException
import json, os

app = FastAPI()
PAGES_DIR = "tds_pages_md"
DISCOURSE_DATA = "discourse_posts.json"

# Load scraped data
with open(DISCOURSE_DATA, encoding="utf-8") as f:
    discourse_posts = json.load(f)

@app.get("/")
def root():
    return {"message": "TDS Virtual Teaching Assistant is alive!"}

@app.post("/query")
def answer_question(question: str):
    # (Stub) Very basic keyword lookup across course page titles
    matches = []
    for fname in os.listdir(PAGES_DIR):
        if question.lower() in fname.lower():
            with open(os.path.join(PAGES_DIR, fname), encoding="utf-8") as md:
                matches.append({"page": fname, "snippet": md.read()[:200]})
    if not matches:
        raise HTTPException(status_code=404, detail="No matching content found")
    return {"query": question, "results": matches}

import json
from pathlib import Path
from app.agent.graph import ask_agent
from app.rag.retrieval import retrieve

DATASET = Path(__file__).with_name("dataset.json")

def run():
    cases = json.loads(DATASET.read_text())
    retrieval_hits = source_hits = keyword_hits = 0
    for case in cases:
        results = retrieve(case["question"], top_k=4)
        if case["expected_source"] in {r["source"] for r in results}:
            retrieval_hits += 1
        response = ask_agent(case["question"])
        if case["expected_source"] in {s["source"] for s in response["sources"]}:
            source_hits += 1
        answer = response["answer"].lower()
        if all(k.lower() in answer for k in case["expected_keywords"]):
            keyword_hits += 1
    total = len(cases)
    print(f"Cases: {total}")
    print(f"Retrieval Recall@4: {retrieval_hits/total:.2%}")
    print(f"Source accuracy:    {source_hits/total:.2%}")
    print(f"Keyword grounding:  {keyword_hits/total:.2%}")

if __name__ == "__main__":
    run()

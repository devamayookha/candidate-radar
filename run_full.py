"""
run_full.py

Runs the full scoring pipeline across all 100,000 candidates, produces the
top 100 ranked list with reasoning, and times the run to confirm it fits
the 5-minute / CPU-only compute budget from submission_spec.md.
"""

import json
import csv
import time
from combine import combine_scores
from score_text import score_jd_text_match_batch
from generate_reasoning import generate_reasoning

t0 = time.time()

print("Loading all candidates...")
candidates = []
with open("data/candidates.jsonl") as f:
    for line in f:
        if line.strip():
            candidates.append(json.loads(line))
print(f"Loaded {len(candidates)} candidates in {time.time()-t0:.1f}s")
print("Computing JD text-match scores (batch TF-IDF over full pool)...")
t1 = time.time()
text_results = score_jd_text_match_batch(candidates)
text_scores = [r["jd_text_match_score"] for r in text_results]
print(f"Text scoring done in {time.time()-t1:.1f}s")

print("Computing combined scores for all candidates...")
t2 = time.time()
all_results = []
for c, text_score in zip(candidates, text_scores):
    r = combine_scores(c, text_score)
    all_results.append((c, r))
print(f"Combined scoring done in {time.time()-t2:.1f}s")

print("Sorting and taking top 100...")
all_results.sort(key=lambda x: -x[1]["final_score"])
top_100 = all_results[:100]

total_time = time.time() - t0
print(f"\nTOTAL TIME: {total_time:.1f}s ({total_time/60:.2f} minutes)")
print(f"Compute budget check: {'PASS' if total_time < 300 else 'FAIL'} (limit: 300s / 5 min)")

print("Writing submission CSV...")
with open("output/submission.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["candidate_id", "rank", "score", "reasoning"])
    for i, (c, r) in enumerate(top_100, 1):
        reasoning = generate_reasoning(c, r, i)
        writer.writerow([r["candidate_id"], i, r["final_score"], reasoning])

print("\nDone. Submission saved to output/submission.csv")
print(f"Score range: {top_100[0][1]['final_score']:.4f} (rank 1) to {top_100[-1][1]['final_score']:.4f} (rank 100)")
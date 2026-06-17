"""
score_text.py

JD text-similarity component of the base score (weight: 0.15). Checks
whether a candidate's own summary/headline reads like the kind of person
this JD describes, even without using the JD's exact keywords. Uses
TF-IDF + cosine similarity - word-frequency statistics, not a neural
embedding model, so it stays fast and CPU-only.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

JD_REFERENCE_TEXT = """
Own the intelligence layer of the product: the ranking, retrieval, and
matching systems that decide what recruiters see when they search for
candidates and what candidates see when they search for roles. Production
experience with embeddings-based retrieval systems deployed to real users,
handling embedding drift, index refresh, retrieval quality regression in
production. Production experience with vector databases and hybrid search
infrastructure. Strong Python and code quality. Hands-on experience designing
evaluation frameworks for ranking systems: NDCG, MRR, MAP, offline to online
correlation, A/B test interpretation. Has shipped at least one end to end
ranking, search, or recommendation system to real users at meaningful scale.
Has strong opinions about retrieval, evaluation, and LLM integration and can
defend them with reference to systems actually built. Comfortable with deep
technical depth in modern ML systems: embeddings, retrieval, ranking, LLMs,
fine tuning. Also comfortable with a scrappy product engineering attitude,
willing to ship a working ranker quickly even if the underlying ML is
suboptimal, learning from real users before knowing what to optimize for.
Thinks about systems, not frameworks. Has applied ML or AI experience at
product companies, not purely services or consulting. Active in the AI and
machine learning space with real production deployment experience, not just
academic research or recent LLM API wrapper projects.
"""


def build_corpus_texts(candidate):
    p = candidate.get("profile", {})
    parts = [p.get("headline", ""), p.get("summary", ""), p.get("current_title", "")]

    history = candidate.get("career_history", [])
    sorted_history = sorted(
        history,
        key=lambda r: (not r.get("is_current", False), r.get("start_date", "")),
        reverse=False,
    )
    for role in sorted_history[:2]:
        parts.append(role.get("description", ""))

    return " ".join(parts)


class JDTextSimilarityScorer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
        )
        self.jd_vector = None

    def fit(self, all_texts):
        corpus = [JD_REFERENCE_TEXT] + list(all_texts)
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        self.jd_vector = tfidf_matrix[0:1]
        return tfidf_matrix[1:]

    def score_all(self, all_texts):
        candidate_vectors = self.fit(all_texts)
        similarities = cosine_similarity(self.jd_vector, candidate_vectors)[0]
        return similarities


def score_jd_text_match_batch(candidates):
    texts = [build_corpus_texts(c) for c in candidates]
    scorer = JDTextSimilarityScorer()
    scores = scorer.score_all(texts)
    return [{"jd_text_match_score": round(float(s), 4)} for s in scores]
"""
jd_config.py

This file encodes the Redrob "Senior AI Engineer - Founding Team" job
description as explicit, structured scoring inputs. Every constant here
should be traceable back to a specific sentence in job_description.md.
"""

MUST_HAVE_SKILL_GROUPS = {
    "embeddings_retrieval": [
        "sentence-transformers", "sentence transformers", "openai embeddings",
        "bge", "e5", "embeddings", "dense retrieval", "text encoders",
        "vector representations", "semantic search",
    ],
    "vector_db_hybrid_search": [
        "pinecone", "weaviate", "qdrant", "milvus", "opensearch",
        "elasticsearch", "faiss", "pgvector", "vector search", "hybrid retrieval",
        "bm25", "search backend",
    ],
    "python": [
        "python",
    ],
    "eval_frameworks": [
        "ndcg", "mrr", "map", "learning to rank", "a/b testing", "offline evaluation",
        "evaluation frameworks", "information retrieval",
    ],
}
NICE_TO_HAVE_SKILLS = [
    "lora", "qlora", "peft", "fine-tuning llms", "xgboost", "neural ranking",
    "distributed systems", "large-scale inference", "open source",
]

AI_KEYWORD_SURFACE_TERMS = (
    MUST_HAVE_SKILL_GROUPS["embeddings_retrieval"]
    + MUST_HAVE_SKILL_GROUPS["vector_db_hybrid_search"]
    + MUST_HAVE_SKILL_GROUPS["eval_frameworks"]
    + NICE_TO_HAVE_SKILLS
    + ["nlp", "llm", "llms", "rag", "retrieval augmented generation",
       "transformers", "deep learning", "machine learning", "gans",
       "diffusion models", "speech recognition", "image classification", "tts"]
)
SHIPPING_EVIDENCE_TERMS = [
    "ranking", "search", "recommendation", "recommender", "retrieval",
    "matching system", "search infrastructure", "discovery", "relevance",
    "personalization", "feed ranking",
]
TITLE_CHASER_MAX_AVG_TENURE_MONTHS = 18
CONSULTING_FIRMS = {
    "tcs", "infosys", "wipro", "accenture", "cognizant", "capgemini",
    "hcl", "tech mahindra", "mphasis", "mindtree", "genpact ai",
}
CV_SPEECH_ROBOTICS_TERMS = [
    "computer vision", "image classification", "object detection", "speech recognition",
    "tts", "robotics", "gans", "diffusion models",
]
NLP_IR_CROSSOVER_TERMS = [
    "nlp", "natural language processing", "information retrieval", "search",
    "ranking", "retrieval", "embeddings", "llm", "text",
]
NON_TECHNICAL_TITLES = {
    "business analyst", "hr manager", "accountant", "project manager",
    "customer support", "operations manager", "content writer",
    "sales executive", "graphic designer", "marketing manager",
    "civil engineer", "mechanical engineer",
}
LANGCHAIN_TOURIST_TERMS = ["langchain", "openai api", "prompt engineering"]
PRE_LLM_ML_PRODUCTION_TERMS = [
    "machine learning", "recommendation", "ranking", "search", "nlp",
    "classification", "feature engineering", "production ml",
]
PURE_LEADERSHIP_TITLE_TERMS = ["architect", "engineering manager", "tech lead", "director", "vp "]
RESEARCH_ONLY_INDUSTRY_TERMS = ["academia", "research institute", "r&d lab"]
RESEARCH_ONLY_TITLE_TERMS = ["research scientist", "research fellow", "postdoc", "phd researcher"]
PREFERRED_LOCATIONS = {"pune", "noida"}
ACCEPTABLE_INDIA_LOCATIONS = {"hyderabad", "pune", "mumbai", "delhi", "noida", "gurgaon", "gurugram", "ncr"}

NOTICE_PERIOD_IDEAL_DAYS = 30
EXPERIENCE_BAND_MIN = 5
EXPERIENCE_BAND_MAX = 9
EXPERIENCE_IDEAL_CENTER = 7.0
BASE_SCORE_WEIGHTS = {
    "career_trajectory": 0.40,
    "skill_match": 0.25,
    "jd_text_match": 0.15,
    "seniority_logistics_fit": 0.20,
}

assert abs(sum(BASE_SCORE_WEIGHTS.values()) - 1.0) < 1e-9, "Base score weights must sum to 1.0"
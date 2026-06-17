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
PENALTY_MULTIPLIERS = {
    "research_only_no_production": 0.05,
    "consulting_only_no_product_experience": 0.20,
    "cv_speech_robotics_no_nlp_crossover": 0.25,
    "langchain_tourist_no_pre_llm_experience": 0.20,
    "pure_leadership_no_recent_code": 0.30,
    "title_chaser_pattern": 0.55,
}
COMPANY_FOUNDING_YEAR = {
    # Real Indian AI-native / product startups - the companies where an
    # implausible "years at company vs founding year" honeypot is plausible.
    "sarvam ai": 2023,
    "krutrim": 2023,
    "rephrase.ai": 2019,
    "aganitha": 2017,
    "niramai": 2016,
    "saarthi.ai": 2017,
    "mad street den": 2014,
    "observe.ai": 2017,
    "wysa": 2015,
    "haptik": 2013,
    "verloop.io": 2015,
    "yellow.ai": 2016,
    "locobuzz": 2011,
    "glance": 2018,  # NOTE: sources conflict between 2018 (commercial launch)
    # and 2019 (legal founding) - we use the earlier year so this check
    # never wrongly flags a real candidate over an ambiguous date.

    # Larger / well-established real Indian product and consulting companies -
    # founded long enough ago that this check will not realistically fire,
    # included for completeness.
    "swiggy": 2014,
    "razorpay": 2014,
    "cred": 2018,
    "capgemini": 1967,
    "hcl": 1976,
    "zomato": 2008,
    "flipkart": 2007,
    "mindtree": 1999,
    "accenture": 1989,
    "cognizant": 1994,
    "tech mahindra": 1986,
    "mphasis": 1998,
    "genpact ai": 1997,
    "meesho": 2015,
    "nykaa": 2012,
    "inmobi": 2007,
    "byju's": 2011,
    "policybazaar": 2008,
    "ola": 2010,
    "zoho": 1996,
    "vedantu": 2014,
    "paytm": 2010,
    "unacademy": 2015,
    "pharmeasy": 2015,
    "upgrad": 2015,
    "freshworks": 2010,
    "phonepe": 2015,
    "dream11": 2008,
    "tcs": 1968,
    "infosys": 1981,
    "wipro": 1945,

    # Global big tech - founding years included for completeness; with only
    # 7-14 candidates each in the dataset and decades of history, this check
    # will not realistically fire on these.
    "google": 1998,
    "netflix": 1997,
    "amazon": 1994,
    "salesforce": 1999,
    "uber": 2009,
    "meta": 2004,
    "adobe": 1982,
    "microsoft": 1975,
    "apple": 1976,
    "linkedin": 2002,

    # Fictional placeholder companies used as filler employers in the dataset.
    # No real founding date exists; treated as "always old enough" so the
    # honeypot check never fires on them.
    "pied piper": 1900,
    "initech": 1900,
    "wayne enterprises": 1900,
    "acme corp": 1900,
    "stark industries": 1900,
    "hooli": 1900,
    "globex inc": 1900,
    "dunder mifflin": 1900,
}
"""
generate_reasoning.py

Produces the `reasoning` column for the submission CSV. Every sentence here
is built from values already present in combine_scores() output - we never
invent a fact. If a value isn't in the candidate's actual profile, it
cannot appear in their reasoning.
"""


def _format_tenure(years):
    if years == int(years):
        return f"{int(years)} years"
    return f"{years:.1f} years"


def _top_skill_groups(skill_component, n=2):
    groups = skill_component["skill_group_scores"]
    sorted_groups = sorted(groups.items(), key=lambda x: -x[1])
    label_map = {
        "embeddings_retrieval": "embeddings/retrieval",
        "vector_db_hybrid_search": "vector search infrastructure",
        "python": "Python",
        "eval_frameworks": "ranking evaluation",
    }
    return [label_map[name] for name, score in sorted_groups[:n] if score > 0.5]


def _weakest_skill_group(skill_component):
    groups = skill_component["skill_group_scores"]
    label_map = {
        "embeddings_retrieval": "embeddings/retrieval",
        "vector_db_hybrid_search": "vector search infrastructure",
        "python": "Python",
        "eval_frameworks": "ranking evaluation",
    }
    weakest_name, weakest_score = min(groups.items(), key=lambda x: x[1])
    if weakest_score < 0.3:
        return label_map[weakest_name]
    return None
_DISQUALIFIER_PHRASES = {
    "research_only_no_production": "career has been research-only with no production deployment",
    "consulting_only_no_product_experience": "career has been entirely at consulting/services firms with no product-company experience",
    "cv_speech_robotics_no_nlp_crossover": "background is in computer vision/speech with no clear NLP or IR crossover",
    "langchain_tourist_no_pre_llm_experience": "AI experience appears recent and LangChain/API-centric without earlier production ML history",
    "pure_leadership_no_recent_code": "has been in an architecture/lead role for an extended period without recent hands-on coding evidence",
    "title_chaser_pattern": "career shows a pattern of short tenures (~18 months or less) across roles",
}
def generate_reasoning(candidate, score_result, rank):
    profile = candidate["profile"]
    comp = score_result["components"]

    title = profile["current_title"]
    company = profile["current_company"]
    years = profile["years_of_experience"]
    location = profile["location"]

    career = comp["career_trajectory"]
    skills = comp["skill_match"]
    behavioral = comp["behavioral"]
    honeypot = comp["honeypot"]

    sentence_parts = []

    sentence_parts.append(f"{title} at {company} with {_format_tenure(years)} experience")

    if career["shipping_evidence_score"] >= 0.6:
        sentence_parts.append("career history shows direct work on ranking/search/recommendation systems")
    else:
        top_skills = _top_skill_groups(skills)
        if top_skills:
            sentence_parts.append(f"strong on {' and '.join(top_skills)}")

    concern = None
    if career["worst_disqualifier"]:
        concern = _DISQUALIFIER_PHRASES[career["worst_disqualifier"]]
    elif behavioral["days_since_active"] is not None and behavioral["days_since_active"] > 60:
        concern = f"inactive on platform for {behavioral['days_since_active']} days"
    elif not behavioral["open_to_work_flag"]:
        concern = "not currently marked as open to work"
    elif behavioral["recruiter_response_rate"] < 0.3:
        concern = f"low recruiter response rate ({behavioral['recruiter_response_rate']:.2f})"
    else:
        weak_group = _weakest_skill_group(skills)
        if weak_group:
            concern = f"{weak_group} not clearly evidenced in profile"

    if concern:
        sentence_parts.append(f"concern: {concern}")

    if honeypot["is_likely_honeypot"]:
        sentence_parts.append(f"profile contains an inconsistency: {honeypot['honeypot_flags'][0]}")

    reasoning = "; ".join(sentence_parts) + "."
    return reasoning
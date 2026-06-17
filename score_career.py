"""
score_career.py

Career trajectory component of the base score (weight: 0.40, the largest
single component). This checks shipping evidence (did they actually build
ranking/search/recommendation systems) and the JD's disqualifier patterns.
"""

from datetime import date
import jd_config


def _years_between(start_str, end_str):
    try:
        start = date.fromisoformat(start_str)
    except (TypeError, ValueError):
        return 0.0
    if end_str:
        try:
            end = date.fromisoformat(end_str)
        except ValueError:
            end = date.today()
    else:
        end = date.today()
    return max(0.0, (end - start).days / 365.25)
def _shipping_evidence_score(career_history):
    if not career_history:
        return 0.0

    total_weight = 0.0
    matched_weight = 0.0
    for role in career_history:
        title_lower = role.get("title", "").strip().lower()
        is_technical_role = title_lower not in jd_config.NON_TECHNICAL_TITLES

        text = (role.get("title", "") + " " + role.get("description", "")).lower()
        duration = role.get("duration_months", 0) or 0
        recency = 1.2 if role.get("is_current") else 1.0
        weight = (duration / 12.0) * recency
        total_weight += weight
        if is_technical_role and any(term in text for term in jd_config.SHIPPING_EVIDENCE_TERMS):
            matched_weight += weight

    if total_weight == 0:
        return 0.0
    return min(1.0, matched_weight / total_weight * 1.3)
def _check_title_chaser(career_history):
    if len(career_history) < 3:
        return False
    durations = [r.get("duration_months", 0) or 0 for r in career_history]
    avg_tenure = sum(durations) / len(durations)
    if avg_tenure <= jd_config.TITLE_CHASER_MAX_AVG_TENURE_MONTHS:
        return True
    return False


def _check_consulting_only(career_history):
    companies = [r.get("company", "").strip().lower() for r in career_history]
    if not companies:
        return False
    all_consulting = all(c in jd_config.CONSULTING_FIRMS for c in companies)
    return all_consulting


def _check_cv_speech_no_nlp_crossover(career_history, skills):
    skill_names = " ".join(s.get("name", "").lower() for s in skills)
    history_text = " ".join(
        (r.get("title", "") + " " + r.get("description", "")).lower()
        for r in career_history
    )
    combined = skill_names + " " + history_text

    has_cv_speech = any(term in combined for term in jd_config.CV_SPEECH_ROBOTICS_TERMS)
    has_nlp_ir = any(term in combined for term in jd_config.NLP_IR_CROSSOVER_TERMS)

    return has_cv_speech and not has_nlp_ir
def _check_langchain_tourist(career_history, skills):
    skill_names = " ".join(s.get("name", "").lower() for s in skills)
    if not any(term in skill_names for term in jd_config.LANGCHAIN_TOURIST_TERMS):
        return False

    for role in career_history:
        try:
            start = date.fromisoformat(role.get("start_date", ""))
        except (TypeError, ValueError):
            continue
        text = (role.get("title", "") + " " + role.get("description", "")).lower()
        duration = role.get("duration_months", 0) or 0
        if start.year < 2023 and duration >= 12 and any(
            term in text for term in jd_config.PRE_LLM_ML_PRODUCTION_TERMS
        ):
            return False
    return True


def _check_pure_leadership(career_history):
    current_roles = [r for r in career_history if r.get("is_current")]
    if not current_roles:
        return False
    current_title = current_roles[0].get("title", "").lower()
    if any(term in current_title for term in jd_config.PURE_LEADERSHIP_TITLE_TERMS):
        duration = current_roles[0].get("duration_months", 0) or 0
        if duration >= 18:
            return True
    return False


def _check_research_only(career_history):
    if not career_history:
        return False
    all_research = True
    for r in career_history:
        title = r.get("title", "").lower()
        industry = r.get("industry", "").lower()
        is_research_title = any(t in title for t in jd_config.RESEARCH_ONLY_TITLE_TERMS)
        is_research_industry = any(t in industry for t in jd_config.RESEARCH_ONLY_INDUSTRY_TERMS)
        if not (is_research_title or is_research_industry):
            all_research = False
            break
    return all_research
def score_career_trajectory(candidate):
    career_history = candidate.get("career_history", [])
    skills = candidate.get("skills", [])

    shipping_score = _shipping_evidence_score(career_history)

    flags = {
        "research_only_no_production": _check_research_only(career_history),
        "consulting_only_no_product_experience": _check_consulting_only(career_history),
        "cv_speech_robotics_no_nlp_crossover": _check_cv_speech_no_nlp_crossover(career_history, skills),
        "langchain_tourist_no_pre_llm_experience": _check_langchain_tourist(career_history, skills),
        "pure_leadership_no_recent_code": _check_pure_leadership(career_history),
        "title_chaser_pattern": _check_title_chaser(career_history),
    }

    penalty_multiplier = 1.0
    worst_flag = None
    for flag_name, fired in flags.items():
        if fired:
            mult = jd_config.PENALTY_MULTIPLIERS[flag_name]
            if mult < penalty_multiplier:
                penalty_multiplier = mult
                worst_flag = flag_name

    final_score = shipping_score * penalty_multiplier

    return {
        "career_trajectory_score": round(final_score, 4),
        "shipping_evidence_score": round(shipping_score, 4),
        "disqualifier_flags": {k: v for k, v in flags.items() if v},
        "applied_penalty_multiplier": penalty_multiplier,
        "worst_disqualifier": worst_flag,
    }
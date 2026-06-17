"""
combine.py

Wires together all six scoring pieces into one final score per candidate:

  base_score = weighted average of skills, career, text, seniority/logistics
  final_score = base_score * behavioral_multiplier * honeypot_multiplier

This matches the architecture we designed from the start: four components
feed a base score, then two multiplicative passes on top.
"""

import jd_config
from score_skills import score_skill_match
from score_career import score_career_trajectory
from score_seniority_logistics import score_seniority_logistics
from score_behavioral import score_behavioral_multiplier
from score_honeypot import score_honeypot_penalty


def combine_scores(candidate, jd_text_match_score):
    skill_result = score_skill_match(candidate)
    career_result = score_career_trajectory(candidate)
    seniority_result = score_seniority_logistics(candidate)
    behavioral_result = score_behavioral_multiplier(candidate)
    honeypot_result = score_honeypot_penalty(candidate)

    w = jd_config.BASE_SCORE_WEIGHTS
    base_score = (
        w["career_trajectory"] * career_result["career_trajectory_score"]
        + w["skill_match"] * skill_result["skill_match_score"]
        + w["jd_text_match"] * jd_text_match_score
        + w["seniority_logistics_fit"] * seniority_result["seniority_logistics_score"]
    )

    final_score = (
        base_score
        * behavioral_result["behavioral_multiplier"]
        * honeypot_result["honeypot_penalty_multiplier"]
    )

    return {
        "candidate_id": candidate["candidate_id"],
        "final_score": round(final_score, 6),
        "base_score": round(base_score, 6),
        "components": {
            "skill_match": skill_result,
            "career_trajectory": career_result,
            "jd_text_match_score": jd_text_match_score,
            "seniority_logistics": seniority_result,
            "behavioral": behavioral_result,
            "honeypot": honeypot_result,
        },
    }
"""
score_skills.py

Skill-match component of the base score (weight: jd_config.BASE_SCORE_WEIGHTS["skill_match"]).

This scorer never just checks "is skill X present" - it weights every
matched skill by proficiency level, duration actually used, and
endorsements received. A candidate who lists "expert in LoRA" but used it
for 2 months gets much less credit than someone who lists "advanced in
LoRA" but used it for 3 years with real endorsements.
"""

import jd_config

PROFICIENCY_WEIGHT = {
    "beginner": 0.25,
    "intermediate": 0.5,
    "advanced": 0.75,
    "expert": 1.0,
}
def _duration_credit(duration_months):
    if duration_months is None:
        return 0.3  # missing duration_months field -> treat as weak signal, not zero
    return min(1.0, duration_months / 24.0)


def _endorsement_credit(endorsements):
    return min(1.0, endorsements / 20.0)
def _skill_strength(skill_record):
    prof = PROFICIENCY_WEIGHT.get(skill_record.get("proficiency", ""), 0.25)
    dur = _duration_credit(skill_record.get("duration_months"))
    end = _endorsement_credit(skill_record.get("endorsements", 0))
    return 0.40 * prof + 0.40 * dur + 0.20 * end
def score_skill_match(candidate):
    skills = candidate.get("skills", [])
    skills_by_name = {}
    for s in skills:
        name = s.get("name", "").strip().lower()
        if name:
            skills_by_name[name] = s
    group_scores = []
    for group_name, terms in jd_config.MUST_HAVE_SKILL_GROUPS.items():
        best = 0.0
        for term in terms:
            term_l = term.lower()
            for skill_name, rec in skills_by_name.items():
                if term_l in skill_name or skill_name in term_l:
                    best = max(best, _skill_strength(rec))
        group_scores.append(best)

    must_have_score = sum(group_scores) / len(group_scores) if group_scores else 0.0
    nice_hits = 0
    for term in jd_config.NICE_TO_HAVE_SKILLS:
        term_l = term.lower()
        for skill_name, rec in skills_by_name.items():
            if term_l in skill_name or skill_name in term_l:
                nice_hits += 1
                break
    nice_bonus = min(0.10, nice_hits * 0.02)

    final = min(1.0, must_have_score * 0.90 + nice_bonus)
    return {
        "skill_match_score": round(final, 4),
        "skill_group_scores": {
            name: round(score, 4)
            for name, score in zip(jd_config.MUST_HAVE_SKILL_GROUPS.keys(), group_scores)
        },
        "nice_to_have_hits": nice_hits,
    }
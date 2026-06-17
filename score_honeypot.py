"""
score_honeypot.py

Honeypot penalty - the last piece, applied at the very end. Catches
profiles that look fine at a glance but contain a fact that can't be true:
years at a company before it existed, or "expert" skill used for 0 months.
The competition disqualifies the WHOLE submission if more than 10% of the
top 100 are honeypots, so this check matters more than its single weight
suggests.
"""

from datetime import date
import jd_config


def _check_company_age_impossibility(career_history):
    issues = []
    for role in career_history:
        company = role.get("company", "").strip().lower()
        founding_year = jd_config.COMPANY_FOUNDING_YEAR.get(company)
        if founding_year is None:
            continue
        start_date_str = role.get("start_date", "")
        try:
            start_year = date.fromisoformat(start_date_str).year
        except (TypeError, ValueError):
            continue
        if start_year < founding_year:
            issues.append(
                f"{role.get('company')}: started {start_year}, company founded {founding_year}"
            )
    return issues
def _check_expert_zero_duration(skills):
    issues = []
    for s in skills:
        if s.get("proficiency") == "expert" and (s.get("duration_months") or 0) <= 2:
            issues.append(f"{s.get('name')}: expert proficiency, {s.get('duration_months')} months used")
    return issues


def _check_total_tenure_mismatch(career_history, years_of_experience):
    total_months = sum((r.get("duration_months") or 0) for r in career_history)
    allowed_months = years_of_experience * 12 + 24
    if total_months > allowed_months:
        return [f"career history totals {total_months} months but stated experience is {years_of_experience} years ({years_of_experience*12:.0f} months)"]
    return []
def score_honeypot_penalty(candidate):
    career_history = candidate.get("career_history", [])
    skills = candidate.get("skills", [])
    years_of_experience = candidate.get("profile", {}).get("years_of_experience", 0)

    all_issues = []
    all_issues += _check_company_age_impossibility(career_history)
    all_issues += _check_expert_zero_duration(skills)
    all_issues += _check_total_tenure_mismatch(career_history, years_of_experience)

    if not all_issues:
        return {"honeypot_penalty_multiplier": 1.0, "honeypot_flags": [], "is_likely_honeypot": False}

    multiplier = max(0.05, 0.5 ** len(all_issues))

    return {
        "honeypot_penalty_multiplier": round(multiplier, 4),
        "honeypot_flags": all_issues,
        "is_likely_honeypot": True,
    }
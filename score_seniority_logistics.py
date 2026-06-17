"""
score_seniority_logistics.py

Seniority + logistics fit component of the base score (weight: 0.20).
Experience band fit uses a smooth curve peaking at the JD's ideal center
(7 years), not a hard cutoff. Location fit acts as a ceiling on the final
result, not just one more averaged-in factor, since visa sponsorship is
closer to a hard constraint than a soft preference.
"""

import jd_config


def _experience_fit(years_of_experience):
    center = jd_config.EXPERIENCE_IDEAL_CENTER
    distance = abs(years_of_experience - center)
    score = pow(2.0, -(distance ** 2) / 18.0)
    return min(1.0, score)
def _location_fit(profile, signals):
    location = profile.get("location", "").lower()
    country = profile.get("country", "").lower()

    if country != "india":
        base = 0.25
        if signals.get("willing_to_relocate"):
            base += 0.20
        return min(1.0, base)

    location_lower = location
    if any(pref in location_lower for pref in jd_config.PREFERRED_LOCATIONS):
        return 1.0
    if any(acc in location_lower for acc in jd_config.ACCEPTABLE_INDIA_LOCATIONS):
        return 0.85
    base = 0.55
    if signals.get("willing_to_relocate"):
        base += 0.30
    return min(1.0, base)
def _notice_period_fit(notice_period_days):
    ideal = jd_config.NOTICE_PERIOD_IDEAL_DAYS
    if notice_period_days <= ideal:
        return 1.0
    excess = notice_period_days - ideal
    return max(0.4, 1.0 - excess / 200.0)
def score_seniority_logistics(candidate):
    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})

    exp_score = _experience_fit(profile.get("years_of_experience", 0))
    loc_score = _location_fit(profile, signals)
    notice_score = _notice_period_fit(signals.get("notice_period_days", 30))

    weighted_avg = 0.40 * exp_score + 0.40 * loc_score + 0.20 * notice_score
    final = weighted_avg * (0.5 + 0.5 * loc_score)

    return {
        "seniority_logistics_score": round(final, 4),
        "experience_fit": round(exp_score, 4),
        "location_fit": round(loc_score, 4),
        "notice_period_fit": round(notice_score, 4),
    }    
"""
score_behavioral.py

Behavioral signal multiplier - applied AFTER the four base-score components
are combined. Answers "are they actually available right now," separate
from "are they qualified." A perfect-on-paper candidate who hasn't logged
in for months gets multiplied down here, even if every other score is high.
"""

from datetime import date

DATASET_REFERENCE_DATE = date(2026, 5, 27)


def _recency_factor(last_active_date_str):
    try:
        last_active = date.fromisoformat(last_active_date_str)
    except (TypeError, ValueError):
        return 0.5
    days_inactive = (DATASET_REFERENCE_DATE - last_active).days
    if days_inactive <= 14:
        return 1.0
    if days_inactive <= 30:
        return 0.9
    if days_inactive <= 60:
        return 0.7
    if days_inactive <= 90:
        return 0.5
    if days_inactive <= 150:
        return 0.3
    return 0.15
def score_behavioral_multiplier(candidate):
    signals = candidate.get("redrob_signals", {})

    open_to_work = signals.get("open_to_work_flag", False)
    recency = _recency_factor(signals.get("last_active_date"))
    response_rate = signals.get("recruiter_response_rate", 0.0)
    applications_30d = signals.get("applications_submitted_30d", 0)
    profile_views_30d = signals.get("profile_views_received_30d", 0)

    open_to_work_factor = 1.0 if open_to_work else 0.5

    engagement_factor = min(1.0, 0.5 + 0.1 * applications_30d + 0.01 * profile_views_30d)

    raw_multiplier = (
        0.40 * open_to_work_factor
        + 0.40 * recency
        + 0.10 * response_rate
        + 0.10 * engagement_factor
    )

    final_multiplier = max(0.3, min(1.0, raw_multiplier))

    return {
        "behavioral_multiplier": round(final_multiplier, 4),
        "open_to_work_flag": open_to_work,
        "recency_factor": round(recency, 4),
        "recruiter_response_rate": response_rate,
        "days_since_active": (
            (DATASET_REFERENCE_DATE - date.fromisoformat(signals["last_active_date"])).days
            if signals.get("last_active_date") else None
        ),
    }
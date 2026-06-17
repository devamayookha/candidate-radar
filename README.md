# Candidate Radar

An explainable candidate ranking system built for Redrob's "Senior AI
Engineer - Founding Team" job description, as part of the India Runs
Data & AI Challenge (Track 1).

## Problem

Given a job description and a pool of 100,000 candidate profiles, produce
a ranked shortlist of the top 100 best-fit candidates. The challenge
explicitly warns against keyword-matching shortcuts: a strong skills list
alone is not sufficient, and the dataset contains deliberate traps
(keyword stuffers, "ghost" candidates who look perfect on paper but are
unreachable, and honeypot profiles with impossible facts).

## Approach

Six independent components are computed for every candidate, then combined:

1. **Skill match** - every listed skill is scored by combining proficiency
   level, months of actual use, and endorsements received, instead of
   just checking whether a keyword is present. This resists candidates who
   list AI buzzwords without real experience behind them.

2. **Career trajectory** - scans actual job history for evidence of having
   shipped a ranking, search, or recommendation system, and checks for six
   disqualifier patterns described in the JD (research-only background,
   consulting-only background with no product experience, computer
   vision/speech background with no NLP crossover, recent LangChain-only
   experience with no earlier production ML, long-term pure leadership
   roles with no recent coding, and a title-chasing pattern of short
   tenures). This check is gated by job title, so a Content Writer or
   Project Manager whose description happens to mention AI/ML topics or
   "ranked on search" does not get false credit for shipping a system.

3. **JD text similarity** - compares each candidate's own headline,
   summary, and recent role descriptions against a reference text built
   from the JD's own description of an ideal candidate, using TF-IDF and
   cosine similarity. This is word-frequency statistics, not a neural
   embedding model, so it runs in seconds with no GPU and no network call.

4. **Seniority and logistics fit** - scores experience-band fit as a
   smooth curve centered on the JD's stated ideal (7 years), and scores
   location fit against the JD's stated preferences (Pune/Noida preferred,
   other Tier-1 Indian cities acceptable, outside-India candidates scored
   lower since the company does not sponsor visas). Location acts as a
   ceiling on the final result rather than a simple averaged term, since
   visa sponsorship is closer to a hard constraint than a soft preference.

These four components combine into a weighted base score (career
trajectory weighted highest at 0.40, since the JD itself warns that
skills-list matching alone is the wrong approach).

5. **Behavioral multiplier** - applied after the base score, this
   down-weights candidates who are not actually reachable right now:
   not marked open to work, inactive on the platform for an extended
   period, or with a very low recruiter response rate. A perfect-on-paper
   candidate who has not logged in for months is ranked below genuinely
   available candidates.

6. **Honeypot penalty** - also applied after the base score, this checks
   for internally impossible facts: career history claiming years at a
   company before that company existed (verified against a hand-built,
   web-sourced lookup table of all 63 distinct company names in the
   dataset), "expert" proficiency in a skill used for two months or less,
   and total career history duration that exceeds the candidate's stated
   years of experience by an implausible margin.

## Reproduce

```
pip install -r requirements.txt
python run_full.py
```

This produces `output/submission.csv`. On the full 100,000-candidate
pool, the entire pipeline runs in under one minute, CPU only, with no
GPU and no network calls during ranking - comfortably inside the
challenge's 5 minute / 16GB / CPU-only compute budget.

## Files

- `jd_config.py` - every scoring rule, weight, and list, traced back to a
  specific line in the job description
- `score_skills.py` - skill match component
- `score_career.py` - career trajectory and disqualifier component
- `score_text.py` - JD text similarity component
- `score_seniority_logistics.py` - experience and location fit component
- `score_behavioral.py` - availability/reachability multiplier
- `score_honeypot.py` - impossible-profile detector
- `combine.py` - wires all six components into one final score
- `generate_reasoning.py` - writes the honest, specific reasoning column
- `run_full.py` - runs the full pipeline end to end on all candidates

## AI tools used

Claude was used throughout for architecture discussion, explaining
concepts, debugging, and code review. All production code in this
repository was typed and committed by the author. No candidate data was
sent to any hosted LLM API at any point during the ranking step itself -
the entire pipeline runs locally with no network access required.
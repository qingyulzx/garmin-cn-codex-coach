---
name: garmin-cn-running-coach
description: Use Garmin China MCP activities and lap data to review running volume, workouts and race preparation in Codex, incorporating the runner's actual goals and data limitations.
---

# Garmin China running review

Use the connected `garmin_cn_coach` MCP, or the user's existing Garmin China server, for requested running analyses. Check its actual available tools rather than assume a particular namespace. If authentication fails, direct the user to the local login script; do not ask for a password, MFA code or token in chat.

## Establish the runner's context

Use goals, race dates, training constraints, perceived effort and symptoms supplied by the runner. Read an athlete profile only when its location is known and the user has asked to use it. Do not assume the example profile contains personal information. Clarify missing context when it materially changes the conclusion; continue independent analysis while awaiting it. Do not infer a permanent preference from one example.

## Read and reconcile actual activity data

- State the dates, timezone and whether the period is complete. Paginate activity lists and deduplicate by activity ID. A planned week is not a completed week, and later syncs may change totals.
- Inspect returned text as well as MCP error flags: the upstream may return an authentication/API error as text with `isError=false`. Treat it as a failed read, not a zero-volume training period.
- Compute distance and duration from activity records. Distinguish a single long continuous run from several shorter runs on the same day. Pull laps for structured or ambiguous sessions rather than classify the entire activity from average pace.
- Prefer explicitly measured race/track distances and manual timing over GPS when the runner confirms a discrepancy. Label unresolved distance uncertainty; do not quietly correct every lap by an arbitrary factor.
- Honor unreliable-metric exclusions. For example, when the runner excludes elevation, do not use ascent, descent or grade-adjusted pace in totals or coaching conclusions.
- A configured heart-rate maximum or zone boundary is not a measured physiological threshold. An empty lactate-threshold response is missing data. Wrist heart rate on very short intervals may lag or be wrong; do not infer low intensity solely from it.

## Interpret training in context

Separate low-intensity running, sustained aerobic running, tempo/threshold-like work, 3–5 km-type intervals, faster speed-endurance and short strides where the evidence permits. For a distance-based questionnaire, allocate only the actual work segments to high intensity, with warm-up/cool-down/recovery running separated. Moderate floats are not necessarily easy. Treat a hard race separately when mapping it to a precise physiological zone would be speculative. Give rounded estimates and explain the largest classification uncertainty.

Compare recent weeks against the runner's own earlier continuous training. Discuss consistency, quality-session completion, perceived effort, recovery and scheduling before attributing progress to any single session, shoe, camp or metric. Training scores and ACWR-style ratios are descriptive aids, not validated personal injury probabilities or race guarantees.

Adapt suggestions to the main event and the runner's accepted schedule. Avoid adding extra workouts merely to gather data. Distinguish an observation, a calculation and a coaching inference. If current symptoms suggest exercise should stop or medical assessment is needed, address those symptoms before proposing more intensity; do not diagnose from watch data.

## Deliver the review

Lead with the practical finding. Include a small table when comparing weekly volume or intensity proportions. Explain what is supported by records, what the runner reported and what remains uncertain. Give actionable changes proportional to that uncertainty. Preserve the user's control over the plan.

If the runner explicitly asks to keep a profile or training log, save it in the connector's application-data directory or a location they select, outside the public source tree. Never add real health data, account credentials or tokens to project examples, issue reports or release packages.

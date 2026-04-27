# Week 8 Checkpoint — Interview Readiness + Portfolio

## Week Summary
Week 8 was interview preparation in applied form. You completed two timed mock interview rounds — Python (Day 36) and SQL (Day 37) — with self-scoring against reference solutions. You practiced data storytelling: translating data outputs into executive narratives with specific, data-referenced sentences and choosing the right chart type for the business message (Day 38). You worked through a 40-concept rapid review of Python and SQL edge cases — from NULL behaviour to join fanout to GROUP BY vs PARTITION BY (Day 39). And you built a portfolio-quality notebook (Day 40) meeting strict requirements: 5+ window functions, 2+ CTEs, modular function library, 3 charts, and a professional executive narrative.

---

## Must-Know Skills
I can…

1. Solve a timed data cleaning problem (5 min): replacing invalid values, capping, logging affected counts
2. Solve a timed aggregation problem (5 min): multi-metric groupby with `.agg()` and `.assign()` for derived columns
3. Solve a timed rolling calculation problem (5 min): 3-month rolling average per group using `.groupby().transform()`
4. Solve a timed outlier detection problem (5 min): z-score calculation and flagging using merge + arithmetic
5. Write a timed SQL window function query (5 min): ranking within a group using DENSE_RANK()
6. Write a timed SQL anti-join (5 min): find customers active in 2024 but absent from 2025
7. Explain my query approach in plain English, using comments in the SQL code
8. Write an executive summary where every sentence references a specific data point — no vague language
9. Choose the correct chart type for a business message (trend = line, comparison = bar, distribution = box)
10. Build a notebook that runs clean from top to bottom with zero errors after Kernel → Restart & Run All

---

## Self-Test Tasks

**Task 1 (Python — 5 min timer):** From `bw_sales_kpis.csv`, calculate a 3-month rolling average of `GROSS_MARGIN` per `REGION`. Add this as a new column `ROLLING_GM_3M`. Handle the first two months in each region gracefully (use `min_periods=1`). Return a sorted result.
```python
# Set a 5-min timer. Write your solution here.
```

**Task 2 (SQL — 5 min timer):** Write a SQL query that finds all customers in `sales_orders` who placed orders in every single sales org (VKORG) that exists in the data. Return KUNNR and the count of distinct sales orgs they ordered from.
```sql
-- Set a 5-min timer. Write your solution here.
```

**Task 3 (Narrative — 5 min):** Write a 5-sentence executive summary of the full analytics dataset. Each sentence must include at least one number. Write from memory using the numbers you've computed throughout the 8 weeks.
```
Write your narrative here (in plain text — no code):
```

---

## Pass Criteria

**Passing:**
- Task 1 completed correctly in ≤5 minutes using `.groupby().transform()` — not `.iterrows()`
- Task 2 uses a HAVING clause to filter customers where `COUNT(DISTINCT VKORG) = (SELECT COUNT(DISTINCT VKORG) FROM sales_orders)` — this is a "division" query
- Task 3 narrative has no sentence starting with "The data shows..." or "It is clear that..." — every statement is specific and data-referenced
- Portfolio notebook (Day 40) runs cleanly end to end; all 3 charts render; all 5 window functions are distinct (ROW_NUMBER, RANK, LAG, SUM OVER, AVG OVER or similar)

**Needs More Work:**
- Task 1 used `.apply()` row-by-row instead of `.transform()` — correct result but would fail in a timed interview due to speed and style
- Task 2 missed the "every sales org" logic — used a simple COUNT instead of comparing to the total distinct VKORG count
- Task 3 narrative contained phrases like "significant improvement" or "good performance" without numbers — this does not meet professional communication standards

---

## Carry-Forward Items

1. **The 5-minute discipline** — continue timed practice even after the bootcamp. Pick one SQL problem and one Python problem per week, set a timer, and score yourself. Fluency decays without practice.
2. **Portfolio maintenance** — update Day 40 regularly with new datasets and techniques. A portfolio notebook that's been updated recently shows initiative and current skills to an interviewer.
3. **Narrative writing** — practice writing data narratives from real outputs every time you complete an analysis. The habit of "here's the number, here's what it means, here's the implication" is what separates a senior analyst from a junior one.

---

## Relevant SAP/Analytics Context

In a senior analytics role interview, you will likely face a case study where you're given a business problem and 30 minutes to sketch an analytical approach. Everything in Week 8 — the timed problem-solving, the data narrative, the portfolio piece — prepares you for that moment. The SQL problems mirror what you'd see in an analytics capability assessment. The narrative writing mirrors what you'd deliver as a "key findings" slide in a client presentation. And the portfolio notebook is your "evidence of work" — the thing you can pull up on screen and walk through when the interviewer says "show me something you've built." Having a clean, well-documented, end-to-end notebook using SAP-realistic data is a differentiator that most candidates don't have.

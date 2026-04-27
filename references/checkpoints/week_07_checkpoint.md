# Week 7 Checkpoint — Integration, Pipelines, and Performance

## Week Summary
Week 7 elevated the craft of Python analytics from "scripts that work" to "code a team can depend on." You built OOP patterns for analytics infrastructure: DataLoader with caching, QueryRunner with logging, typed dataclasses for report configs (Day 31). You implemented structured error handling and pipeline observability with the `logging` module (Day 32). You benchmarked pandas performance — vectorisation vs `.iterrows()`, category dtypes, chunking, and memory profiling (Day 33). You mastered recursive CTEs for org hierarchy traversal with SAP HRP1001 context (Day 34). And you built a proper star schema data warehouse from the 5 source datasets, loading fact and dimension tables and comparing flat vs star schema query performance (Day 35).

---

## Must-Know Skills
I can…

1. Design a Python class with `__init__`, instance methods, properties, and `__repr__` — and explain when a class adds value over a function
2. Implement `__enter__` and `__exit__` to create a context manager for DB connection lifecycle management
3. Use `@dataclass` with `__post_init__` validation and computed properties
4. Configure `logging.basicConfig()` with a formatted log handler and file output
5. Use try/except for specific exception types: `FileNotFoundError`, `pd.errors.EmptyDataError`, `UnicodeDecodeError`, `ValueError`
6. Quantify the speedup of vectorisation over `.iterrows()` — and know when `.apply()` is a middle option
7. Convert low-cardinality string columns to `category` dtype and measure memory savings
8. Write a recursive CTE in SQLite for org hierarchy traversal with level/depth calculation
9. Design a star schema with fact table(s) and dimension tables using surrogate keys
10. Explain the "conformed dimension" concept: one dimension table shared across multiple fact tables

---

## Self-Test Tasks

**Task 1:** Without looking at Day 31, write a `QueryRunner` class with at minimum: `__init__(db_path)`, `load_dataframes(dfs_dict)`, `run(sql)` returning a DataFrame, and a `query_log` property returning a DataFrame of past queries with timing.
```python
# Write your solution here
```

**Task 2:** Write a recursive CTE (SQLite) that starts from the root of the org hierarchy and returns all org units with their depth level and full path string (e.g., "ORG-100 > ORG-110 > ORG-115").
```sql
-- Write your solution here
```

**Task 3:** Demonstrate the memory savings from converting `VKORG`, `STATUS`, and `WAERK` in `sales_orders` to category dtype. Print the before/after memory usage in KB.
```python
# Write your solution here
```

---

## Pass Criteria

**Passing:**
- Task 1: `QueryRunner.run()` uses a context manager (with statement) for the connection — no bare `con.close()` calls
- Task 2: recursive CTE has an anchor member (WHERE PARENT IS NULL) and a recursive member; path concatenation is correct; handles cycles by not having any in the test data
- Task 3: memory reduction is at least 20% — if less, check that `memory_usage(deep=True)` is used (shallow doesn't account for object overhead)
- All three tasks completed without importing anything from Days 31–33

**Needs More Work:**
- Task 1: forgot to handle the case where `db_path=':memory:'` gets a new DB on each connection open — the context manager must store the connection, not reopen it
- Task 2: recursive CTE terminated unexpectedly or had wrong depth — check that the anchor uses `depth = 0` and the recursive step uses `parent.depth + 1`
- Task 3: used `sys.getsizeof()` instead of `df.memory_usage(deep=True)` — `sys.getsizeof()` only measures the DataFrame object shell, not the actual data

---

## Carry-Forward Items

1. **Context managers** — the `with DBConnection(...) as con:` pattern prevents connection leaks in production pipelines. Practice writing a context manager for any resource that needs cleanup (files, connections, locks).
2. **Star schema design muscle memory** — when you see a flat CSV, automatically ask: "What are the facts (numeric measures)? What are the dimensions (text attributes)?" This is what you do when designing a BW InfoCube, and it's the same thinking needed here.
3. **Recursive CTE mental model** — think of it as a loop: anchor = start, recursive = step, implicit UNION ALL = "add these rows to the table and repeat". The termination condition is in the WHERE clause of the recursive member. Write one from scratch once a week until it's automatic.

---

## Relevant SAP/Analytics Context

The OOP patterns from Day 31 (DataLoader, QueryRunner) map directly to what SAP BTP (Business Technology Platform) service classes do in Java and Python. When you configure an OData service or a SAP Analytics Cloud data connector, there's a connection manager class doing exactly what your `DBConnection` context manager does — managing lifecycle, commit, rollback. The star schema from Day 35 is directly analogous to a SAP BW InfoCube: `fact_sales_kpis` = F-table, `dim_material` = SID table for the MATNR characteristic, `dim_time` = the time dimension. When a BW InfoCube "compresses" data, it merges the E-table (new fact rows) into the F-table — the same operation as appending to your fact table with deduplication.

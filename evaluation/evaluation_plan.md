# Evaluation

## Goal
Using the sdk (example in /tests/test_sdk.py) build a evaluation script (run_eval.py) for the ground truth dataset.

## Dependencies
The following libraries are required and added to `requirements.txt`:
- `pandas`
- `openpyxl` (for Excel support)
- `nltk` (for BLEU score calculation)

## Ground Truth
Input is an xlsx with the ground truth: /evaluation/ground_truth.xlsx
In the first sheet of this xlsx there should be two columns (verify this, otherwise: error) with header: query and sql. In the query column there is the text query, in the sql column there is a sql statement based of this query.
Rows with missing `query` or `sql` values should be skipped and logged as a warning.

## Evaluation
Every entry in the xlsx should be run in the graph and the result be captured.
The script should be implemented using `asyncio` to allow concurrent execution of queries.
The default max concurrency should be set to 2.
Every query must be treated as a completely fresh start (isolated state), meaning a new `thread_id` should be generated for each evaluation run.

The evaluation should use the following metrics:
Accuracy where generated sql responses == ground truth sql
BLEU score between generated sql responses and ground truth sql
It should be easy to add more metrics in the future.

If SQLResponse status != success it should be considered failed.

## Output

Output should be a xlsx file in the `evaluation/results/` directory: "evaluation_"+date+time(hhmm)+".xlsx". Example: "evaluation/results/evaluation_2025_12_06_1433.xlsx"
The xlsx has two sheets: Overview with the metrics:
Accuracy (percentage/mean)
BLEU score (mean, median, p80, p90).
percentage and number of status != success
number of skipped/invalid rows

and a Detail sheet:
this should have every query/sql pair (as in the ground_truth) and next to it the following columns:
result (sql result from the graph), "FAILED" if status != success
mapped domain (the domain identified by the system)
equal flag (green if true)
bleu score
error message (capture the error if status != success)
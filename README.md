# SEA-AD DREAM Challenge Evaluation

Validation and scoring scripts for the
[SEA-AD DREAM Challenge: Predicting Alzheimer’s Pathology from scRNA-seq Data].

## Evaluation Overview

Metrics returned and used for ranking are:

- AUC
- precision-recall

## Usage - Python

### Validate

```text
python validate.py \
  -p PATH/TO/PREDICTIONS_FILE.CSV \
  -g PATH/TO/GOLDSTANDARD_FILE.CSV [-o RESULTS_FILE]
```
If `-o/--output` is not provided, then results will print
to STDOUT, e.g.

```json
{"submission_status": "VALIDATED", "submission_errors": ""}
```

What it will check for:

- Two columns named `patient_id`, `probability` (extraneous columns 
  will be ignored)
- `patient_id` values are strings
- `probability` values are floats between 0.0 
  and 1.0, and cannot be null/None
- There is exactly one prediction per ID (so: no missing
  or duplicated `patient_id`s)
- There are no extra predictions (so: no unknown `patient_id`s)

### Score

```text
python score.py \
  -p PATH/TO/PREDICTIONS_FILE.CSV \
  -g PATH/TO/GOLDSTANDARD_FILE.CSV [-o RESULTS_FILE]
```

If `-o/--output` is not provided, then results will output
to `results.json`.

[SEA-AD DREAM Challenge: Predicting Alzheimer’s Pathology from scRNA-seq Data]: https://www.synapse.org/Synapse:syn66496696/wiki/632412

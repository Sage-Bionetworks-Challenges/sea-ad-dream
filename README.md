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
  -g PATH/TO/GROUNDTRUTH.CSV [-o RESULTS_FILE]
```
If `-o/--output` is not provided, then results will print
to STDOUT, e.g.

```json
{"submission_status": "VALIDATED", "submission_errors": ""}
```

What it will check for:

- 9 expected columns (with up to 4 optional columns), where:
  - String values are from accepted sets of values
  - Float values are between 0 and 100, inclusive
- There is exactly one prediction per ID (so: no missing
  or duplicated `Donor ID`s)
- There are no extra predictions (so: no unknown `Donor ID`s)

### Score

```text
python score.py \
  -p PATH/TO/PREDICTIONS_FILE.CSV \
  -g PATH/TO/GROUNDTRUTH_FILE.CSV [-o RESULTS_FILE]
```

If `-o/--output` is not provided, then results will output
to `results.json`.

[SEA-AD DREAM Challenge: Predicting Alzheimer’s Pathology from scRNA-seq Data]: https://www.synapse.org/Synapse:syn66496696/wiki/632412

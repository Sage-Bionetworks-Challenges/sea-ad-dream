# SEA-AD DREAM Challenge Evaluation

Evaluation workflow for the 
[SEA-AD DREAM Challenge: Predicting Alzheimer’s Pathology from scRNA-seq Data],
where the main steps are defined in `workflow.cwl`.

The challenge's infrastructure is powered by the [SynapseWorkflowOrchestrator]
orchesration tool, will continuously monitors the challenge for new submission
to evaluate.

## Evaluation Overview

Metrics returned and used for ranking are:

### Task 1

Metric | Description
:--:|:--
`ADNC_QWK` | Quadratic weighted kappa (QWK) on ADNC, where QWK is a variant of [Cohen's kappa] that applies quadratic weights to account for the ordinality of the data. <br/><br/>Primary metric.
`Braak_QWK` | QWK on Braak. <br/><br/>Used to break ties on `ADNC_QWK`.
`Thal_QWK` | QWK on Thal. <br/><br/>Used to break ties on `Braak_QWK`.
`CERAD_QWK` | QWK on CERAD. <br/><br/>Used to break ties on `Thal_QWK`. 

Other metrics returned (but _not_ used for ranking) include:
* Mean absolute errors (MAE)
* Spearman's rank correlation coefficients

### Task 2

Metric | Description
:--:|:--
`6e10_CCC` | Average Concordance Correlation Coefficients (CCC) computed on the percentages of 6e10 positive areas.
`AT8_CCC` | Average CCC on the percentages of AT8 positive areas.
`NeuN_CCC` | Average CCC on the percentages of NeuN positive areas. <br/><br/>Used to break ties on `6e10_CCC` and `AT8_CCC`.
`GFAP_CCC` | Average CCC on the percentages of GFAP positive areas. <br/><br/>Used to break ties on `NeuN_CCC`.

Other metrics returned (but _not_ used for ranking) include:
* Mean squared errors (MSE)
* R^2

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
  -g PATH/TO/GROUNDTRUTH_FILE.CSV [-t TASK_NUMBER] [-o RESULTS_FILE]
```

If `-o/--output` is not provided, then results will output
to `results.json`. The default `--task_number` is 9616048 (Task 1).

[SEA-AD DREAM Challenge: Predicting Alzheimer’s Pathology from scRNA-seq Data]: https://www.synapse.org/Synapse:syn66496696/wiki/632412
[SynapseWorkflowOrchestrator]: https://github.com/Sage-Bionetworks/SynapseWorkflowOrchestrator
[Cohen's kappa]: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html
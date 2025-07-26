#!/usr/bin/env python3
"""Template scoring script.

Script is currently designed for evaluating submissions for a
single-task challenge.

At a minimum, you will need to:
    1. Define the expected data structures (see GROUNDTRUTH_COLS and
       PREDICTION_COLS)
    2. Customize score_task1() to fit your specific scoring needs
    3. Add helper functions and manage dependencies as needed for your
       scoring process

For challenges with multiple tasks, create additional `score_task*()`
functions and update the `score()` function to route evaluation to
the appropriate task.
"""
import json

import pandas as pd
import typer
from dream_evaluation import goal1_evaluation, goal2_evaluation
from typing_extensions import Annotated


# Groundtruth columns and data type.
GROUNDTRUTH_COLS = {
    "Donor ID": str,
}

# Expected columns and data types for predictions file.
PREDICTION_COLS = {
    "Donor ID": str,
    "predicted ADNC": str,
    "predicted Braak": str,
    "predicted CERAD": str,
    "predicted Thal": str,
    "predicted LATE": str,
    "predicted Lewy": str,
    "predicted 6e10": float,
    "predicted AT8": float,
    "predicted GFAP": float,
    "predicted NeuN": float,
    "predicted aSyn": float,
    "predicted pTDP43": float,
}


def score_task1(gt_file: str, pred_file: str) -> dict[str, int | float]:
    """Scoring function for Task 1.

    Metrics returned:
        - QWK (Quadratic Weighted Kappa)
        - MAE (Mean Absolute Error)
        - Spearman rank correlation
    """
    pred = pd.read_csv(
        pred_file,
        usecols=PREDICTION_COLS,
        dtype=PREDICTION_COLS,
        float_precision="round_trip",
    )
    truth = pd.read_csv(
        gt_file,
        usecols=GROUNDTRUTH_COLS,
        dtype=GROUNDTRUTH_COLS,
    )
    return goal1_evaluation(
        df_adata=truth,
        df=pred,
    )


def score_task2(gt_file: str, pred_file: str) -> dict[str, int | float]:
    """Scoring function for Task 2.

    Metrics returned:
        - CCC (Concordance Correlation Coefficient)
        - MSE (Mean Squared Error)
        - R2 (Coefficient of Determination)
    """
    pred = pd.read_csv(
        pred_file,
        usecols=PREDICTION_COLS,
        dtype=PREDICTION_COLS,
        float_precision="round_trip",
    )
    truth = pd.read_csv(
        gt_file,
        usecols=GROUNDTRUTH_COLS,
        dtype=GROUNDTRUTH_COLS,
    )
    return goal2_evaluation(
        df_adata=truth,
        df=pred,
    )


def score(task_number: int, gt_file: str, pred_file: str) -> dict[str, int | float]:
    """
    Routes evaluation to the appropriate task-specific function.
    """
    scoring_func = {
        1: score_task1,
        2: score_task2,
    }.get(task_number)

    if scoring_func:
        return scoring_func(gt_file=gt_file, pred_file=pred_file)
    raise KeyError


def main(
    predictions_file: Annotated[
        str,
        typer.Option(
            "-p",
            "--predictions_file",
            help="Path to the prediction file.",
        ),
    ],
    groundtruth_file: Annotated[
        str,
        typer.Option(
            "-g",
            "--groundtruth_file",
            help="Path to the groundtruth file.",
        ),
    ],
    task_number: Annotated[
        int,
        typer.Option(
            "-t",
            "--task_number",
            help="Challenge task number for which to validate the predictions file.",
        ),
    ] = 1,
    output_file: Annotated[
        str,
        typer.Option(
            "-o",
            "--output_file",
            help="Path to save the results JSON file.",
        ),
    ] = "results.json",
):
    """
    Scores predictions against the groundtruth and updates the results
    JSON file with scoring status and metrics.
    """
    scores = {}
    status = "INVALID"
    try:
        scores = score(
            task_number=task_number,
            gt_file=groundtruth_file,
            pred_file=predictions_file,
        )
        status = "SCORED"
        errors = ""
    except ValueError:
        errors = "Error encountered during scoring; submission not evaluated."
    except KeyError:
        errors = f"Invalid challenge task number specified: `{task_number}`"

    res = {
        "score_status": status,
        "score_errors": errors,
        **scores,
    }
    with open(output_file, "w", encoding="utf-8") as out:
        out.write(json.dumps(res))
    print(status)


if __name__ == "__main__":
    # Prevent replacing underscore with dashes in CLI names.
    typer.main.get_command_name = lambda name: name
    typer.run(main)

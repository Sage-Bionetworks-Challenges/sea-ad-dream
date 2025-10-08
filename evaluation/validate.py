#!/usr/bin/env python3
"""Template validation script.

Script is currently designed for validating submission for a single-
task challenge.

At a minimum, you will need to:
    1. Define the expected data structures (see GROUNDTRUTH_COLS and
       PREDICTION_COLS)
    2. Customize validate_task1() to fit your specific validation needs
    3. Add helper functions and manage dependencies as needed for your
       validation process

For challenges with multiple tasks, create additional `validate_task*()`
functions and update the `validate()` function to route validation to
the appropriate task.
"""
import json

import numpy as np
import pandas as pd
import typer
from cnb_tools import validation_toolkit as vtk
from typing_extensions import Annotated

# Groundtruth columns and data type.
GROUNDTRUTH_COLS = {
    "Donor ID": str,
}

# Expected columns and data types for predictions file.
TASK1_PRED_COLS = {
    "Donor ID": str,
    "predicted ADNC": str,
    "predicted Braak": str,
    "predicted CERAD": str,
    "predicted Thal": str,
}
TASK2_PRED_COLS = {
    "Donor ID": str,
    "predicted 6e10": float,
    "predicted AT8": float,
    "predicted GFAP": float,
    "predicted NeuN": float,
}
OPTIONAL_COLS = {
    "predicted LATE": str,
    "predicted Lewy": str,
    "predicted aSyn": float,
    "predicted pTDP43": float,
}

ID_COL = "Donor ID"


def check_acceptable_value(col: pd.Series, acceptable_values: set) -> str:
    """Check if all values in column are accepted values."""
    invalid_values = set(col.unique()) - acceptable_values
    if invalid_values:
        return (
            f"Unacceptable values found in column '{col.name}': "
            f"{', '.join(map(str, invalid_values))}. "
            f"Acceptable values are: {', '.join(map(str, acceptable_values))}."
        )
    return ""


def validate_task1(gt_file: str, pred_file: str) -> list[str] | filter:
    """Validate task 1."""
    errors = []
    truth = pd.read_csv(
        gt_file,
        usecols=GROUNDTRUTH_COLS,
        dtype=GROUNDTRUTH_COLS,
    )
    try:
        cols_to_use = [*TASK1_PRED_COLS] + [*OPTIONAL_COLS]
        pred = pd.read_csv(
            pred_file,
            usecols=lambda colname: colname in cols_to_use,
            float_precision="round_trip",
        )
        assert np.isin([*TASK1_PRED_COLS], pred.columns).all()
    except AssertionError:
        errors.append(
            f"Prediction file is missing one or more required columns. "
            f"Expecting: {str(TASK1_PRED_COLS)}."
        )
    else:
        errors.append(vtk.check_duplicate_keys(pred[ID_COL]))
        errors.append(vtk.check_missing_keys(truth[ID_COL], pred[ID_COL]))
        errors.append(vtk.check_unknown_keys(truth[ID_COL], pred[ID_COL]))
        errors.append(
            check_acceptable_value(
                pred["predicted ADNC"],
                {"Not AD", "Low", "Intermediate", "High"},
            )
        )
        errors.append(
            check_acceptable_value(
                pred["predicted Braak"],
                {
                    "Braak 0",
                    "Braak I",
                    "Braak II",
                    "Braak III",
                    "Braak IV",
                    "Braak V",
                    "Braak VI",
                },
            )
        )
        errors.append(
            check_acceptable_value(
                pred["predicted CERAD"],
                {"Absent", "Sparse", "Moderate", "Frequent"},
            )
        )
        errors.append(
            check_acceptable_value(
                pred["predicted Thal"],
                {"Thal 0", "Thal 1", "Thal 2", "Thal 3", "Thal 4", "Thal 5"},
            )
        )
        if "predicted LATE" in pred.columns:
            errors.append(
                check_acceptable_value(
                    pred["predicted LATE"],
                    {
                        "Not Identified",
                        "LATE Stage 1",
                        "LATE Stage 2",
                        "LATE Stage 3",
                        "Unclassifiable",  # TODO: check with Allen folks
                    },
                )
            )
        if "predicted Lewy" in pred.columns:
            errors.append(
                check_acceptable_value(
                    pred["predicted Lewy"],
                    {
                        "Not Identified (olfactory bulb assessed)",
                        "Olfactory bulb only",
                        "Amygdala-predominant",
                        "Brainstem-predominant",
                        "Limbic (Transitional)",
                        "Neocortical (Diffuse)",
                        "Not Identified (olfactory bulb not assessed)",  # TODO: check with Allen folks
                    },
                )
            )
    # Remove any empty strings from the list before return.
    return filter(None, errors)


def validate_task2(gt_file: str, pred_file: str) -> list[str] | filter:
    """Validate task 2."""
    errors = []
    truth = pd.read_csv(
        gt_file,
        usecols=GROUNDTRUTH_COLS,
        dtype=GROUNDTRUTH_COLS,
    )
    try:
        cols_to_use = [*TASK2_PRED_COLS] + [*OPTIONAL_COLS]
        pred = pd.read_csv(
            pred_file,
            usecols=lambda colname: colname in cols_to_use,
            float_precision="round_trip",
        )
        assert np.isin([*TASK2_PRED_COLS], pred.columns).all()
    except AssertionError:
        errors.append(
            f"Prediction file is missing one or more required columns. "
            f"Expecting: {str(TASK2_PRED_COLS)}."
        )
    else:
        errors.append(vtk.check_duplicate_keys(pred[ID_COL]))
        errors.append(vtk.check_missing_keys(truth[ID_COL], pred[ID_COL]))
        errors.append(vtk.check_unknown_keys(truth[ID_COL], pred[ID_COL]))
        for colname in pred.columns:
            if colname.startswith("predicted"):
                errors.append(
                    vtk.check_values_range(
                        pred[colname],
                        min_val=0,
                        max_val=100,
                    )
                )
    # Remove any empty strings from the list before return.
    return filter(None, errors)


def validate(task_number: int, gt_file: str, pred_file: str) -> list[str] | filter:
    """
    Routes validation to the appropriate task-specific function.
    """
    validation_func = {
        9616048: validate_task1,
        9616135: validate_task1,
        9616049: validate_task2,
        9616136: validate_task2,
    }.get(task_number)

    if validation_func:
        return validation_func(gt_file=gt_file, pred_file=pred_file)
    return [f"Invalid challenge task number specified: `{task_number}`"]


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
    ] = 9616048,
    output_file: Annotated[
        str,
        typer.Option(
            "-o",
            "--output_file",
            help="Path to save the results JSON file.",
        ),
    ] = "results.json",
):
    """Validates the predictions file in preparation for evaluation."""
    errors = validate(
        task_number=task_number,
        gt_file=groundtruth_file,
        pred_file=predictions_file,
    )

    invalid_reasons = "\n".join(errors)
    status = "INVALID" if invalid_reasons else "VALIDATED"

    # Truncate validation errors if >500 (char limit for sending Synapse email)
    if len(invalid_reasons) > 500:
        invalid_reasons = invalid_reasons[:496] + "..."
    res = {
        "submission_status": status,
        "submission_errors": invalid_reasons,
    }

    with open(output_file, "w", encoding="utf-8") as out:
        out.write(json.dumps(res))
    print(status)


if __name__ == "__main__":
    # Prevent replacing underscore with dashes in CLI names.
    typer.main.get_command_name = lambda name: name
    typer.run(main)

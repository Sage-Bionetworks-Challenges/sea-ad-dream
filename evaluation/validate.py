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

import pandas as pd
import typer
from cnb_tools import validation_toolkit as vtk
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


def validate(gt_file: str, pred_file: str) -> list[str] | filter:
    """Validation function.

    Checks include:
        - Prediction file has the expected columns and data types
        - There is exactly one prediction for each ID
        - Every ID has a prediction
        - There are no predictions for IDs not present in the groundtruth
        - Prediction values are not null
        - Prediction values are between 0 and 1, inclusive

    Returns a list of error messages. An empty list signifies successful
    validation.
    """
    errors = []
    truth = pd.read_csv(
        gt_file,
        usecols=GROUNDTRUTH_COLS,
        dtype=GROUNDTRUTH_COLS,
    )
    try:
        pred = pd.read_csv(
            pred_file,
            usecols=PREDICTION_COLS,
            dtype=PREDICTION_COLS,
            float_precision="round_trip",
        )
    except ValueError as err:
        errors.append(
            f"Invalid column names and/or types: {str(err)}. "
            f"Expecting: {str(PREDICTION_COLS)}."
        )
    else:
        errors.append(vtk.check_duplicate_keys(pred["patient_id"]))
        errors.append(vtk.check_missing_keys(truth["patient_id"], pred["patient_id"]))
        errors.append(vtk.check_unknown_keys(truth["patient_id"], pred["patient_id"]))
        errors.append(vtk.check_nan_values(pred["probability"]))
        errors.append(
            vtk.check_values_range(
                pred["probability"],
                min_val=0,
                max_val=1,
            )
        )

    # Remove any empty strings from the list before return.
    return filter(None, errors)


# def validate(task_number: int, gt_file: str, pred_file: str) -> list[str] | filter:
#     """
#     Routes validation to the appropriate task-specific function.
#     """
#     validation_func = {
#         1: validate_task1,
#         # --- Add more tasks and their validation functions here ---
#         # 2: validate_task2,
#     }.get(task_number)

#     if validation_func:
#         return validation_func(gt_file=gt_file, pred_file=pred_file)
#     return [f"Invalid challenge task number specified: `{task_number}`"]


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
    """Validates the predictions file in preparation for evaluation."""
    errors = validate(
        gt_file=groundtruth_file,
        pred_file=predictions_file,
    )

    invalid_reasons = "\n".join(errors)
    status = "INVALID" if invalid_reasons else "VALIDATED"

    # Truncate validation errors if >500 (char limit for sending Synapse email)
    if len(invalid_reasons) > 500:
        invalid_reasons = invalid_reasons[:496] + "..."
    res = {
        "validation_status": status,
        "validation_errors": invalid_reasons,
    }

    with open(output_file, "w", encoding="utf-8") as out:
        out.write(json.dumps(res))
    print(status)


if __name__ == "__main__":
    # Prevent replacing underscore with dashes in CLI names.
    typer.main.get_command_name = lambda name: name
    typer.run(main)

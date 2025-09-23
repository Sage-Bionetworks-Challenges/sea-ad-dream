"""Python Model Example"""

import os

import numpy as np
import pandas as pd
import typer
from typing_extensions import Annotated

ADNC_CATEGORIES = ["Not AD", "Low", "Intermediate", "High"]
BRAAK_CATEGORIES = [
    "Braak 0",
    "Braak I",
    "Braak II",
    "Braak III",
    "Braak IV",
    "Braak V",
    "Braak VI",
]
CERAD_CATEGORIES = ["Absent", "Sparse", "Moderate", "Frequent"]
THAL_CATEGORIES = ["Thal 0", "Thal 1", "Thal 2", "Thal 3", "Thal 4"]
LATE_CATEGORIES = ["Not Identified", "LATE Stage 1", "LATE Stage 2", "LATE Stage 3"]
LEWY_CATEGORIES = [
    "Not Identified (olfactory bulb assessed)",
    "Olfactory bulb only",
    "Amygdala-predominant",
    "Brainstem-predominant",
    "Limbic (Transitional)",
    "Neocortical (Diffuse)",
]


def predict(df: pd.DataFrame) -> pd.DataFrame:
    """Sample prediction function.

    TODO: Replace this with your actual model prediction logic. In this
    example, random values are assigned.
    """
    pred = df.loc[:, ["Donor ID"]].copy()
    np.random.seed(2025)  # For reproducibility

    # Task 1
    pred["predicted ADNC"] = np.random.choice(ADNC_CATEGORIES, size=len(df))
    pred["predicted Braak"] = np.random.choice(BRAAK_CATEGORIES, size=len(df))
    pred["predicted CERAD"] = np.random.choice(CERAD_CATEGORIES, size=len(df))
    pred["predicted Thal"] = np.random.choice(THAL_CATEGORIES, size=len(df))
    pred["predicted LATE"] = np.random.choice(LATE_CATEGORIES, size=len(df))
    pred["predicted Lewy"] = np.random.choice(LEWY_CATEGORIES, size=len(df))

    # Task 2
    pred["predicted 6e10"] = np.random.uniform(low=0, high=100, size=len(df))
    pred["predicted AT8"] = np.random.uniform(low=0, high=100, size=len(df))
    pred["predicted GFAP"] = np.random.uniform(low=0, high=100, size=len(df))
    pred["predicted NeuN"] = np.random.uniform(low=0, high=100, size=len(df))
    pred["predicted aSyn"] = np.random.uniform(low=0, high=100, size=len(df))
    pred["predicted pTDP43"] = np.random.uniform(low=0, high=100, size=len(df))
    return pred


def main(
    input_dir: Annotated[str, typer.Option()] = "/input",
    output_dir: Annotated[str, typer.Option()] = "/output",
):
    """
    Run inference using data in input_dir and output predictions to output_dir.
    """
    # data = pd.read_csv(os.path.join(input_dir, "data.csv"))
    data = pd.read_csv("template.csv")
    predictions = predict(data)
    predictions.to_csv(
        os.path.join(output_dir, "predictions.csv"),
        index=False,
    )


if __name__ == "__main__":
    typer.run(main)

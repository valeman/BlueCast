from typing import List, Union

import pandas as pd

from bluecast.eda.analyse import theil_u


def detect_leakage_via_correlation(
    data: pd.DataFrame, target_column: Union[str, float, int], threshold: float = 0.9
) -> List[Union[str, float, int, None]]:
    """
    Detect data leakage by checking for high correlations between the target column
    and other columns in the DataFrame.

    :param data: The DataFrame containing the data (numerical columns only for features)
    :param target_column: The name of the target column to check for correlations.
    :param threshold: The correlation threshold. If the absolute correlation value is greater than
      or equal to this threshold, it will be considered as a potential data leakage.
    :returns: True if data leakage is detected, False if not.
    """
    if target_column not in data.columns:
        raise ValueError(
            f"The target column '{target_column}' is not found in the DataFrame."
        )

    correlations = data.corr()[target_column].abs()
    potential_leakage = correlations[correlations >= threshold].index.tolist()

    # Exclude the target column itself from potential leakage
    potential_leakage.remove(target_column)

    return potential_leakage


def detect_categorical_leakage(
    data: pd.DataFrame, target_column: Union[str, float, int], threshold: float = 0.9
) -> List[Union[str, float, int, None]]:
    """
    Detect data leakage by calculating Theil's U for categorical variables with respect to the target.

    :param data: The DataFrame containing the data.
    :param target_column: The name of the target column.

    :param threshold: The threshold for Theil's U. Columns with U greater than or equal to this threshold
      will be considered potential data leakage.

    :returns: A list of column names with Theil's U greater than or equal to the threshold.
    """
    if target_column not in data.columns:
        raise ValueError(
            f"The target column '{target_column}' is not found in the DataFrame."
        )

    leakage_columns = []
    for column in data.columns:
        if column == target_column:
            continue
        u = theil_u(data[column], data[target_column])
        if u >= threshold:
            leakage_columns.append(column)

    return leakage_columns

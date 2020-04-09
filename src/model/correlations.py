"""Correlations between variables."""
import itertools
import warnings
from contextlib import suppress
from functools import partial
from typing import Callable, Dict, List, Optional

import pandas as pd
import numpy as np
from confuse import NotFoundError
from pandas.core.base import DataError
from scipy import stats
from tqdm.auto import tqdm

from data_profiling.src.config import config
from data_profiling.src.model.base import Variable


def cramers_corrected_stat(confusion_matrix, correction: bool) -> float:
    """Calculate the Cramer's V corrected stat for two variables.

    Args:
        confusion_matrix: Crosstab between two variables.
        correction: Should the correction be applied?

    Returns:
        The Cramer's V corrected stat for the two variables.
    """
    chi2 = stats.chi2_contingency(confusion_matrix, correction=correction)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape

    # Deal with NaNs later on
    with np.errstate(divide="ignore", invalid="ignore"):
        phi2corr = max(0.0, phi2 - ((k - 1.0) * (r - 1.0)) / (n - 1.0))
        rcorr = r - ((r - 1.0) ** 2.0) / (n - 1.0)
        kcorr = k - ((k - 1.0) ** 2.0) / (n - 1.0)
        corr = np.sqrt(phi2corr / min((kcorr - 1.0), (rcorr - 1.0)))
    return corr

def cramers_matrix(df: pd.DataFrame, variables: dict):
    """Calculate the Cramer's V correlation matrix.

    Args:
        df: The pandas DataFrame.
        variables: A dict with column names mapped to variable type.

    Returns:
        A Cramer's V matrix for categorical variables.
    """
    return categorical_matrix(
        df, variables, partial(cramers_corrected_stat, correction=True)
    )

def categorical_matrix(
    df: pd.DataFrame, variables: dict, correlation_function: Callable
) -> Optional[pd.DataFrame]:
    """Calculate a correlation matrix for categorical variables.

    Args:
        df: The pandas DataFrame.
        variables: A dict with column names mapped to variable type.
        correlation_function: A function to calculate the correlation between two variables.

    Returns:
        A correlation matrix for categorical variables.
    """
    categoricals = {
        column_name: df[column_name]
        for column_name, variable_type in variables.items()
        if variable_type == Variable.TYPE_CAT
        and config["categorical_maximum_correlation_distinct"].get(int)
        >= df[column_name].nunique()
        > 1
    }

    if len(categoricals) <= 1:
        return None

    correlation_matrix = pd.DataFrame(
        np.ones((len(categoricals), len(categoricals))),
        index=categoricals.keys(),
        columns=categoricals.keys(),
    )

    for (name1, data1), (name2, data2) in itertools.combinations(
        categoricals.items(), 2
    ):
        confusion_matrix = pd.crosstab(data1, data2)
        correlation_matrix.loc[name2, name1] = correlation_matrix.loc[
            name1, name2
        ] = correlation_function(confusion_matrix)

    return correlation_matrix


def warn_correlation(correlation_name, error):
    warnings.warn(
        f"""There was an attempt to calculate the {correlation_name} correlation, but this failed.
        To hide this warning, disable the calculation
        (using `df.profile_report(correlations={{\"{correlation_name}\": {{\"calculate\": False}}}})`
        """
    )


def calculate_correlations(df: pd.DataFrame, variables: dict) -> dict:
    """Calculate the correlation coefficients between variables for the correlation types selected in the config
    (pearson, cramers).

    Args:
        variables: A dict with column names and variable types.
        df: The DataFrame with variables.

    Returns:
        A dictionary containing the correlation matrices for each of the active correlation measures.
    """
    correlations = {}

    disable_progress_bar = not config["progress_bar"].get(bool)

    correlation_names = [
        correlation_name
        for correlation_name in [
            "pearson",
            "spearman",
            "cramers"
        ]
        if config["correlations"][correlation_name]["calculate"].get(bool)
    ]

    categorical_correlations = {"cramers": cramers_matrix}

    if len(correlation_names) > 0:
        with tqdm(
            total=len(correlation_names),
            desc="correlations",
            disable=disable_progress_bar,
        ) as pbar:
            for correlation_name in correlation_names:
                pbar.set_description_str(f"correlations [{correlation_name}]")

                if correlation_name in ["pearson","spearman"]:
                    try:
                        correlation = df.corr(method=correlation_name)
                        if len(correlation) > 0:
                            correlations[correlation_name] = correlation
                    except (ValueError, AssertionError) as e:
                        warn_correlation(correlation_name, e)
                elif correlation_name in ["cramers"]:
                    try:
                        get_matrix = categorical_correlations[correlation_name]
                        correlation = get_matrix(df, variables)
                        if correlation is not None and len(correlation) > 0:
                            correlations[correlation_name] = correlation
                    except (ValueError, AssertionError) as e:
                        warn_correlation(correlation_name, e)

                if correlation_name in correlations:
                    # Drop rows and columns with NaNs
                    correlations[correlation_name].dropna(inplace=True, how="all")
                    if correlations[correlation_name].empty:
                        del correlations[correlation_name]

                pbar.update()

    return correlations


def get_correlation_mapping() -> Dict[str, List[str]]:
    """Workaround variable type annotations not being supported in Python 3.5

    Returns:
        type annotated empty dict
    """
    return {}


def perform_check_correlation(
    correlation_matrix: pd.DataFrame, threshold: float
) -> Dict[str, List[str]]:
    """Check whether selected variables are highly correlated values in the correlation matrix.

    Args:
        correlation_matrix: The correlation matrix for the DataFrame.
        threshold:.

    Returns:
        The variables that are highly correlated or recoded.
    """

    corr = correlation_matrix.copy()

    mapping = get_correlation_mapping()
    for x, corr_x in corr.iterrows():
        for y, corr in corr_x.iteritems():
            if x == y:
                break

            if corr >= threshold or corr <= -1 * threshold:
                if x not in mapping:
                    mapping[x] = []
                if y not in mapping:
                    mapping[y] = []

                mapping[x].append(y)
                mapping[y].append(x)
    return mapping

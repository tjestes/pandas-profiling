from typing import Optional, List

from data_profiling.src.config import config
from data_profiling.src.report.presentation.abstract.renderable import Renderable
from data_profiling.src.report.presentation.core import (
    Sequence,
    HTML,
    Image,
    ToggleButton,
    Collapse,
)
from data_profiling.src.visualisation import plot


def get_items() -> List[Renderable]:
    return []


def get_correlation_items(summary) -> Optional[Renderable]:
    """Create the list of correlation items

    Args:
        summary: dict of correlations

    Returns:
        List of correlation items to show in the interface.
    """
    items = get_items()

    pearson_description = (
        "The Pearson's correlation coefficient (<em>r</em>) is a measure of linear "
        "correlation between two variables. It's value lies between -1 and +1, where "
        "-1 indicates a total negative linear correlation, 0 indicates no linear "
        "correlation and +1 indicates a total positive linear correlation. <br />"
        "<br /> Pearson's <em>r</em> assumes the following: <br /> "
        "  - Variables are continuous (Spearman's correlation should be used for ordinal) <br /> "
        "  - Measurements are related (e.g. every row has a height and weight measurement) <br /> "
        "  - Minimal to no outliers <br /> "
        "  - Variables are  normally distributed <br /> "
        "  - Variables are linearly related <br /> "
        "  - Homoscedasticy (equal variance of data around regression line)<br /> "
        "<br /> To calculate <em>r</em> for two variables <em>X</em> and <em>Y</em>, one divides the "
        "covariance of <em>X</em> and <em>Y</em> by the product of their standard deviations. "
    )

    spearman_description = (
        "The Spearman's rank correlation coefficient (<em>ρ</em>) is a measure of "
        "monotonic correlation between two variables, and is therefore better in "
        "catching nonlinear correlations than Pearson's <em>r</em>. It's value lies "
        "between -1 and +1, where -1 indicates a total negative correlation, indicates "
        "no correlation, and 1 indicates total positive correlation.<br /> "

        "<br />Spearman's rank correlation assumes two things:<br /> "
        "  - Data is monotomnically related<br /> "
        "  - At least one variable in the correlation is ordinal<br /> "
        
        "<br />A monotonic relationship states one of the following:<br /> "
        "  - As the value of one variable INCREASES, so does the value of another<br /> "
        "  - As the value of one variable DECREASES, the value of another INCREASES<br /> " 
        
        "<br />To calculate <em>ρ</em> for two variables <em>X</em> and <em>Y</em>, one "
        "divides the covariance of the rank variables of <em>X</em> and <em>Y</em> by the" 
        "product of their standard deviations. "
    )
    cramer_description = (
        "Cramer's V is a measure between two nominal (categorical) variables, where the "
        "score is between 0 and 1. Unlike Pearson's and Spearman correlations, Cramer's V "
        "does not indicate a direction of the relationship (positive or negative), but instead "
        "indicates the strength of the relationship. <br /> " 
        
        "<br />The following guidelines can be used to determine the strength of the correlation: <br /> "
        "  - Very strong relationship: 0.25 or higher <br /> "
        "  - Strong relationship: 0.15 to 0.25 <br /> "
        "  - Moderate relationship: 0.11 to 0.15 <br /> "
        "  - weak relationship: 0.06 to 0.10 <br />"
        "  - No or negligible relationship: 0.01 to 0.05 <br /> "
        
        "<br />Cramer's V correlation assumes that your data has more than 2 columns and 2 rows (2x2)."
    )

    key_to_data = {
        "pearson": (-1, "Pearson's r", pearson_description),
        "spearman": (-1, "Spearman's ρ", spearman_description),
        "cramers": (0, "Cramér's V (φc)", cramer_description)
    }

    image_format = config["plot"]["image_format"].get(str)

    for key, item in summary["correlations"].items():
        vmin, name, description = key_to_data[key]

        diagram = Image(
            plot.correlation_matrix(item, vmin=vmin),
            image_format=image_format,
            alt=name,
            anchor_id=f"{key}_diagram",
            name=name,
            classes="correlation-diagram",
        )

        if len(description) > 0:
            desc = HTML(
                f'<div style="padding:20px" class="text-muted"><h3>{name}</h3>{description}</div>',
                anchor_id=f"{key}_html",
                classes="correlation-description",
            )

            tbl = Sequence(
                [diagram, desc], anchor_id=key, name=name, sequence_type="grid"
            )

            items.append(tbl)
        else:
            items.append(diagram)

    corr = Sequence(
        items,
        sequence_type="tabs",
        name="Correlations Tab",
        anchor_id="correlations_tab",
    )

    if len(items) > 0:
        btn = ToggleButton(
            "Toggle correlation descriptions",
            anchor_id="toggle-correlation-description",
            name="Toggle correlation descriptions",
        )

        return Collapse(
            name="Correlations", anchor_id="correlations", button=btn, item=corr
        )
    else:
        return None

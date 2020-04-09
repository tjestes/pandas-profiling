import pandas as pd
import sys
from data_profiling.src.config import config
from data_profiling.src.report.presentation.frequency_table_utils import freq_table
from data_profiling.src.visualisation.plot import histogram
from data_profiling.src.report.presentation.core import (
    Image,
    FrequencyTable,
    FrequencyTableSmall,
    Sequence,
    Table,
    VariableInfo,
)
from data_profiling.src.report.structure.variables.render_common import render_common


def render_categorical(summary):
    varid = summary["varid"]
    n_obs_cat = config["vars"]["cat"]["n_obs"].get(int)
    image_format = config["plot"]["image_format"].get(str)

    template_variables = render_common(summary)

    mini_freq_table_rows = freq_table(
        freqtable=summary["value_counts"],
        n=summary["count"],
        max_number_to_print=n_obs_cat,
    )

    # Top
    # Element composition
    info = VariableInfo(
        summary["varid"], summary["varname"], "Categorical", summary["warnings"]
    )

    table = Table(
        [
            {
                "name": "Distinct count",
                "value": summary["n_unique"],
                "fmt": "fmt",
                "alert": "n_unique" in summary["warn_fields"],
            },
            {
                "name": "Unique (%)",
                "value": summary["p_unique"],
                "fmt": "fmt_percent",
                "alert": "p_unique" in summary["warn_fields"],
            },
            {
                "name": "Missing",
                "value": summary["n_missing"],
                "fmt": "fmt",
                "alert": "n_missing" in summary["warn_fields"],
            },
            {
                "name": "Missing (%)",
                "value": summary["p_missing"],
                "fmt": "fmt_percent",
                "alert": "p_missing" in summary["warn_fields"],
            },
            {
                "name": "Memory size",
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
                "alert": False,
            },
        ]
    )

    fqm = FrequencyTableSmall(mini_freq_table_rows)

    template_variables["top"] = Sequence([info, table, fqm], sequence_type="grid")

    # Bottom
    items = []
    frequency_table = FrequencyTable(
        template_variables["freq_table_rows"],
        name="Common Values",
        anchor_id=f"{varid}common_values",
    )

    items.append(frequency_table)

    check_compositions = config["vars"]["cat"]["check_composition"].get(bool)
    if check_compositions:
        n_freq_table_max = config["n_freq_table_max"].get(int)

        citems = []
        vc = pd.Series(summary["category_alias_values"]).value_counts()
        citems.append(
            FrequencyTable(
                freq_table(
                    freqtable=vc, n=vc.sum(), max_number_to_print=n_freq_table_max
                ),
                name="Categories",
                anchor_id=f"{varid}category_long_values",
            )
        )

        vc = pd.Series(summary["script_values"]).value_counts()
        citems.append(
            FrequencyTable(
                freq_table(
                    freqtable=vc, n=vc.sum(), max_number_to_print=n_freq_table_max
                ),
                name="Scripts",
                anchor_id=f"{varid}script_values",
            )
        )

        vc = pd.Series(summary["block_alias_values"]).value_counts()
        citems.append(
            FrequencyTable(
                freq_table(
                    freqtable=vc, n=vc.sum(), max_number_to_print=n_freq_table_max
                ),
                name="Blocks",
                anchor_id=f"{varid}block_alias_values",
            )
        )

        characters = Sequence(
            citems,
            name="Characters",
            sequence_type="tabs",
            anchor_id=f"{varid}characters",
        )

        items.append(characters)

    template_variables["bottom"] = Sequence(
        items, sequence_type="tabs", anchor_id=f"{varid}bottom"
    )

    return template_variables

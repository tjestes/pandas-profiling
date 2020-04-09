from urllib.parse import quote

from data_profiling.src.report.presentation.core import HTML, Table, Sequence, Warnings


def get_dataset_overview(summary):
    dataset_info = Table(
        [
            {
                "name": "Number of variables",
                "value": summary["table"]["n_var"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "Number of observations",
                "value": summary["table"]["n"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "Missing cells",
                "value": summary["table"]["n_cells_missing"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "Missing cells (%)",
                "value": summary["table"]["p_cells_missing"],
                "fmt": "fmt_percent",
            },
            {
                "name": "Duplicate rows",
                "value": summary["table"]["n_duplicates"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "Duplicate rows (%)",
                "value": summary["table"]["p_duplicates"],
                "fmt": "fmt_percent",
            },
            {
                "name": "Total size in memory",
                "value": summary["table"]["memory_size"],
                "fmt": "fmt_bytesize",
            },
            {
                "name": "Average record size in memory",
                "value": summary["table"]["record_size"],
                "fmt": "fmt_bytesize",
            },
        ],
        name="Dataset statistics",
    )

    dataset_types = Table(
        [
            {"name": type_name, "value": count, "fmt": "fmt_numeric"}
            for type_name, count in summary["table"]["types"].items()
        ],
        name="Variable types",
    )

    return Sequence(
        [dataset_info, dataset_types],
        anchor_id="dataset_overview",
        name="Overview",
        sequence_type="grid",
    )

def get_dataset_warnings(warnings, count):
    return Warnings(warnings=warnings, name=f"Warnings ({count})", anchor_id="warnings")

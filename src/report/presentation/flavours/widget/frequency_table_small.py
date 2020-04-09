from ipywidgets import widgets

from data_profiling.src.report.presentation.core.frequency_table_small import (
    FrequencyTableSmall,
)


class WidgetFrequencyTableSmall(FrequencyTableSmall):
    def render(self):
        return frequency_table_nb(self.content)


def frequency_table_nb(rows):
    items = []

    for row in rows:
        if row["extra_class"] == "missing":
            items.append(
                widgets.HBox(
                    [
                        widgets.FloatProgress(
                            value=row["count"],
                            min=0,
                            max=row["n"],
                            description=str(row["label"]),
                            bar_style="danger",
                        ),
                        widgets.Label(str(row["count"])),
                    ]
                )
            )
        elif row["extra_class"] == "other":
            items.append(
                widgets.HBox(
                    [
                        widgets.FloatProgress(
                            value=row["count"],
                            min=0,
                            max=row["n"],
                            description=str(row["label"]),
                            bar_style="info",
                        ),
                        widgets.Label(str(row["count"])),
                    ]
                )
            )
        else:
            items.append(
                widgets.HBox(
                    [
                        widgets.FloatProgress(
                            value=row["count"],
                            min=0,
                            max=row["n"],
                            description=str(row["label"]),
                            bar_style="",
                        ),
                        widgets.Label(str(row["count"])),
                    ]
                )
            )

    ft = widgets.VBox(items)

    return ft

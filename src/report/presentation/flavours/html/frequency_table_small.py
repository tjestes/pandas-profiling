from data_profiling.src.report.presentation.core import FrequencyTableSmall
from data_profiling.src.report.presentation.flavours.html import templates


class HTMLFrequencyTableSmall(FrequencyTableSmall):
    def render(self):
        return templates.template("frequency_table_small.html").render(
            rows=self.content
        )

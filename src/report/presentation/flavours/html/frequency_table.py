from data_profiling.src.report.presentation.flavours.html import templates
from data_profiling.src.report.presentation.core import FrequencyTable


class HTMLFrequencyTable(FrequencyTable):
    def render(self):
        return templates.template("frequency_table.html").render(
            rows=self.content["rows"]
        )

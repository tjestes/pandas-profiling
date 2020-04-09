from data_profiling.src.report.presentation.core.table import Table
from data_profiling.src.report.presentation.flavours.html import templates


class HTMLTable(Table):
    def render(self):
        return templates.template("table.html").render(**self.content)

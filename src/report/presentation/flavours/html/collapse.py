from data_profiling.src.report.presentation.core import Collapse
from data_profiling.src.report.presentation.flavours.html import templates


class HTMLCollapse(Collapse):
    def render(self):
        return templates.template("collapse.html").render(**self.content)

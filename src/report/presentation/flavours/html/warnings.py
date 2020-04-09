from data_profiling.src.report.presentation.core.warnings import Warnings
from data_profiling.src.report.presentation.flavours.html import templates


class HTMLWarnings(Warnings):
    def render(self):
        return templates.template("warnings.html").render(**self.content)

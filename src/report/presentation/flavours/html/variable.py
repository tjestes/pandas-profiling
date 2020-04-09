from data_profiling.src.report.presentation.core import Variable
from data_profiling.src.report.presentation.flavours.html import templates


class HTMLVariable(Variable):
    def render(self):
        return templates.template("variable.html").render(**self.content)

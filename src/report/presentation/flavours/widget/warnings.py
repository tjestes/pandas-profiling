from ipywidgets import widgets

from data_profiling.src.report.presentation.core import Warnings
from data_profiling.src.report.presentation.flavours.html import templates


class WidgetWarnings(Warnings):
    def render(self):
        return widgets.HTML(templates.template("warnings.html").render(**self.content))

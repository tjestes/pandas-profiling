from ipywidgets import widgets

from data_profiling.src.report.presentation.core.html import HTML


class WidgetHTML(HTML):
    def render(self):
        if type(self.content["html"]) != str:
            return self.content["html"]
        else:
            return widgets.HTML(self.content["html"])

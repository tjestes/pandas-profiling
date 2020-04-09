from ipywidgets import widgets

from data_profiling.src.report.presentation.core.sample import Sample


class WidgetSample(Sample):
    def render(self):
        return widgets.VBox([widgets.HTML(self.content["sample"])])

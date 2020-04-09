from PyQt5.QtWidgets import QPushButton

from data_profiling.src.report.presentation.core import Sample


class QtSample(Sample):
    def render(self):
        return QPushButton(self.content["name"])

from PyQt5.QtWidgets import QPushButton

from data_profiling.src.report.presentation.core import FrequencyTable


class QtFrequencyTable(FrequencyTable):
    def render(self):
        return QPushButton("Frequency Table")

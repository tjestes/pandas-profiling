from PyQt5.QtWidgets import QPushButton

from data_profiling.src.report.presentation.core import FrequencyTableSmall


class QtFrequencyTableSmall(FrequencyTableSmall):
    def render(self):
        return QPushButton("Small Frequency Table")

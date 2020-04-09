from data_profiling.src.report.presentation.core.sample import Sample
from data_profiling.src.report.presentation.flavours.html import templates


class HTMLSample(Sample):
    def render(self):
        return templates.template("sample.html").render(**self.content)

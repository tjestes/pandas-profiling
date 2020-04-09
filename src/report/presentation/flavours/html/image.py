from data_profiling.src.report.presentation.core import Image
from data_profiling.src.report.presentation.flavours.html import templates


class HTMLImage(Image):
    def render(self):
        return templates.template("diagram.html").render(**self.content)

from typing import Any

from data_profiling.src.report.presentation.abstract.item_renderer import ItemRenderer


class HTML(ItemRenderer):
    def __init__(self, content, **kwargs):
        super().__init__("html", {"html": content}, **kwargs)

    def __repr__(self):
        return "HTML"

    def render(self) -> Any:
        raise NotImplementedError()

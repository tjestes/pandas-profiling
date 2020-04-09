from data_profiling.src.config import config

from data_profiling.src.report.presentation.core.sequence import Sequence
from data_profiling.src.report.presentation.flavours.html import templates


class HTMLSequence(Sequence):
    def render(self):
        if self.sequence_type in ["list", "accordion"]:
            return templates.template("sequence/list.html").render(
                anchor_id=self.content["anchor_id"], items=self.content["items"]
            )
        elif self.sequence_type == "tabs":
            return templates.template("sequence/tabs.html").render(
                tabs=self.content["items"], anchor_id=self.content["anchor_id"]
            )
        elif self.sequence_type == "sections":
            return templates.template("sequence/sections.html").render(
                sections=self.content["items"],
                full_width=config["html"]["style"]["full_width"].get(bool),
            )
        elif self.sequence_type == "grid":
            return templates.template("sequence/grid.html").render(
                items=self.content["items"]
            )

        raise ValueError("Template not understood", self.sequence_type)

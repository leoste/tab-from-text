from dataclasses import dataclass


@dataclass
class SegmentRenderState:
    """Mutable state that threads through an entire segment render pass.

    Carries everything that depends on what has been drawn so far —
    not properties of any single note, but of the rendering in progress.
    """
    last_style:            object = None  # style of the last rendered note
    last_annotation_x:     object = None  # x where the current spanning annotation left off (int | None)
    last_annotation_y:     object = None  # y of the current spanning annotation (int | None)
    last_annotation_style: object = None  # which style is currently being spanned (StrumStyle | None)

    def reset_annotation(self) -> None:
        """Clear all spanning-annotation state, called at every new system row."""
        self.last_annotation_x     = None
        self.last_annotation_y     = None
        self.last_annotation_style = None
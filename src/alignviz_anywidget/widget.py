from pathlib import Path

import anywidget
import traitlets


class ParallelTextAlignWidget(anywidget.AnyWidget):
		"""Interactive aligned-text widget for notebook environments.

		passages_json should be a JSON list of objects with keys:
		- label: optional short title for the version
		- html: HTML content for the version where aligned tokens/phrases carry
			a shared identifier via data-align-id or id.
		"""

		_esm = Path(__file__).parent / "static" / "index.js"

		title = traitlets.Unicode("Aligned Text Explorer").tag(sync=True)
		passages_json = traitlets.Unicode("[]").tag(sync=True)
		layout = traitlets.Unicode("horizontal").tag(sync=True)
		width = traitlets.Unicode("100%").tag(sync=True)
		height = traitlets.Unicode("420px").tag(sync=True)
		base_highlight = traitlets.Unicode("#cfe8ff").tag(sync=True)
		hover_highlight = traitlets.Unicode("#ffd166").tag(sync=True)


class AlignViewer(ParallelTextAlignWidget):
		"""Backward-compatible alias for earlier scaffolded class name."""



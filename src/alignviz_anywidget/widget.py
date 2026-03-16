from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

import anywidget
import traitlets
from markdown import markdown as render_markdown

_TOKEN_SPLIT_RE = re.compile(r"(\s+)")


def _render_label_markdown(label: str) -> str:
	"""Render markdown label content as inline-safe HTML."""
	escaped = html.escape(label)
	html_out = render_markdown(escaped)

	# Convert common single-paragraph markdown output into inline HTML.
	if html_out.startswith("<p>") and html_out.endswith("</p>"):
		return html_out[3:-4]
	return html_out


def _normalize_passages(passages: list[dict[str, Any]]) -> list[dict[str, str]]:
	normalized: list[dict[str, str]] = []
	for idx, item in enumerate(passages):
		label = str(item.get("label", f"Version {idx + 1}"))
		label_html = _render_label_markdown(label)
		html_text = str(item.get("html", ""))
		normalized.append({"label": label, "label_html": label_html, "html": html_text})
	return normalized


def _aligned_html_from_text(text: str, alignments: list[list[str]], prefix: str = "align") -> str:
	tokens = _TOKEN_SPLIT_RE.split(text)
	token_tags: list[str | None] = [None] * len(tokens)

	for align_id, group in enumerate(alignments):
		for raw_word in group:
			word = str(raw_word)
			found = False

			# First pass: search forward for next unclaimed exact token.
			for i, token in enumerate(tokens):
				if token_tags[i] is None and token.strip() == word:
					token_tags[i] = f"{prefix}-{align_id}"
					found = True
					break

			# If exact case didn't match, try case-insensitive fallback.
			if not found:
				lower_word = word.lower()
				for i, token in enumerate(tokens):
					if token_tags[i] is None and token.strip().lower() == lower_word:
						token_tags[i] = f"{prefix}-{align_id}"
						break

	html_bits: list[str] = []
	for i, token in enumerate(tokens):
		escaped_token = html.escape(token)
		align_id = token_tags[i]
		if align_id:
			html_bits.append(
				f'<span data-align-id="{align_id}" class="aligned-term">{escaped_token}</span>'
			)
		else:
			html_bits.append(escaped_token)

	return "".join(html_bits)


def _versions_to_passages(versions: list[dict[str, Any]]) -> list[dict[str, str]]:
	passages: list[dict[str, str]] = []
	for idx, version in enumerate(versions):
		text = str(version.get("text", ""))
		alignments = version.get("alignments", [])
		if not isinstance(alignments, list):
			alignments = []

		clean_alignments: list[list[str]] = []
		for group in alignments:
			if isinstance(group, list):
				clean_alignments.append([str(word) for word in group])

		label = str(version.get("label", f"Version {idx + 1}"))
		passages.append(
			{
				"label": label,
				"label_html": _render_label_markdown(label),
				"html": _aligned_html_from_text(text, clean_alignments, prefix="align"),
			}
		)
	return passages


def build_passages_from_versions(versions: list[dict[str, Any]]) -> list[dict[str, str]]:
	"""Convert versions input into widget passages.

	Input format:
	[
		{
			"label": "optional label",
			"text": "raw text",
			"alignments": [["token1"], ["token2", "token3"]],
		},
		...
	]

	Output format:
	[
		{"label": "...", "html": "..."},
		...
	]
	"""
	return _versions_to_passages(versions)


class ParallelTextAlignWidget(anywidget.AnyWidget):
	"""Interactive aligned-text widget for notebook environments.

	Supported initialization styles:
	1) Existing format: passages=[{"label": ..., "html": ...}, ...]
	2) New format: versions=[{"text": ..., "alignments": [[...], ...]}, ...]

	The new ``versions`` format is converted to aligned HTML automatically.
	"""

	_esm = (Path(__file__).parent / "static" / "index.js").read_text(encoding="utf-8")

	title = traitlets.Unicode("Aligned Text Explorer").tag(sync=True)
	passages_json = traitlets.Unicode("[]").tag(sync=True)
	layout = traitlets.Unicode("horizontal").tag(sync=True)
	width = traitlets.Unicode("100%").tag(sync=True)
	height = traitlets.Unicode("420px").tag(sync=True)
	base_highlight = traitlets.Unicode("#cfe8ff").tag(sync=True)
	hover_highlight = traitlets.Unicode("#ffd166").tag(sync=True)

	def __init__(
		self,
		*args: Any,
		passages: list[dict[str, Any]] | None = None,
		versions: list[dict[str, Any]] | None = None,
		**kwargs: Any,
	) -> None:
		# Keep explicit passages_json highest priority if caller provided it.
		if "passages_json" not in kwargs:
			if passages is not None:
				kwargs["passages_json"] = json.dumps(_normalize_passages(passages))
			elif versions is not None:
				kwargs["passages_json"] = json.dumps(_versions_to_passages(versions))

		super().__init__(*args, **kwargs)


class AlignViewer(ParallelTextAlignWidget):
	"""Backward-compatible alias for earlier scaffolded class name."""



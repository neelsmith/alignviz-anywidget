# Usage

This document summarizes how to use `ParallelTextAlignWidget` in marimo notebooks.

## Install

From the repository root:

```bash
pip install -e .
```

## Import

```python
from alignviz_anywidget import ParallelTextAlignWidget
```

## Input Formats

`ParallelTextAlignWidget` supports two input styles.

### 1) Recommended: versions format (`text` + `alignments`)

Each item is a dictionary with:
- `text`: full version text
- `alignments`: list of alignment groups
- `label`: optional display name

Example:

```python
versions_data = [
    {
        "label": "Latin",
        "text": "Gallia est omnis divisa in partes tres",
        "alignments": [["Gallia"], ["est", "divisa"], ["partes"]],
    },
    {
        "label": "English",
        "text": "All of Gaul is divided into three parts",
        "alignments": [["Gaul"], ["is", "divided"], ["parts"]],
    },
]
```

Horizontal layout:

```python
horizontal = ParallelTextAlignWidget(
    title="Aligned Terms (horizontal)",
    versions=versions_data,
    layout="horizontal",
    width="100%",
    height="260px",
)
```

Vertical layout:

```python
vertical = ParallelTextAlignWidget(
    title="Aligned Terms (vertical)",
    versions=versions_data,
    layout="vertical",
    width="100%",
    height="360px",
)
```

### 2) Legacy: passages format (`label` + `html`)

Each item is a dictionary with:
- `label`
- `html` containing aligned spans with shared `data-align-id` values

Example:

```python
passages = [
    {
        "label": "Latin",
        "html": '<span data-align-id="a0" class="aligned-term">Gallia</span> est',
    },
    {
        "label": "English",
        "html": '<span data-align-id="a0" class="aligned-term">Gaul</span> is',
    },
]

widget = ParallelTextAlignWidget(
    title="Legacy Passages",
    passages=passages,
    layout="horizontal",
)
```

You can also pass `passages_json` directly when needed.

## Optional Helper

Use the helper if you want converted passages before widget construction:

```python
from alignviz_anywidget import build_passages_from_versions

passages = build_passages_from_versions(versions_data)
```

## Layout and Style Options

- `layout`: `"horizontal"` or `"vertical"`
- `width`: CSS width (for example `"100%"`)
- `height`: CSS height (for example `"360px"`)
- `base_highlight`: default aligned-term background color
- `hover_highlight`: hover/matched aligned-term highlight color

## Behavior Notes

- Hovering an aligned token highlights all matching tokens across all versions.
- For cross-version highlighting, keep all versions in one widget instance.
- The widget frontend is bundled with the Python package and loaded from `_esm`.

## Notebook Example

See the marimo example in `marimo/usage-example.py` for a complete working notebook.

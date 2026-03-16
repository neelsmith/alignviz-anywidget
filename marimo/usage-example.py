# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = [
#     "anywidget==0.9.21",
#     "marimo>=0.20.4",
# ]
# ///

# pyright: reportMissingImports=false

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import importlib
    import json
    import sys
    from pathlib import Path

    try:
        from alignviz_anywidget import ParallelTextAlignWidget
    except (ImportError, AttributeError):
        repo_src = Path(__file__).resolve().parents[1] / "src"
        if str(repo_src) not in sys.path:
            sys.path.insert(0, str(repo_src))
        for mod_name in list(sys.modules):
            if mod_name == "alignviz_anywidget" or mod_name.startswith("alignviz_anywidget."):
                del sys.modules[mod_name]
        importlib.invalidate_caches()
        from alignviz_anywidget import ParallelTextAlignWidget
    return ParallelTextAlignWidget, json


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Interactive anywidget demo

    Hover any highlighted term to highlight all matching aligned terms across versions.
    """)
    return


@app.cell
def _():
    passages = [
        {
            "label": "Latin",
            "html": """
    <span data-align-id="a0" class="aligned-term">Gallia</span> est omnis
    <span data-align-id="a1" class="aligned-term">divisa</span> in
    <span data-align-id="a2" class="aligned-term">partes</span> tres
    """,
        },
        {
            "label": "English",
            "html": """
    All of <span data-align-id="a0" class="aligned-term">Gaul</span>
    <span data-align-id="a1" class="aligned-term">is</span>
    <span data-align-id="a1" class="aligned-term">divided</span>
    into three <span data-align-id="a2" class="aligned-term">parts</span>
    """,
        },
        {
            "label": "French",
            "html": """
    Toute la <span data-align-id="a0" class="aligned-term">Gaule</span>
    <span data-align-id="a1" class="aligned-term">est</span>
    <span data-align-id="a1" class="aligned-term">divisee</span>
    en trois <span data-align-id="a2" class="aligned-term">parties</span>
    """,
        },
    ]
    return (passages,)


@app.cell
def _(ParallelTextAlignWidget, json, passages):
    # Horizontal layout: single widget with layout="horizontal"
    # This preserves cross-version hover highlighting across side-by-side columns
    horizontal_layout = ParallelTextAlignWidget(
        title="Aligned Terms (horizontal/side-by-side)",
        passages_json=json.dumps(passages),
        layout="horizontal",
        width="100%",
        height="260px",
        base_highlight="#cfe8ff",
        hover_highlight="#ffcf66",
    )

    # Vertical layout: single widget with layout="vertical"
    vertical_layout = ParallelTextAlignWidget(
        title="Aligned Terms (vertical/stacked)",
        passages_json=json.dumps(passages),
        layout="vertical",
        width="100%",
        height="360px",
        base_highlight="#d9f4df",
        hover_highlight="#ffd166",
    )
    return horizontal_layout, vertical_layout


@app.cell
def _(horizontal_layout, mo):
    mo.hstack([horizontal_layout])
    return


@app.cell
def _(horizontal_layout, mo, vertical_layout):
    mo.vstack([
        mo.md("### Horizontal Layout (side-by-side)"),
        horizontal_layout,
        mo.md("### Vertical Layout (stacked)"),
        vertical_layout,
    ])
    return


if __name__ == "__main__":
    app.run()

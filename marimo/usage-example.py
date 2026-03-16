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
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import importlib
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
    return (ParallelTextAlignWidget,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Interactive anywidget demo

    Hover any highlighted term to highlight all matching aligned terms across versions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Labels support markdown formatting (for example, bold and italics).
    """)
    return


@app.cell
def _():
    versions_data = [
        {
            "label": "**Latin** _original_",
            "text": "Gallia est omnis divisa in partes tres",
            "alignments": [["Gallia"], ["est", "divisa"], ["partes"]],
        },
        {
            "label": "**English** _translation_",
            "text": "All of Gaul is divided into three parts",
            "alignments": [["Gaul"], ["is", "divided"], ["parts"]],
        },
        {
            "label": "**French** _traduction_",
            "text": "Toute la Gaule est divisee en trois parties",
            "alignments": [["Gaule"], ["est", "divisee"], ["parties"]],
        },
    ]
    return (versions_data,)


@app.cell
def _(ParallelTextAlignWidget, versions_data):
    horizontal_layout = ParallelTextAlignWidget(
        title="Aligned Terms (horizontal/side-by-side)",
        versions=versions_data,
        layout="horizontal",
        width="100%",
        height="260px",
        base_highlight="#cfe8ff",
        hover_highlight="#ffcf66",
    )
    return (horizontal_layout,)


@app.cell
def _(ParallelTextAlignWidget, versions_data):
    vertical_layout = ParallelTextAlignWidget(
        title="Aligned Terms (vertical/stacked)",
        versions=versions_data,
        layout="vertical",
        width="100%",
        height="360px",
        base_highlight="#d9f4df",
        hover_highlight="#ffd166",
    )
    return (vertical_layout,)


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

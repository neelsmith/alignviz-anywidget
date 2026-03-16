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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Interactive anywidget demo
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Demo of usage
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Hover any highlighted term to highlight all matching aligned terms across versions.
    """)
    return


@app.cell
def _(ParallelTextAlignWidget, versions_data):
    # Horizontal layout: single widget with layout="horizontal"
    # This preserves cross-version hover highlighting across side-by-side columns
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
def _(horizontal_layout):
    horizontal_layout
    return


@app.cell
def _(ParallelTextAlignWidget, versions_data):
    # Vertical layout: single widget with layout="vertical"
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
def _(vertical_layout):
    vertical_layout
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Sample data
    """)
    return


@app.cell
def _():
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
        {
            "label": "French",
            "text": "Toute la Gaule est divisee en trois parties",
            "alignments": [["Gaule"], ["est", "divisee"], ["parties"]],
        },
    ]
    return (versions_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Imports
    """)
    return


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


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()

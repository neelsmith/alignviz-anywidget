# /// script
# requires-python = ">=3.13"
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
    import sys
    from pathlib import Path

    #try:
    #    from alignviz_anywidget import AlignViewer
    #except (ImportError, AttributeError):
    #    repo_src = Path(__file__).resolve().parents[1] / "src"
    #    if str(repo_src) not in sys.path:
    #        sys.path.insert(0, str(repo_src))
    #    for name in list(sys.modules):
    #        if name == "alignviz_anywidget" or name.startswith("alignviz_anywidget."):
    #            del sys.modules[name]
    #    importlib.invalidate_caches()
    #    from alignviz_anywidget import AlignViewer
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Static HTML display
    """)
    return


@app.cell
def _():
    import re

    return (re,)


@app.cell
def _(re):
    def generate_aligned_html(versions_data):
        """
        versions_data: List of dicts, e.g.:
        [
            {
                "text": "Gallia est omnis divisa in partes tres",
                "alignments": [["Gallia"], ["est", "divisa"], ["partes"]]
            },
            {
                "text": "Gaul is divided into three parts",
                "alignments": [["Gaul"], ["is", "divided"], ["parts"]]
            }
        ]
        """
        output_html_versions = []

        for v_idx, version in enumerate(versions_data):
            text = version["text"]
            alignment_groups = version["alignments"]

            # 1. Tokenize preserving whitespace/punctuation
            # This regex captures words and the spaces between them separately
            tokens = re.split(r'(\s+)', text)

            # Track which tokens are already "claimed" by an alignment ID
            # and keep a pointer to search forward for repeats
            token_tags = [None] * len(tokens)
            search_start_index = 0

            for align_id, group in enumerate(alignment_groups):
                for word in group:
                    # Find the next available occurrence of this word
                    found = False
                    for i in range(search_start_index, len(tokens)):
                        if tokens[i].strip() == word and token_tags[i] is None:
                            token_tags[i] = f"align-{align_id}"
                            # We don't update search_start_index here because 
                            # words in the same group might be out of order 
                            # or non-contiguous.
                            found = True
                            break

                    if not found:
                        # Fallback: search from beginning if not found ahead
                        for i in range(0, len(tokens)):
                            if tokens[i].strip() == word and token_tags[i] is None:
                                token_tags[i] = f"align-{align_id}"
                                break

            # 2. Build HTML string
            html_bits = []
            for i, token in enumerate(tokens):
                if token_tags[i]:
                    html_bits.append(f'<span id="{token_tags[i]}" class="aligned-term">{token}</span>')
                else:
                    html_bits.append(token)

            output_html_versions.append("".join(html_bits))

        return output_html_versions


    return (generate_aligned_html,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Demo of static display
    """)
    return


@app.cell
def _():
    inputdata = [
        {
            "text": "Gallia est omnis divisa in partes tres",
            "alignments": [["Gallia"], ["est", "divisa"], ["partes"]]
        },
        {
            "text": "Gaul is divided into three parts",
            "alignments": [["Gaul"], ["is", "divided"], ["parts"]]
        }
    ]
    return (inputdata,)


@app.cell
def _(generate_aligned_html, inputdata):
    htmlout = generate_aligned_html(inputdata)
    return (htmlout,)


@app.cell
def _(htmlout, mo):

    columns_html = "".join(
        [
            f'<div class="version-col"><div class="version-content">{version_html}</div></div>'
            for version_html in htmlout
        ]
    )

    display = mo.Html(
        f"""
        <style>
            .aligned-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 1rem;
                align-items: start;
            }}
            .version-col {{
                border: 1px solid #d9e2ec;
                border-radius: 8px;
                background: #f8fbff;
                padding: 0.9rem;
                line-height: 1.65;
            }}
            .aligned-term {{
                background-color: #cfe8ff;
                border-radius: 3px;
                padding: 0 0.1em;
            }}
        </style>
        <div class="aligned-grid">{columns_html}</div>
        """
    )

    display
    return


if __name__ == "__main__":
    app.run()

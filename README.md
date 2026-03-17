# alignviz-anywidget

An `anywidget` project scaffold for building alignment visualization widgets used in marimo notebooks.


```python
from alignviz_anywidget import ParallelTextAlignWidget

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

 caesar = ParallelTextAlignWidget(
        title="Caesar *BG* 1.1 (horizontal layout)",
        versions=versions_data,
        layout="horizontal",
        width="100%",
        height="260px",
        base_highlight="#cfe8ff",
        hover_highlight="#ffcf66",
    )	

	
```
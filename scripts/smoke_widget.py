import json

from alignviz_anywidget import AlignViewer


def main() -> None:
    passages = [
        {
            "label": "Latin",
            "html": '<span data-align-id="a0" class="aligned-term">Gallia</span> est omnis <span data-align-id="a1" class="aligned-term">divisa</span>',
        },
        {
            "label": "English",
            "html": '<span data-align-id="a0" class="aligned-term">Gaul</span> is <span data-align-id="a1" class="aligned-term">divided</span>',
        },
    ]

    viewer = AlignViewer(
        title="Smoke Test",
        passages_json=json.dumps(passages),
        layout="horizontal",
        height="240px",
        width="100%",
    )

    assert viewer.title == "Smoke Test"
    assert "Latin" in viewer.passages_json
    assert viewer.layout == "horizontal"

    versions = [
        {
            "label": "Latin",
            "text": "Gallia est omnis divisa in partes tres",
            "alignments": [["Gallia"], ["est", "divisa"], ["partes"]],
        },
        {
            "label": "English",
            "text": "Gaul is divided into three parts",
            "alignments": [["Gaul"], ["is", "divided"], ["parts"]],
        },
    ]

    viewer2 = AlignViewer(
        title="Versions Format",
        versions=versions,
        layout="vertical",
    )

    converted = json.loads(viewer2.passages_json)
    assert len(converted) == 2
    assert converted[0]["label"] == "Latin"
    assert "data-align-id=\"align-0\"" in converted[0]["html"]
    assert viewer2.layout == "vertical"
    print("AlignViewer smoke test passed")


if __name__ == "__main__":
    main()

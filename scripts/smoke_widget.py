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
    print("AlignViewer smoke test passed")


if __name__ == "__main__":
    main()

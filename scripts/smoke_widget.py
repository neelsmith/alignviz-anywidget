from alignviz_anywidget import AlignViewer


def main() -> None:
    viewer = AlignViewer(
        title="Smoke Test",
        data="seq1 ACTG\nseq2 ACTA",
        height="240px",
        width="100%",
    )

    assert viewer.title == "Smoke Test"
    assert "seq1 ACTG" in viewer.data
    print("AlignViewer smoke test passed")


if __name__ == "__main__":
    main()

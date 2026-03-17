# alignviz-anywidget

An `anywidget` project scaffold for building alignment visualization widgets used in marimo notebooks.

This repo is organized similarly to `iiif-anywidget`:

- Python source in `src/alignviz_anywidget`
- JavaScript source in `js/src`
- Bundled widget assets in `src/alignviz_anywidget/static`
- Marimo examples in `marimo`
- Smoke scripts in `scripts`

## Project layout

```text
.
├── pyproject.toml
├── js/
│   ├── package.json
│   └── src/index.js
├── marimo/
│   └── demo.py
├── scripts/
│   └── smoke_widget.py
└── src/
	└── alignviz_anywidget/
		├── __init__.py
		├── widget.py
		└── static/
			└── index.js
```

## 1) Create and activate a Python environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

## 2) Install Python and JS dependencies

```bash
pip install -e ".[dev]"
cd js
npm install
cd ..
```

## 3) Build widget frontend assets

```bash
cd js
npm run build
cd ..
```

For active development in one terminal:

```bash
cd js
npm run dev
```

## 4) Run marimo demo

In another terminal:

```bash
source .venv/bin/activate
marimo run marimo/demo.py
```

## 5) Smoke test

```bash
python scripts/smoke_widget.py
```

## Packaging notes

- `hatch-jupyter-builder` runs the JS build during wheel/sdist builds.
- The static assets are included as shared data for notebook environments.

Build a package:

```bash
python -m pip install build
python -m build
```

function parsePassages(raw) {
  try {
    const parsed = JSON.parse(raw || "[]");
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function cssEscape(value) {
  if (window.CSS && typeof window.CSS.escape === "function") {
    return window.CSS.escape(value);
  }

  return String(value).replace(/[\\"']/g, "\\$&");
}

function normalizeLayout(layout) {
  const clean = `${layout || "vertical"}`.trim().toLowerCase();
  return clean === "horizontal" ? "horizontal" : "vertical";
}

function applyGroupLayoutStyles(group, layout, columnCount) {
  if (layout === "horizontal") {
    group.style.display = "grid";
    group.style.gridTemplateColumns = `repeat(${Math.max(columnCount, 1)}, minmax(0, 1fr))`;
    group.style.alignItems = "start";
    group.style.columnGap = "12px";
    group.style.rowGap = "12px";
    group.style.flexDirection = "";
    group.style.gap = "";
    return;
  }

  group.style.display = "flex";
  group.style.flexDirection = "column";
  group.style.gap = "12px";
  group.style.gridTemplateColumns = "";
  group.style.alignItems = "";
  group.style.columnGap = "";
  group.style.rowGap = "";
}

function injectStyles() {
  const styleId = "alignviz-anywidget-style-v2";
  if (document.getElementById(styleId)) {
    return;
  }

  const style = document.createElement("style");
  style.id = styleId;
  style.textContent = `
    .aw-root {
      width: 100%;
      border: 1px solid #d8e2ec;
      border-radius: 12px;
      background: linear-gradient(180deg, #fcfdff 0%, #f5f9ff 100%);
      overflow: hidden;
      font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      display: flex;
      flex-direction: column;
    }

    .aw-header {
      padding: 10px 14px;
      font-size: 0.95rem;
      font-weight: 650;
      color: #23374d;
      background: #ebf2fa;
      border-bottom: 1px solid #d8e2ec;
    }

    .aw-content {
      flex: 1;
      width: 100%;
      padding: 12px;
      overflow: auto;
    }

    .aw-group {
      display: flex;
      flex-direction: column;
      gap: 12px;
      width: 100%;
    }

    .aw-group.aw-horizontal {
      align-items: start;
    }

    .aw-column {
      flex: 1 1 0;
      min-width: 0;
      display: flex;
      flex-direction: column;
      max-width: 100%;
    }

    .aw-panel {
      background: #f9fbff;
      border: 1px solid #d5e2f0;
      border-radius: 10px;
      padding: 10px 12px;
      line-height: 1.7;
      color: #1d2a37;
      flex-shrink: 1;
      min-width: 0;
    }

    .aw-panel-title {
      font-weight: 650;
      margin-bottom: 8px;
      color: #304860;
      font-size: 0.86rem;
      letter-spacing: 0.02em;
      text-transform: uppercase;
    }

    .aw-panel-content {
      overflow-wrap: break-word;
      word-break: break-word;
      min-width: 0;
    }

    .aw-term,
    .aligned-term {
      border-radius: 4px;
      padding: 0 0.12em;
      transition: background-color 110ms ease-out, color 110ms ease-out;
      cursor: default;
    }

    .aw-empty {
      color: #5b6f82;
      font-size: 0.92rem;
      padding: 8px;
    }
  `;

  document.head.appendChild(style);
}

function makePanel(passage, index) {
  const column = document.createElement("div");
  column.className = "aw-column";

  const panel = document.createElement("section");
  panel.className = "aw-panel";

  const title = document.createElement("div");
  title.className = "aw-panel-title";
  title.textContent = passage.label || `Version ${index + 1}`;

  const content = document.createElement("div");
  content.className = "aw-panel-content";
  content.innerHTML = passage.html || "";

  panel.append(title, content);
  column.appendChild(panel);
  return column;
}

function collectAlignedTerms(root) {
  const terms = root.querySelectorAll("[data-align-id], [id], .aligned-term");
  const withId = [];
  for (const term of terms) {
    const id = term.getAttribute("data-align-id") || term.getAttribute("id");
    term.classList.add("aw-term");
    if (id) {
      withId.push({ id, el: term });
    }
  }
  return withId;
}

function attachHoverSync(root, withId, baseColor, hoverColor) {
  for (const { el } of withId) {
    el.style.backgroundColor = baseColor;
  }

  let activeId = null;

  const applyHighlight = (alignId) => {
    if (!alignId) {
      return;
    }

    const escaped = cssEscape(alignId);
    const matches = root.querySelectorAll(
      `[data-align-id="${escaped}"], [id="${escaped}"]`,
    );
    for (const item of matches) {
      item.style.backgroundColor = hoverColor;
    }
  };

  const clearHighlight = (alignId) => {
    if (!alignId) {
      return;
    }

    const escaped = cssEscape(alignId);
    const matches = root.querySelectorAll(
      `[data-align-id="${escaped}"], [id="${escaped}"]`,
    );
    for (const item of matches) {
      item.style.backgroundColor = baseColor;
    }
  };

  const onOver = (event) => {
    const target = event.target.closest("[data-align-id], [id]");
    if (!target || !root.contains(target)) {
      return;
    }

    const alignId = target.getAttribute("data-align-id") || target.getAttribute("id");
    if (!alignId || alignId === activeId) {
      return;
    }

    if (activeId) {
      clearHighlight(activeId);
    }
    activeId = alignId;
    applyHighlight(activeId);
  };

  const onOut = (event) => {
    const related = event.relatedTarget;
    if (related && root.contains(related)) {
      return;
    }

    if (activeId) {
      clearHighlight(activeId);
      activeId = null;
    }
  };

  root.addEventListener("mouseover", onOver);
  root.addEventListener("mouseleave", onOut);

  return () => {
    root.removeEventListener("mouseover", onOver);
    root.removeEventListener("mouseleave", onOut);
  };
}

function render({ model, el }) {
  injectStyles();

  el.style.width = "100%";
  el.style.display = "flex";

  const root = document.createElement("div");
  root.className = "aw-root";
  root.style.width = "100%";

  const header = document.createElement("div");
  header.className = "aw-header";

  const content = document.createElement("div");
  content.className = "aw-content";

  root.append(header, content);
  el.replaceChildren(root);

  let disposeHoverSync = () => {};

  const refresh = () => {
    disposeHoverSync();

    root.style.width = model.get("width") || "100%";
    root.style.height = model.get("height") || "420px";
    header.textContent = model.get("title") || "Aligned Text Explorer";

    const passages = parsePassages(model.get("passages_json"));
    const baseColor = model.get("base_highlight") || "#cfe8ff";
    const hoverColor = model.get("hover_highlight") || "#ffd166";
    const layout = normalizeLayout(model.get("layout"));

    if (!passages.length) {
      content.innerHTML = '<div class="aw-empty">No passages to display. Set passages_json to a non-empty JSON list.</div>';
      return;
    }

    const group = document.createElement("div");
    const className = layout === "horizontal" ? "aw-group aw-horizontal" : "aw-group";
    group.className = className;
    applyGroupLayoutStyles(group, layout, passages.length);

    passages.forEach((passage, index) => {
      group.appendChild(makePanel(passage, index));
    });

    content.replaceChildren(group);

    const withId = collectAlignedTerms(group);
    disposeHoverSync = attachHoverSync(group, withId, baseColor, hoverColor);
  };

  refresh();
  model.on("change:title", refresh);
  model.on("change:passages_json", refresh);
  model.on("change:layout", refresh);
  model.on("change:width", refresh);
  model.on("change:height", refresh);
  model.on("change:base_highlight", refresh);
  model.on("change:hover_highlight", refresh);
}

export default { render };

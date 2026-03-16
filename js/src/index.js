function parseRows(raw) {
  const lines = `${raw ?? ""}`
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.length > 0);

  return lines.map((line, idx) => {
    const [label, sequence] = line.split(/\s+/);
    return {
      id: idx + 1,
      label: label ?? `seq_${idx + 1}`,
      sequence: sequence ?? "",
    };
  });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderTable(rows) {
  const body = rows
    .map(
      (row) => `
        <tr>
          <td class="av-label">${escapeHtml(row.label)}</td>
          <td class="av-seq">${escapeHtml(row.sequence)}</td>
        </tr>
      `,
    )
    .join("");

  return `
    <table class="av-table">
      <thead>
        <tr>
          <th>Label</th>
          <th>Sequence</th>
        </tr>
      </thead>
      <tbody>${body}</tbody>
    </table>
  `;
}

function injectStyles() {
  if (document.getElementById("alignviz-anywidget-style")) {
    return;
  }

  const style = document.createElement("style");
  style.id = "alignviz-anywidget-style";
  style.textContent = `
    .av-root {
      border: 1px solid #ced7e0;
      border-radius: 10px;
      background: linear-gradient(180deg, #f9fbfd 0%, #f3f7fa 100%);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      font-family: ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .av-header {
      padding: 10px 14px;
      font-size: 0.95rem;
      font-weight: 600;
      color: #253445;
      background: #e8eff6;
      border-bottom: 1px solid #ced7e0;
    }

    .av-content {
      padding: 10px 14px;
      overflow: auto;
    }

    .av-table {
      border-collapse: collapse;
      width: 100%;
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.86rem;
    }

    .av-table th,
    .av-table td {
      text-align: left;
      padding: 6px 8px;
      border-bottom: 1px solid #d8e2ec;
      white-space: pre;
    }

    .av-table th {
      position: sticky;
      top: 0;
      background: #eef4fa;
      color: #30475d;
      z-index: 1;
    }

    .av-label {
      color: #1e3d59;
      min-width: 140px;
    }

    .av-seq {
      letter-spacing: 0.03em;
      color: #1d2731;
    }

    .av-empty {
      color: #5b6f82;
      font-size: 0.9rem;
      padding: 8px 0;
    }
  `;

  document.head.appendChild(style);
}

function render({ model, el }) {
  injectStyles();

  const root = document.createElement("div");
  root.className = "av-root";
  root.style.width = model.get("width") || "100%";
  root.style.height = model.get("height") || "360px";

  const header = document.createElement("div");
  header.className = "av-header";

  const content = document.createElement("div");
  content.className = "av-content";

  const refresh = () => {
    header.textContent = model.get("title") || "Alignment Viewer";
    const rows = parseRows(model.get("data"));

    if (!rows.length) {
      content.innerHTML = '<div class="av-empty">No alignment rows yet. Set the widget `data` trait.</div>';
      return;
    }

    content.innerHTML = renderTable(rows);
  };

  root.append(header, content);
  el.replaceChildren(root);

  refresh();
  model.on("change:title", refresh);
  model.on("change:data", refresh);
  model.on("change:width", refresh);
  model.on("change:height", refresh);
}

export default { render };

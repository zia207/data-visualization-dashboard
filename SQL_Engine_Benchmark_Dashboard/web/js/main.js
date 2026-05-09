(function () {
  "use strict";

  var yearEl = document.querySelector("[data-year]");
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");

  function closeNav() {
    if (!nav) return;
    nav.classList.remove("is-open");
    if (toggle) toggle.setAttribute("aria-expanded", "false");
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeNav);
    });

    window.matchMedia("(min-width: 641px)").addEventListener("change", function (e) {
      if (e.matches) closeNav();
    });
  }

  /* —— Streamlit-like preview: tabs, metrics, demo runs —— */
  var DATASET = {
    taxi: {
      rows: "50,000",
      cols: "10",
      mem: "~7",
      hint: "Synthetic trips · tpep_pickup_datetime, fare_amount, PULocationID…",
    },
    nys: {
      rows: "50,000",
      cols: "10",
      mem: "~6",
      hint: "NYS tax sample · County, NY_AGI_FDAP, Tax_Liability_Status…",
    },
    upload: {
      rows: "—",
      cols: "—",
      mem: "—",
      hint: "In Streamlit: upload CSV or Parquet in the sidebar first.",
    },
  };

  function setMetricsFromDataset(key) {
    var d = DATASET[key] || DATASET.taxi;
    var r = document.getElementById("metric-rows");
    var c = document.getElementById("metric-cols");
    var m = document.getElementById("metric-mem");
    var h = document.getElementById("dataset-hint");
    if (r) r.textContent = d.rows;
    if (c) c.textContent = d.cols;
    if (m) m.textContent = d.mem;
    if (h) h.textContent = d.hint;
  }

  function setEngineCount() {
    var checks = document.querySelectorAll(".eng-chk:checked");
    var el = document.getElementById("metric-engines");
    if (el) el.textContent = String(checks.length);
  }

  function initPreviewTabs() {
    var tablist = document.querySelector(".tab-pills[role='tablist']");
    if (!tablist) return;

    var tabs = tablist.querySelectorAll('[role="tab"]');
    var panels = document.querySelectorAll(".preview-panels .tab-panel");
    if (!tabs.length || !panels.length) return;

    function activate(key) {
      tabs.forEach(function (t) {
        var on = t.getAttribute("data-tab") === key;
        t.classList.toggle("is-active", on);
        t.setAttribute("aria-selected", on ? "true" : "false");
      });
      panels.forEach(function (p) {
        var on = p.getAttribute("data-panel") === key;
        p.classList.toggle("is-active", on);
      });
    }

    tabs.forEach(function (tab, idx) {
      tab.addEventListener("click", function () {
        activate(tab.getAttribute("data-tab"));
      });
      tab.addEventListener("keydown", function (e) {
        var keys = ["ArrowRight", "ArrowLeft", "Home", "End"];
        if (keys.indexOf(e.key) === -1) return;
        e.preventDefault();
        var next = idx;
        if (e.key === "ArrowRight") next = (idx + 1) % tabs.length;
        if (e.key === "ArrowLeft") next = (idx - 1 + tabs.length) % tabs.length;
        if (e.key === "Home") next = 0;
        if (e.key === "End") next = tabs.length - 1;
        tabs[next].focus();
        activate(tabs[next].getAttribute("data-tab"));
      });
    });
  }

  function initDatasetRadios() {
    document.querySelectorAll('input[name="dataset-demo"]').forEach(function (inp) {
      inp.addEventListener("change", function () {
        if (inp.checked) setMetricsFromDataset(inp.value);
      });
    });
  }

  function initEngineChecks() {
    document.querySelectorAll(".eng-chk").forEach(function (cb) {
      cb.addEventListener("change", setEngineCount);
    });
    setEngineCount();
  }

  function mockBenchOutput() {
    var n = document.querySelectorAll(".eng-chk:checked").length || 3;
    var lines = [];
    var engines = ["DuckDB", "Polars", "SQLAlchemy", "PySpark", "Dask-SQL", "psycopg2"];
    var checks = document.querySelectorAll(".eng-chk");
    var msBase = [14, 21, 38, 180, 62, 999];
    var j = 0;
    checks.forEach(function (cb, i) {
      if (!cb.checked) return;
      var ms = msBase[i] + Math.floor(Math.random() * 8);
      lines.push(
        engines[i] + ": <strong>ok</strong> · avg " + ms + " ms (×3 runs demo)"
      );
      j++;
    });
    if (!j) lines.push("Select at least one engine in the sidebar preview.");
    return lines.join("<br>");
  }

  function initDemoRuns() {
    var btnB = document.getElementById("btn-run-bench");
    var btnC = document.getElementById("btn-run-custom");
    var outB = document.getElementById("out-bench");
    var outC = document.getElementById("out-custom");
    if (btnB && outB) {
      btnB.addEventListener("click", function () {
        outB.innerHTML =
          '<span style="color:#6b9fc9;">[demo]</span> Template benchmark<br>' +
          mockBenchOutput();
        outB.classList.add("is-visible");
      });
    }
    if (btnC && outC) {
      btnC.addEventListener("click", function () {
        outC.innerHTML =
          '<span style="color:#6b9fc9;">[demo]</span> Custom query<br>' +
          "<strong>ok</strong> · 20 rows · DuckDB ~11 ms (static page mock)";
        outC.classList.add("is-visible");
      });
    }
  }

  initPreviewTabs();
  initDatasetRadios();
  initEngineChecks();
  initDemoRuns();
})();

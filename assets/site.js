// Theme: dark by default; the visitor's choice is remembered.
(function () {
  var root = document.documentElement;
  var btn = document.querySelector("[data-theme-toggle]");

  function apply(theme) {
    root.setAttribute("data-theme", theme);
    if (btn) {
      var label = theme === "dark" ? "Switch to light theme" : "Switch to dark theme";
      btn.setAttribute("aria-label", label);
      btn.setAttribute("title", label);
      btn.setAttribute("aria-pressed", theme === "light" ? "true" : "false");
    }
  }

  apply(root.getAttribute("data-theme") || "dark");

  if (btn) {
    btn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      apply(next);
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }

  // Highlight the section in view in the side nav.
  var links = document.querySelectorAll(".ident nav a");
  if (!links.length || !("IntersectionObserver" in window)) return;
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      links.forEach(function (a) { a.removeAttribute("aria-current"); });
      var a = byId[e.target.id];
      if (a) a.setAttribute("aria-current", "true");
    });
  }, { rootMargin: "-30% 0px -60% 0px" });
  Object.keys(byId).forEach(function (id) {
    var el = document.getElementById(id);
    if (el) obs.observe(el);
  });
})();

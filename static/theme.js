(function () {
  const root = document.documentElement;
  const btn = document.getElementById("theme-toggle");

  function isLight() {
    return root.getAttribute("data-theme") === "light";
  }

  function applyTheme(light) {
    if (light) {
      root.setAttribute("data-theme", "light");
      localStorage.setItem("theme", "light");
      btn.setAttribute("aria-label", "Switch to dark mode");
      btn.title = "Switch to dark mode";
    } else {
      root.removeAttribute("data-theme");
      localStorage.setItem("theme", "dark");
      btn.setAttribute("aria-label", "Switch to light mode");
      btn.title = "Switch to light mode";
    }
  }

  applyTheme(isLight());

  btn.addEventListener("click", function () {
    applyTheme(!isLight());
  });
})();

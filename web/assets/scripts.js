function changeMap(url) {
  document.getElementById("mapFrame").src = url;
}

const _ = (el) => [...document.querySelectorAll(el)];
_("[role=tab]")[0].setAttribute("aria-current", true);

_("[role=tab]").forEach((tab) => {
  tab.addEventListener("click", (e) => {
    e.preventDefault();

    !e.target.hasAttribute("aria-current")
      ? e.target.setAttribute("aria-current", true)
      : null;

    _("[role=tab]").forEach((t) => {
      t.hasAttribute("aria-current") && t != e.target
        ? t.removeAttribute("aria-current")
        : null;
    });
  });
});

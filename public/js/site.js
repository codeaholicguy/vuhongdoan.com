(function () {
  function closeNav() {
    document.body.classList.remove("responsive-nav-open");
  }

  function openNav() {
    document.body.classList.add("responsive-nav-open");
  }

  document.querySelectorAll(".js-hamburger").forEach(function (el) {
    el.addEventListener("click", openNav);
    el.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        openNav();
      }
    });
  });

  document.querySelectorAll(".js-close-responsive-nav").forEach(function (el) {
    el.addEventListener("click", closeNav);
  });

  document.querySelectorAll(".back-to-top a, .js-back-to-top").forEach(function (el) {
    el.addEventListener("click", function (e) {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });
})();

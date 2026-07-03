(function () {
  var cfg = window.SITE_CONFIG || {};
  var key = cfg.authKey || "portfolio_auth_v1";
  var form = document.getElementById("gate-form");
  var input = form.querySelector(".js-password");
  var button = form.querySelector(".js-btn-submit");
  var error = document.querySelector(".js-gate-error");
  var params = new URLSearchParams(window.location.search);
  var returnTo = params.get("r") || "/work/";

  if (sessionStorage.getItem(key) === "1") {
    window.location.replace(returnTo);
    return;
  }

  function setButtonState() {
    button.disabled = !input.value.trim();
  }

  async function hashPassword(value) {
    var buf = await crypto.subtle.digest(
      "SHA-256",
      new TextEncoder().encode(value)
    );
    return Array.from(new Uint8Array(buf))
      .map(function (b) {
        return b.toString(16).padStart(2, "0");
      })
      .join("");
  }

  input.addEventListener("input", setButtonState);
  setButtonState();

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    error.hidden = true;
    var digest = await hashPassword(input.value);
    if (digest === cfg.passwordHash) {
      sessionStorage.setItem(key, "1");
      window.location.replace(returnTo);
      return;
    }
    error.hidden = false;
    input.select();
  });
})();

(function () {
  var cfg = window.SITE_CONFIG || {};
  var key = cfg.authKey || "portfolio_auth_v1";

  if (sessionStorage.getItem(key) === "1") {
    return;
  }

  var redirect = encodeURIComponent(
    window.location.pathname + window.location.search + window.location.hash
  );
  window.location.replace("gate.html?r=" + redirect);
})();

/* Built by Compo: small behaviours. No tracking, no cookies.
   The only thing saved in the browser is the "pause animations" choice. */
(function () {
  var root = document.documentElement;
  root.classList.remove("no-js"); root.classList.add("js");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ----- Pause / play all movement ----- */
  var paused = reduce;
  try { if (localStorage.getItem("bbc-motion") === "off") paused = true; } catch (e) {}
  var motionBtn = document.querySelector(".motion-btn");
  function setPaused(p) {
    paused = p; root.classList.toggle("paused", p); window.BBC_PAUSED = p;
    if (motionBtn) { motionBtn.setAttribute("aria-pressed", String(p)); motionBtn.setAttribute("aria-label", p ? "Play animations" : "Pause animations"); }
  }
  setPaused(paused);
  if (motionBtn) motionBtn.addEventListener("click", function () {
    setPaused(!paused);
    try { localStorage.setItem("bbc-motion", paused ? "off" : "on"); } catch (e) {}
  });

  /* ----- Mobile menu ----- */
  var menuBtn = document.querySelector(".menu-btn"), nav = document.getElementById("nav");
  if (menuBtn && nav) {
    var closeMenu = function () { nav.classList.remove("open"); root.classList.remove("menu-open"); menuBtn.setAttribute("aria-expanded", "false"); menuBtn.textContent = "Menu"; };
    menuBtn.addEventListener("click", function () {
      var open = !nav.classList.contains("open");
      if (!open) return closeMenu();
      nav.classList.add("open"); root.classList.add("menu-open"); menuBtn.setAttribute("aria-expanded", "true"); menuBtn.textContent = "Close";
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav.classList.contains("open")) { closeMenu(); menuBtn.focus(); } });
  }

  /* ----- Reveal on scroll ----- */
  var items = document.querySelectorAll(".reveal, .wipe");
  if (!("IntersectionObserver" in window) || reduce) { items.forEach(function (el) { el.classList.add("in"); }); }
  else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in"); en.target.querySelectorAll(":scope > .wipe").forEach(function (w) { w.classList.add("in"); });
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    items.forEach(function (el) { io.observe(el.classList.contains("wipe") ? el.parentElement : el); });
  }

  /* ----- Ribbons drift a little further as you scroll ----- */
  var shifts = document.querySelectorAll(".ribbon-shift");
  if (shifts.length && !reduce) {
    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking || paused) return; ticking = true;
      requestAnimationFrame(function () {
        var y = window.scrollY;
        shifts.forEach(function (el) { el.style.setProperty("--shift", (y * parseFloat(el.dataset.speed || "-0.25")).toFixed(1) + "px"); });
        ticking = false;
      });
    }, { passive: true });
  }

  /* ----- Work slider: drifts sideways, can be swiped or dragged ----- */
  document.querySelectorAll(".slider").forEach(function (sl) {
    var track = sl.querySelector(".slider-track"); if (!track) return;
    var originals = Array.prototype.slice.call(track.children);
    originals.forEach(function (c) {              // a second copy so the row can loop
      var k = c.cloneNode(true); k.setAttribute("aria-hidden", "true"); k.setAttribute("tabindex", "-1");
      k.querySelectorAll("a").forEach(function (a) { a.setAttribute("tabindex", "-1"); });
      track.appendChild(k);
    });
    var hold = false, down = false, startX = 0, startL = 0, moved = 0, pos = 0, acc = 0;
    function half() { return (track.scrollWidth - parseFloat(getComputedStyle(track).paddingLeft) - parseFloat(getComputedStyle(track).paddingRight) + parseFloat(getComputedStyle(track).columnGap || 0)) / 2; }
    function wrap() { var h = half(); if (h > 0) { if (sl.scrollLeft >= h) sl.scrollLeft -= h; else if (sl.scrollLeft <= 0 && down) sl.scrollLeft += h; } }
    sl.addEventListener("pointerenter", function (e) { if (e.pointerType === "mouse") hold = true; });
    sl.addEventListener("pointerleave", function () { hold = false; down = false; sl.classList.remove("drag"); });
    sl.addEventListener("focusin", function () { hold = true; });
    sl.addEventListener("focusout", function () { hold = false; });
    sl.addEventListener("touchstart", function () { hold = true; }, { passive: true });
    sl.addEventListener("touchend", function () { setTimeout(function () { hold = false; pos = sl.scrollLeft; }, 2500); }, { passive: true });
    sl.addEventListener("pointerdown", function (e) { if (e.pointerType !== "mouse") return; down = true; moved = 0; startX = e.clientX; startL = sl.scrollLeft; sl.classList.add("drag"); });
    window.addEventListener("pointerup", function () { down = false; sl.classList.remove("drag"); pos = sl.scrollLeft; });
    sl.addEventListener("pointermove", function (e) { if (!down) return; var dx = e.clientX - startX; moved = Math.max(moved, Math.abs(dx)); sl.scrollLeft = startL - dx; wrap(); });
    sl.addEventListener("click", function (e) { if (moved > 8) { e.preventDefault(); e.stopPropagation(); } }, true);
    sl.addEventListener("dragstart", function (e) { e.preventDefault(); });
    var visible = true;
    if ("IntersectionObserver" in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }).observe(sl);
    var last = 0;
    function step(t) {
      var dt = Math.min(50, t - (last || t)); last = t;
      if (!paused && !hold && !down && visible) { acc += dt * 0.045; var whole = Math.floor(acc); if (whole > 0) { sl.scrollLeft += whole; acc -= whole; wrap(); } }
      requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  });

  /* ----- Testimonial card deck ----- */
  document.querySelectorAll(".deck-wrap").forEach(function (w) {
    var cards = Array.prototype.slice.call(w.querySelectorAll(".deck > li")), btn = w.querySelector(".deck-next"), count = w.querySelector(".deck-count");
    if (cards.length < 2 || !btn) { if (btn) btn.hidden = true; return; }
    var top = 0, busy = false;
    function layout() {
      cards.forEach(function (c, i) {
        var p = (i - top + cards.length) % cards.length;
        c.dataset.pos = p > 2 ? "2" : String(p);
        c.setAttribute("aria-hidden", String(p !== 0));
      });
      if (count) count.textContent = (top + 1) + " / " + cards.length;
    }
    layout();
    btn.addEventListener("click", function () {
      if (busy) return; busy = true;
      var out = cards[top]; out.dataset.pos = "out";
      setTimeout(function () { top = (top + 1) % cards.length; layout(); busy = false; }, reduce ? 0 : 380);
    });
  });

  /* ----- Contact: builds an email or WhatsApp message, then opens the visitor's own app ----- */
  var form = document.getElementById("project-form");
  if (form) {
    var out = document.getElementById("form-out"), go = document.getElementById("form-go");
    function how() { var r = form.querySelector('input[name="how"]:checked'); return r ? r.value : "email"; }
    function label() { go.firstChild.textContent = how() === "whatsapp" ? "Open WhatsApp " : "Open my email app "; }
    form.querySelectorAll('input[name="how"]').forEach(function (r) { r.addEventListener("change", label); });
    label();
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var f = form.first.value.trim(), l = form.last.value.trim(), b = form.business.value.trim();
      if (!f || !l) { out.textContent = "Please add your first and last name."; out.className = "err"; (f ? form.last : form.first).focus(); return; }
      var msg = "Hi Luke,\n\nI'm " + f + " " + l + (b ? " from " + b : "") + ". I'd like to talk about a website.\n\n";
      var url = how() === "whatsapp"
        ? "https://wa.me/" + form.dataset.wa + "?text=" + encodeURIComponent(msg)
        : "mailto:" + form.dataset.email + "?subject=" + encodeURIComponent("Website enquiry" + (b ? ": " + b : "")) + "&body=" + encodeURIComponent(msg);
      out.className = "small";
      out.textContent = how() === "whatsapp" ? "Opening WhatsApp with your message ready to send. Nothing has been sent yet." : "Opening your email app with your message ready to send. Nothing has been sent yet.";
      if (how() === "whatsapp") window.open(url, "_blank", "noopener") || (location.href = url); else location.href = url;
    });
  }

  /* ----- Copy email button ----- */
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var t = b.dataset.copy, done = function () { var o = b.textContent; b.textContent = "Copied"; setTimeout(function () { b.textContent = o; }, 1600); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(done, function () {});
    });
  });
})();

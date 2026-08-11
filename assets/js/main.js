/* ==========================================================================
   DS Comfort — main.js
   Geen dependencies. Alles progressive enhancement: zonder JS blijft de
   volledige site leesbaar en bruikbaar.
   ========================================================================== */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------------
     1. Header condenseert bij scrollen
     ------------------------------------------------------------------ */
  var header = document.querySelector(".site-header");
  if (header) {
    var lastStuck = null;
    var onScroll = function () {
      var stuck = window.scrollY > 8;
      if (stuck !== lastStuck) {
        header.classList.toggle("is-stuck", stuck);
        lastStuck = stuck;
      }
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ------------------------------------------------------------------
     2. Mobiele navigatie
     ------------------------------------------------------------------ */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav");
  if (toggle && nav) {
    var scrim = document.createElement("div");
    scrim.className = "nav-scrim";
    document.body.appendChild(scrim);

    var setNav = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
      scrim.classList.toggle("is-visible", open);
      document.documentElement.style.overflow = open ? "hidden" : "";
      toggle.setAttribute("aria-label", open ? "Menu sluiten" : "Menu openen");
    };

    toggle.addEventListener("click", function () {
      setNav(toggle.getAttribute("aria-expanded") !== "true");
    });
    scrim.addEventListener("click", function () { setNav(false); });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setNav(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setNav(false);
        toggle.focus();
      }
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 1040 && toggle.getAttribute("aria-expanded") === "true") {
        setNav(false);
      }
    });
  }

  /* ------------------------------------------------------------------
     3. Scroll-reveal
     ------------------------------------------------------------------ */
  var revealables = document.querySelectorAll("[data-reveal]");
  if (revealables.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      revealables.forEach(function (el) { el.classList.add("is-revealed"); });
    } else {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-revealed");
          observer.unobserve(entry.target);
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

      revealables.forEach(function (el, i) {
        // Trapsgewijze vertraging binnen dezelfde groep
        var group = el.closest("[data-reveal-group]");
        if (group) {
          var siblings = Array.prototype.slice.call(group.querySelectorAll("[data-reveal]"));
          el.style.setProperty("--reveal-delay", Math.min(siblings.indexOf(el), 6) * 80 + "ms");
        }
        observer.observe(el);
      });
    }
  }

  /* ------------------------------------------------------------------
     4. FAQ-accordeon
     ------------------------------------------------------------------ */
  document.querySelectorAll(".faq__q").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".faq__item");
      var open = btn.getAttribute("aria-expanded") === "true";
      // Eén tegelijk open houden geeft een rustiger beeld
      if (!open) {
        var wrap = btn.closest(".faq");
        wrap.querySelectorAll(".faq__q[aria-expanded='true']").forEach(function (other) {
          other.setAttribute("aria-expanded", "false");
          other.closest(".faq__item").classList.remove("is-open");
        });
      }
      btn.setAttribute("aria-expanded", String(!open));
      item.classList.toggle("is-open", !open);
    });
  });

  /* ------------------------------------------------------------------
     5. Actieve navigatie markeren
     ------------------------------------------------------------------ */
  var path = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav__link").forEach(function (link) {
    var href = link.getAttribute("href");
    if (!href || href.charAt(0) === "#") return;
    if (href === path) link.setAttribute("aria-current", "page");
  });

  /* ------------------------------------------------------------------
     6. Formuliervalidatie + verzending
     ------------------------------------------------------------------
     Statische site: er is geen server. Het formulier post naar het
     endpoint in het action-attribuut (bv. Formspree). Zolang dat een
     placeholder bevat, valt het terug op een vooringevulde e-mail.
     Zie README.md, sectie "Formulier aansluiten".
     ------------------------------------------------------------------ */
  document.querySelectorAll("form[data-validate]").forEach(function (form) {
    var status = form.querySelector(".form-status");

    var showError = function (field, message) {
      var box = field.closest(".field");
      var err = box && box.querySelector(".field__error");
      field.setAttribute("aria-invalid", "true");
      if (err) {
        err.textContent = message;
        err.classList.add("is-visible");
      }
    };

    var clearError = function (field) {
      var box = field.closest(".field");
      var err = box && box.querySelector(".field__error");
      field.removeAttribute("aria-invalid");
      if (err) err.classList.remove("is-visible");
    };

    var validateField = function (field) {
      var value = (field.value || "").trim();
      if (field.hasAttribute("required") && !value) {
        showError(field, "Dit veld is verplicht.");
        return false;
      }
      if (field.type === "email" && value && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
        showError(field, "Vul een geldig e-mailadres in.");
        return false;
      }
      if (field.type === "tel" && value && value.replace(/[^\d]/g, "").length < 8) {
        showError(field, "Vul een geldig telefoonnummer in.");
        return false;
      }
      clearError(field);
      return true;
    };

    form.querySelectorAll("input, textarea, select").forEach(function (field) {
      field.addEventListener("blur", function () { validateField(field); });
      field.addEventListener("input", function () {
        if (field.getAttribute("aria-invalid") === "true") validateField(field);
      });
    });

    var setStatus = function (type, message) {
      if (!status) return;
      status.className = "form-status is-visible form-status--" + type;
      status.textContent = message;
    };

    form.addEventListener("submit", function (e) {
      var fields = Array.prototype.slice.call(
        form.querySelectorAll("input[required], textarea[required], select[required]")
      );
      var firstBad = null;
      fields.forEach(function (field) {
        if (!validateField(field) && !firstBad) firstBad = field;
      });

      // Honeypot: bots vullen dit onzichtbare veld in.
      var honey = form.querySelector('input[name="_gotcha"]');
      if (honey && honey.value) { e.preventDefault(); return; }

      if (firstBad) {
        e.preventDefault();
        setStatus("err", "Enkele velden zijn nog niet correct ingevuld.");
        firstBad.focus();
        firstBad.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
        return;
      }

      var action = form.getAttribute("action") || "";
      var isPlaceholder = action.indexOf("VERVANG") !== -1 || action === "" || action === "#";

      if (isPlaceholder) {
        // Fallback zolang het endpoint niet is aangesloten: mailto met inhoud.
        e.preventDefault();
        var get = function (name) {
          var el = form.querySelector('[name="' + name + '"]');
          if (!el) return "";
          if (el.type === "radio") {
            var checked = form.querySelector('[name="' + name + '"]:checked');
            return checked ? checked.value : "";
          }
          return el.value || "";
        };
        var lines = [
          "Naam: " + get("naam"),
          "E-mail: " + get("email"),
          "Telefoon: " + get("telefoon"),
          "Gemeente: " + get("gemeente"),
          "Type woning: " + get("woning"),
          "Interesse: " + get("onderwerp"),
          "",
          get("bericht")
        ];
        setStatus("ok", "Uw e-mailprogramma wordt geopend met de ingevulde gegevens.");
        window.location.href =
          "mailto:info@dscomfort.be" +
          "?subject=" + encodeURIComponent("Offerteaanvraag via website — " + get("naam")) +
          "&body=" + encodeURIComponent(lines.join("\n"));
        return;
      }

      // Echt endpoint: async versturen zodat de bezoeker op de pagina blijft.
      e.preventDefault();
      var submitBtn = form.querySelector('button[type="submit"]');
      var originalLabel = submitBtn ? submitBtn.textContent : "";
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = "Versturen…"; }
      setStatus("ok", "Bezig met versturen…");

      fetch(action, {
        method: form.getAttribute("method") || "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" }
      })
        .then(function (res) {
          if (!res.ok) throw new Error("Netwerkfout");
          form.reset();
          setStatus("ok", "Bedankt. Uw aanvraag is verstuurd — u hoort snel van ons.");
        })
        .catch(function () {
          setStatus("err", "Verzenden lukte niet. Bel ons gerust op 0485 79 66 84 of mail naar info@dscomfort.be.");
        })
        .finally(function () {
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = originalLabel; }
        });
    });
  });

  /* ------------------------------------------------------------------
     7. Huidig jaartal in de footer
     ------------------------------------------------------------------ */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();

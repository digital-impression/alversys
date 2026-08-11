/* Veerle Borremans — advocaat & bemiddelaar
   Minimale progressive enhancement. Geen afhankelijkheden, geen cookies,
   geen externe verzoeken. De site werkt volledig zonder dit bestand. */

(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- 1. Vaste kop krijgt achtergrond zodra er gescrold wordt ---------- */
  var header = document.querySelector('.site-header');
  if (header) {
    var ticking = false;
    var setStuck = function () {
      header.classList.toggle('is-stuck', window.scrollY > 24);
      ticking = false;
    };
    setStuck();
    window.addEventListener(
      'scroll',
      function () {
        if (!ticking) {
          window.requestAnimationFrame(setStuck);
          ticking = true;
        }
      },
      { passive: true }
    );
  }

  /* ---- 2. Navigatie op klein scherm ------------------------------------ */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    var closeNav = function () {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    };

    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    nav.addEventListener('click', function (event) {
      if (event.target.closest('a')) closeNav();
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && nav.classList.contains('is-open')) {
        closeNav();
        toggle.focus();
      }
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 992) closeNav();
    });
  }

  /* ---- 3. Rustig in beeld schuiven ------------------------------------- */
  var targets = document.querySelectorAll('.reveal');
  if (!targets.length) return;

  if (reduced || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(targets, function (el) {
      el.classList.add('is-visible');
    });
    return;
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
  );

  Array.prototype.forEach.call(targets, function (el) {
    observer.observe(el);
  });
})();

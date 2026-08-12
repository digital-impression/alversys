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

  /* ---- 3. Beeldband met lichte parallax --------------------------------- */
  var bands = document.querySelectorAll('[data-parallax]');
  if (bands.length && !reduced && 'IntersectionObserver' in window) {
    var actief = [];
    var bandObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            if (actief.indexOf(entry.target) === -1) actief.push(entry.target);
          } else {
            actief = actief.filter(function (b) { return b !== entry.target; });
          }
        });
      },
      { rootMargin: '10% 0px' }
    );
    Array.prototype.forEach.call(bands, function (b) { bandObserver.observe(b); });

    var bezig = false;
    var verschuif = function () {
      actief.forEach(function (band) {
        var bg = band.querySelector('.band__bg');
        if (!bg) return;
        var rect = band.getBoundingClientRect();
        var midden = rect.top + rect.height / 2 - window.innerHeight / 2;
        // De foto steekt 12% boven en onder de band uit; verder verschuiven
        // dan dat zou een gat laten vallen.
        var grens = rect.height * 0.11;
        var verzet = Math.max(-grens, Math.min(grens, -midden * 0.06));
        bg.style.transform = 'translate3d(0,' + verzet.toFixed(1) + 'px,0)';
      });
      bezig = false;
    };
    window.addEventListener(
      'scroll',
      function () {
        if (!bezig) {
          window.requestAnimationFrame(verschuif);
          bezig = true;
        }
      },
      { passive: true }
    );
    verschuif();
  }

  /* ---- 4. Rustig in beeld schuiven ------------------------------------- */
  var targets = document.querySelectorAll('.reveal, .media');
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

/* Jacobs Law — site behaviour.
   Vanilla, no dependencies. Progressive enhancement only:
   the site is fully readable and navigable with JS disabled. */

(function () {
  'use strict';

  document.documentElement.classList.remove('no-js');

  /* --- Header: solid state once scrolled past the hero ------------------ */
  var header = document.querySelector('.header');
  if (header) {
    var solidAt = 24;
    var ticking = false;

    var applyHeaderState = function () {
      header.classList.toggle('is-solid', window.scrollY > solidAt);
      ticking = false;
    };

    applyHeaderState();
    window.addEventListener('scroll', function () {
      if (!ticking) {
        window.requestAnimationFrame(applyHeaderState);
        ticking = true;
      }
    }, { passive: true });
  }

  /* --- Mobile drawer ---------------------------------------------------- */
  var burger = document.querySelector('.burger');
  var drawer = document.getElementById('drawer');

  if (burger && drawer) {
    var setDrawer = function (open) {
      burger.setAttribute('aria-expanded', String(open));
      drawer.classList.toggle('is-open', open);
      drawer.setAttribute('aria-hidden', String(!open));
      document.body.classList.toggle('is-locked', open);
    };

    burger.addEventListener('click', function () {
      setDrawer(burger.getAttribute('aria-expanded') !== 'true');
    });

    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a')) setDrawer(false);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && burger.getAttribute('aria-expanded') === 'true') {
        setDrawer(false);
        burger.focus();
      }
    });

    // Close the drawer if the viewport grows past the mobile breakpoint.
    var desktop = window.matchMedia('(min-width: 1060px)');
    var onBreakpoint = function (e) { if (e.matches) setDrawer(false); };
    if (desktop.addEventListener) desktop.addEventListener('change', onBreakpoint);
    else if (desktop.addListener) desktop.addListener(onBreakpoint);
  }

  /* --- Scroll reveal ---------------------------------------------------- */
  var reveals = document.querySelectorAll('.reveal');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!reveals.length) return;

  if (reduced || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(reveals, function (el) { el.classList.add('is-in'); });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-in');
        observer.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -9% 0px', threshold: 0.06 });

  Array.prototype.forEach.call(reveals, function (el) { observer.observe(el); });
})();

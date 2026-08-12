/* Veerle Borremans, advocaat en bemiddelaar
   Minimale progressive enhancement: alleen de navigatie op kleine schermen.
   Geen scroll-animaties, geen parallax. Bij dit onderwerp is terughoudende
   beweging zelf een ontwerpkeuze. De site werkt volledig zonder dit bestand. */

(function () {
  'use strict';

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (!toggle || !nav) return;

  function sluit() {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  }

  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  nav.addEventListener('click', function (event) {
    if (event.target.closest('a')) sluit();
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && nav.classList.contains('is-open')) {
      sluit();
      toggle.focus();
    }
  });

  window.addEventListener('resize', function () {
    if (window.innerWidth > 980) sluit();
  });
})();

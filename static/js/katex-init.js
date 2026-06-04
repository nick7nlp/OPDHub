/**
 * KaTeX renderer for OPD paper cards.
 *
 * Walks every .paper-detail-eq element, reads raw LaTeX from its data-tex
 * attribute, and renders it in display mode. If a paper's LaTeX fails to
 * parse (truncated, unbalanced braces, unsupported macro), the whole
 * .detail-equation block is removed so the card stays clean rather than
 * showing a red error or raw source.
 *
 * The script delays the first render by a tick so it runs after KaTeX itself
 * has finished loading from CDN (the KaTeX <script> is tagged `defer`, but
 * this file is also deferred, and module ordering between two defer scripts
 * is browser-stable). If `katex` is not yet defined we retry once.
 */
(function () {
  'use strict';

  function renderAll() {
    if (typeof katex === 'undefined') {
      // KaTeX still loading — try again on next paint.
      requestAnimationFrame(renderAll);
      return;
    }
    var els = document.querySelectorAll('.paper-detail-eq[data-tex]');
    var rendered = 0;
    var failed = 0;
    els.forEach(function (el) {
      var tex = el.getAttribute('data-tex');
      if (!tex) return;
      try {
        katex.render(tex, el, {
          displayMode: true,
          throwOnError: true,
          strict: 'ignore',
          maxSize: 25,
          maxExpand: 1000,
          trust: false,
          // Common OPD-paper macros that KaTeX doesn't ship with by default.
          macros: {
            '\\E': '\\mathbb{E}',
            '\\R': '\\mathbb{R}',
            '\\KL': '\\mathrm{KL}',
            '\\softmax': '\\mathrm{softmax}'
          }
        });
        rendered++;
      } catch (e) {
        // Hide the entire equation block on parse failure.
        var block = el.closest('.detail-equation');
        if (block && block.parentNode) {
          block.parentNode.removeChild(block);
        }
        failed++;
      }
    });
    if (window.console && console.debug) {
      console.debug('[katex] rendered ' + rendered + ' / failed ' + failed +
                    ' (of ' + els.length + ' equations)');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderAll);
  } else {
    renderAll();
  }
})();

// BibTeX copy-to-clipboard widget.
document.addEventListener('DOMContentLoaded', function () {
  const btn   = document.getElementById('bibtex-copy');
  const block = document.getElementById('bibtex-block');
  if (!btn || !block) return;

  btn.addEventListener('click', async () => {
    const text = block.innerText;
    try {
      await navigator.clipboard.writeText(text);
    } catch (_) {
      // fallback for non-https / older browsers
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); } catch (_) {}
      document.body.removeChild(ta);
    }
    btn.classList.add('is-copied');
    const label = btn.querySelector('.copy-label');
    const old = label ? label.textContent : '';
    if (label) label.textContent = 'copied';
    setTimeout(() => {
      btn.classList.remove('is-copied');
      if (label) label.textContent = old;
    }, 1400);
  });
});

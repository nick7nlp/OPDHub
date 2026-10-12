// The complete collection is rendered in HTML; JavaScript adds search and citation tools.
(function () {
  'use strict';

  const scriptVersion = new URL(document.currentScript.src).searchParams.get('v') || '';
  const PAPERS_URL = `static/data/papers.json?v=${encodeURIComponent(scriptVersion)}`;
  const paperToCard = new Map();
  const active = { section: new Set(), mechanism: new Set(), year: new Set() };
  let allPapers = [];
  let fuse = null;
  let searchQuery = '';
  let statusTimer;

  function debounce(fn, ms) {
    let timer;
    return (...args) => { clearTimeout(timer); timer = setTimeout(() => fn(...args), ms); };
  }

  function buildIndex(papers) {
    allPapers = papers;
    fuse = typeof Fuse === 'function' ? new Fuse(papers, {
      keys: [
        { name: 'title', weight: 3 },
        { name: 'authors', weight: 2 },
        { name: 'description', weight: 2 },
        { name: 'objective', weight: 1 },
        { name: 'mechanism', weight: 1 },
        { name: 'paper_id', weight: 1 },
        { name: 'arxiv_id', weight: 1 }
      ],
      threshold: 0.35,
      ignoreLocation: true,
      minMatchCharLength: 2
    }) : null;
  }

  function applyFilter() {
    const query = searchQuery.trim().toLocaleLowerCase();
    // An exact identifier should not be diluted by fuzzy matches to nearby IDs.
    const exact = query ? allPapers.filter(p =>
      [p.paper_id, p.arxiv_id].some(id => String(id || '').toLocaleLowerCase() === query.replace(/v\d+$/, ''))
    ) : [];
    let candidates;
    if (exact.length) {
      candidates = new Set(exact.map(p => p.paper_id));
    } else if (query && fuse) {
      candidates = new Set(fuse.search(query).map(result => result.item.paper_id));
    } else {
      candidates = new Set(allPapers.filter(p => !query ||
        [p.title, ...(p.authors || []), p.description, p.objective, p.mechanism, p.paper_id, p.arxiv_id || '']
          .join(' ').toLocaleLowerCase().includes(query)
      ).map(p => p.paper_id));
    }
    const filtered = allPapers.filter(p => {
      if (!candidates.has(p.paper_id)) return false;
      if (active.section.size && !active.section.has(p.home)) return false;
      const mechanisms = Array.isArray(p.mechanism) ? p.mechanism : [p.mechanism];
      if (active.mechanism.size && !mechanisms.some(value => active.mechanism.has(value))) return false;
      return !active.year.size || active.year.has(String(p.year));
    });
    const visible = new Set(filtered.map(p => p.paper_id));
    paperToCard.forEach((card, id) => card.classList.toggle('is-hidden', !visible.has(id)));
    document.querySelectorAll('.paper-section-group').forEach(group => {
      const count = group.querySelectorAll('.paper-card:not(.is-hidden)').length;
      group.classList.toggle('is-hidden', count === 0);
      group.querySelector('.section-total').textContent = `${count} ${count === 1 ? 'paper' : 'papers'}`;
    });
    document.getElementById('visible-count').textContent = filtered.length === allPapers.length
      ? `${allPapers.length} papers` : `${filtered.length} of ${allPapers.length} papers`;
    document.getElementById('empty-state').classList.toggle('is-hidden', filtered.length > 0);
    document.getElementById('export-bibtex').disabled = filtered.length === 0;
    document.querySelectorAll('.topic-link').forEach(link => {
      const selected = active.section.size ? active.section.has(link.dataset.topic) : !link.dataset.topic;
      link.classList.toggle('is-active', selected);
      if (selected) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });
  }

  function resetFilters() {
    Object.values(active).forEach(values => values.clear());
    searchQuery = '';
    document.getElementById('search-input').value = '';
    document.querySelectorAll('.chip').forEach(chip => {
      chip.classList.remove('is-active');
      chip.setAttribute('aria-pressed', 'false');
    });
    applyFilter();
  }

  function chooseTopic(topic, reset = false) {
    if (reset) resetFilters();
    active.section.clear();
    if (topic) active.section.add(topic);
    applyFilter();
    document.querySelector('.search-tools').scrollIntoView({ block: 'start' });
  }

  function bindFilters() {
    document.querySelectorAll('.chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const group = chip.parentElement.dataset.filterGroup;
        const value = chip.dataset.value;
        if (!active[group]) return;
        if (active[group].has(value)) active[group].delete(value);
        else active[group].add(value);
        chip.classList.toggle('is-active', active[group].has(value));
        chip.setAttribute('aria-pressed', String(active[group].has(value)));
        applyFilter();
      });
    });
    document.querySelectorAll('.topic-link').forEach(link => {
      link.addEventListener('click', event => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        chooseTopic(link.dataset.topic);
      });
    });
    document.querySelectorAll('.reading-paths a').forEach(link => {
      link.addEventListener('click', event => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        chooseTopic(link.hash.replace('#topic-', ''), true);
      });
    });
    document.getElementById('clear-filters').addEventListener('click', resetFilters);
    const input = document.getElementById('search-input');
    input.addEventListener('input', debounce(() => {
      searchQuery = input.value;
      applyFilter();
    }, 120));
    document.addEventListener('keydown', event => {
      const target = event.target;
      if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey &&
          !target.matches('input, textarea, select, [contenteditable="true"]') &&
          !document.getElementById('citation-dialog').open) {
        event.preventDefault();
        input.focus();
      }
    });
  }

  function announce(message) {
    const status = document.getElementById('copy-status');
    clearTimeout(statusTimer);
    status.textContent = message;
    status.classList.add('is-visible');
    statusTimer = setTimeout(() => status.classList.remove('is-visible'), 2000);
  }

  function legacyCopy(text) {
    const previousFocus = document.activeElement;
    const area = document.createElement('textarea');
    area.value = text;
    area.setAttribute('aria-label', 'Citation to copy');
    Object.assign(area.style, { position: 'fixed', opacity: '0', left: '-9999px' });
    document.body.appendChild(area);
    area.select();
    let copied = false;
    try { copied = document.execCommand('copy'); } catch (_) { /* Use the readable dialog below. */ }
    area.remove();
    if (previousFocus) previousFocus.focus({ preventScroll: true });
    return copied;
  }

  function showCitation(text) {
    const dialog = document.getElementById('citation-dialog');
    const area = document.getElementById('citation-text');
    area.value = text;
    dialog.showModal();
    area.focus();
    area.select();
  }

  function bindCitations() {
    document.querySelectorAll('.badge-cite').forEach(button => {
      button.addEventListener('click', async () => {
        const bib = button.closest('.paper-card').dataset.bibtex;
        if (!bib) return;
        let copied = false;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          try { await navigator.clipboard.writeText(bib); copied = true; } catch (_) { /* Try legacy copy. */ }
        }
        if (!copied) copied = legacyCopy(bib);
        if (!copied) { showCitation(bib); return; }
        announce('Citation copied');
        button.classList.add('is-copied');
        button.querySelector('.cite-label').textContent = 'Copied';
        setTimeout(() => {
          button.classList.remove('is-copied');
          button.querySelector('.cite-label').textContent = 'Cite';
        }, 1600);
      });
    });
    document.getElementById('export-bibtex').addEventListener('click', () => {
      const bibs = [...document.querySelectorAll('.paper-card:not(.is-hidden)')].map(card => card.dataset.bibtex).filter(Boolean);
      if (!bibs.length) return;
      const blob = new Blob([bibs.join('\n\n') + '\n'], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'opd-papers.bib';
      document.body.appendChild(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      announce(`Exported ${bibs.length} ${bibs.length === 1 ? 'citation' : 'citations'}`);
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    const embedded = [];
    document.querySelectorAll('.paper-card').forEach(card => {
      paperToCard.set(card.dataset.paperId, card);
      embedded.push(JSON.parse(card.dataset.paper));
    });
    // Start from the static records immediately, including offline and slow-network visits.
    buildIndex(embedded);
    bindFilters();
    bindCitations();
    document.body.classList.add('js-ready');
    applyFilter();
    fetch(PAPERS_URL).then(response => {
      if (!response.ok) throw new Error(`Catalog HTTP ${response.status}`);
      return response.json();
    }).then(data => {
      const papers = Array.isArray(data) ? data : data.papers;
      const ids = new Set(papers.map(p => p.paper_id));
      if (papers.length !== paperToCard.size || ids.size !== papers.length ||
          papers.some(p => !paperToCard.has(p.paper_id))) {
        throw new Error('Catalog and page snapshots differ');
      }
      buildIndex(papers);
      applyFilter();
    }).catch(error => {
      console.warn('Using the embedded paper catalog:', error.message);
    });
  });
})();

// ============================================================
// On-Policy Distillation Survey — search & filter widget
// Uses Fuse.js loaded above for fuzzy search, then intersects
// the result set with active chip predicates.
// ============================================================

(function () {
  'use strict';

  const scriptVersion = new URL(document.currentScript.src).searchParams.get('v') || '';
  const PAPERS_URL = `static/data/papers.json?v=${encodeURIComponent(scriptVersion)}`;
  let fuse = null;
  let allPapers = [];
  const paperToCard = new Map(); // stable catalog paper_id -> <li> DOM node

  // Active filter state, group -> Set of selected values
  const active = {
    section: new Set(),
    mechanism: new Set(),
    year: new Set()
  };
  let searchQuery = '';

  // ---- helpers ----
  function debounce(fn, ms) {
    let t = null;
    return function (...args) {
      if (t) clearTimeout(t);
      t = setTimeout(() => fn.apply(this, args), ms);
    };
  }

  function indexCards() {
    document.querySelectorAll('li.paper-card').forEach(card => {
      const id = card.getAttribute('data-paper-id');
      if (id) paperToCard.set(id, card);
    });
  }

  function applyFilter() {
    // Determine the visible set of catalog IDs, including software records.
    let candidates;
    if (searchQuery.trim().length > 0 && fuse) {
      candidates = new Set(fuse.search(searchQuery).map(r => r.item.paper_id));
    } else {
      const query = searchQuery.trim().toLocaleLowerCase();
      candidates = new Set(allPapers.filter(p => !query ||
        [p.title, ...(p.authors || []), p.description, p.source_version, p.paper_id, p.arxiv_id || '']
          .join(' ').toLocaleLowerCase().includes(query)
      ).map(p => p.paper_id));
    }

    // Apply each chip group as AND across groups, OR within a group.
    const filtered = [];
    for (const p of allPapers) {
      if (!candidates.has(p.paper_id)) continue;
      if (active.section.size > 0 && !active.section.has(p.home)) continue;
      const mechanisms = Array.isArray(p.mechanism) ? p.mechanism : [p.mechanism];
      if (active.mechanism.size > 0 && !mechanisms.some(m => active.mechanism.has(m))) continue;
      if (active.year.size > 0 && !active.year.has(String(p.year))) continue;
      filtered.push(p);
    }

    // Toggle DOM nodes
    const visibleSet = new Set(filtered.map(p => p.paper_id));
    let visibleCount = 0;
    paperToCard.forEach((card, id) => {
      if (visibleSet.has(id)) {
        card.classList.remove('is-hidden');
        visibleCount += 1;
      } else {
        card.classList.add('is-hidden');
      }
    });

    // Hide empty section groups
    document.querySelectorAll('.paper-section-group').forEach(group => {
      const anyVisible = group.querySelectorAll('li.paper-card:not(.is-hidden)').length > 0;
      group.classList.toggle('is-hidden', !anyVisible);
    });

    // Update counter + empty state
    const counter = document.getElementById('visible-count');
    if (counter) {
      counter.textContent = `${visibleCount}/${allPapers.length}`;
    }
    const empty = document.getElementById('empty-state');
    if (empty) empty.classList.toggle('is-hidden', visibleCount > 0);
  }

  function bindChips() {
    document.querySelectorAll('.chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const group = chip.parentElement.getAttribute('data-filter-group');
        const value = chip.getAttribute('data-value');
        if (!group || !value || !active[group]) return;
        if (active[group].has(value)) {
          active[group].delete(value);
          chip.classList.remove('is-active');
          chip.setAttribute('aria-pressed', 'false');
        } else {
          active[group].add(value);
          chip.classList.add('is-active');
          chip.setAttribute('aria-pressed', 'true');
        }
        applyFilter();
      });
    });

    const clearBtn = document.getElementById('clear-filters');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        Object.values(active).forEach(values => values.clear());
        searchQuery = '';
        document.querySelectorAll('.chip.is-active').forEach(c => {
          c.classList.remove('is-active');
          c.setAttribute('aria-pressed', 'false');
        });
        const input = document.getElementById('search-input');
        if (input) input.value = '';
        applyFilter();
      });
    }
  }

  function bindSearch() {
    const input = document.getElementById('search-input');
    if (!input) return;
    const handler = debounce(() => {
      searchQuery = input.value;
      applyFilter();
    }, 120);
    input.addEventListener('input', handler);
  }

  function bindCite() {
    document.querySelectorAll('.badge-cite').forEach(btn => {
      btn.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();
        const card = btn.closest('li.paper-card');
        const bib = card ? card.getAttribute('data-bibtex') : '';
        if (!bib) return;
        const label = btn.querySelector('.cite-label');
        const onCopied = () => {
          if (label) label.textContent = '✓ Copied';
          btn.classList.add('is-copied');
          setTimeout(() => {
            if (label) label.textContent = 'Cite';
            btn.classList.remove('is-copied');
          }, 1400);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(bib).then(onCopied).catch(() => {
            const ta = document.createElement('textarea');
            ta.value = bib; ta.style.position = 'fixed'; ta.style.opacity = '0';
            document.body.appendChild(ta); ta.select();
            try { document.execCommand('copy'); } catch (_) {}
            document.body.removeChild(ta); onCopied();
          });
        } else {
          const ta = document.createElement('textarea');
          ta.value = bib; ta.style.position = 'fixed'; ta.style.opacity = '0';
          document.body.appendChild(ta); ta.select();
          try { document.execCommand('copy'); } catch (_) {}
          document.body.removeChild(ta); onCopied();
        }
      });
    });
  }

  function bindExport() {
    const btn = document.getElementById('export-bibtex');
    if (!btn) return;
    btn.addEventListener('click', () => {
      const bibs = [];
      document.querySelectorAll('li.paper-card:not(.is-hidden)').forEach(card => {
        const bib = card.getAttribute('data-bibtex');
        if (bib) bibs.push(bib);
      });
      if (!bibs.length) return;
      const blob = new Blob([bibs.join('\n\n')], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = 'opd-papers.bib';
      document.body.appendChild(a); a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  }

  function init(papers) {
    allPapers = papers;
    fuse = typeof Fuse === 'function' ? new Fuse(papers, {
      keys: [
        { name: 'title',          weight: 3 },
        { name: 'authors',        weight: 2 },
        { name: 'description',    weight: 2 },
        { name: 'source_version', weight: 1 },
        { name: 'paper_id',       weight: 0.5 },
        { name: 'arxiv_id',       weight: 0.5 }
      ],
      threshold: 0.4,
      ignoreLocation: true,
      includeScore: false,
      minMatchCharLength: 2
    }) : null;
    indexCards();
    bindChips();
    bindSearch();
    bindCite();
    bindExport();
    applyFilter();
  }

  document.addEventListener('DOMContentLoaded', () => {
    fetch(PAPERS_URL)
      .then(r => {
        if (!r.ok) throw new Error(`Catalog HTTP ${r.status}`);
        return r.json();
      })
      .then(data => {
        const papers = Array.isArray(data) ? data : (data.papers || []);
        const cardIds = new Set([...document.querySelectorAll('li.paper-card')].map(c => c.dataset.paperId));
        const paperIds = new Set(papers.map(p => p.paper_id));
        if (papers.length !== cardIds.size || paperIds.size !== papers.length ||
            papers.some(p => !cardIds.has(p.paper_id))) {
          throw new Error('Catalog and page snapshots differ');
        }
        init(papers);
      })
      .catch(err => {
        console.warn('papers.json fetch failed', err);
        // The rendered cards contain the same public metadata, including authors.
        const fallback = [];
        document.querySelectorAll('li.paper-card').forEach(card => {
          fallback.push(JSON.parse(card.getAttribute('data-paper')));
        });
        init(fallback);
      });
  });
})();

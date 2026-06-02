// ============================================================
// On-Policy Distillation Survey — search & filter widget
// Uses Fuse.js loaded above for fuzzy search, then intersects
// the result set with active chip predicates.
// ============================================================

(function () {
  'use strict';

  const PAPERS_URL = 'static/data/papers.json';
  let fuse = null;
  let allPapers = [];
  let arxivToCard = new Map(); // arxiv_id -> <li> DOM node

  // Active filter state, group -> Set of selected values
  const active = {
    section: new Set(),
    loss:    new Set(),
    year:    new Set(),
    domain:  new Set(),
    signal:  new Set(),
    freq:    new Set(),
    size:    new Set()
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
      const aid = card.getAttribute('data-arxiv-id');
      if (aid) arxivToCard.set(aid, card);
    });
  }

  function applyFilter() {
    // Determine the visible set of arxiv ids.
    let candidates;
    if (searchQuery.trim().length > 0 && fuse) {
      candidates = new Set(fuse.search(searchQuery).map(r => r.item.arxiv_id));
    } else {
      candidates = new Set(allPapers.map(p => p.arxiv_id));
    }

    // Apply each chip group as AND across groups, OR within a group.
    const filtered = [];
    for (const p of allPapers) {
      if (!candidates.has(p.arxiv_id)) continue;
      if (active.section.size > 0) {
        // section is e.g. "§4.3"; chip values may be "§4" (parent) or "§4.3" (exact)
        const matchesSection = [...active.section].some(s => {
          if (s === p.section) return true;
          // parent match: chip "§4" matches section "§4.1" / "§4.2" / "§4.3"
          if (p.section && p.section.startsWith(s + '.')) return true;
          return false;
        });
        if (!matchesSection) continue;
      }
      if (active.loss.size > 0 && !active.loss.has(p.loss_class)) continue;
      if (active.year.size > 0 && !active.year.has(String(p.year))) continue;
      if (active.domain.size > 0 && !active.domain.has(p.domain || '')) continue;
      if (active.signal.size > 0 && !active.signal.has(p.signal || '')) continue;
      if (active.freq.size > 0 && !active.freq.has(p.freq || '')) continue;
      if (active.size.size > 0 && !active.size.has(p.size || '')) continue;
      filtered.push(p);
    }

    // Toggle DOM nodes
    const visibleSet = new Set(filtered.map(p => p.arxiv_id));
    let visibleCount = 0;
    arxivToCard.forEach((card, aid) => {
      if (visibleSet.has(aid)) {
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
        } else {
          active[group].add(value);
          chip.classList.add('is-active');
        }
        applyFilter();
      });
    });

    const clearBtn = document.getElementById('clear-filters');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        active.section.clear();
        active.loss.clear();
        active.year.clear();
        active.domain.clear();
        active.signal.clear();
        active.freq.clear();
        active.size.clear();
        searchQuery = '';
        document.querySelectorAll('.chip.is-active').forEach(c => c.classList.remove('is-active'));
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

  function bindExpand() {
    // Toggle .is-expanded on paper-card when clicking title/toggle/non-link area
    document.querySelectorAll('li.paper-card.has-detail').forEach(card => {
      card.addEventListener('click', (e) => {
        // Ignore clicks on links / badge anchors so they navigate normally
        if (e.target.closest('a')) return;
        // Ignore clicks inside .paper-detail (let inner links work, no toggle)
        if (e.target.closest('.paper-detail')) return;
        card.classList.toggle('is-expanded');
      });
    });
  }

  function init(papers) {
    allPapers = papers;
    fuse = new Fuse(papers, {
      keys: [
        { name: 'title',          weight: 3 },
        { name: 'authors',        weight: 2 },
        { name: 'description',    weight: 2 },
        { name: 'arxiv_id',       weight: 0.5 }
      ],
      threshold: 0.4,
      ignoreLocation: true,
      includeScore: false,
      minMatchCharLength: 2
    });
    indexCards();
    bindChips();
    bindSearch();
    bindExpand();
    applyFilter();
  }

  document.addEventListener('DOMContentLoaded', () => {
    fetch(PAPERS_URL)
      .then(r => r.json())
      .then(data => {
        const papers = Array.isArray(data) ? data : (data.papers || []);
        init(papers);
      })
      .catch(err => {
        console.warn('papers.json fetch failed', err);
        // Still allow chip-based filtering using DOM data attributes only.
        const fallback = [];
        document.querySelectorAll('li.paper-card').forEach(card => {
          fallback.push({
            arxiv_id: card.getAttribute('data-arxiv-id') || '',
            title: card.querySelector('.paper-title')?.textContent || '',
            authors: '',
            description: '',
            section: card.getAttribute('data-section') || '',
            loss_class: card.getAttribute('data-loss') || '',
            year: card.getAttribute('data-year') || '',
            domain: card.getAttribute('data-domain') || '',
            signal: card.getAttribute('data-signal') || '',
            freq: card.getAttribute('data-freq') || '',
            size: card.getAttribute('data-size') || ''
          });
        });
        init(fallback);
      });
  });
})();

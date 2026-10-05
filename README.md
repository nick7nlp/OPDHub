<div align="center">

# 📚 OPDHub

**Companion website for [A Survey of On-Policy Distillation for Large Language Models](https://arxiv.org/abs/2604.00626).**

[![Live Site](https://img.shields.io/badge/🌐_Live_Site-nick7nlp.github.io/OPDHub-5698C3?style=flat-square)](https://nick7nlp.github.io/OPDHub/)
[![arXiv](https://img.shields.io/badge/arXiv-2604.00626-b31b1b?style=flat-square&logo=arxiv)](https://arxiv.org/abs/2604.00626)
[![Awesome List](https://img.shields.io/badge/📋_Awesome_List-Awesome--LLM--On--Policy--Distillation-75B975?style=flat-square)](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation)
[![License](https://img.shields.io/badge/License-CC_BY--SA_4.0-867892?style=flat-square)](LICENSE)

<img src="static/images/model-atlas-heatmap.png" alt="Teacher–student model atlas: historical snapshot" width="640"/>

*Historical figure snapshot, preserved from the original site; it is not regenerated from the current catalog.*

</div>

---

## Live site

**https://nick7nlp.github.io/OPDHub/**

The companion survey and the [current Awesome catalog](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation)
are linked separately on the site. The catalog includes background references as well as OPD work.
All catalog records are displayed under §4 Objectives, §5 Supervision, §6 Training,
§7 Agentic, §8 Analysis, §9 Applications, or Background.

Search covers titles, full author lists, descriptions, source versions, and identifiers.
Filters use the catalog's mechanism labels, section, and year; several labels can be
selected within a group. Monthly counts use actual `submitted` dates, include background
entries with full submission dates, and state the snapshot date and date range.
Year-only software dates are retained but excluded from monthly counts. Empty optional metadata does not
remove a record. Code buttons use only the supplied code URLs, and non-arXiv sources
retain their original links. Citation export uses full supplied author lists.

## Build from the public catalog

Python 3.10 or later and the public
[`resources/catalog.json`](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation/blob/master/resources/catalog.json)
are sufficient; no API, private notes, or local research checkout is required.
The page displays the catalog's `updated_on` as its checked date, and each record's
`metadata_checked_on` and `source_version` where supplied.

With OPDHub and Awesome checked out as siblings:

```sh
python3 scripts/build.py
```

With the catalog stored elsewhere:

```sh
python3 scripts/build.py --catalog /path/to/catalog.json
```

The research project also provides the equivalent wrapper `python3 scripts/build_site.py`.
The builder writes `index.html` and `static/data/papers.json`; it leaves images and styles
unchanged. An optional `--output-dir /path/to/preview` writes just these generated files
elsewhere; copy `static/` into that directory to preview the page with its assets.

A missing catalog or invalid record stops the build before output is written. There is
no fallback to old notes or README scraping. Every valid catalog record is retained,
including software references and records with empty descriptions. Only documented
public metadata fields and derived display fields are exported; unrelated source keys
are ignored. Builds are deterministic, with asset and search-index cache keys tied to
content. The browser can search embedded card metadata if the search index is unavailable.

## Contributing

To add or correct a paper, please open an issue or PR against the source-of-truth repo: **[Awesome-LLM-On-Policy-Distillation](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation)**. Updates flow from there to this site.

For template / styling fixes (CSS / JS / layout) on the site itself, PRs here are welcome.

## Citation

If this site or the survey helps your work, please cite:

```bibtex
@article{song2026opdsurvey,
  title  = {A Survey of On-Policy Distillation for Large Language Models},
  author = {Mingyang Song and Mao Zheng},
  journal= {arXiv preprint arXiv:2604.00626},
  year   = {2026}
}
```

## Acknowledgements

Site template adapted from the [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template) (originally [Nerfies](https://nerfies.github.io)).

## License

Site source under [CC BY-SA 4.0](LICENSE). Paper metadata cited under fair use for academic survey purposes.

<div align="center">

# OPDHub

**Companion website for [A Survey of On-Policy Distillation for Large Language Models](https://arxiv.org/abs/2604.00626).**

[Explore OPDHub](https://nick7nlp.github.io/OPDHub/) · [Browse the reading list](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation) · [Release history](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation/blob/master/CHANGELOG.md)

</div>

## News

- **2026-10-05** — The catalog now covers literature through September 2026, with updated reading sections, search and citation export.
- **2026-06-18** — [Survey v4](https://arxiv.org/abs/2604.00626v4) is available on arXiv.
- **2026-05-18** — [Survey v3](https://arxiv.org/abs/2604.00626v3) is available on arXiv.
- **2026-05-12** — [Survey v2](https://arxiv.org/abs/2604.00626v2) is available on arXiv.
- **2026-04-01** — [The first survey version](https://arxiv.org/abs/2604.00626v1) is available on arXiv.

## Explore the literature

Search by title, author, description, source version or paper identifier. Filters
cover reading sections, mechanisms and release years. Each entry links to the
source paper and any listed repository, with complete-author BibTeX export.

The catalog includes methods, analyses, application reports and background
references. Its literature coverage can extend beyond the latest public survey PDF.

## Teacher–Student Model Atlas

<img src="static/images/model-atlas-heatmap.png" alt="Teacher–student model combinations, June 2026 snapshot" width="960"/>

*June 2026 snapshot. Rows represent teachers and columns represent students.
The image shows historical model-pair coverage, not the current catalog's counts
or a ranking of model quality. Same-name models may use different contexts.*

## Build the site

With OPDHub and the Awesome repository checked out as siblings:

```sh
python3 scripts/build.py
```

Or specify the catalog file:

```sh
python3 scripts/build.py --catalog /path/to/catalog.json
```

The build uses Python 3.10 or later. Paper records and release announcements are
read from the Awesome repository's `resources/catalog.json` and
`resources/news.json`. An optional `--news` argument selects another announcement
file. To generate a preview, use `--output-dir /path/to/preview` and copy the
site's `static/` assets there.

## Contributing

Suggest paper additions and corrections in
[Awesome-LLM-On-Policy-Distillation](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation).
Website issues and improvements are welcome in this repository.

## Citation

```bibtex
@article{song2026opdsurvey,
  title  = {A Survey of On-Policy Distillation for Large Language Models},
  author = {Mingyang Song and Mao Zheng},
  journal= {arXiv preprint arXiv:2604.00626},
  year   = {2026}
}
```

## Acknowledgements

Site template adapted from the
[Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template)
(originally [Nerfies](https://nerfies.github.io/)).

## License

Site source is distributed under [CC BY-SA 4.0](LICENSE).

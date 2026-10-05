# OPDHub

A focused search interface for papers on on-policy distillation.

[Search papers](https://nick7nlp.github.io/OPDHub/) · [Survey](https://arxiv.org/abs/2604.00626) · [Reading list and news](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation)

Search titles, authors, methods and paper identifiers. Expand Filters to narrow
results by topic, mechanism or year. Each result provides a short description,
source and repository links, and a citation button. Export BibTeX for the current
results with one click.

## Build

With OPDHub and the Awesome repository checked out as siblings:

```sh
python3 scripts/build.py
```

Or specify the public catalog:

```sh
python3 scripts/build.py --catalog /path/to/catalog.json
```

Python 3.10 or later is required. Use `--output-dir` for a preview and copy
the site's `static/` assets into that directory.

## Contributing

Suggest paper additions and corrections in
[Awesome-LLM-On-Policy-Distillation](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation).
Website improvements are welcome here.

## Credits and license

Adapted from the [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template)
and [Nerfies](https://nerfies.github.io/). Distributed under [CC BY-SA 4.0](LICENSE).

# OPDHub

**A reading companion for on-policy distillation.**

[Explore the collection](https://nick7nlp.github.io/OPDHub/) · [Read the survey](https://arxiv.org/abs/2604.00626) · [Awesome reading list](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation)

Explore the field through objectives, supervision, training, agents, analysis,
and applications. Research questions connect the topics; each paper includes
a concise contribution description and links to its source and available code.

- Search titles, authors, methods, and exact paper identifiers. Press `/` to search.
- Choose a topic, then refine by mechanism and year.
- Copy individual citations or export the visible results as BibTeX.
- Browse the complete collection without JavaScript. Search and filters also
  work from the embedded catalog when the separate data request fails.

The interface uses a compact reading layout with a persistent topic index on
desktop and a horizontal topic bar on mobile. All fonts and assets are local
or provided by the browser.

## Build

With OPDHub and the Awesome repository checked out as siblings:

```sh
python3 scripts/build.py
```

Or supply the public catalog explicitly:

```sh
python3 scripts/build.py --catalog /path/to/catalog.json
```

Python 3.10 or later is required. To preview in a separate directory, pass
`--output-dir` and copy the site's `static/` assets into that directory.

The data export preserves `source_version` and, when available, `latest_version`.
The former records the source used for the description; the latter identifies
the latest arXiv version checked in the catalog metadata.

## Contributing

Suggest paper additions and corrections in
[Awesome-LLM-On-Policy-Distillation](https://github.com/nick7nlp/Awesome-LLM-On-Policy-Distillation/issues).
Website improvements are welcome here.

## Credits and license

Adapted from the [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template)
and [Nerfies](https://nerfies.github.io/). Distributed under [CC BY-SA 4.0](LICENSE).

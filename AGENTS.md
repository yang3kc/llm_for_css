# AGENTS.md

Guidance for AI agents working in this repository.

## What this is

This repository is the source of the tutorial website
[LLM for Computational Social Science](https://yang3kc.github.io/llm_for_css/).
The website is the canonical version of the tutorial.
It is built with Material for MkDocs and the `mkdocs-jupyter` plugin.

The readers are researchers who want to call LLM APIs from Python.
Many of them are new to these APIs, and many run the notebooks on Google Colab.

## Layout

```
docs/                  The website pages
  index.md             Landing page: chapter cards and the provider table
  api_key.md           API key page
  *.ipynb              One notebook per runnable chapter, with stored outputs
  local_llms.md        A chapter that is a Markdown page and embeds scripts
  *.jsonl              Data files that the chapters read
  assets/, stylesheets/
async_programming/, batch_processing/, local_llms/
                       Scripts that the chapters embed or link to
basics/, structured_output/
                       Pointer READMEs kept for old links
mkdocs.yml             Site configuration and the nav
pyproject.toml, uv.lock
                       Dependencies, managed with uv
.env.template          Template for the local .env file
.github/workflows/docs.yml
                       Builds and deploys the site on every push to main
```

## Environment

```bash
uv sync                          # dependencies of the notebooks and scripts
uv sync --group docs             # also the site dependencies
uv run mkdocs serve              # preview at http://127.0.0.1:8000/llm_for_css/
uv run mkdocs build --strict     # the build that CI runs; it must pass
```

The chapters read their keys from the environment or from a `.env` file:
`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY`, and `TYPESAFE_API_KEY`.

## Rules

- **Never commit `.env` or a key.** `.env` is git-ignored. Never print a key value,
  and check that no stored notebook output holds one.
- **Do not push to `main` directly.** Every push to `main` deploys the site.
  Work on a branch, open a pull request, and let the maintainer review the change
  on the local preview before the merge. Merge with a squash merge so that the
  history of `main` stays linear.
- **Run `uv run mkdocs build --strict` before you consider a change done.**
  It fails on broken internal links and anchors.
- **Do not re-run a notebook without need.** A run costs money and changes the
  stored outputs. See "Notebooks" below.
- **Change dependencies with `uv add`** and commit `uv.lock` together with
  `pyproject.toml`. When the lock file changes a shared package such as `openai`
  or `pydantic`, check that the other notebooks still run. Run copies outside
  `docs/` so that their stored outputs do not change.
- Keep `README.md` in sync with the landing page and the repository layout.

## Notebooks

The site shows the outputs that are stored in each notebook. The build does not
execute any notebook.

- **First cell.** The title, then the Open in Colab badge that points to the
  notebook on `main`, then a short introduction.
- **Setup section.** One install cell (`%pip install -q ...`) and one key cell.
  The key cell calls `load_dotenv()` and then reads the key from Colab Secrets
  when the environment does not have it. Copy the cell from an existing chapter.
- **Keys.** Each chapter names its own key in its Setup section. The API key
  page and `.env.template` name only `OPENAI_API_KEY`.
- **Colab.** Every notebook must run on Google Colab from top to bottom. A data
  file is read from the current folder, or downloaded from its raw GitHub URL on
  `main` when it is missing. Such a URL, the link to the data file, and the Colab
  badge of a new chapter work only after the merge. Test a new chapter on Colab
  from its branch before the merge.
- **After a run.** Clear the output of the install cell, because it can hold a
  local path. Check that the file holds no key value, no home directory path,
  no warning, and no traceback.
- **Numbers in the text.** Some Markdown cells quote numbers from the stored
  outputs. After a new run, compare every such number with the new outputs.
  Model answers differ slightly between runs.
- **Models and prices.** Each chapter uses one example model. A price or a
  vendor fact carries a date, for example "as of October 2026". When the example
  model or its price changes, also update the provider table on the landing page.

### Adding a chapter

1. Add the notebook (or the Markdown page) to `docs/`.
2. Add it to the `nav` in `mkdocs.yml`.
3. Add a card to the landing page, and a row or a paragraph in the section
   "Which provider should I use?". Check that every sentence on the landing
   page is still true.
4. Add new packages with `uv add`.
5. Update `README.md` if the layout changed.
6. Run the strict build and check the new links and anchors.
7. Run the notebook on Colab.
8. A new chapter needs a new minor version. See the next section.

## Writing style

- Write short, plain sentences. Many readers are not native English speakers.
- Address the reader as "you" and use "we" for the steps of the chapter.
- Explain a term when it first appears, and link to the earlier chapter that
  introduces a pattern instead of repeating it.
- Give the source and the date of every number that comes from a paper or a
  vendor page.

## Versions and releases

The tutorial has a version of the form `vMAJOR.MINOR`. The website always shows
`main`. Older versions stay available at their tags.

**When the version changes**

- **Major** (for example `v4.0`): the tutorial changes its form or its main API.
  `v1.0` used the Chat Completions API, `v2.0` moved to the Responses API, and
  `v3.0` turned the tutorial into a website.
- **Minor** (for example `v3.1`): a chapter is added or rewritten.
- **No new version**: fixes, updates of a model name or a price, wording
  changes, and dependency updates.

A change that needs a new version is released right after its pull request is
merged. Do not leave unreleased entries in the Versions list.

**Where the version is recorded**

- the git tag `vMAJOR.MINOR`,
- the GitHub release with the same name,
- the Versions list in `README.md`,
- `version` in `pyproject.toml`, written as `MAJOR.MINOR.0`, and the matching
  entry in `uv.lock`.

**How to release**

1. Create a branch `release-MAJOR.MINOR`.
2. Update the Versions list in `README.md`. The new entry comes first and is
   marked "(current)". The previous entry loses "(current)" and gets a link to
   its tag.
3. Set `version` in `pyproject.toml` and run `uv lock`.
4. Open a pull request and merge it after the review.
5. Create an annotated tag on the merge commit and push it:

   ```bash
   git tag -a vMAJOR.MINOR -m "vMAJOR.MINOR: <one-line summary>"
   git push origin vMAJOR.MINOR
   ```

6. Create the GitHub release for the tag with the title `vMAJOR.MINOR`. The
   notes are a short list of what changed for readers, followed by a line
   "Full history" with the compare link from the previous tag.

Ask the maintainer before you create a tag or a release.

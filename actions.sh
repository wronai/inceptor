#!/bin/bash
mkdocs build --verbose || { echo "❌ mkdocs build failed"; exit 1; }
python -m pip install --upgrade mkdocs-material mkdocs-awesome-pages-plugin mkdocs-minify-plugin mkdocstrings[python] mkdocs-material-extensions pygments
mkdocs build --verbose
yamllint .github/workflows/
gh actions lint
rm -rf site public
mkdocs build --strict --verbose
python -m pip install --upgrade pip
pip install mkdocs-material mkdocs-awesome-pages-plugin mkdocs-minify-plugin mkdocstrings[python] mkdocs-material-extensions pygments
ls -l mkdocs.yml docs/
pytest
flake8 .
black --check .
black --check --diff .
black .
git diff
act
mkdocs build --strict
mkdocs serve
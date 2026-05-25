# Repository Guidelines

## Project Structure & Module Organization

This repository is a Python Streamlit app for a fintech navigation system.

- `app.py` is the Streamlit entry point and top-level navigation shell.
- `src/pages/` contains page modules such as `course_page.py`, `job_page.py`, `skill_page.py`, `cert_page.py`, `search_page.py`, and `roadmap_page.py`.
- `src/utils/` contains shared helpers and data-loading logic.
- `config/settings.py` stores project paths, theme constants, roadmap data, and recommendation rules.
- `data/` stores Excel source files: `课程表.xlsx`, `职业表.xlsx`, `技能表.xlsx`, and `证书表.xlsx`.
- `requirements.txt` and `setup.py` define Python dependencies and package metadata.

Avoid committing generated files such as `__pycache__/`, `.pyc`, or build artifacts.

## Build, Test, and Development Commands

Create and activate a virtual environment before installing dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the app locally:

```powershell
streamlit run app.py
```

Install the package in editable mode when developing imports or packaging:

```powershell
pip install -e .
```

There is currently no dedicated test command in the repository.

## Coding Style & Naming Conventions

Use Python 3.8+ and follow PEP 8 style: 4-space indentation, clear function names, and imports grouped by standard library, third-party packages, then local modules. Prefer `snake_case` for functions, variables, and module names. Page modules should follow the existing `*_page.py` pattern.

Keep shared constants in `config/settings.py`; avoid duplicating file paths or theme colors inside page modules. Put reusable UI/data helpers in `src/utils/` instead of copying logic between pages.

## Testing Guidelines

No tests are currently present. For new logic, add focused tests under a future `tests/` directory using `pytest`. Name files `test_<module>.py` and tests `test_<behavior>()`.

Prioritize tests for data parsing, recommendation rules, filtering/search behavior, and helper functions that do not require a Streamlit runtime. Manually verify UI changes with:

```powershell
streamlit run app.py
```

## Commit & Pull Request Guidelines

This working tree has no Git history available, so no project-specific commit convention can be inferred. Use concise, imperative commit messages such as `Add roadmap filtering` or `Fix Excel data loading`.

Pull requests should include a short description, the user-facing behavior changed, manual test steps, and screenshots for visible UI changes. Link related issues when available, and mention any changes to the Excel data schema or required dependencies.

## Security & Configuration Tips

Do not hard-code local absolute paths, credentials, or private data. Keep data file references relative through `config/settings.py`. If adding environment-specific configuration later, document required variables and provide safe defaults.

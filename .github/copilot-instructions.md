## Repo overview

- Entry point: `Home_Page.py` — a Streamlit app that composes the site.
- Multipage components: `pages/01_Data_Overview.py`, `pages/02_Geographical_Analysis.py`, `pages/03_Feminist_Wave_Analysis.py`, `pages/04_Text_Classification.py` (Streamlit `pages/` pattern).
- Data lives under `data/` (CSV & JSONL). Typical workflows read `data/cleaned_pageview_data.csv` and other CSVs.
- Dependencies are minimal: see `requirements.txt` (`streamlit`, `pandas`, `plotly`, `matplotlib`, `seaborn`).

## Big picture & intent

- This project is a Streamlit data-exploration site focused on feminist-article pageviews and text classification. The app is designed to be launched locally with Streamlit and uses the `pages/` folder for separate views.
- Keep UI logic in the top-level page files and treat `data/` as read-only fixtures for analysis (no data-writing flows expected).

## What an AI coding agent should do first

- Use `Home_Page.py` as the app entrypoint to understand global layout and app-level state.
- Open representative pages in `pages/` to learn UI patterns and how plots/tables are created (they show pandas→plotly/matplotlib usage).
- Inspect `data/` files to understand dataframe schemas (column names and types). Example: `data/cleaned_pageview_data.csv` is referenced by multiple pages.

## Project-specific conventions & patterns

- Streamlit multipage: new views are Python files in `pages/` — avoid changing the import pattern; add pages by adding files there.
- Data loading: pages load CSVs directly from `data/` using `pandas.read_csv` (no centralized data loader). When refactoring, preserve column names and order or update all pages that reference them.
- Plotting: prefer `plotly` for interactive plots and `matplotlib`/`seaborn` for static visuals; follow existing style in each page file.

## Running, debugging, and testing

- Install deps: `pip install -r requirements.txt`.
- Run locally: `streamlit run Home_Page.py` from repo root (this launches the multipage Streamlit app).
- Debugging: use `st.write()` / `st.table()` for quick variable inspection in pages; changes to `pages/` are picked up by Streamlit live-reload.

## Integration points & external dependencies

- No external APIs appear in the repo; data is bundled in `data/`. If you add external data sources, update README and include fallback cached CSVs in `data/` for reproducibility.

## Guidance for common agent tasks

- Add a new page: create `pages/NN_NewName.py` and follow the structure of existing pages (read CSV → process with `pandas` → render with `plotly`/`st.write`).
- Rename a dataset column: search for the column name across `pages/` and `Home_Page.py` and update all references; prefer to add a compatibility shim (`df.rename(columns={...}, inplace=True)`) at top of affected pages.
- Update dependencies: change `requirements.txt` and run `pip install -r requirements.txt` locally; confirm `streamlit run Home_Page.py` still launches.

## Files to inspect for context

- `Home_Page.py` — app entry and global layout.
- `pages/01_Data_Overview.py` — canonical example of data load → transform → plot.
- `data/cleaned_pageview_data.csv` — primary dataset; check columns before schema changes.
- `requirements.txt` — minimal dependency list.

## Examples (quick snippets)

- Run the app locally:

```
pip install -r requirements.txt
streamlit run Home_Page.py
```

- Typical data load pattern used across pages:

```
import pandas as pd
df = pd.read_csv('data/cleaned_pageview_data.csv')
```

## When to ask maintainers

- If a page reads a CSV that is not in `data/`, or if adding network/data-write behavior, ask before changing project data assumptions.
- If adding heavy dependencies (e.g., scikit-learn), confirm they are needed since current `requirements.txt` is intentionally small.

---
Please review this draft — tell me which sections need more detail or any workflows I missed.

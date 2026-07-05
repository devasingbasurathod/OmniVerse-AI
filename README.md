# OmniVerse AI

A simple AI-powered web application for uploading, analyzing, and chatting with your data files.

## Features

- **Home Page** — Landing page with app overview
- **Login & Register** — Secure user authentication (SQLite)
- **Dashboard** — Overview of uploads, reports, and quick actions
- **File Upload** — CSV, Excel, PDF, and image files
- **File Preview** — Instant preview of uploaded content
- **AI Summary** — Automatic insights from your data
- **Charts** — Interactive Plotly visualizations
- **AI Chatbot** — Ask questions about uploaded files
- **Reports** — Save and download analysis reports
- **Profile** — Manage account information
- **Settings** — Dark / Light mode toggle

## Tech Stack

| Layer      | Technology        |
|------------|-------------------|
| Frontend   | Streamlit         |
| Backend    | Python            |
| Data       | Pandas            |
| Charts     | Plotly            |
| Database   | SQLite            |

## Project Structure

```
OmniVerse AI/
├── app.py              # Main entry point — run this file
├── requirements.txt    # Python dependencies
├── utils.py            # Shared utilities
├── database.db         # SQLite database (auto-created)
├── backend/
│   ├── database.py     # DB models & queries
│   ├── auth.py         # Login & registration
│   ├── file_handler.py # Upload & preview
│   ├── ai_engine.py    # Summary & chatbot
│   └── charts.py       # Plotly chart builders
├── frontend/
│   ├── styles.py       # Dark/light theme CSS
│   ├── components.py   # Reusable UI components
│   └── pages.py        # Page renderers
├── uploads/            # Uploaded files (auto-created)
├── reports/            # Generated reports (auto-created)
└── static/             # Static assets
```

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the app

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**.

### 3. Create an account

1. Click **Get Started** on the home page
2. Switch to the **Register** tab
3. Create an account, then sign in

## Navigation Flow

```
Home → Login → Dashboard → Upload → AI Analysis → Report
```

## Supported File Types

| Type   | Extensions              |
|--------|-------------------------|
| CSV    | `.csv`                  |
| Excel  | `.xlsx`, `.xls`         |
| PDF    | `.pdf`                  |
| Image  | `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp` |

## AI Features

The built-in AI engine works **locally without an API key**:

- **Summary** — Statistical overview for CSV/Excel, extractive summary for PDFs
- **Chatbot** — Rule-based Q&A about rows, columns, stats, and content
- **Charts** — Auto-generated and custom Plotly visualizations

> To connect OpenAI or another LLM, extend `backend/ai_engine.py`.

## License

MIT — free for personal and educational use.

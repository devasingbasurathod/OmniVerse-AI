"""AI summary and chatbot (local, rule-based — no API key required)."""

import re

import pandas as pd


def summarize_dataframe(df):
    """Generate a summary for tabular data."""
    lines = [
        f"**Dataset Overview**",
        f"- Rows: {len(df):,}",
        f"- Columns: {len(df.columns)}",
        f"- Column names: {', '.join(df.columns.astype(str).tolist())}",
        "",
        "**Data Types:**",
    ]
    for col, dtype in df.dtypes.items():
        lines.append(f"- {col}: {dtype}")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        lines.append("")
        lines.append("**Numeric Summary:**")
        desc = df[numeric_cols].describe().round(2)
        lines.append(desc.to_string())

    null_counts = df.isnull().sum()
    if null_counts.any():
        lines.append("")
        lines.append("**Missing Values:**")
        for col, count in null_counts[null_counts > 0].items():
            lines.append(f"- {col}: {count} missing")

    return "\n".join(lines)


def summarize_text(text, max_sentences=5):
    """Simple extractive summary from plain text."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    if not sentences:
        return "No sufficient text content to summarize."
    selected = sentences[:max_sentences]
    summary = " ".join(selected)
    return f"**Summary** ({min(len(selected), max_sentences)} key sentences):\n\n{summary}"


def summarize_image(filename):
    """Placeholder summary for image files."""
    return (
        f"**Image Analysis**\n\n"
        f"- File: `{filename}`\n"
        f"- Type: Image upload\n"
        f"- Note: Connect a vision API for detailed image analysis. "
        f"This demo provides metadata and chat context from the filename."
    )


def generate_summary(preview, filename):
    """Generate AI summary from preview data."""
    kind = preview["kind"]

    if kind == "dataframe":
        return summarize_dataframe(preview["data"])
    if kind == "text":
        return summarize_text(preview["data"])
    if kind == "image":
        return summarize_image(filename)
    return "Unable to generate summary for this file type."


def chat_with_file(question, preview, filename):
    """Simple rule-based chatbot using file context."""
    q = question.lower().strip()
    kind = preview["kind"]

    if any(word in q for word in ["hello", "hi", "hey"]):
        return f"Hello! I can help you explore **{filename}**. Ask about rows, columns, stats, or content."

    if kind == "dataframe":
        df = preview["data"]
        if any(w in q for w in ["row", "rows", "count", "how many"]):
            return f"This dataset has **{len(df):,}** rows and **{len(df.columns)}** columns."
        if any(w in q for w in ["column", "columns", "fields"]):
            cols = ", ".join(df.columns.astype(str).tolist())
            return f"The columns are: **{cols}**"
        if any(w in q for w in ["missing", "null", "empty"]):
            nulls = df.isnull().sum()
            if nulls.any():
                parts = [f"{c}: {n}" for c, n in nulls[nulls > 0].items()]
                return "Missing values:\n" + "\n".join(f"- {p}" for p in parts)
            return "No missing values detected."
        if any(w in q for w in ["average", "mean", "avg"]):
            numeric = df.select_dtypes(include="number")
            if numeric.empty:
                return "No numeric columns to compute averages."
            col = numeric.columns[0]
            return f"Average of **{col}**: **{numeric[col].mean():.2f}**"
        if any(w in q for w in ["max", "maximum", "highest"]):
            numeric = df.select_dtypes(include="number")
            if numeric.empty:
                return "No numeric columns found."
            col = numeric.columns[0]
            return f"Maximum **{col}**: **{numeric[col].max():.2f}**"
        if any(w in q for w in ["min", "minimum", "lowest"]):
            numeric = df.select_dtypes(include="number")
            if numeric.empty:
                return "No numeric columns found."
            col = numeric.columns[0]
            return f"Minimum **{col}**: **{numeric[col].min():.2f}**"
        if any(w in q for w in ["head", "first", "preview", "sample"]):
            return "First 5 rows:\n\n" + df.head().to_markdown(index=False)
        if any(w in q for w in ["describe", "stats", "statistics", "summary"]):
            numeric = df.select_dtypes(include="number")
            if numeric.empty:
                return "No numeric statistics available."
            return numeric.describe().round(2).to_markdown()
        return (
            "Try asking about: row count, columns, missing values, "
            "averages, min/max, or a data preview."
        )

    if kind == "text":
        text = preview["data"]
        if any(w in q for w in ["length", "how long", "words"]):
            words = len(text.split())
            return f"The document has approximately **{words:,}** words."
        if any(w in q for w in ["summary", "summarize"]):
            return summarize_text(text)
        if len(q) > 3:
            matches = [s for s in re.split(r"(?<=[.!?])\s+", text) if q[:4] in s.lower()]
            if matches:
                return matches[0]
        return "Ask about word count, a summary, or mention keywords from the document."

    if kind == "image":
        return (
            f"This is an image file (**{filename}**). "
            "Ask about the filename or connect a vision model for deeper analysis."
        )

    return "I don't have enough context to answer that question."

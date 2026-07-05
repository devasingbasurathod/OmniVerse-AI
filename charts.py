"""Plotly chart helpers."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_numeric_columns(df):
    """Return list of numeric column names."""
    return df.select_dtypes(include="number").columns.tolist()


def get_categorical_columns(df):
    """Return list of categorical/object column names."""
    return df.select_dtypes(include=["object", "category"]).columns.tolist()


def build_bar_chart(df, x_col, y_col=None):
    """Create a bar chart."""
    if y_col:
        fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
    else:
        counts = df[x_col].value_counts().head(15).reset_index()
        counts.columns = [x_col, "count"]
        fig = px.bar(counts, x=x_col, y="count", title=f"Count by {x_col}")
    fig.update_layout(template="plotly_white", height=400)
    return fig


def build_line_chart(df, x_col, y_col):
    """Create a line chart."""
    fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} over {x_col}")
    fig.update_layout(template="plotly_white", height=400)
    return fig


def build_scatter_chart(df, x_col, y_col, color_col=None):
    """Create a scatter plot."""
    fig = px.scatter(
        df, x=x_col, y=y_col, color=color_col, title=f"{y_col} vs {x_col}"
    )
    fig.update_layout(template="plotly_white", height=400)
    return fig


def build_histogram(df, col):
    """Create a histogram."""
    fig = px.histogram(df, x=col, title=f"Distribution of {col}")
    fig.update_layout(template="plotly_white", height=400)
    return fig


def build_pie_chart(df, col):
    """Create a pie chart from value counts."""
    counts = df[col].value_counts().head(10)
    fig = go.Figure(data=[go.Pie(labels=counts.index.astype(str), values=counts.values)])
    fig.update_layout(title=f"Breakdown of {col}", template="plotly_white", height=400)
    return fig


def auto_chart(df):
    """Pick a sensible default chart for the dataframe."""
    numeric = get_numeric_columns(df)
    categorical = get_categorical_columns(df)

    if len(numeric) >= 2:
        return build_scatter_chart(df, numeric[0], numeric[1])
    if len(numeric) == 1 and categorical:
        return build_bar_chart(df, categorical[0], numeric[0])
    if categorical:
        return build_bar_chart(df, categorical[0])
    if numeric:
        return build_histogram(df, numeric[0])
    return None

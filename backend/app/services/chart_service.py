from typing import Dict, Any, List
import numpy as np
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class ChartService:
    def create_chart(
        self,
        data: List[Dict[str, Any]],
        chart_type: str,
        title: str = "Chart",
        axis_labels: List[str] = [],
    ) -> Dict[str, Any]:
        """
        Create a chart based on data and chart type using Plotly
        Returns dictionary with chart JSON
        """
        if not data:
            raise ValueError("No data provided for chart creation")

        # For the sake of simplicity, we assume axis_labels is a list of two items
        if axis_labels and len(axis_labels) > 2:
            raise ValueError("Axis labels should not exceed 2 items (x and y axis)")

        # Convert to pandas DataFrame for easier manipulation
        df = pd.DataFrame(data)

        if df.empty:
            raise ValueError("Empty dataset provided")

        fig = self._create_chart_by_type(df, chart_type, title, axis_labels)

        # Convert to JSON for frontend consumption
        chart_json = json.loads(fig.to_json())

        return {"chart_json": chart_json, "chart_type": chart_type, "title": title}

    def _create_chart_by_type(
        self, df: pd.DataFrame, chart_type: str, title: str, axis_labels: List[str] = []
    ) -> go.Figure:
        """
        Create specific chart type based on the data and chart type
        """
        chart_type = chart_type.lower()

        if chart_type == "bar":
            return self._create_bar_chart(df, title, axis_labels)
        elif chart_type == "line":
            return self._create_line_chart(df, title, axis_labels)
        elif chart_type == "pie":
            return self._create_pie_chart(df, title)
        elif chart_type == "area":
            return self._create_area_chart(df, title)
        else:
            raise ValueError(
                f"Unsupported chart type: {chart_type}. Supported types: bar, line, pie, area."
            )

    def _create_bar_chart(
        self, df: pd.DataFrame, title: str, axis_labels: List[str] = []
    ) -> go.Figure:
        """Create a bar chart"""
        # Assume first column is x-axis, second is y-axis
        if len(df.columns) >= 2:
            x_col = df.columns[0]
            y_col = df.columns[1]

            fig = px.bar(df, x=x_col, y=y_col, title=title)

            # Apply custom axis labels if provided
            if len(axis_labels) >= 1:
                fig.update_xaxes(title=axis_labels[0])
            if len(axis_labels) >= 2:
                fig.update_yaxes(title=axis_labels[1])

        else:
            # Single column - create a value count bar chart
            col = df.columns[0]
            value_counts = df[col].value_counts()
            fig = px.bar(x=value_counts.index, y=value_counts.values, title=title)

            # Apply custom axis labels if provided
            if len(axis_labels) >= 1:
                fig.update_xaxes(title=axis_labels[0])
            else:
                fig.update_xaxes(title=col)

            if len(axis_labels) >= 2:
                fig.update_yaxes(title=axis_labels[1])
            else:
                fig.update_yaxes(title="Count")

        return fig

    def _create_line_chart(
        self, df: pd.DataFrame, title: str, axis_labels: List[str] = []
    ) -> go.Figure:
        """Create a line chart"""
        if len(df.columns) >= 2:
            x_col = df.columns[0]
            y_col = df.columns[1]

            fig = px.line(df, x=x_col, y=y_col, title=title)

            # Apply custom axis labels if provided
            if len(axis_labels) >= 1:
                fig.update_xaxes(title=axis_labels[0])
            if len(axis_labels) >= 2:
                fig.update_yaxes(title=axis_labels[1])

        else:
            # Single column - plot values by index
            col = df.columns[0]
            fig = px.line(y=df[col], title=title)

            # Apply custom axis labels if provided
            if len(axis_labels) >= 1:
                fig.update_xaxes(title=axis_labels[0])
            else:
                fig.update_xaxes(title="Index")

            if len(axis_labels) >= 2:
                fig.update_yaxes(title=axis_labels[1])

        return fig

    def _create_pie_chart(self, df: pd.DataFrame, title: str) -> go.Figure:
        """Create a pie chart"""
        if len(df.columns) >= 2:
            labels_col = df.columns[0]
            values_col = df.columns[1]

            fig = px.pie(df, names=labels_col, values=values_col, title=title)
        else:
            # Single column - create pie chart from value counts
            col = df.columns[0]
            value_counts = df[col].value_counts()
            fig = px.pie(
                names=value_counts.index, values=value_counts.values, title=title
            )

        return fig

    def _create_area_chart(self, df: pd.DataFrame, title: str) -> go.Figure:
        """Create an area chart"""
        if len(df.columns) >= 2:
            x_col = df.columns[0]
            y_col = df.columns[1]

            fig = px.area(df, x=x_col, y=y_col, title=title)
        else:
            # Single column - area plot by index
            col = df.columns[0]
            fig = px.area(y=df[col], title=title)
            fig.update_xaxes(title="Index")

        return fig

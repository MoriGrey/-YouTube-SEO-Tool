"""
Enhanced Analytics Module
Advanced analytics with Plotly visualizations, custom date ranges, and comparison tools.

AGI Paradigm: Quantum Knowledge Synthesis
- Multi-dimensional data visualization
- Trend prediction visualization
- Channel comparison tools
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))


class EnhancedAnalytics:
    """
    Enhanced analytics with advanced visualizations.
    
    Features:
    - Interactive Plotly charts
    - Custom date range filtering
    - Channel comparison
    - Trend predictions
    - Export capabilities
    """
    
    def __init__(self, client):
        """Initialize enhanced analytics."""
        self.client = client
    
    def create_growth_chart(
        self,
        data: List[Dict[str, Any]],
        metric: str = "subscribers",
        date_range: Optional[Tuple[datetime, datetime]] = None
    ) -> go.Figure:
        """
        Create interactive growth chart.
        
        Args:
            data: List of data points with timestamp and metric values
            metric: Metric to visualize (subscribers, views, etc.)
            date_range: Optional tuple of (start_date, end_date)
        
        Returns:
            Plotly figure
        """
        if not data:
            # Return empty chart
            fig = go.Figure()
            fig.add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Filter by date range if provided
        if date_range and 'timestamp' in df.columns:
            start_date, end_date = date_range
            df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
        
        # Create figure
        fig = go.Figure()
        
        # Add main metric line
        if 'timestamp' in df.columns and metric in df.columns:
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df[metric],
                mode='lines+markers',
                name=metric.title(),
                line=dict(color='#4a9eff', width=2),
                marker=dict(size=6)
            ))
            
            # Add trend line if enough data points
            if len(df) > 2:
                z = np.polyfit(range(len(df)), df[metric], 1)
                p = np.poly1d(z)
                fig.add_trace(go.Scatter(
                    x=df['timestamp'],
                    y=p(range(len(df))),
                    mode='lines',
                    name='Trend',
                    line=dict(color='#ffc107', width=2, dash='dash')
                ))
        
        # Update layout
        fig.update_layout(
            title=f"{metric.title()} Growth Over Time",
            xaxis_title="Date",
            yaxis_title=metric.title(),
            hovermode='x unified',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#fafafa'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def create_comparison_chart(
        self,
        channels_data: List[Dict[str, Any]],
        metric: str = "subscribers"
    ) -> go.Figure:
        """
        Create channel comparison chart.
        
        Args:
            channels_data: List of channel data dictionaries
            metric: Metric to compare
        
        Returns:
            Plotly figure
        """
        if not channels_data:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
        
        # Prepare data
        channel_names = [ch.get('name', ch.get('channel_handle', 'Unknown')) for ch in channels_data]
        metric_values = [ch.get('statistics', {}).get(metric, 0) for ch in channels_data]
        
        # Create bar chart
        fig = go.Figure(data=[
            go.Bar(
                x=channel_names,
                y=metric_values,
                marker_color='#4a9eff',
                text=[f"{val:,}" for val in metric_values],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title=f"Channel Comparison - {metric.title()}",
            xaxis_title="Channel",
            yaxis_title=metric.title(),
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#fafafa')
        )
        
        return fig
    
    def create_trend_prediction_chart(
        self,
        historical_data: List[Dict[str, Any]],
        predictions: List[Dict[str, Any]],
        metric: str = "subscribers"
    ) -> go.Figure:
        """
        Create trend prediction chart with historical and predicted data.
        
        Args:
            historical_data: Historical data points
            predictions: Predicted future data points
            metric: Metric to visualize
        
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        # Historical data
        if historical_data:
            hist_df = pd.DataFrame(historical_data)
            if 'timestamp' in hist_df.columns and metric in hist_df.columns:
                fig.add_trace(go.Scatter(
                    x=hist_df['timestamp'],
                    y=hist_df[metric],
                    mode='lines+markers',
                    name='Historical',
                    line=dict(color='#4a9eff', width=2)
                ))
        
        # Predictions
        if predictions:
            pred_df = pd.DataFrame(predictions)
            if 'timestamp' in pred_df.columns and metric in pred_df.columns:
                fig.add_trace(go.Scatter(
                    x=pred_df['timestamp'],
                    y=pred_df[metric],
                    mode='lines+markers',
                    name='Predicted',
                    line=dict(color='#ffc107', width=2, dash='dash'),
                    marker=dict(symbol='diamond')
                ))
        
        # Add vertical line separating historical and predicted
        if historical_data and predictions:
            last_hist_date = pd.DataFrame(historical_data)['timestamp'].max()
            fig.add_vline(
                x=last_hist_date,
                line_dash="dot",
                line_color="gray",
                annotation_text="Now"
            )
        
        fig.update_layout(
            title=f"{metric.title()} Trend Prediction",
            xaxis_title="Date",
            yaxis_title=metric.title(),
            hovermode='x unified',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#fafafa')
        )
        
        return fig
    
    def create_metric_dashboard(
        self,
        metrics: Dict[str, Any],
        date_range: Optional[Tuple[datetime, datetime]] = None
    ) -> go.Figure:
        """
        Create comprehensive metric dashboard.
        
        Args:
            metrics: Dictionary of metric data
            date_range: Optional date range filter
        
        Returns:
            Plotly figure with subplots
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Subscribers', 'Views', 'Engagement Rate', 'Video Count'),
            specs=[[{"type": "scatter"}, {"type": "scatter"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # Subscribers
        if 'subscribers' in metrics:
            sub_data = metrics['subscribers']
            if isinstance(sub_data, list) and len(sub_data) > 0:
                sub_df = pd.DataFrame(sub_data)
                if 'timestamp' in sub_df.columns and 'value' in sub_df.columns:
                    fig.add_trace(
                        go.Scatter(x=sub_df['timestamp'], y=sub_df['value'], name='Subscribers'),
                        row=1, col=1
                    )
        
        # Views
        if 'views' in metrics:
            views_data = metrics['views']
            if isinstance(views_data, list) and len(views_data) > 0:
                views_df = pd.DataFrame(views_data)
                if 'timestamp' in views_df.columns and 'value' in views_df.columns:
                    fig.add_trace(
                        go.Scatter(x=views_df['timestamp'], y=views_df['value'], name='Views'),
                        row=1, col=2
                    )
        
        # Update layout
        fig.update_layout(
            title="Analytics Dashboard",
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#fafafa'),
            height=800
        )
        
        return fig
    
    def export_chart(
        self,
        fig: go.Figure,
        format: str = "png",
        filename: Optional[str] = None
    ) -> bytes:
        """
        Export chart to file.
        
        Args:
            fig: Plotly figure
            format: Export format (png, pdf, html, svg)
            filename: Optional filename
        
        Returns:
            File bytes
        """
        if format == "png":
            return fig.to_image(format="png", width=1200, height=600)
        elif format == "pdf":
            return fig.to_image(format="pdf", width=1200, height=600)
        elif format == "html":
            return fig.to_html().encode()
        elif format == "svg":
            return fig.to_image(format="svg", width=1200, height=600)
        else:
            raise ValueError(f"Unsupported format: {format}")


"""
Report Generator Module
Generate automated PDF reports.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
import os


class ReportGenerator:
    """
    Automated report generation with AGI-powered insights.
    
    AGI Paradigm: Continuous Learning Mechanism
    - Generates comprehensive reports
    - Tracks progress over time
    - Provides actionable insights
    """
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_channel_report(
        self,
        analysis_data: Dict[str, Any],
        filename: Optional[str] = None
    ) -> str:
        """
        Generate a comprehensive channel analysis report.
        
        Args:
            analysis_data: Channel analysis data from ChannelAnalyzer
            filename: Optional custom filename
        
        Returns:
            Path to generated PDF report
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"channel_report_{timestamp}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#1a1a1a"),
            spaceAfter=30
        )
        
        story.append(Paragraph("YouTube Channel Analysis Report", title_style))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
        story.append(Spacer(1, 0.3*inch))
        
        # Channel Info
        story.append(Paragraph("Channel Information", styles["Heading2"]))
        channel_info = analysis_data.get("channel_info", {})
        info_data = [
            ["Channel ID", channel_info.get("id", "N/A")],
            ["Title", channel_info.get("title", "N/A")],
            ["Created", channel_info.get("created", "N/A")[:10] if channel_info.get("created") else "N/A"]
        ]
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Statistics
        story.append(Paragraph("Statistics", styles["Heading2"]))
        stats = analysis_data.get("statistics", {})
        stats_data = [
            ["Metric", "Value"],
            ["Subscribers", f"{stats.get('subscribers', 0):,}"],
            ["Total Views", f"{stats.get('total_views', 0):,}"],
            ["Total Videos", stats.get("total_videos", 0)],
            ["Avg Views/Video", f"{stats.get('average_views_per_video', 0):,.0f}"],
            ["Views/Subscriber", f"{stats.get('views_per_subscriber', 0):,.1f}"]
        ]
        stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
        stats_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(stats_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Video Performance
        story.append(Paragraph("Video Performance", styles["Heading2"]))
        video_perf = analysis_data.get("video_performance", {})
        perf_text = f"""
        Total Videos: {video_perf.get('total_videos', 0)}
        Total Views: {video_perf.get('total_views', 0):,}
        Total Likes: {video_perf.get('total_likes', 0):,}
        Total Comments: {video_perf.get('total_comments', 0):,}
        Average Views: {video_perf.get('average_views', 0):,.0f}
        Engagement Rate: {video_perf.get('engagement_rate', 0):.2f}%
        """
        story.append(Paragraph(perf_text, styles["Normal"]))
        story.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        story.append(Paragraph("Recommendations", styles["Heading2"]))
        recommendations = analysis_data.get("recommendations", [])
        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", styles["Normal"]))
            story.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def generate_weekly_report(
        self,
        weekly_data: Dict[str, Any],
        filename: Optional[str] = None
    ) -> str:
        """Generate weekly performance report."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d")
            filename = f"weekly_report_{timestamp}.pdf"
        
        filepath = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        story.append(Paragraph("Weekly Performance Report", styles["Heading1"]))
        story.append(Paragraph(f"Week of: {datetime.now().strftime('%Y-%m-%d')}", styles["Normal"]))
        story.append(Spacer(1, 0.3*inch))
        
        # Add weekly data sections
        # ... (similar structure to channel report)
        
        doc.build(story)
        return filepath


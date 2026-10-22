import io
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_pdf_report(analysis: Dict[str, Any], job_title: str = "", company: str = "") -> bytes:
    """
    Generates an executive PDF report for the resume matching results.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#0B1020'),
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#8B5CF6'),
        spaceAfter=20
    )
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#121A2B'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['BodyText'],
        fontSize=10,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("ResumeMatch AI — Analysis Report", title_style))
    target_info = f"Target Role: {job_title or 'General Application'}"
    if company:
        target_info += f" | Company: {company}"
    story.append(Paragraph(target_info, subtitle_style))

    # Match Score Table
    score = analysis.get("overall_match_score", 0)
    score_data = [
        [Paragraph("<b>Overall ATS Match Score</b>", body_style), Paragraph(f"<b>{score} / 100</b>", body_style)]
    ]
    t = Table(score_data, colWidths=[350, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (-1, -1), 1, colors.HexColor('#8B5CF6'))
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph(analysis.get("summary", "N/A"), body_style))
    story.append(Spacer(1, 10))

    # Matched Skills
    story.append(Paragraph("Matched Qualifications & Skills", heading_style))
    matched = ", ".join(analysis.get("matched_skills", [])) or "None identified"
    story.append(Paragraph(matched, body_style))
    story.append(Spacer(1, 10))

    # Missing Skills
    story.append(Paragraph("Missing Core Requirements", heading_style))
    missing = ", ".join(analysis.get("missing_skills", [])) or "None identified"
    story.append(Paragraph(missing, body_style))
    story.append(Spacer(1, 10))

    # Actionable Improvements
    story.append(Paragraph("Recommended Resume Improvements", heading_style))
    for item in analysis.get("actionable_improvements", []):
        story.append(Paragraph(f"• {item}", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

import os
import re
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable
from reportlab.lib.styles import getSampleStyleSheet

REPORT_FOLDER = "reports"


def clean_text(text):
    text = text.replace("**", "")
    text = text.replace("*", "")
    return text


def split_sections(text):
    """Split AI response into sections"""
    sections = {
        "Overview": "",
        "Pros": [],
        "Cons": [],
        "Observations": []
    }

    text = clean_text(text)

    # Split sentences
    sentences = re.split(r'\.\s+', text)

    current = "Overview"

    for s in sentences:
        s = s.strip().lower()
        
        if any(word in s for word in ["pros", "advantages", "benefits", "strengths"]):
            current = "Pros"
            continue

        elif any(word in s for word in ["cons", "limitations", "issues", "drawbacks"]):
            current = "Cons"
            continue

        elif any(word in s for word in ["observation", "remarks", "notes"]):
            current = "Observations"
            continue

        if current == "Overview":
            sections["Overview"] += s + ". "

        else:
            sections[current].append(s)

    return sections


def create_pdf(data):

    os.makedirs(REPORT_FOLDER, exist_ok=True)

    vendor_name = data["vendor_name"]
    file_name = data["File_name"]
    comments = data["comments"]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    pdf_name = f"{vendor_name}_{timestamp}.pdf"
    file_path = os.path.join(REPORT_FOLDER, pdf_name)

    sections = split_sections(comments)

    styles = getSampleStyleSheet()
    content = []

    # Title
    content.append(Paragraph("AI Drawing Scrutiny Report", styles["Title"]))
    content.append(Spacer(1, 20))

    # Metadata
    content.append(Paragraph(f"<b>Vendor Name:</b> {vendor_name}", styles["Normal"]))
    content.append(Paragraph(f"<b>Drawing File:</b> {file_name}", styles["Normal"]))
    content.append(Spacer(1, 20))

    # Overview
    content.append(Paragraph("<b>Overview</b>", styles["Heading2"]))
    content.append(Paragraph(sections["Overview"], styles["Normal"]))
    content.append(Spacer(1, 15))

    # Pros
    if sections["Pros"]:
        content.append(Paragraph("<b>Advantages (Pros)</b>", styles["Heading2"]))
        bullets = [Paragraph(p, styles["Normal"]) for p in sections["Pros"]]
        content.append(ListFlowable(bullets, bulletType="bullet"))
        content.append(Spacer(1, 15))

    # Cons
    if sections["Cons"]:
        content.append(Paragraph("<b>Limitations (Cons)</b>", styles["Heading2"]))
        bullets = [Paragraph(c, styles["Normal"]) for c in sections["Cons"]]
        content.append(ListFlowable(bullets, bulletType="bullet"))
        content.append(Spacer(1, 15))

    # Observations
    if sections["Observations"]:
        content.append(Paragraph("<b>Additional Observations</b>", styles["Heading2"]))
        bullets = [Paragraph(o, styles["Normal"]) for o in sections["Observations"]]
        content.append(ListFlowable(bullets, bulletType="bullet"))

    pdf = SimpleDocTemplate(file_path)
    pdf.build(content)

    return pdf_name
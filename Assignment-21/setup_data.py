"""
setup_data.py - Dataset Setup (mandatory step)

Creates the sample files that go with Movie_recommendation.csv:
  data/notes.txt              -> one .txt file (notes / explanation)
  data/company_handbook.pdf   -> one .pdf file (small 3-page document)
  extra/handbook.md           -> markdown file used only by Task 9

These files are already included in the project. Run this script only if you want to
regenerate them (the PDF needs the optional package:  pip install reportlab).

Run:  python setup_data.py
"""

import os

from config import DATA_DIR, EXTRA_DIR, MD_FILE, PDF_FILE, TXT_FILE

NOTES = """Personal Knowledge Assistant - Study Notes

A Personal Knowledge Assistant is a GenAI system that answers questions from your own data instead of only from what a language model learned during training. The data can be company documents, personal notes, CSV tables, PDF files and website pages.

Before any question can be answered, the data has to be prepared. This preparation has two steps. The first step is loading: a document loader reads a file or a webpage and converts it into a Document object that holds the text (page_content) and extra information about it (metadata) such as the file path or the page number.

The second step is splitting. A large document is cut into smaller chunks because language models have a limited context window, and because a small, focused chunk is easier to match with a question than a whole book. Each chunk should be big enough to carry a complete idea, but small enough to stay focused on one topic.

Chunk overlap means that the end of one chunk is repeated at the start of the next chunk. Overlap protects sentences and ideas that would otherwise be cut in half at a chunk boundary. A typical setting is an overlap of ten percent of the chunk size.

There are several families of text splitters. Length-based splitters cut text after a fixed number of characters or tokens. Structure-based splitters try to cut at natural boundaries such as paragraphs, sentences and words. Document-structure splitters follow headers in Markdown or pages in a PDF. Semantic splitters use embeddings to cut the text where the meaning changes.

Good ingestion is the foundation of retrieval augmented generation. If the chunks are poor, even the best language model will return poor answers. This is why loading and splitting must be understood before building any RAG application or chatbot.
"""

HANDBOOK_PAGES = [
    (
        "1. Company Overview",
        [
            "NovaTech Solutions is a software company that builds data and AI products for retail and healthcare customers. The company was founded in 2015 and today has about four hundred employees working from offices in Pune, Bengaluru and Remote locations.",
            "Our mission is to turn raw data into decisions that people can trust. We do this by combining careful engineering, clear documentation and a culture where every team member can ask questions and challenge assumptions.",
            "The company is organised into four divisions: Product Engineering, Data Science, Customer Success and Operations. Each division has its own lead, and all leads report to the Chief Executive Officer.",
        ],
    ),
    (
        "2. Leave and Work Policy",
        [
            "Every full-time employee receives twenty-four paid leave days per calendar year, in addition to public holidays. Unused leave of up to ten days can be carried forward to the next year. Leave requests must be submitted through the HR portal at least three working days in advance, except in emergencies.",
            "The standard working week is Monday to Friday. Employees may work from home up to three days a week with the approval of their manager. Core collaboration hours are between eleven in the morning and four in the afternoon so that teams can meet and pair on tasks.",
            "Sick leave is separate from paid leave. Employees receive twelve sick days per year and a medical certificate is required for absences longer than two consecutive days.",
        ],
    ),
    (
        "3. IT and Security Guidelines",
        [
            "All company laptops must use full disk encryption and a screen lock that activates after five minutes of inactivity. Passwords must be at least fourteen characters long and must be stored in the approved password manager. Multi-factor authentication is mandatory for email, source code and cloud accounts.",
            "Confidential customer data must never be copied to personal devices or sent through personal email. Any suspected security incident, such as a lost laptop or a phishing email, must be reported to the security team within one hour using the incident form.",
            "Software that is not on the approved list needs a written request to the IT team. New tools are reviewed for licensing, data privacy and security before they are allowed on company machines.",
        ],
    ),
]

HANDBOOK_MD = """# Employee Handbook

NovaTech Solutions handbook for new and existing employees.

## Company Overview

NovaTech Solutions builds data and AI products for retail and healthcare customers. The company has about four hundred employees in Pune, Bengaluru and remote locations.

### Mission

Our mission is to turn raw data into decisions that people can trust, using careful engineering and clear documentation.

### Divisions

The company has four divisions: Product Engineering, Data Science, Customer Success and Operations.

## Leave Policy

Every full-time employee receives twenty-four paid leave days per calendar year. Unused leave of up to ten days can be carried forward.

### Requesting Leave

Leave requests are submitted through the HR portal at least three working days in advance, except in emergencies.

### Sick Leave

Employees receive twelve sick days per year. A medical certificate is required for absences longer than two consecutive days.

## IT and Security

All laptops must use full disk encryption and multi-factor authentication is mandatory for email, source code and cloud accounts.

### Reporting Incidents

Any suspected security incident, such as a lost laptop or phishing email, must be reported to the security team within one hour.
"""


def create_notes():
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        f.write(NOTES)


def create_markdown():
    with open(MD_FILE, "w", encoding="utf-8") as f:
        f.write(HANDBOOK_MD)


def create_pdf():
    try:
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer
    except ImportError:
        print("reportlab is not installed -> skipped PDF (pip install reportlab).")
        return

    styles = getSampleStyleSheet()
    story = []
    for number, (heading, paragraphs) in enumerate(HANDBOOK_PAGES):
        if number > 0:
            story.append(PageBreak())
        story.append(Paragraph(heading, styles["Heading1"]))
        story.append(Spacer(1, 12))
        for text in paragraphs:
            story.append(Paragraph(text, styles["BodyText"]))
            story.append(Spacer(1, 10))

    doc = SimpleDocTemplate(PDF_FILE, pagesize=A4, title="NovaTech Company Handbook")
    doc.build(story)


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(EXTRA_DIR, exist_ok=True)
    create_notes()
    create_markdown()
    create_pdf()
    print("Created:", TXT_FILE)
    print("Created:", PDF_FILE)
    print("Created:", MD_FILE)
    print("Dataset CSV expected at: data/Movie_recommendation.csv")

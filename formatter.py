import re

# 🏷️ Clause Tagging Logic

def tag_clause(header: str) -> str:
    h = header.lower()
    if "confidential" in h:
        return "confidentiality"
    elif "term" in h:
        return "term"
    elif "jurisdiction" in h or "governing law" in h:
        return "jurisdiction"
    elif "exceptions" in h:
        return "exceptions"
    elif "return" in h or "destruction" in h:
        return "data_handling"
    elif "signator" in h:
        return "signatories"
    elif "entire" in h:
        return "entire_agreement"
    elif "introduction" in h:
        return "introduction"
    elif "title" in h:
        return "title"
    else:
        return "misc"


# 🨹 Step 1: Clean raw model output

def clean_contract_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r' +\n', '\n', text)
    text = re.sub(r'\n +', '\n', text)
    text = re.sub(r'—+', '—', text)
    return text


# 🧱 Step 2: Format clause titles

def emphasize_titles(text: str) -> str:
    lines = text.split("\n")
    section_num = 1
    formatted = []
    for line in lines:
        if re.match(r'^\.* ?[A-Z][A-Z ]{3,}$', line.strip()):
            title = line.strip().lstrip('. ').strip()
            formatted.append(f"\n{section_num}. {title.upper()}\n")
            section_num += 1
        else:
            formatted.append(line)
    return "\n".join(formatted)


# 📄 Step 3: Indent subclauses

def format_subclauses(text: str) -> str:
    return re.sub(r'\n([A-Da-d])\. ', r'\n    \1. ', text)


# • Step 4: Format bullets

def format_bullets(text: str) -> str:
    return re.sub(r'\n[-•]\s+', r'\n    • ', text)


# ✍️ Step 5: Add signature block

def add_signature_block() -> str:
    return """
============================================================

SIGNATORIES:

This Agreement shall be executed by _______________________ on behalf of Company 1  
and _______________________ on behalf of Company 2, and delivered as of the date written above.

OWNER:  
By: _______________________        Date: _______________

RECIPIENT:  
By: _______________________        Date: _______________
"""


# 🎯 Step 6: Apply full formatting pipeline

def format_contract(text: str) -> str:
    text = clean_contract_text(text)
    text = emphasize_titles(text)
    text = format_subclauses(text)
    text = format_bullets(text)
    text += add_signature_block()
    return text


# 📦 Step 7: Format contract into clause-level dicts with tags

def format_sections(text: str) -> list:
    sections = text.strip().split("\n\n")
    formatted = []

    for section in sections:
        first_line = section.split("\n")[0] if "\n" in section else section
        tag = tag_clause(first_line)
        formatted.append({
            "tag": tag,
            "text": section.strip()
        })

    return formatted


# ✅ Step 8: Check if contract is valid

def is_contract_ready(text: str) -> bool:
    if text.startswith("❌"):
        return False
    keywords = ["agreement", "confidential", "parties", "terms", "termination", "jurisdiction"]
    return all(k.lower() in text.lower() for k in keywords)

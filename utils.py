import re

PII_PATTERNS = {
    "full_name": r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+(?:[-][A-Z][a-z]+)?)+)\b",
    "email": r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
    "phone_number": r"\b\d{10}\b",
    "dob": r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",
    "aadhar_num": r"\b\d{4}\s\d{4}\s\d{4}\b",
    "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
    "cvv_no": r"\b\d{3}\b",
    "expiry_no": r"\b(0[1-9]|1[0-2])\/\d{2,4}\b"
}

COMMON_PHRASES = {"Dear Customer", "Customer Support", "Technical Support"}

def mask_pii(text):
    entities = []
    matches = []

    # Collect all matches with original positions
    for entity_type, pattern in PII_PATTERNS.items():
        for match in re.finditer(pattern, text):
            matched_text = match.group()

            # Skip if the matched text is a common phrase
            if any(phrase in matched_text for phrase in COMMON_PHRASES):
                continue

            matches.append({
                "start": match.start(),
                "end": match.end(),
                "entity": matched_text,
                "classification": entity_type
            })

    # Sort matches by start index (important to avoid overlap issues)
    matches.sort(key=lambda x: x["start"])

    # Mask entities in the text, adjusting indices as we go
    masked_text = text
    offset = 0
    for m in matches:
        start = m["start"] + offset
        end = m["end"] + offset
        replacement = f"[{m['classification']}]"
        masked_text = masked_text[:start] + replacement + masked_text[end:]
        offset += len(replacement) - (m["end"] - m["start"])

        entities.append({
            "position": [m["start"], m["end"]],
            "classification": m["classification"],
            "entity": m["entity"]
        })

    return masked_text, entities

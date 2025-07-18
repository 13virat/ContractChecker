def extract_clauses(text):
    import re
    clauses = {}
    lines = text.splitlines()
    current_title = None
    current_body = []
    for line in lines:
        if re.match(r'^\d+[\.\)]?\s+', line):  # e.g., 1. Title or 1) Title
            if current_title:
                clauses[current_title] = "\n".join(current_body).strip()
            current_title = line.strip()
            current_body = []
        else:
            current_body.append(line)
    if current_title:
        clauses[current_title] = "\n".join(current_body).strip()
    return clauses

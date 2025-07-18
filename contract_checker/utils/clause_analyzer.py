from utils.ollama import call_ollama
from utils.section_extractor import extract_clauses_by_llm as extract_clauses_by_section


# Wrapper for LLM prompt (Ollama)
def query_llm(prompt):
    return call_ollama(prompt)

# Main function to analyze clause differences
def analyze_contract_diff(old_text, new_text):
    old_sections = extract_clauses_by_section(old_text)
    new_sections = extract_clauses_by_section(new_text)

    diff_report = []
    red_flags = []

    for clause in set(old_sections) | set(new_sections):
        old_clause = old_sections.get(clause, "")
        new_clause = new_sections.get(clause, "")

        if old_clause != new_clause:
            prompt = (
                f"🔍 Analyze the legal risk of this clause change:\n\n"
                f"📄 Old Clause:\n{old_clause}\n\n"
                f"🆕 New Clause:\n{new_clause}\n\n"
                f"Explain what changed, any risk introduced, and why it matters in simple legal terms."
            )
            explanation = query_llm(prompt)

            diff_report.append({
                "clause": clause,
                "old": old_clause,
                "new": new_clause,
                "explanation": explanation
            })

    # Red Flag Check
    required_clauses = {"Indemnity", "Termination", "Confidentiality"}
    missing = required_clauses - set(new_sections.keys())

    for clause in missing:
        red_flags.append(f"🚨 Alert: Missing key clause – {clause}")

    return {
        "differences": diff_report,
        "red_flags": red_flags
    }

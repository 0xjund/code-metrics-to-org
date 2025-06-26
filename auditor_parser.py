import re
import os

# --- Regex patterns ---
heading_pattern = re.compile(r"^##\s+(.*)")
table_pattern = re.compile(r"((?:\|.*\n)+)", re.MULTILINE)

def remove_pre_content_lines(text):
    #Removes lines before the first heading
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("##"):
            return "\n".join(lines[i:])
    return text  # fallback if no headings found

def extract_sections(output_text):
    lines = output_text.splitlines()
    i = 0
    sections = []
    current_section = None

    while i < len(lines):
        line = lines[i]

        # Detect Section Headings
        heading_match = heading_pattern.match(line)
        if heading_match:
            current_section = heading_match.group(1).strip()
            i += 1
            continue

        # Detect Tables
        table_match = table_pattern.match(line)
        if table_match:
            table_text = table_match.group(1)
            if current_section:
                sections.append((current_section, clean_table(table_text)))
                i += table_text.count("\n") + 1
                continue

        i += 1

    return sections

def clean_output(output_text):
    # Remove blocks
    block_patterns = [
        r"<div.*?</div>", r"<canvas.*?</canvas>", r"<sub>.*?</sub>",
    ]
    for pattern in block_patterns:
        output_text = re.sub(pattern, "", output_text, flags=re.DOTALL)

    # Remove inline HTML tags
    output_text = re.sub(r"<[^>]+>", "", output_text)

    # Remove markdown links  [](...) and [(...)]
    output_text = re.sub(r"\[\s*\]\(.*?\)", "", output_text)  # empty link
    output_text = re.sub(r"\[\(.*?\)\]", "", output_text)     # icon cluster

    # Remove duplicate newlines
    output_text = re.sub(r"\n\s*\n", "\n", output_text)

    # Convert markdown headings (##, ###, etc.) to Org stars (**)
    def convert_heading(line):
        match = re.match(r'^(#+)\s+(.*)', line)
        if match:
            hashes, title = match.groups()
            return f"{'*' * len(hashes)} {title}"
        return line

    lines = output_text.strip().split('\n')
    lines = [convert_heading(line) for line in lines if not re.match(r"^\[\s*\(.*?\)\]$", line)]

    return "\n".join(lines)

def clean_table(table_text):
    # Clean up the MD tables to work better in Org
    # Remove <abbr> and similar tags
    table_text = re.sub(r"<abbr[^>]*>(.*?)</abbr>", r"\1", table_text)
    table_text = re.sub(r"<.*?>", "", table_text)
    return table_text.strip()

def write_to_org(sections, org_path):
    with open(org_path, "a") as f:
        for title, table in sections:
            f.write(f"* {title}\n\n")
            f.write("#+BEGIN_SRC org\n")
            f.write(table + "\n")
            f.write("#+END_SRC\n\n")

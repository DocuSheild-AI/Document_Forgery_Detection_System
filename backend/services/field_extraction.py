import re

def extract_fields(full_text):
    try:
        text = full_text.lower()

        fields = {
            "name": None,
            "marks": [],
            "board": None
        }

        # Extract name (simple heuristic)
        name_match = re.search(r'name[:\s]+([a-z\s]+)', text)
        if name_match:
            fields["name"] = name_match.group(1).strip()

        # Extract board
        if "board" in text:
            fields["board"] = "present"

        # Extract marks (numbers near marks/grade)
        marks_matches = re.findall(r'(?:marks|score|grade)[^\d]*(\d{1,3})', text)

        for m in marks_matches:
            fields["marks"].append(int(m))

        return fields

    except Exception as e:
        return {"error": str(e)}
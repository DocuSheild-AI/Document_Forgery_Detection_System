def run_rule_based_validation(fields, domain):
    try:
        issues = []
        strong_flag = False

        if domain == "education_certificate":

            # 🔥 Check marks properly
            for mark in fields.get("marks", []):
                if mark > 100:
                    issues.append(f"Invalid marks: {mark}")
                    strong_flag = True

            # Check board
            if not fields.get("board"):
                issues.append("Missing board")

        return {
            "issues": issues,
            "strong_violation": strong_flag,
            "result": "Violation Found" if strong_flag else "OK",
            "suspicious": strong_flag
        }

    except Exception as e:
        return {"error": str(e)}
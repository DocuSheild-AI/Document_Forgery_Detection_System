def run_template_matching(full_text, domain):
    try:
        text = full_text.lower()

        score = 0
        total_checks = 0

        # EDUCATION CERTIFICATE TEMPLATE
        if domain == "education_certificate":

            checks = [
                "certificate",
                "marks",
                "name",
                "board",
                "grade",
                "roll"
            ]

        elif domain == "id_card":

            checks = [
                "name",
                "dob",
                "id",
                "government"
            ]

        elif domain == "invoice":

            checks = [
                "invoice",
                "amount",
                "total",
                "date"
            ]

        else:
            checks = []

        total_checks = len(checks)

        for word in checks:
            if word in text:
                score += 1

        # Calculate match percentage
        if total_checks > 0:
            match_percentage = (score / total_checks) * 100
        else:
            match_percentage = 0

        # Decision
        if match_percentage < 50:
            result = "Template Mismatch"
            suspicious = True
        else:
            result = "Template Matched"
            suspicious = False

        return {
            "match_score": round(match_percentage, 2),
            "result": result,
            "suspicious": suspicious
        }

    except Exception as e:
        return {"error": str(e)}
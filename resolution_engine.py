def suggest_resolution(issue_type, root_cause, analysis):
    # Transaction-level resolutions
    if issue_type == "Transaction Level Issue":

        if not analysis:
            return ["Manual investigation required"]

        summary = analysis.get("summary", "").lower()
        cause = root_cause.get("cause", "").lower()

        if "insufficient balance" in summary:
            return [
                "Inform customer about insufficient balance",
                "Retry transaction after balance correction"
            ]

        if "timeout" in cause:
            return [
                "Check network connectivity",
                "Retry transaction after system stabilization"
            ]

        if "duplicate" in cause:
            return [
                "Verify duplicate entry in transaction table",
                "Reverse duplicate transaction if posted"
            ]

    # Batch-level resolutions
    if issue_type == "Batch Level Issue":
        return [
            "Re-run failed batch",
            "Check batch scheduler logs",
            "Validate input file format"
        ]

    # Default fallback
    return ["Manual investigation required"]

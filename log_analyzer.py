def analyze_logs(issue_type, user_issue, logs):

    result = {
        "summary": None,
        "errors_found": []
    }

    if logs is None:
        return result

    logs = logs.lower()

    if "timeout" in logs:
        result["errors_found"].append("Timeout error detected")
        result["summary"] = "System timeout observed in logs"

    if "database" in logs or "db" in logs:
        result["errors_found"].append("Database connectivity issue")
        result["summary"] = "Database related error observed"

    if "failed" in logs:
        result["errors_found"].append("Transaction failure recorded")
        result["summary"] = "Transaction failure detected in logs"

    if "api" in logs:
        result["errors_found"].append("API failure detected")
        result["summary"] = "API service failure observed"

    if not result["summary"]:
        result["summary"] = "No critical errors detected in logs"

    return result
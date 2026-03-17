from error_code_kb import ERROR_CODE_KB


def analyze_root_cause(issue_type, user_issue, analysis=None, log_analysis=None):

    # 🔹 Error-code driven RCA (Highest Priority)
    if isinstance(analysis, dict) and "error_code" in analysis:
        error_code = analysis["error_code"]

        if error_code in ERROR_CODE_KB:
            return {
                "cause": ERROR_CODE_KB[error_code]["cause"],
                "severity": ERROR_CODE_KB[error_code]["severity"],
                "owner": ERROR_CODE_KB[error_code]["owner"]
            }

    # 🔹 Log-driven RCA (L2 investigation)
    if log_analysis:
        summary = log_analysis.get("summary", "").lower()

        if "database" in summary:
            return {
                "cause": "Database connectivity issue",
                "severity": "High",
                "owner": "DB Support"
            }

        if "api" in summary:
            return {
                "cause": "External API service failure",
                "severity": "Medium",
                "owner": "Integration Team"
            }

        if "timeout" in summary:
            return {
                "cause": "System timeout due to backend delay",
                "severity": "High",
                "owner": "Application Support"
            }

    # 🔹 Fallback generic RCA
    if "failed" in user_issue.lower():
        return {
            "cause": "Transaction failure due to system issue",
            "severity": "Medium",
            "owner": "L2"
        }

    # 🔹 Default case
    return {
        "cause": "General inquiry",
        "severity": "Low",
        "owner": "L1"
    }
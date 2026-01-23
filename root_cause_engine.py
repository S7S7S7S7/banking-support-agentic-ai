from error_code_kb import ERROR_CODE_KB

def analyze_root_cause(issue_type, user_issue, analysis=None):
    # 🔹 Error-code driven RCA
    if isinstance(analysis, dict) and "error_code" in analysis:
        error_code = analysis["error_code"]

        if error_code in ERROR_CODE_KB:
            return {
                "cause": ERROR_CODE_KB[error_code]["cause"],
                "severity": ERROR_CODE_KB[error_code]["severity"],
                "owner": ERROR_CODE_KB[error_code]["owner"]
            }

    # 🔹 Fallback generic RCA
    if "failed" in user_issue.lower():
        return {
            "cause": "Transaction failure due to system issue",
            "severity": "Medium",
            "owner": "L2"
        }

    return {
        "cause": "General inquiry",
        "severity": "Low",
        "owner": "L1"
    }

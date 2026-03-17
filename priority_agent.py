def assign_priority(issue_type, root_cause, analysis, context):

    severity = root_cause.get("severity", "Low")
    txn_id = context.get("txn_id")

    priority = "P4"
    reason = "Low impact issue"

    # Critical system issues
    if severity == "Critical":
        priority = "P1"
        reason = "Critical system impact"

    # High severity problems
    elif severity == "High":
        priority = "P2"
        reason = "High impact issue affecting operations"

    # Medium issues
    elif severity == "Medium":
        if txn_id:
            priority = "P3"
            reason = "Single transaction issue"
        else:
            priority = "P2"
            reason = "Multiple transactions may be affected"

    # Low severity
    else:
        priority = "P4"
        reason = "Minor issue with minimal impact"

    return {
        "priority": priority,
        "reason": reason
    }
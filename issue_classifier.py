def classify_issue(text):
    text = text.lower()

    if "not posted" in text:
        return "POSTING_FAILURE"
    if "stuck" in text or "pending" in text:
        return "STATUS_PENDING"
    if "batch" in text:
        return "BATCH_ISSUE"
    if "failed" in text:
        return "TRANSACTION_FAILURE"

    return "UNKNOWN"

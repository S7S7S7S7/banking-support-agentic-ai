def ask_followup(issue_type, text):
    questions = []

    if issue_type in ["POSTING_FAILURE", "STATUS_PENDING"]:
        if "txn" not in text:
            questions.append("Please provide the Transaction ID.")

    if issue_type == "BATCH_ISSUE":
        if "batch" not in text:
            questions.append("Please provide the batch name.")

    return questions

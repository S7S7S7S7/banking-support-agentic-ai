import re

def extract_context(user_text, context):

    txn_match = re.search(r"txn\s*id\s*(\d+)", user_text, re.IGNORECASE)
    if txn_match:
        context["txn_id"] = txn_match.group(1)

    batch_match = re.search(r"batch\s*([\w_]+)", user_text, re.IGNORECASE)
    if batch_match:
        context["batch_name"] = batch_match.group(1)

    return context

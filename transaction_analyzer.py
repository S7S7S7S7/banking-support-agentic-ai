def analyze_transaction(issue_type, user_issue, txn_id, df):

    if df is None:
        return {"summary": "No transaction data available"}

    txn = df[df["txn_id"] == txn_id]

    if txn.empty:
        return {"summary": "Transaction not found"}

    row = txn.iloc[0]

    return {
        "summary": f"Transaction {txn_id} status: {row['status']}",
        "status": row["status"],
        "error_code": row.get("error_code", None),
        "module": str(row.get("module", row.get("service", "Unknown")))
    }

    # 🔹 Issue-based fallback
    failed = df[df["status"] == "FAILED"]

    if failed.empty:
        return "No failed transactions found."

    return {
        "failed_count": len(failed),
        "error_codes": failed["error_code"].value_counts().to_dict()
    }

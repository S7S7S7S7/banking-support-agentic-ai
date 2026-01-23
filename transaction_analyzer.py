def analyze_transaction(issue_type, user_issue, txn_id=None, df=None):

    if df is None or df.empty:
        return "No transaction data available."

    # 🔹 TXN-ID based analysis
    if txn_id:
        txn_df = df[df["txn_id"] == txn_id]

        if txn_df.empty:
            return f"No transaction found for TXN ID: {txn_id}"

        row = txn_df.iloc[0]
        return {
                "txn_id": str(row["txn_id"]),
                "status": str(row["status"]),
                "error_code": str(row["error_code"]),
                "amount": int(row["amount"]),
                "module": str(row["module"])
        }

    # 🔹 Issue-based fallback
    failed = df[df["status"] == "FAILED"]

    if failed.empty:
        return "No failed transactions found."

    return {
        "failed_count": len(failed),
        "error_codes": failed["error_code"].value_counts().to_dict()
    }

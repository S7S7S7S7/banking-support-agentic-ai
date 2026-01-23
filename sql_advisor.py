def suggest_sql(issue_type, ticket_context):
    txn_id = ticket_context.get("txn_id")
    batch_name = ticket_context.get("batch_name")

    queries = []

    if issue_type == "Transaction Level Issue" and txn_id:
        queries.append(f"""
-- Verify transaction status
SELECT txn_id, status, error_code, error_message
FROM transactions
WHERE txn_id = '{txn_id}';
""")

        queries.append(f"""
-- Check account balance at time of transaction
SELECT account_id, available_balance
FROM accounts
WHERE account_id = (
    SELECT account_id FROM transactions WHERE txn_id = '{txn_id}'
);
""")

        queries.append(f"""
-- Check posting logs
SELECT txn_id, posted_flag, posted_date
FROM posting_log
WHERE txn_id = '{txn_id}';
""")

    elif issue_type == "Batch Level Issue" and batch_name:
        queries.append(f"""
-- Check batch execution status
SELECT batch_name, status, start_time, end_time
FROM batch_control
WHERE batch_name = '{batch_name}';
""")

        queries.append("""
-- Identify failed records in batch
SELECT *
FROM batch_error_log
WHERE batch_name = :batch_name;
""")

    else:
        queries.append("""
-- General system error check
SELECT *
FROM system_error_log
WHERE error_date >= SYSDATE - 1;
""")

    return "\n".join(queries)

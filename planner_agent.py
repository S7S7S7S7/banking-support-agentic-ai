def plan_actions(issue_type, ticket_context):
    """
    Rule-based planner (LLM will replace/enhance this later)
    """

    plan = {
        "need_followup": False,
        "run_transaction_analysis": False,
        "run_root_cause": True,
        "run_sql": True,
        "owner": "L2"
    }

    if issue_type in ["Payment Failure", "EMI Failure"]:
        plan["run_transaction_analysis"] = True
        plan["owner"] = "L3"

    if not ticket_context.get("txn_id"):
        plan["need_followup"] = True

    return plan

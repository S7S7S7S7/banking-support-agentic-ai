import pandas as pd
import streamlit as st
from issue_classifier import classify_issue
from followup_question import ask_followup
from transaction_analyzer import analyze_transaction
from resolution_engine import suggest_resolution
from sql_advisor import suggest_sql
from root_cause_engine import analyze_root_cause
from context_extractor import extract_context
from llm_reasoner import llm_reason
from planner_agent import plan_actions
import os 

USE_LLM = bool(os.getenv("OPENAI_API_KEY"))

if "ticket_context" not in st.session_state:
    st.session_state.ticket_context = {
        "issue_type": None,
        "txn_id": None,
        "batch_name": None,
        "severity": None,
        "owner": None
    }

st.set_page_config(page_title="Banking Agentic AI")

st.title("🏦 Banking Production Support – AI Agent")
st.write("Agentic AI for L1 / L2 / L3 Support")

uploaded_file = st.file_uploader(
    "Upload Transaction Data (CSV)",
    type=["csv"]
)

def generate_ai_reasoned_explanation(issue_type, analysis, root_cause, resolution):
    explanation = []

    explanation.append(
        f"The issue has been classified as a {issue_type} based on the provided context."
    )

    if analysis and isinstance(analysis, dict):
        summary = analysis.get("summary")
        if summary:
            explanation.append(f"Analysis indicates that {summary}.")

    if root_cause:
        cause = root_cause.get("cause")
        if cause:
            explanation.append(f"The identified root cause is {cause}.")

        severity = root_cause.get("severity")
        owner = root_cause.get("owner")
        if severity and owner:
            explanation.append(
                f"The issue severity is assessed as {severity} and assigned to {owner} support."
            )

    if resolution:
        explanation.append(
            "The recommended resolution steps directly address the identified cause "
            "and are expected to prevent recurrence."
        )

    return " ".join(explanation)

if uploaded_file:
    st.session_state["txn_df"] = pd.read_csv(uploaded_file)
    st.success("Transaction data uploaded successfully")
    
    st.subheader("🧪 Uploaded Transaction Data")
    st.dataframe(st.session_state.get("txn_df"))

user_issue = st.text_area("Describe the production issue")
txn_id_input = st.text_input("Transaction ID")

if user_issue:
    # 🔹 Update ticket memory first
    st.session_state.ticket_context = extract_context(
        user_issue,
        st.session_state.ticket_context
    )

    # 🔹 Capture TXN ID
    if txn_id_input:
        st.session_state.ticket_context["txn_id"] = txn_id_input

    # 🔹 Determine issue type (TXN-first logic)
    if st.session_state.ticket_context.get("txn_id"):
        issue_type = "Transaction Level Issue"
    else:
        issue_type = classify_issue(user_issue)

    # 🔹 Planner runs AFTER context is ready
    plan = plan_actions(issue_type, st.session_state.ticket_context)

    if plan["need_followup"]:
        st.subheader("❓ Additional Information Required")
        for q in ask_followup(issue_type, user_issue):
            st.write(f"- {q}")

    else:
        analysis = None

        txn_id = st.session_state.ticket_context.get("txn_id")

        if txn_id:
            analysis = analyze_transaction(issue_type,user_issue,txn_id,
                        st.session_state.get("txn_df"))
        elif plan["run_transaction_analysis"]:
            analysis = analyze_transaction(issue_type,user_issue,None,
                            st.session_state.get("txn_df"))

        sql_checks = suggest_sql(issue_type,st.session_state.ticket_context)
        # root_cause = analyze_root_cause(issue_type, user_issue)
        root_cause = analyze_root_cause(issue_type, user_issue, analysis)
        resolution = suggest_resolution(issue_type, root_cause, analysis)

        # 🤖 AI Reasoned Explanation (Rule-based default)
        ai_explanation = generate_ai_reasoned_explanation(
                         issue_type,analysis,root_cause,resolution)

        # Optional LLM enhancement (polish only)
        if USE_LLM:
            enhanced = llm_reason(issue_type,analysis,resolution,
                            st.session_state.ticket_context)
            if enhanced:
                ai_explanation = enhanced
            
        # st.subheader("🧪 Uploaded Transaction Data")
        # st.dataframe(st.session_state.get("txn_df"))

        st.subheader("🔍 Issue Type")
        st.write(issue_type)

        st.subheader("📊 Analysis")
        if analysis:
            st.write(analysis)
        else:
            st.warning("No analysis available yet.")

        st.subheader("🛠️ Resolution")
        for step in resolution:
            st.write(f"- {step}")

        st.subheader("🤖 AI Reasoned Explanation")
        st.write(ai_explanation)

        st.subheader("🧾 SQL Diagnostic Suggestions (Read-Only)")
        st.code(sql_checks, language="sql")

        st.subheader("🧠 Root Cause Analysis")
        st.write(f"Cause: {root_cause['cause']}")
        st.write(f"Severity: {root_cause['severity']}")
        st.write(f"Owner: {root_cause['owner']}")

        st.session_state.ticket_context["issue_type"] = issue_type
        st.session_state.ticket_context["severity"] = root_cause["severity"]
        st.session_state.ticket_context["owner"] = root_cause["owner"]

        st.subheader("🗂️ Ticket Context (Session Memory)")
        st.json(st.session_state.ticket_context)
        


ERROR_CODE_KB = {
    "E101": {
        "cause": "Network timeout during transaction posting",
        "severity": "High",
        "owner": "L3",
        "resolution": "Retry transaction or check network connectivity"
    },
    "E205": {
        "cause": "Insufficient balance during EMI debit",
        "severity": "Medium",
        "owner": "L2",
        "resolution": "Notify customer and retry after balance update"
    },
    "E301": {
        "cause": "Duplicate transaction detected",
        "severity": "Low",
        "owner": "L1",
        "resolution": "No action required, monitor transaction"
    }
}

# Define a function to highlight the "Total" row
def highlight_total_row(row):
    if row["Material"] == "Total":
        return ['background-color: lightgrey'] * len(row)
    else:
        return [''] * len(row)
    
def status_icon(percent):
    if percent >= 95:
        return f"🟢 {percent:,.2f}%"  # Green circle
    elif percent >= 85:
        return f"🟡 {percent:,.2f}%"  # Orange circle
    else:
        return f"🔴 {percent:,.2f}%"  # Red circle
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
    
def color(product) :
    color_dict = {
        "PERTALITE" : "#23B200",
        "PERTAMAX" : "#076BCB",
        "PERTAMAX TURBO" : "#D9201E",
        "PERTAMAX GREEN" : "#631ED1",
        "BIOSOLAR" : "#707070",
        "DEXLITE" : "#25AB25",
        "PERTAMINA DEX" : "#03583B",
        "LPG PSO 3 KG" : "#92D14F",
        "LPG NPSO 5,5 KG" : "#FF66FF",
        "LPG NPSO 12 KG": "#63A4F6",
        "LPG NPSO 50 KG" : "#FE0000",
        "BULK" : "#D9D9D9",
        "BG Can" : "#D01971",
        "Musicool" : "#27B24B",
        "Total" : "#000000"
    }

    return color_dict.get(product, "#000000")
# Project Gaurav - Module 2 Auto Dashboard
# Prepared for: Soni Maurya
# Install: pip install pandas openpyxl

import pandas as pd
from datetime import datetime

# 1. LEAD TRACKER DATA - Yahan tum roz naye leads add karogi
leads = [
    {
        "Lead ID": "L001", "Date Added": "2026-11-01",
        "Prospect Name": "Amit Sharma", "Company": "TechStart Pvt",
        "Designation": "CEO", "Industry": "IT",
        "LinkedIn Profile URL": "linkedin.com/in/amit",
        "Connection Date": "2026-11-01", "Connection Status": "Accepted",
        "Initial Message Date": "2026-11-02", "Message Status": "Sent",
        "Response Status": "Interested", "Lead Priority": "High",
        "Last Contact Date": "2026-11-02", "Next Follow-up Date": "2026-11-05",
        "Lead Stage": "Interested", "Lead Source": "LinkedIn Search",
        "Notes": "Good potential"
    },
    {
        "Lead ID": "L002", "Date Added": "2026-11-01",
        "Prospect Name": "Neha Gupta", "Company": "InfoSys Solutions",
        "Designation": "Operations Manager", "Industry": "Corporate",
        "LinkedIn Profile URL": "linkedin.com/in/neha",
        "Connection Date": "2026-11-01", "Connection Status": "Pending",
        "Initial Message Date": "", "Message Status": "Not Sent",
        "Response Status": "No Response", "Lead Priority": "Medium",
        "Last Contact Date": "", "Next Follow-up Date": "2026-11-04",
        "Lead Stage": "Connection Pending", "Lead Source": "LinkedIn Search",
        "Notes": ""
    },
    {
        "Lead ID": "L003", "Date Added": "2026-11-02",
        "Prospect Name": "Raj Verma", "Company": "Manufacture Co",
        "Designation": "Founder", "Industry": "Manufacturing",
        "LinkedIn Profile URL": "linkedin.com/in/raj",
        "Connection Date": "2026-11-02", "Connection Status": "Accepted",
        "Initial Message Date": "2026-11-03", "Message Status": "Sent",
        "Response Status": "Interested", "Lead Priority": "High",
        "Last Contact Date": "2026-11-03", "Next Follow-up Date": "2026-11-06",
        "Lead Stage": "Qualified Lead", "Lead Source": "Referral",
        "Notes": "Need to follow up"
    }
]

df_tracker = pd.DataFrame(leads)

# 2. AUTO CODING LOGIC - Dashboard Calculations
total = len(df_tracker)
accepted = len(df_tracker[df_tracker["Connection Status"] == "Accepted"])
interested = len(df_tracker[df_tracker["Response Status"] == "Interested"])

acceptance_rate = round((accepted / total) * 100, 2) if total else 0
response_rate = round((interested / total) * 100, 2) if total else 0

print(f"Total Prospects: {total}")
print(f"Accepted: {accepted} -> Acceptance Rate: {acceptance_rate}%")
print(f"Interested: {interested} -> Response Rate: {response_rate}%")

# 3. AUTO FOLLOW-UP REMINDER LOGIC
today = datetime.now().strftime("%Y-%m-%d")
for index, row in df_tracker.iterrows():
    if row["Next Follow-up Date"] == today:
        print(f"REMINDER: Aaj {row['Prospect Name']} ko follow-up karna hai!")

# 4. SAVE TO EXCEL WITH AUTO DASHBOARD
df_dashboard = pd.DataFrame({
    "KPI": ["Total Prospects", "Connection Accepted", "Interested", "Acceptance Rate", "Response Rate"],
    "Value": [total, accepted, interested, f"{acceptance_rate}%", f"{response_rate}%"],
    "Formula (Coding Thought)": [
        "COUNT(Total)", 
        "COUNTIF(Status='Accepted')", 
        "COUNTIF(Response='Interested')",
        "(Accepted/Total)*100", 
        "(Interested/Total)*100"
    ]
})

with pd.ExcelWriter("Project_Gaurav_Auto_Dashboard.xlsx", engine="openpyxl") as writer:
    df_tracker.to_excel(writer, sheet_name="Lead Tracker", index=False)
    df_dashboard.to_excel(writer, sheet_name="Dashboard (Auto)", index=False)

print("\nExcel ban gaya: Project_Gaurav_Auto_Dashboard.xlsx")
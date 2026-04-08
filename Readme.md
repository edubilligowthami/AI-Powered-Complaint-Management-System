 Problem
=============================================================================================================================================
In many apartments, hostels, and office complexes, tenants face recurring issues such as broken facilities, IT outages, or maintenance delays.

The traditional complaint process is manual and inefficient:

Complaints are reported verbally, on paper, or scattered across emails.

Owners struggle to track which complaints are pending vs resolved.

No standardized categorization or prioritization exists.

Urgent issues (e.g., Wi‑Fi outages, water leaks) often get delayed.

Tenants lack visibility into the status of their complaints, leading to frustration.

This results in delays, mismanagement, and tenant dissatisfaction, while owners lack a clear system to monitor and resolve issues efficiently.

✅ Solution
===========================================================================================================================
I developed a digital, AI‑powered Complaint Management Dashboard that transforms this process into a structured workflow:

Tenant Dashboard → Tenants submit complaints online with room/block details.

Owner Dashboard → Owners view all complaints in one place, resolve issues, and track lifecycle.

AI/NLP Integration → Complaint text is processed using TF‑IDF (TfidfVectorizer) and classified into categories (IT, Facilities, Maintenance) via Logistic Regression.

Priority Assignment → Rule‑based logic assigns urgency levels (High/Medium/Low).

Lifecycle Tracking → Complaints move from Pending → Completed → History.

Summary Section → Owners see pending vs resolved counts for quick reporting.

--------------------------------------------------------------------------------------------------------------------------------------------
 System Workflow Diagram

Tenant (User)  
   │  
   ▼  
[ Complaint Submission Form ]  
(Room, Block, Complaint Text)  
   │  
   ▼  
[ NLP + AI Processing ]  
- TF-IDF converts text → numerical features  
- Logistic Regression predicts Category  
- Rule-based logic assigns Priority  
   │  
   ▼  
Owner Dashboard  
- View all complaints (Pending)  
- Resolve complaints → mark Completed  
   │  
   ▼  
Complaint Lifecycle  
- Status changes: Pending → Completed  
- Complaint moves to Resolved History  
   │  
   ▼  
History Records  
- Stores completed complaints  
- Provides accountability & reporting

Tech Stack

🔹 Programming & Core
Python 3.11 → Main programming language for complaint handling, AI/NLP, and workflow automation.
VS Code → Development environment used for coding, debugging, and testing the Streamlit app.

🔹 Data Handling
Pandas → For reading, writing, and managing complaint data in CSV files.
CSV Storage → Lightweight database substitute to store active and resolved complaints.

🔹 AI / NLP
Scikit‑learn → Machine learning library used for:
TF‑IDF (TfidfVectorizer) → Converts complaint text into numerical features.
Logistic Regression → Predicts complaint categories (IT, Facilities, Maintenance).
Rule‑based Logic → Keyword matching for priority assignment (High/Medium/Low).

🔹 Dashboard / UI
Streamlit → Interactive web app framework for building tenant and owner dashboards.
Tenant view → Complaint submission form.
Owner view → Complaint table, resolve button, summary counts, and history logs.

🔹 Version Control & Hosting
GitHub → Repository hosting, version control, and portfolio showcase.

===========================================================================================
🎯 Impact

Efficiency → Owners save time with automated classification and prioritization.
Transparency → Tenants know their complaint is logged and tracked.
Accountability → Historical records ensure issues are documented and resolved.
Decision Support → Priority levels highlight urgent issues for faster action.
Scalability → The system can be extended to larger complexes or integrated with databases/cloud deployment.

================================================================================================================================

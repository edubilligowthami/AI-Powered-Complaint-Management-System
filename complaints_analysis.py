import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import os

# -------------------------------
# File setup
# -------------------------------
ACTIVE_FILE = "complaints.csv"
HISTORY_FILE = "resolved_complaints.csv"

# Initialize files if not exist, enforce string dtype
for file in [ACTIVE_FILE, HISTORY_FILE]:
    if not os.path.exists(file):
        pd.DataFrame({
            "Room": pd.Series(dtype="str"),
            "Block": pd.Series(dtype="str"),
            "Complaint": pd.Series(dtype="str"),
            "Category": pd.Series(dtype="str"),
            "Priority": pd.Series(dtype="str"),
            "Status": pd.Series(dtype="str")
        }).to_csv(file, index=False)

# Load active complaints with string dtype
df = pd.read_csv(ACTIVE_FILE, dtype=str)

# -------------------------------
# Train simple ML model (Category prediction)
# -------------------------------
training_data = {
    "Complaint_Text": [
        "Wi-Fi not working in lab",
        "Printer out of ink",
        "AC leaking water in office",
        "Chairs broken in cafeteria",
        "Elevator not working",
        "Ceiling fan noisy"
    ],
    "Category": ["IT", "IT", "Maintenance", "Facilities", "Facilities", "Maintenance"]
}
train_df = pd.DataFrame(training_data)

vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(train_df["Complaint_Text"])
y = train_df["Category"]

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# -------------------------------
# Priority assignment function
# -------------------------------
def assign_priority(text):
    text = text.lower()
    if any(word in text for word in ["wifi","internet","elevator","ac","leak"]):
        return "High"
    elif any(word in text for word in ["printer","chair","tap"]):
        return "Medium"
    else:
        return "Low"

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🏢 Complaint Management System")

role = st.sidebar.radio("Select Role", ["Tenant", "Owner"])

# -------------------------------
# Tenant Section
# -------------------------------
if role == "Tenant":
    st.header("Raise a Complaint")
    room_no = st.text_input("Room Number")
    block_no = st.text_input("Block Number")
    complaint = st.text_area("Complaint Text")

    if st.button("Submit Complaint"):
        new_entry = {
            "Room": room_no,
            "Block": block_no,
            "Complaint": complaint,
            "Category": "",
            "Priority": "",
            "Status": "Pending"
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(ACTIVE_FILE, index=False)
        st.success("✅ Complaint submitted successfully!")

# -------------------------------
# Owner Section
# -------------------------------
if role == "Owner":
    st.header("All Complaints Dashboard")

    if len(df) == 0:
        st.info("No active complaints.")
    else:
        # Only predict for rows that are still Pending
        pending_mask = df["Status"] == "Pending"
        pending_complaints = df.loc[pending_mask, "Complaint"].fillna("")

        if not pending_complaints.empty:
            predictions = model.predict(vectorizer.transform(pending_complaints))
            df.loc[pending_mask, "Category"] = predictions.astype(str)
            df.loc[pending_mask, "Priority"] = pending_complaints.apply(assign_priority).astype(str)

        # Show table with Status column
        st.dataframe(df[["Room","Block","Complaint","Category","Priority","Status"]])

        # Resolve by Room + Block
        st.subheader("Resolve a Complaint")
        room_input = st.text_input("Enter Room Number to Resolve").strip()
        block_input = st.text_input("Enter Block Number to Resolve").strip()

        if st.button("Resolve Complaint"):
            match = df[(df["Room"].astype(str).str.strip().str.lower() == room_input.lower()) &
                       (df["Block"].astype(str).str.strip().str.lower() == block_input.lower()) &
                       (df["Status"] == "Pending")]

            if not match.empty:
                # Mark as Completed
                df.loc[match.index, "Status"] = "Completed"

                # Move to history
                resolved_row = df.loc[match.index]
                history_df = pd.read_csv(HISTORY_FILE, dtype=str)
                history_df = pd.concat([history_df, resolved_row], ignore_index=True)
                history_df.to_csv(HISTORY_FILE, index=False)

                # Remove from active
                df = df.drop(match.index)
                df.to_csv(ACTIVE_FILE, index=False)

                st.success(f"✅ Complaint for Room {room_input}, Block {block_input} resolved and marked Completed!")
            else:
                st.error("❌ No pending complaint found for that Room + Block combination.")

        # -------------------------------
        # Summary Section (Pending vs Resolved)
        # -------------------------------
        st.subheader("📊 Complaint Summary")
        active_count = len(pd.read_csv(ACTIVE_FILE, dtype=str))
        resolved_count = len(pd.read_csv(HISTORY_FILE, dtype=str))

        st.write(f"🟡 Pending Complaints: **{active_count}**")
        st.write(f"🟢 Resolved Complaints: **{resolved_count}**")

        # Show history table
        st.subheader("📜 Resolved Complaints History")
        history_df = pd.read_csv(HISTORY_FILE, dtype=str)
        st.dataframe(history_df)

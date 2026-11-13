import streamlit as st
from db import setup_db, CargoApp


setup_db()
app = CargoApp()

# 2. Page Title
st.title("🚛 Nexus Cargo Pipeline")
st.write("Welcome to the Local Delivery & Internal Cargo Tracking Portal")

# 3. Creating Two Main Tabs (Customer vs Staff)
customer_tab, staff_tab = st.tabs(["Customer Tracking", "Staff Operations"])


# TAB 1: CUSTOMER TRACKING (READ)
with customer_tab:
    st.header("Track Your Parcel")
    
    # box for tracking number
    track_no = st.text_input("Enter Tracking Number (e.g., TRK-1234AB)", autocomplete ="off").strip().upper()

    if st.button("Search Parcel"):
        if not track_no:
            st.warning("Please enter a tracking number.")
        else:
          
            parcel = app.lookup_parcel(track_no)
            
            if parcel:
                tracking_id = parcel[1]
                sender = parcel[2]
                receiver = parcel[3]
                phone = parcel[4]
                origin = parcel[5]
                destination = parcel[6]
                weight = parcel[7]
                description = parcel[8]
                status = parcel[9]
                updated_at = parcel[10]
                
                st.success("Parcel Found!")

                st.write(f"Tracking Number: {tracking_id}")
                st.write(f"Status: {status}")
                st.write(f"Route:{origin} to {destination}")
                st.write(f"Sender:{sender} | Receiver: {receiver} ({phone})")
                st.write(f"Weight: {weight} kg")
                st.write(f"Description: {description}")
                st.caption(f"Last Updated: {updated_at or 'just logged (No updates yet)'}")
            else:
                st.error("No parcel found with this tracking number.")


# TAB 2: STAFF OPERATIONS (CREATE, UPDATE, DELETE, EXPORT)
with staff_tab:
    st.header("Staff Dashboard")
    
    action = st.selectbox(
        "Select Action:",
        ["Log New Parcel", "Update Parcel Status", "Delete Parcel Record", "Export Dispatches to CSV"]
    )

    # CREATE: Log New Parcel
    if action == "Log New Parcel":
        st.subheader("Log New Cargo Consignment")
        
        with st.form("parcel_form", clear_on_submit=True):
            sender = st.text_input("Sender Name", autocomplete="off")
            receiver = st.text_input("Receiver Name", autocomplete="off")
            phone = st.text_input("Receiver Phone", autocomplete="off")
            origin = st.text_input("Origin Hub",autocomplete="off" )
            destination = st.text_input("Destination",autocomplete="off" )
            weight = st.number_input("Weight (kg)", min_value=0.1, step=0.1)
            description = st.text_input("Package Description", autocomplete="off")

            submitted = st.form_submit_button("Save Dispatch")

            if submitted:
                if sender.strip() and receiver.strip():
                    # add_parcel from db.py and gets the generated tracking ID back
                    tracking_id = app.add_parcel(
                        sender.strip(),
                        receiver.strip(),
                        phone.strip(),
                        origin.strip(),
                        destination.strip(),
                        weight,
                        description.strip(),
                    )
                    if tracking_id:
                        st.success(f"Dispatch logged successfully! Your Tracking Number is: {tracking_id}")
                    else:
                        st.error("Failed to save dispatch to database.")
                else:
                    st.warning("Please enter both Sender and Receiver names.")

    # UPDATE: Change Status
    elif action == "Update Parcel Status":
        st.subheader("Update Transit Status")
        
        update_track = st.text_input("Enter Tracking Number to Update").strip().upper()
        new_status = st.selectbox(
            "Select New Status",
            ["Received", "In Transit", "At Hub", "Out for Delivery", "Delivered"]
        )

        if st.button("Update Status"):
            if not update_track:
                st.warning("Please enter a tracking number.")
            else:
                parcel = app.lookup_parcel(update_track)
                if parcel:
                    if app.change_status(update_track, new_status):
                        st.success(f"Status for {update_track} updated to {new_status}!")
                    else:
                        st.error("Could not update status.")
                else:
                    st.error("Tracking number not found.")

    # DELETE: Remove Record
    elif action == "Delete Parcel Record":
        st.subheader("Remove Parcel Record")
        
        delete_track = st.text_input("Enter Tracking Number to Delete", autocomplete="off").strip().upper()

        if st.button("Delete Record"):
            if not delete_track:
                st.warning("Please enter a tracking number.")
            else:
                parcel = app.lookup_parcel(delete_track)
                if parcel:
                    if app.purge_parcel(delete_track):
                        st.success(f"Record {delete_track} permanently deleted.")
                    else:
                        st.error("Could not delete record.")
                else:
                    st.error("Tracking number not found.")

    # EXPORT: CSV Report
    elif action == "Export Dispatches to CSV":
        st.subheader("Export Dispatch Ledger")
        
        if st.button("Generate CSV Report"):
            if app.export_to_csv():
                st.success("Exported successfully to cargo_export.csv in your project folder!")
            else:
                st.error("Could not export data.")





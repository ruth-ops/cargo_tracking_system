# 🚛 Nexus Cargo Pipeline

**The problem:** Local logistics companies waste time and resources on manual phone calls to track dispatches, so this system provides an automated digital portal to record parcels, generate tracking numbers, and look up real-time statuses instantly.

**By Ruth Macharia**

## Description
**Nexus Cargo Pipeline**  is a local delivery and internal cargo tracking portal designed for logistic teams. It allows staff members to register incoming parcels, generate unique tracking numbers, update transit statuses as packages move through the delivery pipeline and export ledger reports to CSV. customers can also look up their parcel status in real time without making phone calls.


## Project Features
* **Customer Tracking Portal:** Instant parcel lookup using a unique 'TRK-' tracking number.
* **Staff Operations Dashboard:** Full CRUD functionality to log new parcels, update transit statuses, and delete records.
* **Persistent SQLite Storage:** saves all dispatch data safely in a local relational database ('nexus_cargo.db')
* **CSV Ledger Export:** Exports all dispatch records into an Excel-ready 'cargo_export.csv' file.

## Setup & Installation requirements
1. **Clone this repository to your local computer:**
'''bash
git clone https://github.com/ruth-ops/cargo_tracking_system/blob/main/db.py
cd capstone_project
'''

2. ** Create and activate a python virtual environment:**
'''bash
python -m venv venv
Source venv/Scripts/activate
'''

3. **install required dependencies:**
'''bash
pip install -r requirements.txt
'''

4. ** Run the application:**
'''bash
streamlit run main.py
'''

## Known Bugs
No known bugs at this time, input validation is configured to catch invalid weights, empty fields, or missing tracking numbers gracefully.

## Technologies Used
* **python 3**
* **SQLite** (Relational Database)
* **streamlit** (frontend UI Library)
* **Git & GitHub** (Version Control)

## Support and contact details
If you run into any issues or have questions regarding this project, feel free to submit an issue on the Github repository or reach out via email at **ruthmacharia880@gmail.com**.

### License
This project is licensed under the MIT License. copyright(c)2026 Ruth Macharia.
 

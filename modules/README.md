🚌 Smart Tracking Bus System

📌 Project Description

The Smart Tracking Bus System is a web-based application developed to simplify and improve college transportation management.

The system helps administrators manage student details, bus information and attendance records. It also aims to improve communication between colleges and parents through automated notifications.

The project uses Python and Flask for backend development and SQLite for database management.

🎯 Objectives

- To maintain student and bus information digitally.
- To simplify student attendance management.
- To provide a QR-based attendance facility.
- To improve communication between parents and college management.
- To support bus location tracking and estimated arrival time.

🛠️ Technologies Used

Technology| Purpose
Python| Backend programming
Flask| Web application framework
HTML| Frontend structure
CSS| User interface design
SQLite| Database management
VS Code| Development environment

✨ Key Features

1. Login System – Separate login access for Admin, Students and Parents.
2. Student Management – Add, view and edit student details.
3. Bus Management – Manage bus numbers, driver details and routes.
4. Attendance Management – Maintain student attendance records.
5. QR-Based Attendance – Support student identification through QR scanning.
6. Parent Notifications – Maintain notifications related to student attendance.
7. Bus Tracking – Support bus location monitoring and estimated arrival time.

📂 Project Structure

Smart-Tracking-Bus/
│
├── server.py
├── database.py
├── bus_tracking.py
├── ai_eta.py
├── import_student.py
│
├── database/
│   └── college_bus.db
│
├── screenshots/
│   ├── login.png
│   ├── admin_dashboard.png
│   ├── student_management.png
│   ├── bus_management.png
│   ├── attendance.png
│   └── parent_dashboard.png
│
└── README.md

Note: The structure above is illustrative. Keep only the files and screenshots that actually exist in your project.

⚙️ Installation and Execution

Step 1: Clone the Repository

git clone YOUR_GITHUB_REPOSITORY_URL

Step 2: Open the Project Folder

cd Smart-Tracking-Bus

Step 3: Install Required Packages

pip install flask pandas openpyxl

Install any additional packages required by your implementation.

Step 4: Run the Application

python server.py

Step 5: Open in Browser

Open your browser and visit:

http://127.0.0.1:5000/

The Smart Tracking Bus System login page will appear.

📸 Project Screenshots

1. Login Page

"Login Page" (screenshots/login.png)

2. Admin Dashboard

"Admin Dashboard" (screenshots/admin_dashboard.png)

3. Student Management

"Student Management" (screenshots/student_management.png)

4. Bus Management

"Bus Management" (screenshots/bus_management.png)

5. Attendance Management

"Attendance" (screenshots/attendance.png)

6. Parent Dashboard

"Parent Dashboard" (screenshots/parent_dashboard.png)

💡 Future Enhancements

- Real-time GPS-based bus tracking.
- AI-based bus arrival time prediction.
- Automated SMS notifications to parents.
- Mobile application integration.
- Improved QR-based attendance automation.

👩‍💻 Project Details

Project Title: Smart Tracking Bus System

Domain: Web Development / Artificial Intelligence

Programming Language: Python

Database: SQLite

Framework: Flask

🏁 Conclusion

The Smart Tracking Bus System aims to make college transportation management more efficient through digital student records, attendance management, bus information and parent communication. It provides a foundation for integrating intelligent bus tracking and arrival-time prediction features.
# **LuigiHealth - Hospital Information Management System (HIMS)**  

This project, **LuigiHealth**, is a **Hospital Information Management System** (HIMS) designed for secure user authentication with **two-factor authentication (2FA)** and role-specific dashboards.  

---

## **Overview**  
The application allows users to:  
- **Patients**: View their profiles.  
- **Personnel**: Manage patient data and assign rooms.  
- **Managers**: Monitor hospital statistics and oversee room management.  

---

## **Setup Instructions**  

### **Requirements**  
- **Python 3.12** or higher.  
- Required libraries:  
   ```bash
   pip install tk Pillow matplotlib
- Important node, if your system supports python3, use python3 in the code blocks
  ```bash
  subprocess.Popen(["python3", "floors_rooms.py"])
  subprocess.Popen(["python3", "login.py"])
- Otherwise if your system supports python, use python in the code blocks
  ```bash
  subprocess.Popen(["python", "floors_rooms.py"])
  subprocess.Popen(["python", "login.py"])
- If you encounter a problem about this python compatibility issue, you can contact with our team members. 
---

## **Run the Application** 
1.	Place all files in the same directory.
2.	Run the following command to start the login system:
    python login.py

---

## **File Structure** 
* login.py - Handles user login and 2FA.
* two_factor_auth.py - Sends and verifies 2FA codes via email.
* patient_dashboard.py - Displays patient information.
* personnel_dashboard.py - Allows personnel to manage patients and rooms.
* manager_dashboard.py - Displays hospital statistics and manages data.
* floors_rooms.py - Manages room assignments.
* open_dental_users.db - SQLite database for user, patient, and room data.

---

## **Features** 
* Secure Login with 2FA: Ensures safe and authorized user access.
* Role-based Dashboards:
* Patients: Access personal information and assigned rooms.
* Personnel: Manage patient data and room assignments.
* Managers: Monitor statistics and oversee operations.
* Room Management: Real-time room availability and assignment tracking.

---

## **How to Use** 
1.	Log In: Enter your username and password.
2.	Verify with 2FA: Use the verification code sent to your email.
3.	Access Dashboard: View and manage data based on your role.

---

## **Contributors** 
* Eylül Badem	- 22003079	
* Yusuf Şenyüz - 21903105	
* Sabri Eren Dağdelen - 22001764	
* Yaşar Tatlıcıoğlu - 22003856	

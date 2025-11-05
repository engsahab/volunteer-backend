# Volunteer Management System - Backend API

## 1. Description

My project is a **Volunteer Management System**. It is a full-stack application designed to help organizations post opportunities and allow volunteers to apply for them.

This repository contains the **Backend API** only. It is built using Python, Django REST Framework, and PostgreSQL.

---
## 2. Technologies Used

* **Backend**: Python, Django, Django REST Framework, PostgreSQL
* **Authentication**: JWT (Simple JWT)
* **Database**: PostgreSQL (`psycopg2-binary`)
* **CORS**: `django-cors-headers` (to connect with the React frontend)
* **Environment**: `python-decouple` (to manage environment variables)

---
## 3. Project Links

* **Frontend Repository:** https://github.com/engsahab/Volunteer-frontend
---
## 4. (Planning)
The project was planned by first defining the models and their relationships (ERD), and then specifying the routes (Routing Table) needed for the frontend.


### (ERD Diagram)

This diagram shows the four models used in the application and the relationships between them.


<img width="409" height="362" alt="Screenshot 2025-11-04 172210 (1)" src="https://github.com/user-attachments/assets/c1875a79-a7a8-4a14-a25d-b3aa26999715" />


### API (Routing Table)

This table shows all the API endpoints, their functions, and the required access level to reach them.

<img width="483" height="222" alt="Screenshot 2025-11-04 173344" src="https://github.com/user-attachments/assets/0a9ac0c6-f6c4-475e-9454-8422a1ebcfb1" />


---

## 5. IceBox Features

While this project successfully meets all core requirements, the following features are planned for future development:

* **Implement Application Withdrawal (User Story #8):**
    * **Description:** Allow a registered user to "withdraw" (Delete) their own application if it is still "pending".
    * **Status:** The backend API endpoint (`DELETE /api/applications/<id>/`) is already built and functional. This only requires a "Withdraw" button to be added to the frontend.

* **Admin Notifications:**
    * **Description:** Implement a system (possibly using Django Signals or a scheduled task) to send an email or an in-app notification to the admin when a new application is submitted.

* **Advanced API Filtering:**
    * **Description:** Enhance the `OpportunityList` view to allow users to filter opportunities based on query parameters in the URL, such as `?location=Riyadh` or `?specialization=Medical`.

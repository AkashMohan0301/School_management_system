# School Management System with Role-Based Access Control

## Project Description
The School Management System is a Django-based web application that allows managing student details, library history, and fees history. It uses Role-Based Access Control (RBAC) to restrict user permissions based on their roles, ensuring security and proper segregation of duties. The system supports three user roles: **School Admin**, **Office Staff**, and **Librarian**, each with specific access rights and functionalities.

---

## Features

### Authentication
- User authentication with Django's built-in system.
- Role-based access control using Django Permissions.
- Session management to handle login states and roles.

### Role-Based Access Control (RBAC)
- Implemented using Django's built-in `Permissions` and `Groups`.
- Roles:
  - **Admin:** Full access to all features.
  - **Office Staff:** Restricted to managing fees and viewing student and library details.
  - **Librarian:** Restricted to viewing library and student details.

### State Management
- Django sessions are used to maintain user login state and roles.

### Confirmation Mechanism
- Django messages framework is used to add confirmation prompts for critical actions (e.g., deletions).
---
## Roles
  1. Admin
  2. Office Staff
  3. Librarian
### Admin Dashboard
- Full access to the system.
- Manage (create, edit, delete) Office Staff and Librarian accounts.
- Perform CRUD operations on:
  - Student details
  - Library history
  - Fees history

### Office Staff Dashboard
- Access to all student details.
- Manage fees history (add, edit, delete).
- View library borrowing records.

### Librarian Dashboard
- View-only access to student details and library borrowing records.
---
## Technology Stack
- **Backend Framework:** Django ,Django Rest Framework
- **Frontend Framework:** Django templates
- **Database:** SQLite (default)
- **RBAC:** Django Permissions
- **State Management:** Django sessions
- **Messaging Framework:** Django messages for notifications
---
## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```
3. Create and activate a virtual environment:
   ```bash
    python -m venv venv
    source venv/bin/activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
7. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
9. Run the development server:
   ```bash 
   python manage.py runserver
   ```
11. Create Superuser for administrative privileges
    ```bash
    py manage.py createsuperuser
    ```
13. Run Development server:
    ```
    py manage.py runserver
    ```
14. Access the Application
   - Open your browser and navigate to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Contributors
1. Fork the repository.
2. Create a feature branch.
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes.
   ```bash
   git commit -m "Add a meaningful message"
   ```
4. Push to the branch.
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## Contact
Feel free to contact me for any queries or contributions:
- **Name:** Akash Mohankumar M
- **email:** akashmohan940@gmail.com
- **Phone:** 9400942178



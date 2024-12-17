# School Management System with Role-Based Access Control

## Project Description
The School Management System is a Django-based web application that allows managing student details, library history, and fees history. It uses Role-Based Access Control (RBAC) to restrict user permissions based on their roles, ensuring security and proper segregation of duties. The system supports three user roles: **School Admin**, **Office Staff**, and **Librarian**, each with specific access rights and functionalities.

---

## Features

### Authentication
- User authentication with Django's built-in system.
- Role-based access control using Django Permissions and Groups.
- Session management to handle login states and roles.

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

### Student Management
- Create, update, view, and delete student records.

### Library History Management
- Add, edit, delete, and view borrowing records.
- Fields: `book_name`, `borrow_date`, `return_date`, `status`.

### Fees History Management
- Add, edit, delete, and view fees records.
- Fields: `student_id`, `fee_type`, `amount`, `payment_date`, `remarks`.

---

## Technology Stack
- **Backend Framework:** Django ,DRF
- **Frontend Framework:** Django templates (optional)
- **Database:** SQLite (default) or other Django-supported databases
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
  - git clone <repository_url>
  - cd <repository_name>
2. Create and activate a virtual environment:
  -python -m venv venv
  -source venv/bin/activate
3. Install dependencies:
  - pip install -r requirements.txt
4. Apply database migrations:
  -python manage.py makemigrations
  -python manage.py migrate
6. Run the development server:
  -python manage.py runserver

### Contributors
1.Akash Mohankumar M


# My Favorite Shows Tracker
#### Video Demo:  <[URL HERE](https://youtu.be/kXntzJfWUzg)>
#### Description:

## Project Overview

The "My Favorite Shows Tracker" is a web application built using Flask, Python, HTML, CSS, and SQLite3. The purpose of this project is to allow users to register, securely log in, manage their password, and maintain a personalized list of TV shows along with the last episode they have watched. The application emphasizes both functionality and user experience, providing a simple, clean, and responsive interface for desktop and mobile devices.

Users can perform the following actions:
1. Register for an account and securely store a hashed password.
2. Log in to their account to access and manage their personal shows.
3. Change their password securely.
4. Add, edit, and delete TV shows from their personal list.
5. Track the season and episode number of the last watched episode in a clear and structured format.

The project focuses on security (through password hashing), usability, and a clean design that works across devices.

---

## File Structure and Purpose

The project has the following structure:

CS50X Final Project/
│
├─ app.py
├─ helpers.py
├─ db.py
├─ requirements.txt
├─ templates/
│ ├─ layout.html
│ ├─ login.html
│ ├─ register.html
│ ├─ change_password.html
│ ├─ add_show.html
│ ├─ edit_show.html
│ └─ index.html
└─ static/
  └─ styles.css


### **app.py**
This is the main application file that contains all the Flask routes and logic. It handles user registration, login, logout, password changes, and CRUD operations for the shows. The application uses session management to keep track of logged-in users. Each route is designed with security in mind, ensuring that only authenticated users can access their data. Flash messages are used throughout to provide feedback to the user for actions such as successful login, registration, or show management.

Key features in `app.py` include:
- Route `/register`: Handles new user registration, validates input, hashes passwords, and logs users in automatically.
- Route `/login`: Authenticates users and sets the session.
- Route `/logout`: Clears the session to log out the user.
- Route `/change_password`: Allows users to update their password securely after verifying their current password.
- Routes `/add_show`, `/edit_show/<id>`, `/delete_show/<id>`: Enable users to add new shows, edit existing ones (including season and episode), and delete shows.

---

### **helpers.py**
This file contains utility functions for security and access control:
- `login_required(f)`: A decorator that ensures only authenticated users can access certain routes.
- `hash_password(password)`: Hashes passwords using `Werkzeug` for secure storage.
- `check_password(hash, password)`: Compares a plain text password with a hashed password for authentication.

By separating these helper functions into a dedicated file, the project maintains **modularity** and **readability**, allowing for easy future extensions, such as implementing additional security features.

---

### **db.py**
The `db.py` file is responsible for initializing the SQLite3 database and creating tables if they do not already exist. It defines two main tables:

1. `users`: Stores user information, including a unique ID, username, and hashed password.
2. `shows`: Stores user-specific TV shows, including the show name, last episode watched, and a foreign key linking it to the user.

This separation of database logic from application logic in `app.py` makes the project **cleaner and easier to maintain**. The database connection function is also centralized here for reuse throughout the project.

---

### **templates/**
This folder contains all HTML templates rendered by Flask routes:

- `layout.html`: The base template that includes the header, navigation bar, and placeholders for dynamic content. All other templates extend from this layout for consistency.
- `login.html`: Provides the login form and a link to the registration page.
- `register.html`: Contains the registration form, prompting the user to create an account.
- `change_password.html`: Allows users to update their password after providing the current password.
- `add_show.html`: Form to add a new TV show, including separate inputs for season and episode.
- `edit_show.html`: Form to edit an existing show, pre-filled with the current season and episode.
- `index.html`: Displays the user's list of shows in a clean, responsive table with options to edit or delete each entry.

All templates are designed with **user experience and responsiveness** in mind, using CSS for clean layouts and readable typography.

---

### **static/styles.css**
This CSS file contains styling for the application, including:
- Centering forms and aligning input fields.
- Styling buttons with colors, hover effects, and proper padding.
- Creating responsive tables and layouts suitable for mobile devices.
- Displaying flash messages in a visually distinct manner at the top of pages.

The CSS focuses on simplicity, readability, and a modern clean appearance, ensuring a professional look with minimal complexity.

---

## Design Decisions

Several design choices were made during development:

1. **Password Hashing**: To ensure user data security, all passwords are hashed using `Werkzeug`. This prevents plain text passwords from being stored in the database.
2. **Session Management**: User authentication is maintained via sessions to provide a seamless experience across pages.
3. **Separate Season and Episode Fields**: Instead of a single text input for the last episode, the application collects season and episode separately, then formats it as `S1 : E3`. This ensures consistent formatting and prevents input errors.
4. **Flash Messages**: Used throughout to provide immediate feedback to the user, enhancing usability.
5. **Modular Structure**: Helper functions and database initialization are separated from the main application file to improve readability, maintainability, and scalability.

Overall, these design choices aim to balance **security, usability, and clean code organization**.

---

## Conclusion

The "My Favorite Shows Tracker" is a fully functional, secure, and responsive web application that allows users to manage their personal TV show lists efficiently. By carefully structuring files, separating logic, and focusing on user experience, this project serves as a solid example of a Python Flask web application with SQLite database integration.

This project could be extended in the future with features such as:
- External APIs to fetch show details automatically.
- User profile customization.
- Notifications for new episodes.
- Sorting and filtering shows by genre or watch status.

---

*This README describes the project thoroughly, explains file purposes, design choices, and functionality to demonstrate a comprehensive understanding of the application.*

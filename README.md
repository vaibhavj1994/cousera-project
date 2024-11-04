# Restaurant Management System 🍽️🧑‍🍳

## Project Structure

The project consists of two Django apps:

- **Restaurant**: The web application that allows customers to interact with the restaurant's services.
- **Restaurant API**: The backend **RESTful APIs** that handle various operations related to menu item management, delivery orders, table bookings, and staff (owner, managers, delivery crew) administration.

---

## Technology Stack 🛠️

- **Django**: Web framework to build the application core, along with **HTML**, **CSS**, and **JavaScript** for front-end development.
- **Django REST Framework (DRF)**: For creating, authenticating, and securing various RESTful APIs.
- **MySQL**: Database system to store and manage data.
- **Djoser**: Library for token-based authentication.
- **Django unittest Library**: For application testing to ensure code quality and reliability.
- **Insomnia**: For API testing and debugging.

---

## API Endpoints

Below is a brief overview of the API endpoints available in the project:

- **Restaurant Menu API** 🍝: Manage menu items (view, add, update, delete).
- **Menu Cart API** 🛒: Handle cart operations (add items, view contents, empty cart).
- **Delivery Order API** 🚚: Manage orders (view, place, assign delivery crew, update status, delete).
- **Table Booking API** 🍽️: View table bookings.
- **Delivery Crew Staffing API** 👨‍💼: Hire or fire delivery crew members.
- **Manager Staffing API** 👔: Hire or fire managers.

For detailed information about the API endpoints, refer to the [API EndPoints Documentation](documentation/API.md).

---

## Setup and Installation ⚙️

1. **Clone the Repository**  
   Clone the repository to your local machine and navigate into the project directory:
   ```bash
   git clone https://github.com/MarcAbouAbdallah/LittleLemon.git
   cd LittleLemon
   ```

2. **Create a Virtual Environment**  
   ```bash
   pipenv shell
   ```

3. **Install the project dependencies**  
   ```bash
   pipenv install
   ```

4. **Set Up the database**  
   Make sure you have MySQL installed and configured. Then run:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**  
   ```bash
   python manage.py runserver
   ```







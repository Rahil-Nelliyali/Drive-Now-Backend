# Car Rental Booking App - Backend

Welcome to the Car Rental Booking App backend repository! This project provides the server-side logic and APIs for managing and booking rental cars. The backend is built using Python Django, Django Rest Framework, JWT token authentication, and other technologies to ensure a secure and efficient backend for your app.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)


## Features

- RESTful APIs for managing cars, bookings, and user accounts.
- User authentication and authorization using JWT tokens.
- Secure endpoints for user registration, login, and profile management.
- CRUD operations for cars, allowing for easy car management.
- Booking functionality, allowing users to reserve rental cars.
- Integration with a relational database (e.g., PostgreSQL) for data storage.
- Robust error handling and validation using Django Rest Framework.


## Technologies Used

- Python Django
- Django Rest Framework
- JWT Token Authentication
- PostgreSQL (or other database of choice)
- CORS (Cross-Origin Resource Sharing) configuration
- API documentation using tools like Swagger or DRF's built-in tools


## Getting Started

To get started with the Car Rental Booking App backend, follow the steps below:

### Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/Rahil-Nelliyali/Drive-Now-Backend.git
```

2. Navigate to the project directory:

```bash
cd backend
```

3. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

1. Configure your database settings in the `settings.py` file.

2. Set up JWT token authentication, CORS, and other configurations as needed.

### API Documentation

The backend APIs are documented for ease of use. You can access the API documentation by visiting a designated endpoint (e.g., `/api/docs/`) or using tools like Swagger.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to create a pull request or submit an issue in the repository. We appreciate your feedback and help in making this backend robust and efficient!



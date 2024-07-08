# Kidternship Flask API

## Description:
This is the 2024 KIDternship Flask API project. It is a set of basic API calls designed to provide practical examples for understanding APIs. The project focuses on simulating a coffee shop/bakery, covering topics such as error handling in API responses and data sanitization practices. This project sets up a Postgres database to hold the data as well as a Flask server allowing the client to interact with the APIs.

### Key Features:

Demonstrates error handling and data sanitization techniques.
Utilizes Flask for building RESTful APIs and integrates with PostgreSQL for data storage.
Provides endpoints for managing menu items, orders, and user interactions within a simulated bakery environment.
Technologies Used:
Flask, PostgreSQL, Docker, Python, RESTful API principles.

### Target Audience:
Developers seeking practical experience with API development, students learning web development concepts, and anyone interested in exploring backend systems with Flask and PostgreSQL.

### Learning Objectives:
By engaging with this project, users will gain insights into:

- Implementing RESTful APIs with Flask.
- Integrating and managing data using PostgreSQL.
- Implementing error handling strategies and data validation in API responses.

This repository contains two directories: `flask_docker_kidternship` and `postgres_docker_kidternship`.
### Running the Flask Server
1. Navigate to `flask_docker_kidternship`.
2. Execute `docker-compose up -d` to bring up the Flask server.

### Running Postgres Docker
1. Navigate to `postgres_docker_kidternship`.
2. Execute `docker-compose up -d` to bring up the PostgreSQL database.

## Notes
- Make sure Docker and Docker Compose are installed.
- Adjust network configurations and file paths as needed.

## Flask Directory

### Prerequisites
- Create a `.env` file in this directory with the following parameters (modify to fit your needs):

    - `DATABASE_HOST="127.0.0.1"`

    - `DATABASE_PORT="5432"`

    - `DATABASE_NAME="store"`

    - `DATABASE_USER="CREATEYOUROWNUSERNAME"`

    - `DATABASE_PASS="CREATEYOUROWNPASSWORD"`

    - `POSTS_JSON_FILE="posts.json"`

    - `POSTS_LOG_FILE="posts.log"`
    
## Postgres Directory

### Prerequisites
- Create a `.env` file in this directory with the following parameters (modify to fit your needs):

    - `DATABASE_HOST="127.0.0.1"`

    - `DATABASE_PORT="5432"`

    - `DATABASE_NAME="store"`

    - `DATABASE_USER="CREATEYOUROWNUSERNAME"`

    - `DATABASE_PASS="CREATEYOUROWNPASSWORD"`

    - `POSTS_JSON_FILE="posts.json"`

    - `POSTS_LOG_FILE="posts.log"`

### Initializing Default Databases
- Execute `.sh` file to create default databases.

# API Endpoints
- **Root Route**: `/` (GET)
- Returns "Welcome to the API!".

- **Wordcloud Resources**:
- `/wordcloud/words` (POST)
    - Adds a new word to the wordcloud.
- `/wordcloud/display` (GET)
    - Generates and returns the wordcloud image.

- **Introductory Resources**:
- `/introduction/hello-world` (GET)
    - Returns "Hello World!".
- `/introduction/user-id/<username>` (GET)
    - Returns a user ID based on the provided username.
- `/introduction/food` (POST)
    - Determines if a given food is allowed or not.

- **Bakery Resources**:
- `/bakery/menu` (GET)
    - Returns all menu items.
- `/bakery/menu/<category>` (GET)
    - Returns menu items for a specific category.
- `/bakery/orders` (GET, POST, PUT)
    - GET: Returns all orders.
    - POST: Inserts a new order.
    - PUT: Updates an existing order.
- `/bakery/orders/<orderNumber>` (GET)
    - Returns details of a specific order.

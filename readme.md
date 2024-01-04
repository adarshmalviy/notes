# Speer Technologies Notes Project

## Overview

This project is a secure and scalable RESTful API for note management built using FastAPI and Tortoise ORM. Users can create, read, update, and delete notes, as well as share notes with other users. Additionally, the API supports searching for notes based on keywords.

## Tech Stacks

- **FastAPI:** A modern, fast, web framework for building APIs with Python 3.
- **Tortoise ORM:** An easy-to-use asyncio ORM inspired by Django.
- **MySQL:** An easy-to-use RDBMS. We can use any Database of our choice.

## Features

### Authentication Endpoints

- `POST /api/auth/signup`: Create a new user account.
- `POST /api/auth/login`: Log in to an existing user account and receive an access token.

### Note Endpoints

- `GET /api/notes`: Get a list of all notes for the authenticated user.
- `GET /api/notes/:id`: Get a note by ID for the authenticated user.
- `POST /api/notes`: Create a new note for the authenticated user.
- `PUT /api/notes/:id`: Update an existing note by ID for the authenticated user.
- `DELETE /api/notes/:id`: Delete a note by ID for the authenticated user.
- `POST /api/notes/:id/share`: Share a note with another user for the authenticated user.
- `GET /api/notes/note/search?q=:query`: Search for notes based on keywords for the authenticated user.

## Running the Project

1. Clone the repository:

    ```bash
    git clone https://github.com/adarshmalviy/notes.git
    ```

2. Navigate to the project directory:

    ```bash
    cd notes
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Update the `.env` file with your database URL.

5. Run the FastAPI application:

    ```bash
    uvicorn main:app --reload
    ```

   The API will be available at `http://127.0.0.1:8000`.

## Why FastAPI?

- **Fast:** FastAPI is one of the fastest web frameworks for building APIs, thanks to its use of asynchronous programming.
- **Easy:** FastAPI is easy to use, with automatic data validation, interactive documentation, and automatic generation of OpenAPI and JSON Schema.
- **Pythonic:** Being based on standard Python type hints, FastAPI leverages Python's static analysis tools and provides excellent code completion support.

## Why Tortoise ORM?

- **Asyncio Support:** Tortoise ORM is built with asyncio in mind, making it suitable for high-concurrency applications.
- **Ease of Use:** Tortoise ORM offers a simple and intuitive API, making it easy to learn and use.
- **Compatibility:** Tortoise ORM supports multiple database backends, including PostgreSQL and MongoDB, providing flexibility for different project requirements.

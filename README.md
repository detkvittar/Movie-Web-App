Movie Web App
Overview

This Movie Web App is a Flask-based web application that allows users to manage movie collections. It integrates the OMDB API for movie information and uses SQLite for data management. Also looks like a budget-version of Netflix!

Features:

    User Management: Create, list, view, and delete users.
    Movie Management: Add, list, update, and delete movies for each user.
    Review Management: Add, update, and delete reviews for movies.
    External API Integration: Fetch movie details from OMDB API.
    Error Handling: Custom error pages for 400, 404, and 500 status codes.

Tech Stack

    Backend: Python, Flask
    Database: SQLite
    Frontend: HTML, CSS
    API: OMDB API

Installation

    Clone Repository: Clone this repository to your local machine.

git clone [here goes repository-url]

Set up a Virtual Environment (optional but recommended):


python -m venv venv
source venv/bin/activate  # For Unix or MacOS
venv\Scripts\activate  # For Windows

Install Dependencies:

pip install Flask Flask-SQLAlchemy requests

Environment Variables: Set up the necessary environment variables (if any), such as API_KEY for the OMDB API.

Database Setup: Initialize the SQLite database as per the provided schema.

Run the Application:

    python app.py

Usage

    Access the web app via localhost:5000 in your web browser.
    Navigate through the app using the provided routes for managing users, movies, and reviews.

API Endpoints

    GET /api/users: List all users.
    GET /api/users/{user_id}/movies: Get movies of a specific user.
    POST /api/users/{user_id}/movies: Add a movie to a user.

Limitations and Known Issues
Limitations

    API Dependency: The application relies heavily on the OMDB API for movie information. Any downtime or rate limiting from the API will significantly impact the app's functionality.

    Basic User Authentication: Currently, the app does not support advanced user authentication and authorization features. All users have equal access to all functionalities. Rejoice.

    Scalability: The application uses SQLite, which we all know is not the heavy-lifter of SQL

    Front-end Design: The user interface is basic and implemented with minimal HTML/CSS :D

    No Automated Testing: The project lacks a suite of automated tests

Known Issues

    Error Handling: The app's error handling (especially around the external API calls) is minimal. Could lead to unhandled exceptions and crashes in certain scenarios.

    Database Session Management: The current implementation of database sessions may not efficiently handle concurrent requests, potentially leading to database lock issues or leaks.

    Hardcoded Configuration: Some configurations, such as the database file path, are hardcoded, which could limit flexibility in different environments.

    Security Concerns: The application has not been extensively tested for security vulnerabilities. It might be susceptible to common web application security risks like SQL injection, cross-site scripting (XSS), etc.

License

This project is licensed under the MIT License.

MIT License

Copyright (c) [2023] [Emilia Malmqvist]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

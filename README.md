# Meeting Organizer Application

## Project Overview

This case study focuses on the development of a Meeting Organizer application, which is a single-page application (SPA) for organizing meetings. The application allows users to create, update, delete, and view meetings. It includes both frontend and backend components, with the frontend implemented using HTML, JavaScript, and Bootstrap 5, and the backend implemented using Flask (a Python web framework) with MongoDB as the database.

## Technologies Used

- **Frontend**: HTML, JavaScript, Bootstrap 5
- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Validation**: Cerberus library
- **Sanitization**: Bleach library
- **Logging**: Python logging module
- **Containerization**: Docker Compose

## Project Structure

1. **Frontend**:
    - HTML forms for creating and updating meetings
    - JavaScript for handling form submissions and interactions
    - Bootstrap 5 for responsive and modern UI

2. **Backend**:
    - Flask routes for handling API requests
    - MongoDB for storing meeting data
    - Data validation and sanitization to ensure data integrity and security
    - Logging for error tracking and debugging

## Frontend Details

The frontend consists of:
- A form for adding and updating meetings.
- A list to display all meetings with options to edit or delete them.

## Backend Details

The backend provides the following API endpoints:
- `POST /api/meetings`: Create a new meeting.
- `GET /api/meetings`: Retrieve all meetings.
- `GET /api/meetings/<id>`: Retrieve a single meeting by ID.
- `PUT /api/meetings/<id>`: Update a meeting by ID.
- `DELETE /api/meetings/<id>`: Delete a meeting by ID.

## Validation and Sanitization

- **Validation**: We use the Cerberus library to validate incoming data against a predefined schema. This ensures that the data is correctly formatted and meets the required criteria before being processed or stored.
- **Sanitization**: We use the Bleach library to sanitize data by cleaning HTML and JavaScript from string fields. This helps prevent security issues such as cross-site scripting (XSS) attacks.

### Data Validation Schema

The schema used for validating meeting data includes:
- `subject`: Must be a string with a minimum length of 1 and a maximum length of 255 characters.
- `date`: Must match the regex pattern for a valid date (YYYY-MM-DD).
- `start_time` and `end_time`: Must match the regex pattern for valid time (HH:MM).
- `participants`: Must be a string with a minimum length of 1 and a maximum length of 1024 characters.

## How It Works

1. **Creating a Meeting**:
   - User fills out the form and submits it.
   - The frontend sends a `POST` request to the backend.
   - The backend validates and sanitizes the data, then stores it in MongoDB.

2. **Updating a Meeting**:
   - User edits an existing meeting and submits the form.
   - The frontend sends a `PUT` request to the backend with the meeting ID.
   - The backend validates and sanitizes the data, then updates the meeting in MongoDB.

3. **Deleting a Meeting**:
   - User clicks the delete button for a meeting.
   - The frontend sends a `DELETE` request to the backend with the meeting ID.
   - The backend deletes the meeting from MongoDB.

4. **Retrieving Meetings**:
   - The frontend sends a `GET` request to retrieve all meetings.
   - The backend fetches and returns the meeting data from MongoDB.

## Summary

The Meeting Organizer application provides a simple yet effective way to manage meetings. It ensures data integrity through validation and sanitization and offers a user-friendly interface built with Bootstrap 5. The use of Docker Compose for containerization ensures easy deployment and scalability. By implementing robust error handling and logging, the application maintains reliability and facilitates debugging.

# Lost & Found API

This is a FastAPI-based Lost & Found system that allows users to report lost and found items, upload images, and receive automated email notifications when a match is found. The system uses JWT authentication for secure access and TheFuzz library for approximate text matching.

## Live Demo

- Check out the live version of the API at: [Live API](https://lostnfound-fastapi.onrender.com/docs)


## Features
- **Report Lost & Found Items**: Users can report lost or found items along with an optional image.
- **Image Upload**: Supports uploading images for better identification.
- **Automated Email Notifications**: Sends an email when a matching lost or found item is detected.
- **Fuzzy Matching**: Uses `TheFuzz` library for approximate text matching to improve match accuracy.
- **JWT Authentication**: Secures API endpoints with JSON Web Token authentication.

## Technologies Used
- **FastAPI** - For building the API
- **SQLAlchemy** - For database management
- **TheFuzz** - For approximate string matching
- **aiosmtplib** - For sending asynchronous email notifications
- **JWT** - For authentication and authorization
- **Pydantic** - For data validation

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Shivansh-Raj/LostNFound-FastAPI.git
   cd app
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Configure database URL, JWT secret key, and email credentials in a `.env` file.

## Running the Project

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

# Lost & Found Items API

## Lost Items

### `GET /lost-items/`
- Retrieve all lost items

### `POST /lost-items/`
- Report a lost item

### `DELETE /lost-items/{id}`
- Delete a lost item

### `GET /lost-items/images/{item_id}`
- Get lost item image

### `POST /lost-items/claim/{id}`
- Claim a found item

### `GET /lost-items/history`
- Retrieve lost items history

### `GET /lost-items/nearby-lost-items?location={location}`
- Find lost items nearby (filtered by location)

## Found Items

### `GET /found-items/`
- Retrieve all found items

### `POST /found-items/`
- Report a found item

### `DELETE /found-items/{id}`
- Remove a found item

### `GET /found-items/images/{item_id}`
- Get found item image

### `GET /found-items/nearby-found-items?location={location}`
- Find found items nearby (filtered by location)

## Matching

### `GET /match-items/`
- Get matched lost and found items (return items that are possibly a match)

## Users

### `POST /user/register`
- Register a new user

### `POST /user/login`
- Authenticate and log in a user

### `GET /user/{id}`
- Get user details by ID


### Automated Notifications
- When a new lost or found item is reported, the system checks for potential matches using `TheFuzz`.
- If a match is found, an email is sent to the respective user using `aiosmtplib`.

## Contributing
Feel free to fork this repository, submit issues, or contribute via pull requests!

### Author: SHIVANSH RAJDEHL


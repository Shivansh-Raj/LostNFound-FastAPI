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
   git clone https://github.com/your-username/lostnfound-api.git
   cd lostnfound-api
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

## API Endpoints

### Authentication
- **POST** `/user/register` - Register a new user
- **POST** `/user/login` - Authenticate and get JWT token

### Lost & Found Items
- **POST** `/lost-items/` - Report a lost item
- **POST** `/found-items/` - Report a found item
- **POST** `/lost-items/claim/{id}` - Claim a found item
- **GET** `/lost-items/history` - View user's lost item history
- **GET** `/nearby-lost-items?location=xyz` - Filter lost items by location

### Automated Notifications
- When a new lost or found item is reported, the system checks for potential matches using `TheFuzz`.
- If a match is found, an email is sent to the respective user using `aiosmtplib`.

## Contributing
Feel free to fork this repository, submit issues, or contribute via pull requests!

## License
This project is licensed under the MIT License.


# gvsu-folio-subject-search

A Flask web application for searching the Grand Valley State University library catalog by subject. This application integrates with the FOLIO library management system via the Okapi API to provide a user-friendly subject search interface.

## Features

- **Subject Search**: Search the GVSU library catalog by subject terms
- **Pagination**: Load more results dynamically without page refresh
- **Responsive Design**: Mobile-friendly interface with GVSU branding
- **Error Handling**: User-friendly error messages for better UX
- **Secure Authentication**: Credentials passed via environment variables

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- A `.env` file with FOLIO/Okapi credentials

### Installation

1. **Clone or extract the repository:**
   ```bash
   cd gvsu-folio-subject-search
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (see section below)

5. **Run the application:**
   ```bash
   python3 app.py
   ```

6. **Access the app:**
   Open your browser and navigate to `http://localhost:5000`

## Environment Variables

Create a `.env` file in the project root directory with the following variables:

```
OKAPI_BASE_URL=https://your-folio-okapi-base-url
OKAPI_TENANT=fs00001041
OKAPI_USERNAME=your_username
OKAPI_PASSWORD=your_password
```

### Variable Descriptions

- **OKAPI_BASE_URL**: The base URL of your FOLIO/Okapi instance (e.g., `https://folio.example.com`)
- **OKAPI_TENANT**: Your FOLIO tenant ID (defaults to `fs00001041` if not provided)
- **OKAPI_USERNAME**: Username for FOLIO authentication
- **OKAPI_PASSWORD**: Password for FOLIO authentication

**Security Note**: Never commit the `.env` file to version control. The `.env` file is for local development only.

## Project Structure

```
gvsu-folio-subject-search/
├── app.py                    # Flask application entry point
├── config.py                 # Configuration and environment variables
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── services/
│   ├── auth.py              # FOLIO authentication logic
│   └── folio_search.py       # FOLIO search API integration
├── static/
│   ├── css/
│   │   └── main.css         # Styling
│   └── js/
│       └── main.js          # Client-side search functionality
└── templates/
    ├── index.html            # Main page template
    └── _partials/
        └── subject_card.html # Result card component
```

## How It Works

1. User enters a subject term in the search bar
2. Query is sent to the Flask backend (`/` route)
3. Backend authenticates with FOLIO/Okapi and queries the search API
4. Results are rendered as cards with title, subjects, contributors, and creation date
5. User can load additional results via the "Show more results" button
6. The `/load-more` endpoint provides pagination support

## Dependencies

- **Flask**: Web framework
- **requests**: HTTP library for API calls
- **python-dotenv**: Environment variable management

See `requirements.txt` for versions.

## Troubleshooting

- **"Unable to connect to the library system"**: Check your FOLIO credentials and network connectivity
- **"No results found"**: Try a different subject term
- **"Couldn't load more results"**: The button will automatically retry after 3 seconds
- **Missing `.env`**: Ensure the `.env` file exists in the project root with all required variables

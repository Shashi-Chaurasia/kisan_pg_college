# Kisan PG College Website

A comprehensive Flask-based web application for Kisan PG College, Sewarhi, Kushinagar.

## Features

- **Public Website**
  - Home page with college information
  - Faculty profiles
  - Course listings
  - Campus facilities
  - News and notifications
  - Gallery
  - Committee information
  - Alumni section
  - Contact information

- **Admin Panel**
  - Secure authentication
  - CSRF protection
  - Manage faculty members
  - Manage courses and facilities
  - Manage news and notifications
  - Manage committees and members
  - Manage gallery and alumni
  - Responsive design
  - Flash message notifications

## Technology Stack

- **Backend**: Flask 3.1.0
- **Database**: SQLAlchemy with SQLite
- **Forms**: Flask-WTF with CSRF protection
- **Migrations**: Flask-Migrate
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with responsive design

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kishan_pg_college
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -9 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (Optional)
   Create a `.env` file in the project root:
   ```env
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///kishanpgcollege.db
   ```

5. **Initialize the database**
   ```bash
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

   The application will be available at `http://localhost:5005`

## Project Structure

```
kishan_pg_college/
├── app.py                 # Application entry point
├── config.py             # Configuration settings
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── routes/               # Route handlers
│   ├── main_routes.py   # Public website routes
│   └── admin/           # Admin panel routes
│       ├── admin_routes.py
│       ├── committees_routes.py
│       ├── faculty_routes.py
│       └── ...
├── templates/            # HTML templates
│   ├── base.html        # Main layout
│   ├── home.html
│   └── admin/           # Admin templates
├── static/              # Static files
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   ├── images/         # Images
│   └── uploads/        # User uploads
└── migrations/          # Database migrations
```

## Admin Access

1. Navigate to `/admin/login`
2. Use admin credentials to log in
3. Access the dashboard to manage content

## Security Features

- CSRF protection on all forms
- Secure session management
- Password hashing with Werkzeug
- File upload validation
- SQL injection protection via SQLAlchemy ORM
- XSS prevention in templates

## Key Improvements Made

### Admin Panel
- ✅ Added "Back to Website" navigation button
- ✅ Improved UI with modern, responsive design
- ✅ Enhanced flash message system with auto-dismiss
- ✅ Better form styling and validation
- ✅ Added loading states for committee members
- ✅ Improved error handling and user feedback
- ✅ Added CSRF protection
- ✅ Responsive design for mobile devices

### Committee Management
- ✅ Fixed member display issues on frontend
- ✅ Improved photo path handling
- ✅ Added empty state messages
- ✅ Better error handling in API endpoints
- ✅ Enhanced member cards with modal details

### Security
- ✅ Implemented CSRF protection
- ✅ Secure session configuration
- ✅ Environment-based configuration
- ✅ Input validation and sanitization

## Development

### Running in Development Mode

```bash
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python app.py
```

### Running in Production Mode

```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5005 app:application
```

## Database Migrations

Create a new migration:
```bash
flask db migrate -m "Description of changes"
```

Apply migrations:
```bash
flask db upgrade
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

© 2024 Kisan PG College. All rights reserved.

## Support

For issues or questions, please contact the development team.

## Changelog

### Version 2.0 (Current)
- Complete admin panel redesign
- Enhanced security features
- Improved committee management
- Better error handling
- Responsive design improvements
- Flash message system
- Loading states and better UX

### Version 1.0
- Initial release
- Basic CRUD operations
- Public website
- Admin authentication

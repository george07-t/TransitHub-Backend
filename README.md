# TransitHub - Bus Management System

A comprehensive bus and driver management system built with Django REST Framework backend and React frontend.

## Overview

TransitHub is a CRUD application that allows administrators to manage buses and drivers for a transit system. The application provides a clean interface for adding, updating, deleting, and viewing buses and drivers, with functionality to assign drivers to specific buses.

## Project Structure

```
Django React/
├── backend/                    # Django REST Framework API
│   ├── backend/               # Django project configuration
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py        # Main settings file
│   │   ├── urls.py            # Main URL configuration
│   │   └── wsgi.py
│   ├── crud/                  # Main app for CRUD operations
│   │   ├── migrations/        # Database migrations
│   │   ├── __init__.py
│   │   ├── admin.py           # Django admin configuration
│   │   ├── apps.py            # App configuration
│   │   ├── models.py          # Database models (Driver, Bus)
│   │   ├── serializers.py     # DRF serializers
│   │   ├── signals.py         # Django signals
│   │   ├── tests.py           # Unit tests
│   │   └── views.py           # API views (ViewSets)
│   ├── utils/                 # Utility modules
│   │   ├── __init__.py
│   │   └── model_abstracts.py # Abstract model classes
│   ├── db.sqlite3             # SQLite database
│   ├── manage.py              # Django management script
│   └── requirements.txt       # Python dependencies
├── transithub/                # React frontend application
│   ├── public/                # Static assets
│   ├── src/                   # React source code
│   │   ├── Components/        # React components
│   │   │   ├── BusList/       # Bus management component
│   │   │   ├── DriverList/    # Driver management component
│   │   │   ├── Dashbord/      # Main dashboard
│   │   │   ├── LogIn/         # Authentication component
│   │   │   └── ...            # Other components
│   │   ├── App.js             # Main app component
│   │   └── index.js           # Entry point
│   ├── package.json           # Node.js dependencies
│   └── README.md              # Frontend documentation
└── steps/                     # Development modules/steps
    ├── module_1.md
    ├── module_2.md
    └── ...
```

## Backend Features

### Models
- **Driver Model**: Manages driver information with auto-incremented ID, name, and phone number
- **Bus Model**: Manages bus information with name, route, and optional driver assignment

### API Endpoints

#### Authentication
- `POST /api-token-auth/` - Obtain authentication token

#### Driver Management
- `GET /api/drivers/` - List all drivers
- `POST /api/drivers/` - Create a new driver
- `GET /api/drivers/{id}/` - Retrieve a specific driver
- `PUT /api/drivers/{id}/` - Update a driver
- `PATCH /api/drivers/{id}/` - Partially update a driver
- `DELETE /api/drivers/{id}/` - Delete a driver

#### Bus Management
- `GET /api/buses/` - List all buses
- `POST /api/buses/` - Create a new bus
- `GET /api/buses/{id}/` - Retrieve a specific bus
- `PUT /api/buses/{id}/` - Update a bus
- `PATCH /api/buses/{id}/` - Partially update a bus
- `DELETE /api/buses/{id}/` - Delete a bus

### Security & Permissions
- Token-based authentication using Django REST Framework
- Admin/superuser only access to all endpoints
- Custom permission class `IsAdminOrSuperUser`
- CORS enabled for React frontend integration

### Data Validation
- Phone number validation (7-15 digits, numbers only)
- Required field validation for all models
- Driver assignment validation for buses
- Empty string validation for bus names and routes

## Technology Stack

### Backend
- **Django 4.1.3** - Web framework
- **Django REST Framework 3.14.0** - API framework
- **SQLite** - Database (development)
- **Token Authentication** - API security
- **CORS Headers** - Cross-origin resource sharing

### Dependencies
```
asgiref==3.5.2
Django==4.1.3
django-extensions==3.2.1
django-filter==22.1
djangorestframework==3.14.0
python-dotenv==0.21.0
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Django React"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   Create a `.env` file in the backend directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=1
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../transithub
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

## API Usage Examples

### Authentication
```bash
# Get authentication token
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

### Create a Driver
```bash
curl -X POST http://localhost:8000/api/drivers/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your_token_here" \
  -d '{"name": "John Doe", "phone_number": "1234567890"}'
```

### Create a Bus
```bash
curl -X POST http://localhost:8000/api/buses/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token your_token_here" \
  -d '{"bus_name": "City Express", "route": "Downtown Loop", "assigned_driver_id": 1}'
```

## Testing

Run the test suite:
```bash
cd backend
python manage.py test crud
```

The test suite includes:
- Driver CRUD operations
- Bus CRUD operations
- Authentication testing
- Validation testing
- Permission testing

## Development Features

### Django Admin
Access the admin interface at `http://localhost:8000/admin/` to manage data through Django's built-in admin panel.

### API Documentation
The API is self-documenting through Django REST Framework's browsable API. Visit `http://localhost:8000/api/` when the server is running.

### Custom Signals
- Automatic token creation for new users via Django signals

### Validation & Error Handling
- Comprehensive input validation
- Custom error messages
- Proper HTTP status codes

## Production Considerations

### Security
- Update `SECRET_KEY` for production
- Set `DEBUG=False`
- Configure proper `ALLOWED_HOSTS`
- Use environment variables for sensitive data
- Implement proper database (PostgreSQL/MySQL)

### Database
The project uses SQLite for development. For production:
- PostgreSQL recommended
- Update `DATABASES` setting in `settings.py`
- Run migrations on production database

### CORS
Currently configured for development (`localhost:3000`). Update `CORS_ALLOWED_ORIGINS` for production frontend domain.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Contact

For questions or support, please contact the development team.
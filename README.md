# Page Analyzer
***

## About the Project

**Page Analyzer** is a web application for analyzing web pages for their SEO suitability. The project allows you to check websites, save them to a database, and track key SEO metrics.

### Hexlet tests and linter status:
[![Actions Status](https://github.com/Scopp1337/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Scopp1337/python-project-83/actions)

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Scopp1337_python-project-83&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Scopp1337_python-project-83)

### Key Features

- ✅ Add URLs for analysis
- ✅ Validation and normalization of entered addresses
- ✅ Store check history in database
- ✅ View list of all checked websites
- ✅ Detailed information for each URL
- ✅ Modern responsive interface

## Demo

🔗 **[Page Analyzer on Render.com](https://python-project-83.onrender.com)**

## Technologies

### Backend
- **Python 3.10+** — core programming language
- **Flask 3.0+** — web framework
- **Jinja2** — template engine
- **PostgreSQL** — database
- **psycopg2** — PostgreSQL database adapter
- **python-dotenv** — environment variables management
- **validators** — URL validation
- **gunicorn** — WSGI server for production

### Frontend
- **Bootstrap 5** — CSS framework for responsive design
- **HTML5** — page markup

### Development Tools
- **uv** — fast package manager
- **Ruff** — linter and code formatter
- **GitHub Actions** — CI/CD
- **SonarCloud** — code quality analysis
- **Make** — command automation

### Deployment
- **Render.com** — application and database hosting

## Project Structure
page_analyzer/ # Main application package
├── templates/ # HTML templates
│ ├── components/ # Reusable UI components
│ ├── errors/ # Error pages
│ ├── layouts/ # Base layout templates
│ ├── index.html # Main page
│ ├── url.html # Single URL details page
│ └── urls.html # All URLs list page
├── init.py # Package initialization
├── app.py # Flask application and routes
├── parser.py # HTML parsing logic
├── repository.py # Database operations
└── validator.py # URL validation and normalization

database.sql # SQL for database tables
Makefile # Development commands
pyproject.toml # Project dependencies
README.md # Documentation


## Installation

### Clone the repository:

```
git clone https://github.com/Scopp1337/python-project-83.git

cd python-project-83
```


### To use this application, you need to configure the .env file.

After cloning the repository, rename the `.env_example` file to `.env`. Inside the file, you will find the `SECRET_KEY` and `DATABASE_URL` variables. Replace their values with your own.
****

### Next, use the command below to install the required dependencies and generate the database tables.

```
make build
```

### Start the application with the following command:

```
make start
```
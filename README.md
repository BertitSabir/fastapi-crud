# Fastapi-crud: FastAPI CRUD Example

A simple CRUD (Create, Read, Update, Delete) API built with FastAPI and SQLModel for practicing API development in Python.

## Features

- **FastAPI** for high-performance asynchronous APIs
- **SQLModel** for ORM and data validation
- **SQLite** as the database backend
- **CRUD operations** for managing heroes and teams
- **Relationship modeling** between heroes and teams
- Automatic database creation and sample data on startup
- Structured code organization with separate modules for models, routers, and CRUD operations

## Project Structure

```
src/
├── __init__.py
├── crud/                # Database CRUD operations
│   ├── __init__.py
│   ├── hero.py          # Hero CRUD operations
│   └── team.py          # Team CRUD operations
├── database.py          # Database setup, initialization, and sample data
├── dependencies.py      # Dependency injection for DB sessions
├── main.py              # FastAPI app initialization
├── models/              # SQLModel models and schemas
│   ├── __init__.py
│   ├── hero.py          # Hero models
│   └── team.py          # Team models
└── routers/             # API endpoints
    ├── __init__.py
    ├── heroes.py        # Hero endpoints
    └── teams.py         # Team endpoints
pyproject.toml           # Project metadata and dependencies
LICENSE                  # MIT License
README.md                # Project documentation
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd fastapi-crud
   ```
2. **Sync dependencies and create a virtual environment using [uv](https://github.com/astral-sh/uv):**
   ```bash
   uv sync
   source .venv/bin/activate
   ```
   If you don't have `uv` installed, you can install it with:
   ```bash
   pipx install uv
   ```

## Usage

Start the development server:
```bash
fastapi dev main.py
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

Interactive API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Endpoints

### Heroes
- `POST   /heroes/`         - Create a new hero
- `GET    /heroes/`         - List all heroes (with pagination)
- `GET    /heroes/{id}`     - Get a hero by ID
- `PATCH  /heroes/{id}`     - Update a hero by ID
- `DELETE /heroes/{id}`     - Delete a hero by ID

### Teams
- `POST   /teams/`          - Create a new team
- `GET    /teams/`          - List all teams (with pagination)
- `GET    /teams/{id}`      - Get a team by ID
- `PATCH  /teams/{id}`      - Update a team by ID
- `DELETE /teams/{id}`      - Delete a team by ID

## Database

- Uses SQLite (`crud.db`) for storage
- Tables and sample data are created automatically on first run
- Includes relationship between heroes and teams

## Requirements

- Python 3.13+
- FastAPI
- SQLModel
- Uvicorn

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Pull requests and issues are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

> Educational project for learning FastAPI and SQLModel. Inspired by official documentation and examples.

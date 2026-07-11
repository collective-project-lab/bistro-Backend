# Bistro Backend

## Start the project with uv

This project is already set up to use `uv`.

### 1. Create and activate the environment

From the project root:

```bash
uv venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Apply database migrations

```bash
uv run python manage.py migrate
```

### 4. Start the development server

```bash
uv run python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Optional: create a superuser

```bash
uv run python manage.py createsuperuser
```

## Notes

- The project uses Django, Django REST Framework, and Simple JWT.
- If you want to run commands inside the environment, use `uv run ...` so `uv` manages the interpreter for you.

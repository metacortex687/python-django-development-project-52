install:
	uv sync --frozen

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate --noinput

build:
	./build.sh
	
render-start:
	gunicorn task_manager.wsgi

create-superuser-from-env:
	uv run python manage.py create_superuser_from_env
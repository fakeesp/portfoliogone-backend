
project_dir := .

.PHONY: reformat
reformat:
	@uv run black $(project_dir)
	@uv run ruff check $(project_dir) --fix

.PHONY: lint
lint: reformat
	@uv run mypy $(project_dir)

.PHONY: migration
migration:
	@uv run alembic revision \
	  --autogenerate \
	  --rev-id $(shell python migrations/_get_revision_id.py) \
	  --message $(message)

.PHONY: migrate
migrate:
	@uv run alembic upgrade head

.PHONY: run
run:
	@uv run python -m app

.PHONY: app-build
app-build:
	@docker compose build 

.PHONY: app-run-db
app-run-db:
	@docker compose up -d --remove-orphans postgres dragonfly nats

.PHONY: app-destroy
app-destroy:
	@docker compose down -v --remove-orphans


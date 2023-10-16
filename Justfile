# Show this help
help:
  @just --list

# Do file linting
lint:
  poetry run flake8

# Perform static type checking
types:
  poetry run mypy circpy

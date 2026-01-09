#!/bin/bash
# Скрипт для автоматического исправления проблем с Ruff
uv tool run ruff check --fix app/
uv tool run ruff format app/

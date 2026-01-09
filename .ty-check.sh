#!/bin/bash
# Скрипт для запуска проверки типов с ty
# Игнорируем unresolved-reference для forward references в SQLAlchemy моделях
uv tool run ty check app/models/ app/routers/ app/schemas/ --ignore unresolved-reference

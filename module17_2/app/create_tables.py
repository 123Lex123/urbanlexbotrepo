from sqlalchemy import create_engine
from app.backend.db import Base, engine
from app.models import user
from app.models import task


# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)
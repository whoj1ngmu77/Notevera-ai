"""
Notevera AI – SQLAlchemy table definitions
"""
import sqlalchemy
from database import metadata

users = sqlalchemy.Table(
    "users", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(200), unique=True, nullable=False),
    sqlalchemy.Column("password_hash", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("avatar", sqlalchemy.String(500), default=""),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
)

materials = sqlalchemy.Table(
    "materials", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(300), nullable=False),
    sqlalchemy.Column("source_type", sqlalchemy.String(50), nullable=False),  # pdf, image, text, youtube
    sqlalchemy.Column("extracted_text", sqlalchemy.Text, default=""),
    sqlalchemy.Column("original_filename", sqlalchemy.String(300), default=""),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
)

notes = sqlalchemy.Table(
    "notes", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("material_id", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("title", sqlalchemy.String(300), nullable=False),
    sqlalchemy.Column("content", sqlalchemy.Text, nullable=False),  # JSON string of structured notes
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
)

study_plans = sqlalchemy.Table(
    "study_plans", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(300), nullable=False),
    sqlalchemy.Column("exam_date", sqlalchemy.String(50), default=""),
    sqlalchemy.Column("plan_data", sqlalchemy.Text, nullable=False),  # JSON string
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
)

study_tasks = sqlalchemy.Table(
    "study_tasks", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("plan_id", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("title", sqlalchemy.String(300), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(500), default=""),
    sqlalchemy.Column("due_date", sqlalchemy.String(50), default=""),
    sqlalchemy.Column("completed", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()),
)

settings = sqlalchemy.Table(
    "settings", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, unique=True, nullable=False),
    sqlalchemy.Column("theme", sqlalchemy.String(20), default="dark"),
    sqlalchemy.Column("calendar_integration", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("notifications", sqlalchemy.Boolean, default=True),
)

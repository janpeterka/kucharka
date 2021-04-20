from app import db

# Define models
users_have_roles = db.Table(
    "users_have_roles",
    db.Column("user_id", db.Integer(), db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("roles.id")),
)

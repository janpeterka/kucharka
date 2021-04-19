from app import db

# Define models
users_have_roles = db.Table(
    "users_have_roles",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)

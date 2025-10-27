from app.models.user import create_user

create_user("admin1", "pass123", role="admin")
create_user("operator1", "pass123", role="operator")
create_user("viewer1", "pass123", role="viewer")

print("Usuarios de prueba creados:")
print("admin1 / pass123 (Admin)")
print("operator1 / pass123 (Operator)")
print("viewer1 / pass123 (Viewer)")

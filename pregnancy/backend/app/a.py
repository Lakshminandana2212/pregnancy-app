from flask_jwt_extended import get_jwt_identity
print(get_jwt_identity)  # Should not throw an error

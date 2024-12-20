from fastapi_users.authentication import BearerTransport

# TODO update URL
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

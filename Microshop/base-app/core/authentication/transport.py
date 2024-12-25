from fastapi_users.authentication import BearerTransport

from core.config import settings

# TODO update URL
bearer_transport = BearerTransport(tokenUrl=settings.api.bearer_token_url)

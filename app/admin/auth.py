import jwt
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.authentification.auth import create_access_token
from app.config import settings
from app.users.auth import auth_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        try:
            form = await request.form()
            email, password = form["username"], form["password"]

            user = await auth_user(email=email, password=password)
            if not user:
                return False

            access_token = create_access_token({
                "sub": str(user.id)
            })

            request.session.update({
                "token": access_token,
                "user_id": str(user.id)
            })

            return True
        except Exception as e:
            print(f"Login error: {e}")
            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        try:
            token = request.session.get("token")
            if not token:
                return False

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

            user_id = payload.get("sub")
            if not user_id:
                return False

            return True
        except jwt.PyJWTError as e:
            print(f"Auth error: {e}")
            return False


authentication_backend = AdminAuth(secret_key="...")

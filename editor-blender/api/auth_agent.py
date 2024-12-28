import asyncio
import traceback
from dataclasses import dataclass
from typing import Any

from ..client import client

# TODO: Handle returned cookies
# CookieJar?


@dataclass
class LoginResult:
    success: bool
    token: str = ""
    err: str = ""


class AuthAgent:
    async def login(self, username: str, password: str) -> LoginResult:
        """Login to the server and get a token or an error message."""
        data = {"username": username, "password": password}

        try:
            res: dict[str, Any] = await client.post("/login", json=data)
            token = res.get("token")
            if not token:
                raise Exception(res["err"])
            return LoginResult(success=True, token=token)

        except asyncio.CancelledError:
            return LoginResult(success=False, err="Timeout")

        except Exception as e:
            traceback.print_exc()
            return LoginResult(success=False, err=str(e))

    async def logout(self) -> bool:
        """Logout from the server."""
        try:
            res: dict[str, Any] = await client.post("/logout")
            if not res.get("success"):
                raise Exception(res["err"])
            return True

        except asyncio.CancelledError:
            return False

        except Exception:
            traceback.print_exc()
            return False

    async def check_token(self) -> bool:
        """Check if the authentication token is still valid."""
        try:
            res: dict[str, Any] = await client.get("/checkToken")
            token = res.get("token")
            if not token:
                raise Exception(res["err"])
            return True

        except asyncio.CancelledError:
            return False

        except Exception:
            traceback.print_exc()
            return False


auth_agent = AuthAgent()

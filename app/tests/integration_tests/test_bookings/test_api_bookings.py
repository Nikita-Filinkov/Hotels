
from unittest.mock import MagicMock, patch

from httpx import AsyncClient


async def test_get_bookings(auth_asyncclient: AsyncClient):
    with patch('app.tasks.tasks.send_email_conformation_booking.delay', MagicMock()):
        response = await auth_asyncclient.get("/bookings")
        assert response.status_code == 200
        assert len(response.json()) == 2

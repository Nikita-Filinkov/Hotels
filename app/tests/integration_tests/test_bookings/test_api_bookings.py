
from httpx import AsyncClient
from unittest.mock import patch, MagicMock


async def test_get_bookings(auth_asyncclient: AsyncClient):
    with patch('app.tasks.tasks.send_email_conformation_booking.delay', MagicMock()):
        response = await auth_asyncclient.get("/bookings")
        assert response.status_code == 200
        assert len(response.json()) == 2

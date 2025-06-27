from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from httpx import AsyncClient

from app.bookings.service import BookingsService
from app.tests.conftest import auth_asyncclient, session


@pytest.mark.parametrize(
    ['user_id', 'room_id', 'date_from', 'date_to', 'status_code'],
    [
        (1, 1, '2026-05-15', '2026-06-30', 200),
        (1, 2, '2026-05-15', '2026-06-30', 409)
    ]
)
async def test_add_booking(
        user_id,
        room_id,
        date_from,
        date_to,
        status_code,
        auth_asyncclient: AsyncClient,
        session
):
    date_from = datetime.strptime(date_from, '%Y-%m-%d')
    date_to = datetime.strptime(date_to, '%Y-%m-%d')
    response = await auth_asyncclient.post("/bookings/add", params={
        'user_id': user_id,
        'room_id': room_id,
        'date_from': date_from,
        'date_to': date_to
    })
    assert response.status_code == status_code


async def test_auth_client(auth_asyncclient):
    with patch('app.tasks.tasks.send_email_conformation_booking.delay', MagicMock()):
        response = await auth_asyncclient.get("/bookings")
        assert response.status_code == 200
        assert "booking_access_token" in auth_asyncclient.cookies

import pytest
from httpx import AsyncClient


from app.tests.conftest import asyncclient


@pytest.mark.parametrize(
    ['locations', 'date_from', 'date_to', 'status_code'],
    [
        ('Республика Алтай, Майминский район, село Урлу-Аспак, Лесхозная улица, 20', '2023-06-15', '2023-06-30', 200),
        ('корректный адрес', '2023-06-30', '2023-06-15', 400),
        ('Республика Алтай, Майминский район, село Урлу-Аспак, Лесхозная улица, 20', '2023-04-01', '2023-04-39', 200),
        ('Республика Алтай, Майминский район, поселок Барангол, Чуйская улица 40а', '2023-04-01', '2023-04-19', 200),
    ]
)
async def test_get_hotels(
        locations,
        date_from,
        date_to,
        status_code,
        asyncclient: AsyncClient,
):
    request = await asyncclient.get(
        url=f'/hotels/{locations}',
        params={
            'date_from': date_from,
            'date_to': date_to
        }
    )

    assert request.status_code == status_code
    if status_code == 200:
        assert len(request.json()) > 0

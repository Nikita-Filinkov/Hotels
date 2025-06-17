import pytest
from app.users.service import UsersService


@pytest.mark.parametrize(['id_user', 'email', 'is_present'], [
    (1, 'test@test.com', True),
    (2, 'artem@example.com', True),
    (6, '...', False),
])
async def test_find_user_by_id(id_user, email, is_present):
    user = await UsersService.find_by_id(id_user)

    if is_present:
        assert user.id == id_user
        assert user.email == email
    else:
        assert not user


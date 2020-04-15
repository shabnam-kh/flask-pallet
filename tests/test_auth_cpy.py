import pytest

from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response=client.post(
        '/auth/register',
        data={"username":'a', 'password':'a'}
    )
    assert 'hhtp://localhost/auth/login' in response.headers['Location']
    with app.app_context():
        assert get_db().execute(
            "select * from users where user_name='a'"
        ).fetchOne() is not None

@pytest.mark.parametrize(
    ('username','password','message'),(
    ('','a',b'username is required'),
    ('a','',b'password is required'),
    ('test','test',b'user already exist')
    ))
def test_register_validation(client, username, password, message):
    response=client.post(
        'auth/register',
        data={'username':username, 'password':password}
    )
    assert message in response.data

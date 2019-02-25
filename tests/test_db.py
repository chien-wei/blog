import pytest
from flaskr.db import get_mongo_client

def test_get_close_db(app):
    with app.app_context():
        db = get_mongo_client()
        assert db is get_mongo_client()

    with pytest.raises(TypeError) as e:
        db.web.posts.findd()
    assert 'not callable' in str(e)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_client', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
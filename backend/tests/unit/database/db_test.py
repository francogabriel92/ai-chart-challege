import pytest

from app.database.db import run_query


@pytest.fixture
def mock_session(mocker):
    # Create a mock session object
    return mocker.Mock()


def test_run_query_returns_results(mocker, mock_session):
    # Patch get_session to yield our mock session
    mocker.patch("app.database.db.get_session", return_value=iter([mock_session]))
    # Mock session.exec to return a list of rows with _mapping attribute
    mock_row = mocker.Mock()
    mock_row._mapping = {"id": 1, "name": "test"}
    mock_session.exec.return_value = [mock_row]
    result = run_query("SELECT * FROM test")
    assert result == [{"id": 1, "name": "test"}]


def test_run_query_empty_query_raises(mocker, mock_session):
    mocker.patch("app.database.db.get_session", return_value=iter([mock_session]))
    with pytest.raises(ValueError):
        run_query("")


def test_run_query_session_none(mocker):
    mocker.patch("app.database.db.get_session", return_value=iter([None]))
    with pytest.raises(Exception, match="Database session not available"):
        run_query("SELECT 1")


def test_run_query_exec_exception(mocker, mock_session):
    mocker.patch("app.database.db.get_session", return_value=iter([mock_session]))
    mock_session.exec.side_effect = Exception("DB error")
    with pytest.raises(Exception, match="DB error"):
        run_query("SELECT * FROM test")


def test_run_query_no_results(mocker, mock_session):
    mocker.patch("app.database.db.get_session", return_value=iter([mock_session]))
    mock_session.exec.return_value = []
    result = run_query("SELECT * FROM test")
    assert result == []

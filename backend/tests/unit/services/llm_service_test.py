import pytest
from app.services.llm_service import LLMService


def test_make_query_success(mocker):
    # Mocked response from OpenAI
    mock_content = '{"sql": "SELECT * FROM sales;", "chart_type": "bar", "title": "Test", "axis_labels": ["x", "y"]}'
    mock_response = mocker.Mock()
    mock_response.choices = [mocker.Mock(message=mocker.Mock(content=mock_content))]

    # Patch the OpenAI client call
    mocker.patch(
        "app.services.llm_service.client.chat.completions.create",
        return_value=mock_response,
    )

    service = LLMService()
    result = service.make_query("Show me sales")
    assert result["sql"] == "SELECT * FROM sales;"
    assert result["chart_type"] == "bar"
    assert result["title"] == "Test"
    assert result["axis_labels"] == ["x", "y"]


def test_make_query_invalid_json(mocker):
    # Mocked response with invalid JSON
    mock_content = '{"sql": "SELEC"'
    mock_response = mocker.Mock()
    mock_response.choices = [mocker.Mock(message=mocker.Mock(content=mock_content))]

    # Patch the OpenAI client call
    mocker.patch(
        "app.services.llm_service.client.chat.completions.create",
        return_value=mock_response,
    )

    service = LLMService()

    with pytest.raises(Exception, match="Invalid JSON"):
        service.make_query("Show me sales")

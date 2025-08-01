import pytest
from app.services.chart_service import ChartService


@pytest.fixture
def chart_service():
    # Instantiate ChartService for testing
    return ChartService()


def test_create_bar_chart(chart_service):
    # Test bar chart creation with valid data and axis labels
    data = [{"Category": "A", "Value": 10}, {"Category": "B", "Value": 20}]
    result = chart_service.create_chart(
        data, chart_type="bar", title="Bar Chart", axis_labels=["Category", "Value"]
    )
    assert result["chart_type"] == "bar"
    assert result["title"] == "Bar Chart"
    assert "chart_json" in result
    assert result["chart_json"]["layout"]["title"]["text"] == "Bar Chart"


def test_create_line_chart(chart_service):
    # Test line chart creation with valid data and axis labels
    data = [{"Time": 1, "Value": 5}, {"Time": 2, "Value": 15}]
    result = chart_service.create_chart(
        data, chart_type="line", title="Line Chart", axis_labels=["Time", "Value"]
    )
    assert result["chart_type"] == "line"
    assert result["title"] == "Line Chart"
    assert "chart_json" in result
    assert result["chart_json"]["layout"]["title"]["text"] == "Line Chart"


def test_create_pie_chart(chart_service):
    # Test pie chart creation with valid data
    data = [{"Type": "X", "Amount": 30}, {"Type": "Y", "Amount": 70}]
    result = chart_service.create_chart(data, chart_type="pie", title="Pie Chart")
    assert result["chart_type"] == "pie"
    assert result["title"] == "Pie Chart"
    assert "chart_json" in result
    assert result["chart_json"]["layout"]["title"]["text"] == "Pie Chart"


def test_create_area_chart(chart_service):
    # Test area chart creation with valid data
    data = [{"Day": 1, "Score": 100}, {"Day": 2, "Score": 200}]
    result = chart_service.create_chart(data, chart_type="area", title="Area Chart")
    assert result["chart_type"] == "area"
    assert result["title"] == "Area Chart"
    assert "chart_json" in result
    assert result["chart_json"]["layout"]["title"]["text"] == "Area Chart"


def test_create_chart_with_empty_data(chart_service):
    # Test that ValueError is raised when data is empty
    with pytest.raises(ValueError, match="No data provided"):
        chart_service.create_chart([], chart_type="bar")


def test_create_chart_with_unsupported_axis_labels_amount(chart_service):
    # Test that ValueError is raised when too many axis labels are provided
    data = [{"A": 1, "B": 2}]
    with pytest.raises(ValueError, match="Axis labels should not exceed 2 items"):
        chart_service.create_chart(data, chart_type="bar", axis_labels=["A", "B", "C"])


def test_create_chart_with_unsupported_type(chart_service):
    # Test that ValueError is raised for unsupported chart type
    data = [{"A": 1, "B": 2}]
    with pytest.raises(ValueError, match="Unsupported chart type"):
        chart_service.create_chart(data, chart_type="histogram")

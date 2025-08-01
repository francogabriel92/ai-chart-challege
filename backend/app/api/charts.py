from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.services.llm_service import LLMService
from app.services.chart_service import ChartService
from app.database.db import run_query, get_session

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    chart: Optional[Dict[str, Any]] = None


@router.post("/create", response_model=QueryResponse)
async def answer_question(request: QuestionRequest, session=Depends(get_session)):
    ai_service = LLMService()
    chart_service = ChartService()

    if len(request.question.strip()) < 10 or len(request.question.strip()) > 200:
        raise HTTPException(
            status_code=400,
            detail="Question must be between 10 and 200 characters long",
        )

    try:
        # Get AI response with SQL query and chart type
        ai_response = ai_service.make_query(request.question)

        if not ai_response or "sql" not in ai_response:
            raise HTTPException(status_code=400, detail="No valid query generated")

        if not ai_response["axis_labels"] or len(ai_response["axis_labels"]) > 2:
            raise HTTPException(
                status_code=400,
                detail="This chart is not currently supported, please try another one",
            )

        sql_query = ai_response["sql"]
        chart_type = ai_response.get("chart_type", "bar")
        title = ai_response.get("title", "Chart")
        axis_labels = ai_response.get("axis_labels", [])

        # Execute the query
        result = run_query(sql_query)

        if not result or len(result) == 0:
            raise HTTPException(status_code=404, detail="No data found for the query")

        # Generate chart
        chart_json = None

        try:
            chart_result = chart_service.create_chart(
                data=result, chart_type=chart_type, title=title, axis_labels=axis_labels
            )
            chart_json = chart_result["chart_json"]
        except Exception as chart_error:
            raise HTTPException(status_code=400, detail=f"Chart creation error")

        return QueryResponse(
            chart=chart_json,
        )

    except Exception as e:
        # Handle specific exceptions and return appropriate HTTP errors
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error: Internal server error")

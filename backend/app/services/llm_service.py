from app.utils.config import get_settings
from openai import OpenAI
import json

client = OpenAI(api_key=get_settings().OPENAI_API_KEY)


class LLMService:
    def make_query(self, query_text: str) -> dict:
        prompt = f"""
        You are a data analyst assistant.

        Table: sales(id:int, date:timestamp, week_day:text, ticket_number:text, waiter:text, product_name:text, quantity:float, unitary_price:float, total:float)
        Data range: 2024-09-21 to 2024-11-20

        Rules:
        - If question can't be answered with this table, return: {{ error: "This question cannot be answered with the available data" }}
        - Always return a valid SQL query suited to the question and a chart type
        - Match axis labels to the language of the question
        - Use correct date filters and aggregations
        - Avoid UPDATE, DELETE, or INSERT queries

        Output format:
        {{
        "sql": "...",
        "chart_type": "bar|line|pie|area"
        "title": "Chart Title"
        "axis_labels": ["label1", "label2", ...]
        }}

        Chart guide:
        bar: categorical comparison (e.g. top products, sales by waiter)
        line: trends over time (e.g. daily sales)
        area: cumulative time series
        pie: share of total (e.g. sales per product as %)

        Q: {query_text}
        JSON:
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            result = response.choices[0].message.content

            # Parse the JSON response
            parsed_result = json.loads(result)
            return parsed_result
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response from AI: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

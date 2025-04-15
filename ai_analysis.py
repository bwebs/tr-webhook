import json
import os

from google import genai
from google.genai import types

from markdown_mail import send_markdown_message


def analyze_stock_data(metadata: dict, rows: list) -> str:
    """
    Analyzes stock data using Gemini AI and returns a markdown formatted analysis.

    Args:
        metadata: Dictionary containing metadata about the query
        rows: List of dictionaries containing the stock data

    Returns:
        str: Markdown formatted analysis of the stock data
    """
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-pro-preview-03-25"

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"""Can you analyze this stock data and provide a summary with recent news or reasons for change? Write this in markdown format. I would like the markdown to also have links back to the sources you found. Here is the data:
<metadata>
{json.dumps(metadata, indent=2)}
</metadata>
<data>
{json.dumps(rows, indent=2)}
</data>"""
                ),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            properties={
                "markdown": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
                "email_subject_line": genai.types.Schema(
                    type=genai.types.Type.STRING,
                ),
            },
            required=["markdown", "email_subject_line"],
        ),
    )

    # Get the response from Gemini
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    # Parse the response and return the markdown
    response_json = json.loads(response.text)
    markdown = response_json.get("markdown")
    subject = response_json.get("email_subject_line")
    if not markdown:
        raise Exception("No markdown returned from Gemini")
    send_markdown_message(markdown, subject)

    return markdown

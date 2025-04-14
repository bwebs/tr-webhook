import json

import flask
import functions_framework

from ai_analysis import analyze_stock_data


@functions_framework.http
def main(request: flask.Request) -> flask.typing.ResponseReturnValue:
    if request.method != "POST":
        return flask.jsonify({"error": "Method not allowed"}), 405

    try:
        # Get the request data
        request_data = request.get_json()

        if not request_data or "attachment" not in request_data:
            return flask.jsonify({"error": "No attachment provided"}), 400

        # Extract metadata and rows from the attachment
        attachment = request_data.get("attachment", {})
        data = json.loads(attachment.get("data", "{}"))

        # The attachment typically contains metadata and rows
        metadata = data.get("metadata", {})
        rows = data.get("rows", [])

        # Get AI analysis of the data
        analysis = analyze_stock_data(metadata, rows)

        # Prepare response
        response_data = {"metadata": metadata, "rows": rows, "analysis": analysis}

        return flask.jsonify(response_data)

    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    main()

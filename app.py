from flask import Flask, jsonify, render_template, request
from services.folio_search import search_instances_by_subject, FolioSearchError

app = Flask(__name__)

# Main page: accepts a subject query and renders results (or an error).
@app.route("/")
def index():
    # Pull query params from the URL so refresh/back works naturally.
    subject = request.args.get("subject", "").strip()
    offset = int(request.args.get("offset", 0))

    # Default state for the template.
    results = None
    error = None

    # Only call the API if the user actually searched.
    if subject:
        try:
            results = search_instances_by_subject(subject, offset=offset)
        except FolioSearchError as e:
            error = str(e)

    # Render the page with whatever we have.
    return render_template(
        "index.html",
        subject=subject,
        offset=offset,
        results=results,
        error=error
    )


@app.route("/load-more")
def load_more():
    subject = request.args.get("subject", "").strip()
    offset = int(request.args.get("offset", 0))

    if not subject:
        return jsonify({"error": "Subject is required."}), 400

    try:
        results = search_instances_by_subject(subject, offset=offset)
    except FolioSearchError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)

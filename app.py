from flask import Flask, render_template

app = Flask(__name__)  # Flask app instance.

@app.route("/")
def index():
    # Render the landing page template.
    return render_template("index.html")

if __name__ == "__main__":
    # Enable debug mode only for local development.
    app.run(debug=True)

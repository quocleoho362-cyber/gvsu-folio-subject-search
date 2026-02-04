from flask import Flask, render_template
from services.auth import get_okapi_token, FolioAuthError

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# TEMP: remove or disable before final
@app.route("/debug-token")
def debug_token():
    try:
        token = get_okapi_token()
        return {"ok": True, "token_prefix": token[:12], "token_len": len(token)}
    except FolioAuthError as e:
        return {"ok": False, "error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)

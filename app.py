from flask import Flask, request, render_template
from scanner import text_scan

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("test")

    #If file doesn't exist, prevent crashing
    if not file:
        return {"error": "File missing"}, 400

    content = file.read().decode("utf-8")

    results = text_scan(content)
    return results

if __name__ == "__main__":
    app.run(debug=True)
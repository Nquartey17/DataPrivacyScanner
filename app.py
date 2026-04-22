from flask import Flask, request, render_template
from scanner import text_scan, keyword_finder

PII_KEYWORDS = ["date of birth","dob", "born", "ssn", "social security", "email", "phone number", "DL", "driver's license",
                "alien", "passport"]

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def upload_file():
    file = request.files.get("test")

    #If file doesn't exist, prevent crashing
    if not file:
        return {"error": "File missing"}, 400

    content = file.read().decode("utf-8")
    results = text_scan(content)
    keywords = keyword_finder(content, PII_KEYWORDS)

    return render_template("results.html", results=results, keywords=keywords)

if __name__ == "__main__":
    app.run(debug=True)
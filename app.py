from flask import Flask, request, render_template
from scanner import text_scan, keyword_finder
from conversion import extract_text

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

    try:
        content = extract_text(file)
        results = text_scan(content)
        keywords = keyword_finder(content, PII_KEYWORDS)

        return render_template("results.html", results=results, keywords=keywords)

    except ValueError as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
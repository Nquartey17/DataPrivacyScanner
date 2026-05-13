from flask import Flask, request, render_template
from scanner import text_scan, keyword_finder
from conversion import extract_text

#Changing PII_KEYWORDS to dictionary for multiple terms
#Idea: Add an option to type custom keywords
PII_KEYWORDS = {
    "dl":["DL","driver's license", "license", "learner's permit"],
    "sid": ["state id", "identification card", "SID"],
    "a_num": ["alien registration number", "A-number", "USCIS"],
    "passport": ["passport", "passport number"]
}
default_keywords = ["date of birth","dob", "born", "ssn", "social security", "email", "phone number"]

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
        pii_selections = request.form.getlist("pii_dropdown")
        all_keywords = default_keywords.copy()

        for selection in pii_selections:
            if selection in PII_KEYWORDS:
                all_keywords.extend(PII_KEYWORDS[selection])

        keywords = keyword_finder(content, all_keywords)

        return render_template("results.html", results=results, keywords=keywords)

    except ValueError as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
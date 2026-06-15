from flask import Flask, request, render_template
from scanner import text_scan, keyword_finder, keyword_count
from conversion import extract_text

#Changing PII_KEYWORDS to dictionary for multiple terms
#Idea: Add an option to type custom keywords
# Idea: Suggested keywords depending on selection. To avoid too many words found, suggest keywords to search

default_keywords = ["date of birth","dob", "born", "ssn", "social security", "email", "phone number"]

DEFAULT_KEYWORDS = {
    "dob":["dob", "date of birth", "birth certificate", "born"],
    "ssn":["ssn", "social security"],
    "contact": ["address", "residence", "phone", "mobile number", "cell number", "email"]
}

PII_KEYWORDS = {
    "dl":["DL","driver's license", "license", "learner's permit"],
    "sid": ["state id", "identification card", "SID"],
    "a_num": ["alien registration number", "A-number", "USCIS"],
    "passport": ["passport", "passport number"],
    "mid": ["dod", "military"]
}

PHI_KEYWORDS = {
    "hx":["history","smoker", "smoking", "allergy", "allergies", "medical history", "hx"], #social, family
    "tx":["therapy", "tx", "treatment", "cpt", "service code", "hcpcs"],
    "dx":["diagnosis", "dx", "diagnosed"], # give examples of DX codes
    "rx": ["medication", "rx"], #mg, take, taking, prescribed
    "lab": ["lab results", "results", "lab", "chemistry"], #mg
    "phys": ["attending", "attn", "physician"], # suggest a list of physician titles
    "mrn": ["mrn", "omrn", "emrn", "medical record number", "mr #", "mr#"],
    "pid": ["pid", "patient id", "pt id", "ptid", "patient number"]
}

FINANCE_HDV = {
    "bnk":["ABA", "bank account", "bank account number", "checking", "savings"],
    "routing":["routing", "RTN", "sort code"],
    "fncl":["IRA", "stock", "roth", "investment", "retirement"],
    "crdt":["credit card", "debit card", "credit"],
    "hdv":["insurance", "policy number", "member id", "group number", "group id", "plan number"],
    "mcd": ["medicare", "medicaid", "tricare"]
}

SECURITY = {
    "user": ["user id", "username", "password", "pwd", "user", "login", "log in"],
    "sq": ["security question", "answer"],
    "dsig": ["digital signature", "electronically signed"]
}

def keyword_addition(list_name, keyword_list, all_keywords):
    for selection in list_name:
        if selection in keyword_list:
            all_keywords.extend(keyword_list[selection])

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def upload_file():
    file = request.files.get("files")

    #If file doesn't exist, prevent crashing
    if not file:
        return {"error": "File missing"}, 400

    try:
        content = extract_text(file)
        results = text_scan(content)
        pii_selections = request.form.getlist("pii_dropdown")
        phi_selections = request.form.getlist("phi_dropdown")
        finance_hdv = request.form.getlist("finance_hdv")
        security = request.form.getlist("security")

        # Taking values from DEFAULT_KEYWORDS and changing it into list
        all_keywords = []
        for keywords in DEFAULT_KEYWORDS.values():
            all_keywords.extend(keywords)

        keyword_addition(DEFAULT_KEYWORDS.keys(), DEFAULT_KEYWORDS, all_keywords)
        keyword_addition(pii_selections, PII_KEYWORDS, all_keywords)
        keyword_addition(phi_selections, PHI_KEYWORDS, all_keywords)
        keyword_addition(finance_hdv, FINANCE_HDV, all_keywords)
        keyword_addition(security, SECURITY, all_keywords)

        keywords = keyword_finder(content, all_keywords)

        pii_count = keyword_count(content, PII_KEYWORDS)
        pii_keywords = keyword_finder(content, PII_KEYWORDS)

        phi_count = keyword_count(content, PHI_KEYWORDS)
        phi_keywords = keyword_finder(content, PHI_KEYWORDS)

        finance_hdv_count = keyword_count(content, FINANCE_HDV)
        fhdv_keywords = keyword_finder(content, FINANCE_HDV)

        security_count = keyword_count(content, SECURITY)
        sq_keywords = keyword_finder(content, SECURITY)

        return render_template("results.html", results=results, keywords=keywords,
                               pii_count=pii_count, pii_keywords=pii_keywords, phi_count=phi_count, phi_keywords=phi_keywords,
                               finance_hdv_count=finance_hdv_count, fhdv_keywords=fhdv_keywords, sq_keywords =sq_keywords,
                               security_count=security_count)

    except ValueError as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
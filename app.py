from flask import Flask, request, render_template
from scanner import text_scan, keyword_finder, keyword_count, keyword_hits, terms_to_labels
from conversion import extract_text
from dashboard import init_dashboard
from lists import *
import plotly.express as px

#Idea: Add an option to type custom keywords
# Idea: Suggested keywords depending on selection. To avoid too many words found, suggest keywords to search

def add_keywords(keyword_ids, all_keywords):
    for keyword_id in keyword_ids:
        if keyword_id in TERMS:
            all_keywords.extend(TERMS[keyword_id]["keywords"])

def convert_to_labels(count_dict):
    return {
        TERMS[key]["label"]: value
        for key, value in count_dict.items()
    }

def checkbox_selections(selected):
    return {
        term: TERMS[term]["keywords"]
        for term in selected
        if term in TERMS
    }

def calculate_average_risk(*count_dicts):
    total_risk = 0
    total_findings = 0

    low = 0
    medium = 0
    high = 0

    for counts in count_dicts:
        for category, count in counts.items():
            #Skip term if count == 0
            if count == 0:
                continue

            risk = TERMS[category]["risk"]

            total_risk += risk * count
            total_findings += count

            if risk == 1:
                low += count
            elif risk == 2:
                medium += count
            elif risk == 3:
                high += count

    average = round(total_risk / total_findings, 2) if total_findings else 0

    return {
        "average": average,
        "low": low,
        "medium": medium,
        "high": high,
        "total": total_findings
    }


app = Flask(__name__)
dash_app = init_dashboard(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/results", methods=["POST"])
def upload_file():
    file = request.files.get("files")

    #If file doesn't exist, prevent crashing
    if not file:
        return {"error": "File missing"}, 400

    try:
        content = extract_text(file)
        results = text_scan(content)

        #Get selected inputs from index.html checklist
        pii_selections = request.form.getlist("pii_dropdown")
        phi_selections = request.form.getlist("phi_dropdown")
        finance_hdv = request.form.getlist("finance_hdv")
        security = request.form.getlist("security")

        # Taking values from DEFAULT_KEYWORDS and changing it into list
        all_keywords = []

        #always including default terms
        add_keywords(CATEGORIES["default"], all_keywords)

        add_keywords(pii_selections, all_keywords)
        add_keywords(phi_selections, all_keywords)
        add_keywords(finance_hdv, all_keywords)
        add_keywords(security, all_keywords)

        keywords = keyword_finder(content, all_keywords)

        # returning new dictionary for selected terms and only displaying selected terms
        selected_pii = checkbox_selections(pii_selections)
        pii_count = keyword_count(content, selected_pii)
        pii_count_display = convert_to_labels(PII_LABELS)
        pii_keywords = keyword_hits(content, selected_pii)
        pii_convert = terms_to_labels(pii_keywords)

        selected_phi = checkbox_selections(phi_selections)
        phi_count = keyword_count(content, selected_phi)
        phi_count_display = convert_to_labels(PHI_LABELS)
        phi_keywords = keyword_hits(content, selected_phi)
        phi_convert = terms_to_labels(phi_keywords)

        selected_finance = checkbox_selections(finance_hdv)
        finance_hdv_count = keyword_count(content, selected_finance)
        finance_hdv_display = convert_to_labels(FINANCE_HDV_LABELS)
        fhdv_keywords = keyword_hits(content, selected_finance)
        fhdv_convert = terms_to_labels(fhdv_keywords)

        selected_security = checkbox_selections(security)
        security_count = keyword_count(content, selected_security)
        security_display = convert_to_labels(SECURITY_LABELS)
        sq_keywords = keyword_hits(content, selected_security)
        sq_convert = terms_to_labels(sq_keywords)

        risk = calculate_average_risk(pii_count,phi_count,finance_hdv_count,security_count)

        # Donut chart display
        fig = px.pie(
            names=["Low", "Medium", "High"],
            values=[risk["low"],risk["medium"],risk["high"]],
            hole=0.4,
            title="Risk Level Distribution",
            color=["Low", "Medium", "High"],
            color_discrete_map={"Low": "green", "Medium": "gold", "High": "red"}
        )
        fig.update_traces(textinfo="percent+label")
        risk_donut = fig.to_html(full_html=False)

        return render_template("results.html", results=results, keywords=keywords,
                               pii_count=pii_count_display, pii_keywords=pii_convert, phi_count=phi_count_display, phi_keywords=phi_convert,
                               finance_hdv_count=finance_hdv_display, fhdv_keywords=fhdv_convert, sq_keywords =sq_convert,
                               security_count=security_display,risk=risk, risk_donut=risk_donut)

    except ValueError as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)
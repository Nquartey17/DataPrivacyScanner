import re
from lists import *

PII_KEYWORDS = ["date of birth","dob", "born", "ssn", "social security", "email", "phone number", "DL", "driver's license",
                "alien", "passport"]
PHI_KEYWORDS = ["history", "social", "family", "treatment", "therapy", "CPT", "diagnosis",
                "DX", "lab", "results", "physician", "doctor", "MRN", "patient"]
FERPA = ["attendance", "class", "grade", "suspension", "disciplinary", "expulsion"]
GDPR = ["religion", "union", "resume"]
ADDITIONAL = ["biometric", "fingerprint", "security questions", "username", "password", "PW", "user"]

def text_scan(text):
    return {
        #re.findall - finds all matches of regular expressions
        #\S - Letters, numbers, symbols, and punctuation
        "ssn": re.findall(r'\b\d{3}-\d{2}-\d{4}\b', text),
        "emails": re.findall(r'\S+@\S+', text),
        "phones": re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
    }

    # count = {key: len(value) for key, value in results.items()}
    #
    # return {"results":results, "count": count}

def keyword_count(text, keyword_list):
    text = text.lower()

    return {
        keyword: text.count(keyword.lower()) for keyword in keyword_list
    }

# combine lists if you want to highlight instances of all words
def keyword_finder(text, keywords):
    lowercase_text = text.lower()
    return [word for word in keywords if word.lower() in lowercase_text]

def keyword_hits(text, keyword_list):
    text = text.lower()
    results = {}

    for category, terms in keyword_list.items():
        findings = []

        for term in terms:
            if term.lower() in text:
                findings.append(term)

        if findings:
            results[category] = findings

    return results

def terms_to_labels(findings_dict):
    return {
        TERMS[key]["label"]: value
        for key,value in findings_dict.items()
    }

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

if __name__ == "__main__":
    sample_text = """
    John Doe was born on 01/15/1990.
    His email is john.doe@example.com and phone number is 123-456-7890.
    SSN: 123-45-6789.
    456-18-8564
    He visited the doctor for diagnosis and treatment.
    """

    # print("PII Scan Results:")
    # print(text_scan(sample_text))

    print("Keywords found:")
    print(keyword_finder(sample_text, PII_KEYWORDS + PHI_KEYWORDS))
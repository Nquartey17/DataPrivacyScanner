import re

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

def terms_to_labels(label_dict, findings_dict):
    return {
        label_dict.get(key, key):value for key,value in findings_dict.items()
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
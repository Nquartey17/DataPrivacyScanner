import re

PII_KEYWORDS = ["date of birth","dob", "born", "ssn", "social security", "email", "phone number"]
PHI_KEYWORDS = ["history", "social", "family", "treatment", "therapy", "CPT", "diagnosis",
                "DX", "lab", "results", "physician", "doctor", "MRN", "patient"]
FERPA = ["attendance", "class", "grade", "suspension", "disciplinary", "expulsion"]
GDPR = ["religion", "union", "resume"]

def pii_scan(text):
    findings = {
        #re.findall - finds all matches of regular expressions
        #\S - Letters, numbers, symbols, and punctuation
        "emails": re.findall(r'\S+@\S+', text),
        "phones": re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text),
        "ssn": re.findall(r'\b\d{3}-\d{2}-\d{4}\b', text),
        "dob": re.findall(r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|'
                          r'\d{4}[/-]\d{1,2}[/-]\d{1,2})\b',
                          text)
    }
    return findings

# combine lists if you want to highlight instances of all words
def keyword_finder(text, keywords):
    lowercase_text = text.lower()
    # result = []
    # for word in keywords:
    #     if word.lower() in lowercase_text:
    #         result.append(word)
    return [word for word in keywords if word.lower() in lowercase_text]

if __name__ == "__main__":
    sample_text = """
    John Doe was born on 01/15/1990.
    His email is john.doe@example.com and phone number is 123-456-7890.
    SSN: 123-45-6789.
    456-18-8564
    He visited the doctor for diagnosis and treatment.
    """

    print("PII Scan Results:")
    print(pii_scan(sample_text))

    print("Keywords found:")
    print(keyword_finder(sample_text, PII_KEYWORDS + PHI_KEYWORDS))
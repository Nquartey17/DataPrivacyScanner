# Labels
DEFAULT_LABELS = {
    "dob":"Date of Birth",
    "ssn":"Social Security",
    "contact":"Email, Address, or Phone Number",
}

PII_LABELS = {
    "dl": "Driver's License",
    "sid": "State ID",
    "a_num": "Alien Registration Number",
    "passport": "Passport",
    "mid": "Military ID"
}

PHI_LABELS = {
    "hx": "Medical History",
    "tx": "Treatment",
    "dx": "Diagnosis",
    "rx": "Prescription / Medication",
    "lab": "Lab Results",
    "phys": "Physician Information",
    "mrn": "Medical Record Number",
    "pid": "Patient ID"
}

FINANCE_HDV_LABELS = {
    "bnk": "Bank Account",
    "routing": "Routing Number",
    "fncl": "Financial Documents",
    "crdt": "Credit Card",
    "hdv": "Insurance Information",
    "mcd": "Medicare / Medicaid / Tricare"
}

SECURITY_LABELS = {
    "user": "Username and Password",
    "sq": "Security Questions",
    "dsig": "Digital Signature"
}

#Related keyword Terms
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

# Keyword risk levels
TERM_RISK_LEVELS = {
    "dob":2,
    "ssn":3,
    "contact": 1,

    "dl":2,
    "sid": 2,
    "a_num": 2,
    "passport": 2,
    "mid": 2,

    "hx": 1,
    "tx": 2,
    "dx": 2,
    "rx": 2,
    "lab": 2,
    "phys": 1,
    "mrn": 2,
    "pid": 2,

    "bnk": 2,
    "routing":1,
    "fncl":2,
    "crdt":2,
    "hdv": 1,
    "mcd": 1,

    "user": 3,
    "sq": 3,
    "dsig": 3
}
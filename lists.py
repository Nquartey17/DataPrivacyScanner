TERMS = {
    # Default
    "dob": {
        "category": "default",
        "label": "Date of Birth",
        "risk": 2,
        "keywords": ["dob","date of birth","birth certificate","born"]
    },

    "ssn": {
        "category": "default",
        "label": "Social Security",
        "risk": 3,
        "keywords": ["ssn","social security"]
    },

    "contact": {
        "category": "default",
        "label": "Email, Address, or Phone Number",
        "risk": 1,
        "keywords": ["address","residence","phone","mobile number","cell number","email"]
    },

    # PII
    "dl": {
        "category": "pii",
        "label": "Driver's License",
        "risk": 2,
        "keywords": ["DL","driver's license","license","learner's permit"]
    },

    "sid": {
        "category": "pii",
        "label": "State ID",
        "risk": 2,
        "keywords": ["state id","identification card","SID"]
    },

    "a_num": {
        "category": "pii",
        "label": "Alien Registration Number",
        "risk": 2,
        "keywords": ["alien registration number","A-number","USCIS"]
    },

    "passport": {
        "category": "pii",
        "label": "Passport",
        "risk": 2,
        "keywords": ["passport","passport number"]
    },

    "mid": {
        "category": "pii",
        "label": "Military ID",
        "risk": 2,
        "keywords": ["dod","military"]
    },

    # PHI
    "hx": {
        "category": "phi",
        "label": "Medical History",
        "risk": 1,
        "keywords": ["history","smoker","smoking","allergy","allergies","medical history","hx"]
    },

    "tx": {
        "category": "phi",
        "label": "Treatment",
        "risk": 2,
        "keywords": ["therapy","tx","treatment","cpt","service code","hcpcs"]
    },

    "dx": {
        "category": "phi",
        "label": "Diagnosis",
        "risk": 2,
        "keywords": ["diagnosis","dx","diagnosed"]
    },

    "rx": {
        "category": "phi",
        "label": "Prescription / Medication",
        "risk": 2,
        "keywords": ["medication","rx"]
    },

    "lab": {
        "category": "phi",
        "label": "Lab Results",
        "risk": 2,
        "keywords": ["lab results","results","lab","chemistry"]
    },

    "phys": {
        "category": "phi",
        "label": "Physician Information",
        "risk": 1,
        "keywords": ["attending","attn","physician"]
    },

    "mrn": {
        "category": "phi",
        "label": "Medical Record Number",
        "risk": 2,
        "keywords": ["mrn","omrn","emrn","medical record number","mr #","mr#"]
    },

    "pid": {
        "category": "phi",
        "label": "Patient ID",
        "risk": 2,
        "keywords": ["pid","patient id","pt id","ptid","patient number"]
    },

    # Finance
    "bnk": {
        "category": "finance",
        "label": "Bank Account",
        "risk": 2,
        "keywords": ["bank account","bank account number","checking","savings"]
    },

    "routing": {
        "category": "finance",
        "label": "Routing Number",
        "risk": 1,
        "keywords": ["routing","RTN","sort code","ABA"]
    },

    "fncl": {
        "category": "finance",
        "label": "Financial Documents",
        "risk": 2,
        "keywords": ["IRA","stock","roth","investment","retirement"]
    },

    "crdt": {
        "category": "finance",
        "label": "Credit Card",
        "risk": 2,
        "keywords": ["credit card","debit card","credit"]
    },

    "hdv": {
        "category": "finance",
        "label": "Insurance Information",
        "risk": 1,
        "keywords": ["insurance","policy number","member id","group number","group id","plan number"]
    },

    "mcd": {
        "category": "finance",
        "label": "Medicare / Medicaid / Tricare",
        "risk": 1,
        "keywords": ["medicare","medicaid","tricare"]
    },

    # Security
    "user": {
        "category": "security",
        "label": "Username and Password",
        "risk": 3,
        "keywords": ["user id","username","password","pwd","user","login","log in"]
    },

    "sq": {
        "category": "security",
        "label": "Security Questions",
        "risk": 3,
        "keywords": ["security question","answer"]
    },

    "dsig": {
        "category": "security",
        "label": "Digital Signature",
        "risk": 3,
        "keywords": ["digital signature","electronically signed"]
    }
}

CATEGORIES = {
    "default": ["dob", "ssn", "contact"],
    "pii": ["dl", "sid", "a_num", "passport", "mid"],
    "phi": ["hx", "tx", "dx", "rx", "lab", "phys", "mrn", "pid"],
    "finance": ["bnk", "routing", "fncl", "crdt", "hdv", "mcd"],
    "security": ["user", "sq", "dsig"],
}
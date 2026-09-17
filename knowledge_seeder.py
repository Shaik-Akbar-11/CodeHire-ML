"""
knowledge_seeder.py
Generates knowledge files for all 115 companies.
Run once: python knowledge_seeder.py
"""
import json
import os
from pathlib import Path

# ======================================================
# COMPANY REGISTRY
# ======================================================

COMPANIES = {

    # ---- IT Services ----
    "TCS":              {"full": "Tata Consultancy Services",  "role": "Assistant System Engineer",   "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Scenario Based",    "calc": False},
    "Infosys":          {"full": "Infosys",                    "role": "Systems Engineer",             "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Scenario Based",    "calc": False},
    "Wipro":            {"full": "Wipro",                      "role": "Project Engineer",             "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Scenario Based",    "calc": False},
    "Cognizant":        {"full": "Cognizant",                  "role": "Programmer Analyst",           "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Practical",         "calc": False},
    "Capgemini":        {"full": "Capgemini",                  "role": "Analyst",                      "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Scenario Based",    "calc": True},
    "Accenture":        {"full": "Accenture",                  "role": "Associate Software Engineer",  "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Practical",         "calc": True},
    "HCL Technologies": {"full": "HCL Technologies",           "role": "Graduate Engineer Trainee",    "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Scenario Based",    "calc": False},
    "Tech Mahindra":    {"full": "Tech Mahindra",              "role": "Software Engineer",            "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Scenario Based",    "calc": False},
    "Mphasis":          {"full": "Mphasis",                    "role": "Software Engineer",            "industry": "IT Services",            "difficulty": "Medium",       "style": "Analytical",        "calc": False},
    "Hexaware":         {"full": "Hexaware Technologies",      "role": "Software Engineer",            "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Scenario Based",    "calc": False},
    "LTIMindtree":      {"full": "LTIMindtree",                "role": "Engineer",                     "industry": "IT Services",            "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Zensar":           {"full": "Zensar Technologies",        "role": "Software Engineer",            "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Scenario Based",    "calc": False},
    "Persistent Systems":{"full":"Persistent Systems",         "role": "Software Engineer",            "industry": "IT Services",            "difficulty": "Medium",       "style": "Analytical",        "calc": False},
    "Cyient":           {"full": "Cyient",                     "role": "Software Engineer",            "industry": "IT Services",            "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Birlasoft":        {"full": "Birlasoft",                  "role": "Software Engineer",            "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Scenario Based",    "calc": False},
    "Sonata Software":  {"full": "Sonata Software",            "role": "Software Engineer",            "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Practical",         "calc": False},
    "Tata Elxsi":       {"full": "Tata Elxsi",                 "role": "Engineer",                     "industry": "IT Services",            "difficulty": "Medium",       "style": "Analytical",        "calc": False},
    "Nisum":            {"full": "Nisum",                      "role": "Software Engineer",            "industry": "IT Services",            "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Xoriant":          {"full": "Xoriant",                    "role": "Software Engineer",            "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Scenario Based",    "calc": False},
    "Mastech Digital":  {"full": "Mastech Digital",            "role": "Software Engineer",            "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Practical",         "calc": False},
    "3i Infotech":      {"full": "3i Infotech",                "role": "Software Engineer",            "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Scenario Based",    "calc": False},
    "Info Edge":        {"full": "Info Edge",                  "role": "Software Engineer",            "industry": "IT Services",            "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "NIIT Technologies":{"full": "NIIT Technologies",          "role": "Software Engineer",            "industry": "IT Services",            "difficulty": "Easy-Medium",  "style": "Practical",         "calc": False},

    # ---- Product ----
    "Amazon":           {"full": "Amazon",                     "role": "Software Development Engineer","industry": "Product",                "difficulty": "Medium-Hard",  "style": "Scenario Based",    "calc": False},
    "Microsoft":        {"full": "Microsoft",                  "role": "Software Engineer",            "industry": "Product",                "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "Google":           {"full": "Google",                     "role": "Software Engineer",            "industry": "Product",                "difficulty": "Hard",         "style": "Analytical",        "calc": False},
    "Meta":             {"full": "Meta",                       "role": "Software Engineer",            "industry": "Product",                "difficulty": "Hard",         "style": "Analytical",        "calc": False},
    "Apple":            {"full": "Apple",                      "role": "Software Engineer",            "industry": "Product",                "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "Adobe":            {"full": "Adobe",                      "role": "Software Engineer",            "industry": "Product",                "difficulty": "Medium-Hard",  "style": "Scenario Based",    "calc": False},
    "Oracle":           {"full": "Oracle",                     "role": "Applications Engineer",        "industry": "Product",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Atlassian":        {"full": "Atlassian",                  "role": "Software Engineer",            "industry": "Product",                "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "Salesforce":       {"full": "Salesforce",                 "role": "Software Engineer",            "industry": "Product",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Qualcomm":         {"full": "Qualcomm",                   "role": "Engineer",                     "industry": "Product",                "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "NVIDIA":           {"full": "NVIDIA",                     "role": "Software Engineer",            "industry": "Product",                "difficulty": "Hard",         "style": "Analytical",        "calc": False},
    "Intel":            {"full": "Intel",                      "role": "Software Engineer",            "industry": "Product",                "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "Intuit":           {"full": "Intuit",                     "role": "Software Engineer",            "industry": "Product",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Cisco":            {"full": "Cisco",                      "role": "Network Engineer",             "industry": "Product",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Samsung RnD":      {"full": "Samsung Research and Development","role":"Software Engineer",         "industry": "Product",                "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "Palo Alto Networks":{"full":"Palo Alto Networks",         "role": "Software Engineer",            "industry": "Product",                "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "ServiceNow":       {"full": "ServiceNow",                 "role": "Software Engineer",            "industry": "Product",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "LinkedIn":         {"full": "LinkedIn",                   "role": "Software Engineer",            "industry": "Product",                "difficulty": "Medium-Hard",  "style": "Scenario Based",    "calc": False},
    "Uber":             {"full": "Uber",                       "role": "Software Engineer",            "industry": "Product",                "difficulty": "Medium-Hard",  "style": "Scenario Based",    "calc": False},
    "Stripe":           {"full": "Stripe",                     "role": "Software Engineer",            "industry": "Product",                "difficulty": "Hard",         "style": "Analytical",        "calc": False},
    "Snowflake":        {"full": "Snowflake",                  "role": "Software Engineer",            "industry": "Product",                "difficulty": "Hard",         "style": "Analytical",        "calc": False},
    "Databricks":       {"full": "Databricks",                 "role": "Software Engineer",            "industry": "Product",                "difficulty": "Hard",         "style": "Analytical",        "calc": False},
    "ThoughtWorks":     {"full": "ThoughtWorks",               "role": "Application Developer",        "industry": "Product",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},

    # ---- Startups ----
    "Flipkart":         {"full": "Flipkart",                   "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium-Hard",  "style": "Scenario Based",    "calc": False},
    "Swiggy":           {"full": "Swiggy",                     "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Zomato":           {"full": "Zomato",                     "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Paytm":            {"full": "Paytm",                      "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "PhonePe":          {"full": "PhonePe",                    "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium-Hard",  "style": "Scenario Based",    "calc": False},
    "Razorpay":         {"full": "Razorpay",                   "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "Groww":            {"full": "Groww",                      "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Meesho":           {"full": "Meesho",                     "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Myntra":           {"full": "Myntra",                     "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Ola":              {"full": "Ola Cabs",                   "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Freshworks":       {"full": "Freshworks",                 "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Analytical",        "calc": False},
    "Zoho":             {"full": "Zoho",                       "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Analytical",        "calc": False},
    "BrowserStack":     {"full": "BrowserStack",               "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "Dream11":          {"full": "Dream11",                    "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium-Hard",  "style": "Scenario Based",    "calc": False},
    "CRED":             {"full": "CRED",                       "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "Zepto":            {"full": "Zepto",                      "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "BYJUS":            {"full": "BYJU'S",                     "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Unacademy":        {"full": "Unacademy",                  "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "MakeMyTrip":       {"full": "MakeMyTrip",                 "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "ShareChat":        {"full": "ShareChat",                  "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "Zerodha":          {"full": "Zerodha",                    "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "Postman":          {"full": "Postman",                    "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "Urban Company":    {"full": "Urban Company",              "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "ClearTax":         {"full": "ClearTax",                   "role": "Software Engineer",            "industry": "Startup",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},

    # ---- Consulting ----
    "Deloitte":         {"full": "Deloitte",                   "role": "Business Technology Analyst",  "industry": "Consulting",             "difficulty": "Medium",       "style": "Case Based",        "calc": True},
    "PwC":              {"full": "PricewaterhouseCoopers",      "role": "Associate",                    "industry": "Consulting",             "difficulty": "Medium",       "style": "Case Based",        "calc": True},
    "KPMG":             {"full": "KPMG",                       "role": "Associate",                    "industry": "Consulting",             "difficulty": "Medium",       "style": "Case Based",        "calc": True},
    "EY":               {"full": "Ernst and Young",            "role": "Associate",                    "industry": "Consulting",             "difficulty": "Medium",       "style": "Case Based",        "calc": True},
    "McKinsey":         {"full": "McKinsey and Company",       "role": "Business Analyst",             "industry": "Consulting",             "difficulty": "Hard",         "style": "Case Based",        "calc": True},
    "BCG":              {"full": "Boston Consulting Group",    "role": "Associate",                    "industry": "Consulting",             "difficulty": "Hard",         "style": "Case Based",        "calc": True},
    "Bain":             {"full": "Bain and Company",           "role": "Associate Consultant",         "industry": "Consulting",             "difficulty": "Hard",         "style": "Case Based",        "calc": True},
    "Oliver Wyman":     {"full": "Oliver Wyman",               "role": "Analyst",                      "industry": "Consulting",             "difficulty": "Hard",         "style": "Case Based",        "calc": True},
    "Genpact":          {"full": "Genpact",                    "role": "Process Associate",            "industry": "Consulting",             "difficulty": "Easy-Medium",  "style": "Practical",         "calc": True},
    "Fractal Analytics":{"full": "Fractal Analytics",          "role": "Analyst",                      "industry": "Consulting",             "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": True},
    "Mu Sigma":         {"full": "Mu Sigma",                   "role": "Trainee Decision Scientist",   "industry": "Consulting",             "difficulty": "Medium",       "style": "Analytical",        "calc": True},
    "Tiger Analytics":  {"full": "Tiger Analytics",            "role": "Analyst",                      "industry": "Consulting",             "difficulty": "Medium",       "style": "Analytical",        "calc": True},
    "LatentView":       {"full": "LatentView Analytics",       "role": "Analyst",                      "industry": "Consulting",             "difficulty": "Medium",       "style": "Analytical",        "calc": True},
    "WNS":              {"full": "WNS Global Services",        "role": "Analyst",                      "industry": "Consulting",             "difficulty": "Easy-Medium",  "style": "Practical",         "calc": True},
    "EXL":              {"full": "EXL Service",                "role": "Analyst",                      "industry": "Consulting",             "difficulty": "Medium",       "style": "Analytical",        "calc": True},

    # ---- BFSI ----
    "JP Morgan":        {"full": "JP Morgan Chase",            "role": "Software Engineer",            "industry": "BFSI",                   "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "Goldman Sachs":    {"full": "Goldman Sachs",              "role": "Analyst",                      "industry": "BFSI",                   "difficulty": "Hard",         "style": "Analytical",        "calc": False},
    "Morgan Stanley":   {"full": "Morgan Stanley",             "role": "Analyst",                      "industry": "BFSI",                   "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "Deutsche Bank":    {"full": "Deutsche Bank",              "role": "Analyst",                      "industry": "BFSI",                   "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "Barclays":         {"full": "Barclays",                   "role": "Analyst",                      "industry": "BFSI",                   "difficulty": "Medium",       "style": "Analytical",        "calc": False},
    "HSBC":             {"full": "HSBC",                       "role": "Analyst",                      "industry": "BFSI",                   "difficulty": "Medium",       "style": "Practical",         "calc": True},
    "Citi":             {"full": "Citibank",                   "role": "Analyst",                      "industry": "BFSI",                   "difficulty": "Medium-Hard",  "style": "Analytical",        "calc": False},
    "Nomura":           {"full": "Nomura",                     "role": "Analyst",                      "industry": "BFSI",                   "difficulty": "Hard",         "style": "Analytical",        "calc": False},
    "American Express": {"full": "American Express",           "role": "Analyst",                      "industry": "BFSI",                   "difficulty": "Medium",       "style": "Scenario Based",    "calc": True},
    "Mastercard":       {"full": "Mastercard",                 "role": "Software Engineer",            "industry": "BFSI",                   "difficulty": "Medium-Hard",  "style": "Scenario Based",    "calc": False},
    "Visa":             {"full": "Visa",                       "role": "Software Engineer",            "industry": "BFSI",                   "difficulty": "Medium-Hard",  "style": "Scenario Based",    "calc": False},
    "ICICI":            {"full": "ICICI Bank",                 "role": "IT Officer",                   "industry": "BFSI",                   "difficulty": "Medium",       "style": "Practical",         "calc": True},
    "HDFC":             {"full": "HDFC Bank",                  "role": "IT Officer",                   "industry": "BFSI",                   "difficulty": "Easy-Medium",  "style": "Practical",         "calc": True},
    "Axis":             {"full": "Axis Bank",                  "role": "IT Officer",                   "industry": "BFSI",                   "difficulty": "Easy-Medium",  "style": "Practical",         "calc": True},
    "SBI":              {"full": "State Bank of India",        "role": "Junior Associate",             "industry": "BFSI",                   "difficulty": "Easy-Medium",  "style": "Practical",         "calc": True},

    # ---- Core Engineering ----
    "Tata Motors":      {"full": "Tata Motors",                "role": "Graduate Engineer Trainee",    "industry": "Core Engineering",       "difficulty": "Medium",       "style": "Technical",         "calc": True},
    "LnT":              {"full": "Larsen and Toubro",          "role": "Graduate Engineer Trainee",    "industry": "Core Engineering",       "difficulty": "Medium",       "style": "Technical",         "calc": True},
    "BHEL":             {"full": "BHEL",                       "role": "Engineer Trainee",             "industry": "Core Engineering",       "difficulty": "Medium",       "style": "Technical",         "calc": True},
    "ONGC":             {"full": "ONGC",                       "role": "Graduate Trainee",             "industry": "Core Engineering",       "difficulty": "Medium",       "style": "Technical",         "calc": True},
    "NTPC":             {"full": "NTPC",                       "role": "Engineer Trainee",             "industry": "Core Engineering",       "difficulty": "Medium",       "style": "Technical",         "calc": True},
    "IOCL":             {"full": "Indian Oil Corporation",     "role": "Engineer Officer",             "industry": "Core Engineering",       "difficulty": "Medium",       "style": "Technical",         "calc": True},
    "GAIL":             {"full": "GAIL India",                 "role": "Executive Trainee",            "industry": "Core Engineering",       "difficulty": "Medium",       "style": "Technical",         "calc": True},
    "BPCL":             {"full": "Bharat Petroleum",           "role": "Engineer",                     "industry": "Core Engineering",       "difficulty": "Medium",       "style": "Technical",         "calc": True},
    "Maruti Suzuki":    {"full": "Maruti Suzuki",              "role": "Graduate Engineer Trainee",    "industry": "Core Engineering",       "difficulty": "Medium",       "style": "Technical",         "calc": True},
    "Mahindra":         {"full": "Mahindra and Mahindra",      "role": "Graduate Engineer Trainee",    "industry": "Core Engineering",       "difficulty": "Medium",       "style": "Technical",         "calc": True},
    "Bosch":            {"full": "Bosch",                      "role": "Associate Engineer",           "industry": "Core Engineering",       "difficulty": "Medium",       "style": "Technical",         "calc": True},
    "Siemens":          {"full": "Siemens",                    "role": "Associate Engineer",           "industry": "Core Engineering",       "difficulty": "Medium",       "style": "Technical",         "calc": True},
    "Honeywell":        {"full": "Honeywell",                  "role": "Engineer",                     "industry": "Core Engineering",       "difficulty": "Medium-Hard",  "style": "Technical",         "calc": True},
    "GE Digital":       {"full": "GE Digital",                 "role": "Software Engineer",            "industry": "Core Engineering",       "difficulty": "Medium-Hard",  "style": "Technical",         "calc": True},
    "Caterpillar":      {"full": "Caterpillar",                "role": "Engineer",                     "industry": "Core Engineering",       "difficulty": "Medium",       "style": "Technical",         "calc": True},
    "Cummins":          {"full": "Cummins",                    "role": "Engineer",                     "industry": "Core Engineering",       "difficulty": "Medium",       "style": "Technical",         "calc": True},
    "Hero MotoCorp":    {"full": "Hero MotoCorp",              "role": "Graduate Engineer Trainee",    "industry": "Core Engineering",       "difficulty": "Easy-Medium",  "style": "Technical",         "calc": True},
    "Bajaj Auto":       {"full": "Bajaj Auto",                 "role": "Graduate Engineer Trainee",    "industry": "Core Engineering",       "difficulty": "Easy-Medium",  "style": "Technical",         "calc": True},

    # ---- Telecom ----
    "Ericsson":         {"full": "Ericsson",                   "role": "Network Engineer",             "industry": "Telecom",                "difficulty": "Medium",       "style": "Technical",         "calc": False},
    "Nokia":            {"full": "Nokia",                      "role": "Software Engineer",            "industry": "Telecom",                "difficulty": "Medium",       "style": "Technical",         "calc": False},
    "Airtel":           {"full": "Bharti Airtel",              "role": "Engineer",                     "industry": "Telecom",                "difficulty": "Easy-Medium",  "style": "Scenario Based",    "calc": False},
    "Jio":              {"full": "Reliance Jio",               "role": "Software Engineer",            "industry": "Telecom",                "difficulty": "Medium",       "style": "Scenario Based",    "calc": False},
    "BSNL":             {"full": "BSNL",                       "role": "Junior Telecom Officer",       "industry": "Telecom",                "difficulty": "Easy-Medium",  "style": "Practical",         "calc": True},

    # ---- FMCG ----
    "HUL":              {"full": "Hindustan Unilever",         "role": "Management Trainee",           "industry": "FMCG",                   "difficulty": "Medium",       "style": "Case Based",        "calc": True},
    "Nestle":           {"full": "Nestle India",               "role": "Management Trainee",           "industry": "FMCG",                   "difficulty": "Medium",       "style": "Case Based",        "calc": True},
    "ITC":              {"full": "ITC Limited",                "role": "Management Trainee",           "industry": "FMCG",                   "difficulty": "Medium",       "style": "Case Based",        "calc": True},
    "PnG":              {"full": "Procter and Gamble",         "role": "Management Trainee",           "industry": "FMCG",                   "difficulty": "Medium-Hard",  "style": "Case Based",        "calc": True},
    "Marico":           {"full": "Marico",                     "role": "Management Trainee",           "industry": "FMCG",                   "difficulty": "Medium",       "style": "Case Based",        "calc": True},
}

# ======================================================
# TOPIC DEFINITIONS BY INDUSTRY
# ======================================================

APTITUDE_TOPICS = {
    "IT Services": [
        ("Percentages",              "Very High", "Easy-Medium", 10),
        ("Profit and Loss",          "Very High", "Easy-Medium", 10),
        ("Ratio and Proportion",     "Very High", "Easy-Medium", 10),
        ("Average",                  "Very High", "Easy",        10),
        ("Time and Work",            "Very High", "Medium",      10),
        ("Time Speed Distance",      "Very High", "Medium",      10),
        ("Simple Interest",          "High",      "Easy",         9),
        ("Compound Interest",        "Medium",    "Medium",       7),
        ("Mixtures and Alligations", "Medium",    "Medium",       7),
        ("Probability",              "Medium",    "Medium",       7),
        ("Permutation and Combination","Low",     "Medium",       5),
        ("Number System",            "High",      "Easy-Medium",  8),
        ("HCF and LCM",              "High",      "Easy",         8),
        ("Simplification",           "Very High", "Easy",        10),
        ("Data Interpretation",      "High",      "Medium",       8),
        ("Ages",                     "Medium",    "Easy",         7),
        ("Pipes and Cisterns",       "Medium",    "Medium",       6),
        ("Boats and Streams",        "Low",       "Medium",       5),
    ],
    "Product": [
        ("Probability",              "Very High", "Medium-Hard", 10),
        ("Data Interpretation",      "Very High", "Medium-Hard", 10),
        ("Percentages",              "High",      "Medium",       9),
        ("Time and Work",            "High",      "Medium-Hard",  9),
        ("Ratio and Proportion",     "High",      "Medium",       8),
        ("Number System",            "High",      "Medium-Hard",  8),
        ("Permutation and Combination","High",    "Hard",         8),
        ("Algebra",                  "Medium",    "Medium-Hard",  7),
        ("Statistics",               "Medium",    "Medium-Hard",  7),
        ("Time Speed Distance",      "Medium",    "Medium",       7),
        ("Profit and Loss",          "Medium",    "Medium",       6),
        ("Compound Interest",        "Medium",    "Medium",       6),
        ("Logarithms",               "Low",       "Hard",         4),
        ("Set Theory",               "Low",       "Medium-Hard",  4),
        ("Geometry",                 "Low",       "Medium",       3),
    ],
    "Startup": [
        ("Data Interpretation",      "Very High", "Medium",      10),
        ("Percentages",              "Very High", "Medium",      10),
        ("Probability",              "High",      "Medium",       9),
        ("Ratio and Proportion",     "High",      "Medium",       9),
        ("Time and Work",            "High",      "Medium",       8),
        ("Profit and Loss",          "High",      "Medium",       8),
        ("Number System",            "Medium",    "Medium",       7),
        ("Average",                  "Medium",    "Easy-Medium",  7),
        ("Permutation and Combination","Medium",  "Medium-Hard",  6),
        ("Algebra",                  "Medium",    "Medium",       6),
        ("Time Speed Distance",      "Medium",    "Medium",       6),
        ("Simple Interest",          "Low",       "Easy-Medium",  5),
        ("Compound Interest",        "Low",       "Medium",       5),
        ("Mixtures and Alligations", "Low",       "Medium",       4),
    ],
    "Consulting": [
        ("Data Interpretation",      "Very High", "Medium-Hard", 10),
        ("Percentages",              "Very High", "Medium",      10),
        ("Ratio and Proportion",     "Very High", "Medium",      10),
        ("Profit and Loss",          "High",      "Medium-Hard",  9),
        ("Average",                  "High",      "Medium",       8),
        ("Probability",              "High",      "Medium-Hard",  8),
        ("Statistics",               "High",      "Medium-Hard",  8),
        ("Time and Work",            "Medium",    "Medium",       7),
        ("Time Speed Distance",      "Medium",    "Medium",       6),
        ("Permutation and Combination","Medium",  "Hard",         6),
        ("Number System",            "Medium",    "Medium",       5),
        ("Algebra",                  "Medium",    "Medium-Hard",  5),
        ("Compound Interest",        "Low",       "Medium",       4),
        ("Mixtures and Alligations", "Low",       "Medium-Hard",  4),
    ],
    "BFSI": [
        ("Data Interpretation",      "Very High", "Medium-Hard", 10),
        ("Percentages",              "Very High", "Medium",      10),
        ("Profit and Loss",          "Very High", "Medium",      10),
        ("Simple Interest",          "Very High", "Medium",      10),
        ("Compound Interest",        "Very High", "Medium-Hard", 10),
        ("Ratio and Proportion",     "High",      "Medium",       8),
        ("Average",                  "High",      "Easy-Medium",  8),
        ("Probability",              "High",      "Medium-Hard",  8),
        ("Time and Work",            "Medium",    "Medium",       7),
        ("Permutation and Combination","Medium",  "Medium-Hard",  6),
        ("Number System",            "Medium",    "Medium",       6),
        ("Statistics",               "High",      "Medium-Hard",  9),
        ("Time Speed Distance",      "Low",       "Medium",       4),
        ("Algebra",                  "Medium",    "Medium",       5),
    ],
    "Core Engineering": [
        ("Percentages",              "Very High", "Medium",      10),
        ("Ratio and Proportion",     "Very High", "Medium",      10),
        ("Data Interpretation",      "High",      "Medium",       8),
        ("Average",                  "High",      "Easy-Medium",  8),
        ("Time and Work",            "High",      "Medium",       8),
        ("Number System",            "High",      "Medium",       8),
        ("Profit and Loss",          "Medium",    "Medium",       7),
        ("Time Speed Distance",      "Medium",    "Medium",       7),
        ("Simple Interest",          "Medium",    "Easy-Medium",  6),
        ("Compound Interest",        "Medium",    "Medium",       6),
        ("Probability",              "Medium",    "Medium",       6),
        ("Permutation and Combination","Low",     "Medium",       5),
        ("HCF and LCM",              "Medium",    "Easy-Medium",  7),
        ("Mixtures and Alligations", "Low",       "Medium",       5),
        ("Pipes and Cisterns",       "Medium",    "Medium",       6),
    ],
    "Telecom": [
        ("Percentages",              "Very High", "Easy-Medium", 10),
        ("Data Interpretation",      "High",      "Medium",       9),
        ("Ratio and Proportion",     "High",      "Easy-Medium",  8),
        ("Time and Work",            "High",      "Medium",       8),
        ("Average",                  "Medium",    "Easy-Medium",  7),
        ("Probability",              "Medium",    "Medium",       7),
        ("Number System",            "Medium",    "Medium",       6),
        ("Profit and Loss",          "Medium",    "Easy-Medium",  6),
        ("Simple Interest",          "Low",       "Easy",         5),
        ("Compound Interest",        "Low",       "Medium",       5),
        ("Time Speed Distance",      "Low",       "Medium",       4),
    ],
    "FMCG": [
        ("Data Interpretation",      "Very High", "Medium",      10),
        ("Percentages",              "Very High", "Medium",      10),
        ("Profit and Loss",          "Very High", "Medium-Hard", 10),
        ("Ratio and Proportion",     "High",      "Medium",       9),
        ("Average",                  "High",      "Medium",       8),
        ("Statistics",               "High",      "Medium-Hard",  8),
        ("Time and Work",            "Medium",    "Medium",       7),
        ("Probability",              "Medium",    "Medium-Hard",  7),
        ("Compound Interest",        "Medium",    "Medium",       6),
        ("Mixtures and Alligations", "Medium",    "Medium-Hard",  6),
        ("Number System",            "Low",       "Medium",       5),
        ("Permutation and Combination","Low",     "Medium-Hard",  4),
    ],
}

LOGICAL_TOPICS = {
    "IT Services": [
        ("Coding Decoding",          "Very High", "Easy",        10),
        ("Blood Relations",          "Very High", "Easy",        10),
        ("Direction Sense",          "Very High", "Easy",        10),
        ("Seating Arrangement",      "High",      "Medium",       9),
        ("Logical Puzzles",          "High",      "Medium",       8),
        ("Statement and Conclusion", "High",      "Medium",       8),
        ("Statement and Assumption", "Medium",    "Medium",       7),
        ("Syllogisms",               "High",      "Medium",       8),
        ("Data Sufficiency",         "Medium",    "Medium",       7),
        ("Input Output",             "Medium",    "Medium",       7),
        ("Pattern Recognition",      "Medium",    "Easy",         6),
        ("Analogy",                  "Medium",    "Easy",         6),
        ("Series Completion",        "High",      "Easy-Medium",  8),
        ("Classification",           "Medium",    "Easy",         6),
    ],
    "Product": [
        ("Logical Puzzles",          "Very High", "Hard",        10),
        ("Seating Arrangement",      "Very High", "Hard",        10),
        ("Data Sufficiency",         "Very High", "Medium-Hard", 10),
        ("Statement and Conclusion", "High",      "Medium-Hard",  9),
        ("Syllogisms",               "High",      "Medium-Hard",  8),
        ("Critical Reasoning",       "High",      "Hard",         8),
        ("Coding Decoding",          "Medium",    "Medium",       7),
        ("Blood Relations",          "Medium",    "Medium",       6),
        ("Input Output",             "High",      "Hard",         8),
        ("Analogy",                  "Medium",    "Medium-Hard",  6),
        ("Venn Diagrams",            "Medium",    "Medium-Hard",  7),
        ("Statement and Assumption", "Medium",    "Hard",         7),
    ],
    "Startup": [
        ("Logical Puzzles",          "Very High", "Medium",      10),
        ("Data Sufficiency",         "High",      "Medium",       9),
        ("Seating Arrangement",      "High",      "Medium",       8),
        ("Syllogisms",               "High",      "Medium",       8),
        ("Coding Decoding",          "Medium",    "Easy-Medium",  7),
        ("Blood Relations",          "Medium",    "Easy-Medium",  6),
        ("Direction Sense",          "Medium",    "Easy-Medium",  6),
        ("Statement and Conclusion", "Medium",    "Medium",       7),
        ("Critical Reasoning",       "Medium",    "Medium-Hard",  7),
        ("Analogy",                  "Low",       "Easy-Medium",  5),
        ("Series Completion",        "Low",       "Easy-Medium",  5),
    ],
    "Consulting": [
        ("Critical Reasoning",       "Very High", "Hard",        10),
        ("Logical Puzzles",          "Very High", "Hard",        10),
        ("Statement and Conclusion", "Very High", "Medium-Hard", 10),
        ("Data Sufficiency",         "High",      "Hard",         9),
        ("Venn Diagrams",            "High",      "Medium-Hard",  8),
        ("Syllogisms",               "High",      "Medium-Hard",  8),
        ("Seating Arrangement",      "Medium",    "Hard",         7),
        ("Blood Relations",          "Medium",    "Medium",       6),
        ("Coding Decoding",          "Low",       "Medium",       4),
        ("Analogy",                  "Medium",    "Medium-Hard",  6),
    ],
    "BFSI": [
        ("Data Sufficiency",         "Very High", "Medium-Hard", 10),
        ("Logical Puzzles",          "Very High", "Medium-Hard", 10),
        ("Seating Arrangement",      "High",      "Medium",       9),
        ("Syllogisms",               "High",      "Medium",       8),
        ("Blood Relations",          "High",      "Easy-Medium",  8),
        ("Coding Decoding",          "Medium",    "Easy-Medium",  7),
        ("Direction Sense",          "Medium",    "Easy",         6),
        ("Statement and Conclusion", "Medium",    "Medium",       7),
        ("Critical Reasoning",       "High",      "Medium-Hard",  8),
        ("Venn Diagrams",            "Medium",    "Medium",       6),
        ("Analogy",                  "Low",       "Easy-Medium",  5),
    ],
    "Core Engineering": [
        ("Coding Decoding",          "Very High", "Easy",        10),
        ("Blood Relations",          "Very High", "Easy",        10),
        ("Direction Sense",          "Very High", "Easy",        10),
        ("Seating Arrangement",      "High",      "Medium",       8),
        ("Logical Puzzles",          "High",      "Medium",       8),
        ("Syllogisms",               "Medium",    "Medium",       7),
        ("Statement and Conclusion", "Medium",    "Medium",       7),
        ("Series Completion",        "High",      "Easy-Medium",  8),
        ("Pattern Recognition",      "Medium",    "Easy-Medium",  6),
        ("Analogy",                  "Medium",    "Easy-Medium",  6),
        ("Data Sufficiency",         "Low",       "Medium",       5),
    ],
    "Telecom": [
        ("Coding Decoding",          "Very High", "Easy",        10),
        ("Blood Relations",          "High",      "Easy",         8),
        ("Direction Sense",          "High",      "Easy",         8),
        ("Syllogisms",               "High",      "Medium",       8),
        ("Logical Puzzles",          "Medium",    "Medium",       7),
        ("Series Completion",        "Medium",    "Easy-Medium",  6),
        ("Seating Arrangement",      "Medium",    "Medium",       6),
        ("Analogy",                  "Low",       "Easy",         5),
        ("Data Sufficiency",         "Low",       "Medium",       5),
    ],
    "FMCG": [
        ("Critical Reasoning",       "Very High", "Medium-Hard", 10),
        ("Logical Puzzles",          "High",      "Medium",       9),
        ("Data Sufficiency",         "High",      "Medium-Hard",  8),
        ("Statement and Conclusion", "High",      "Medium",       8),
        ("Syllogisms",               "Medium",    "Medium",       7),
        ("Seating Arrangement",      "Medium",    "Medium",       7),
        ("Blood Relations",          "Medium",    "Easy-Medium",  6),
        ("Venn Diagrams",            "Medium",    "Medium",       6),
        ("Analogy",                  "Low",       "Easy-Medium",  5),
    ],
}

VERBAL_TOPICS = {
    "IT Services": [
        ("Reading Comprehension",    "Very High", "Medium",      10),
        ("Grammar",                  "Very High", "Easy-Medium", 10),
        ("Vocabulary",               "High",      "Easy-Medium",  9),
        ("Error Spotting",           "Very High", "Easy-Medium", 10),
        ("Sentence Correction",      "High",      "Medium",       8),
        ("Fill in the Blanks",       "High",      "Easy",         8),
        ("Para Jumbles",             "High",      "Medium",       8),
        ("Sentence Completion",      "Medium",    "Easy",         7),
        ("Synonyms and Antonyms",    "High",      "Easy",         8),
        ("Idioms and Phrases",       "Medium",    "Easy-Medium",  6),
    ],
    "Product": [
        ("Reading Comprehension",    "Very High", "Medium-Hard", 10),
        ("Critical Reasoning",       "Very High", "Hard",        10),
        ("Grammar",                  "High",      "Medium",       8),
        ("Vocabulary",               "High",      "Medium-Hard",  8),
        ("Para Jumbles",             "High",      "Medium-Hard",  8),
        ("Error Spotting",           "Medium",    "Medium",       7),
        ("Sentence Correction",      "Medium",    "Medium",       7),
        ("Inference",                "High",      "Hard",         8),
        ("Synonyms and Antonyms",    "Medium",    "Medium",       6),
        ("Fill in the Blanks",       "Low",       "Medium",       5),
    ],
    "Startup": [
        ("Reading Comprehension",    "Very High", "Medium",      10),
        ("Grammar",                  "High",      "Easy-Medium",  8),
        ("Error Spotting",           "High",      "Easy-Medium",  8),
        ("Vocabulary",               "High",      "Medium",       8),
        ("Sentence Correction",      "Medium",    "Medium",       7),
        ("Fill in the Blanks",       "Medium",    "Easy",         7),
        ("Para Jumbles",             "Medium",    "Medium",       6),
        ("Synonyms and Antonyms",    "Medium",    "Easy-Medium",  6),
        ("Inference",                "Medium",    "Medium",       6),
        ("Sentence Completion",      "Low",       "Easy",         5),
    ],
    "Consulting": [
        ("Reading Comprehension",    "Very High", "Hard",        10),
        ("Critical Reasoning",       "Very High", "Hard",        10),
        ("Inference",                "Very High", "Hard",        10),
        ("Vocabulary",               "High",      "Medium-Hard",  8),
        ("Para Jumbles",             "High",      "Medium-Hard",  8),
        ("Grammar",                  "High",      "Medium",       8),
        ("Error Spotting",           "Medium",    "Medium",       6),
        ("Sentence Correction",      "Medium",    "Medium",       6),
        ("Synonyms and Antonyms",    "Medium",    "Medium",       6),
        ("Fill in the Blanks",       "Low",       "Medium",       4),
    ],
    "BFSI": [
        ("Reading Comprehension",    "Very High", "Medium-Hard", 10),
        ("Grammar",                  "Very High", "Medium",      10),
        ("Error Spotting",           "Very High", "Medium",      10),
        ("Vocabulary",               "High",      "Medium",       9),
        ("Sentence Correction",      "High",      "Medium",       8),
        ("Fill in the Blanks",       "High",      "Easy-Medium",  8),
        ("Para Jumbles",             "Medium",    "Medium",       7),
        ("Synonyms and Antonyms",    "Medium",    "Easy-Medium",  6),
        ("Inference",                "Medium",    "Medium-Hard",  7),
        ("Idioms and Phrases",       "Low",       "Medium",       5),
    ],
    "Core Engineering": [
        ("Reading Comprehension",    "Very High", "Medium",      10),
        ("Grammar",                  "Very High", "Easy-Medium", 10),
        ("Vocabulary",               "High",      "Easy-Medium",  8),
        ("Error Spotting",           "High",      "Easy-Medium",  8),
        ("Sentence Correction",      "Medium",    "Medium",       7),
        ("Fill in the Blanks",       "Medium",    "Easy",         7),
        ("Para Jumbles",             "Medium",    "Medium",       6),
        ("Synonyms and Antonyms",    "Medium",    "Easy",         6),
        ("Sentence Completion",      "Low",       "Easy",         5),
        ("Idioms and Phrases",       "Low",       "Easy-Medium",  5),
    ],
    "Telecom": [
        ("Reading Comprehension",    "Very High", "Medium",      10),
        ("Grammar",                  "High",      "Easy-Medium",  8),
        ("Error Spotting",           "High",      "Easy-Medium",  8),
        ("Vocabulary",               "Medium",    "Easy-Medium",  7),
        ("Fill in the Blanks",       "Medium",    "Easy",         7),
        ("Sentence Correction",      "Medium",    "Medium",       6),
        ("Synonyms and Antonyms",    "Low",       "Easy",         5),
        ("Para Jumbles",             "Low",       "Medium",       5),
    ],
    "FMCG": [
        ("Reading Comprehension",    "Very High", "Medium",      10),
        ("Critical Reasoning",       "Very High", "Medium-Hard", 10),
        ("Vocabulary",               "High",      "Medium",       8),
        ("Grammar",                  "High",      "Medium",       8),
        ("Para Jumbles",             "High",      "Medium",       8),
        ("Inference",                "Medium",    "Medium-Hard",  7),
        ("Error Spotting",           "Medium",    "Medium",       6),
        ("Sentence Correction",      "Medium",    "Medium",       6),
        ("Fill in the Blanks",       "Low",       "Easy-Medium",  5),
        ("Synonyms and Antonyms",    "Low",       "Easy-Medium",  4),
    ],
}


# ======================================================
# DIFFICULTY PATTERNS BY INDUSTRY
# ======================================================

DIFFICULTY_PATTERNS = {
    "Easy-Medium": {
        "question_style_default": "Scenario Based",
        "difficulty": {
            "Easy":        {"steps": 1, "time_minutes": 1,   "reasoning": "Basic",              "complexity": "Low"},
            "Easy-Medium": {"steps": 2, "time_minutes": 2,   "reasoning": "Basic-Intermediate", "complexity": "Low-Medium"},
            "Medium":      {"steps": 3, "time_minutes": 2.5, "reasoning": "Intermediate",       "complexity": "Medium"},
            "Medium-Hard": {"steps": 4, "time_minutes": 3,   "reasoning": "Advanced",           "complexity": "Medium-High"},
            "Hard":        {"steps": 5, "time_minutes": 5,   "reasoning": "Expert",             "complexity": "High"},
        }
    },
    "Medium": {
        "question_style_default": "Scenario Based",
        "difficulty": {
            "Easy":        {"steps": 2, "time_minutes": 1.5, "reasoning": "Basic",              "complexity": "Low"},
            "Easy-Medium": {"steps": 2, "time_minutes": 2,   "reasoning": "Basic-Intermediate", "complexity": "Low-Medium"},
            "Medium":      {"steps": 3, "time_minutes": 3,   "reasoning": "Intermediate",       "complexity": "Medium"},
            "Medium-Hard": {"steps": 4, "time_minutes": 4,   "reasoning": "Advanced",           "complexity": "Medium-High"},
            "Hard":        {"steps": 5, "time_minutes": 5,   "reasoning": "Expert",             "complexity": "High"},
        }
    },
    "Medium-Hard": {
        "question_style_default": "Analytical",
        "difficulty": {
            "Easy":        {"steps": 2, "time_minutes": 2,   "reasoning": "Basic",              "complexity": "Low"},
            "Easy-Medium": {"steps": 3, "time_minutes": 2,   "reasoning": "Basic-Intermediate", "complexity": "Medium"},
            "Medium":      {"steps": 3, "time_minutes": 3,   "reasoning": "Intermediate",       "complexity": "Medium"},
            "Medium-Hard": {"steps": 4, "time_minutes": 4,   "reasoning": "Advanced",           "complexity": "Medium-High"},
            "Hard":        {"steps": 5, "time_minutes": 6,   "reasoning": "Expert",             "complexity": "High"},
        }
    },
    "Hard": {
        "question_style_default": "Analytical",
        "difficulty": {
            "Easy":        {"steps": 2, "time_minutes": 2,   "reasoning": "Basic",              "complexity": "Low"},
            "Easy-Medium": {"steps": 3, "time_minutes": 3,   "reasoning": "Basic-Intermediate", "complexity": "Medium"},
            "Medium":      {"steps": 4, "time_minutes": 3,   "reasoning": "Intermediate",       "complexity": "Medium"},
            "Medium-Hard": {"steps": 5, "time_minutes": 4,   "reasoning": "Advanced",           "complexity": "Medium-High"},
            "Hard":        {"steps": 6, "time_minutes": 6,   "reasoning": "Expert",             "complexity": "High"},
        }
    },
    "Very High": {
        "question_style_default": "Analytical",
        "difficulty": {
            "Easy":        {"steps": 2, "time_minutes": 2,   "reasoning": "Basic",              "complexity": "Low"},
            "Easy-Medium": {"steps": 3, "time_minutes": 3,   "reasoning": "Basic-Intermediate", "complexity": "Medium"},
            "Medium":      {"steps": 4, "time_minutes": 4,   "reasoning": "Intermediate",       "complexity": "Medium"},
            "Medium-Hard": {"steps": 5, "time_minutes": 5,   "reasoning": "Advanced",           "complexity": "High"},
            "Hard":        {"steps": 6, "time_minutes": 6,   "reasoning": "Expert",             "complexity": "Very High"},
        }
    },
}


# ======================================================
# SEEDER
# ======================================================

def topics_to_csv_content(topics):
    lines = ["topic,priority,difficulty,weight"]
    for (topic, priority, difficulty, weight) in topics:
        lines.append(f"{topic},{priority},{difficulty},{weight}")
    return "\n".join(lines)


def write_file(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] {path}")


def seed_company(folder_key, meta):
    base = Path("knowledge") / folder_key
    base.mkdir(parents=True, exist_ok=True)

    industry    = meta["industry"]
    full_name   = meta["full"]
    role        = meta["role"]
    difficulty  = meta["difficulty"]
    style       = meta["style"]
    calc        = meta["calc"]

    print(f"\n>> Seeding: {folder_key} ({industry})")

    # ---- company_profile.json ----
    profile = {
        "company":              full_name,
        "short_name":           folder_key,
        "role":                 role,
        "industry":             industry,
        "overall_difficulty":   difficulty,
        "question_style":       style,
        "calculator_allowed":   calc,
        "version":              "1.0"
    }
    write_file(base / "company_profile.json", json.dumps(profile, indent=2))

    # ---- pattern.json ----
    diff_key = difficulty if difficulty in DIFFICULTY_PATTERNS else "Medium"
    diff_template = DIFFICULTY_PATTERNS[diff_key]

    generation_rules = [
        "Generate an original question.",
        "Never copy questions from any source.",
        f"Question must match the requested topic.",
        f"Question must match the requested difficulty.",
        f"Question should resemble a real {full_name} Online Assessment.",
        "Use realistic numerical values.",
        "Avoid ambiguous wording.",
        "Avoid grammatical errors.",
        "Generate exactly four options.",
        "Only one option must be correct.",
        "Distractors should be realistic.",
        "Explanation must justify the correct answer.",
        f"Difficulty level must reflect {difficulty} company standards.",
    ]

    pattern = {
        "company":             folder_key,
        "version":             "1.0",
        "question_style":      style,
        "language":            "Professional English",
        "real_world_context":  True,
        "multi_step_reasoning": True,
        "calculator_allowed":  calc,
        "difficulty":          diff_template["difficulty"],
        "generation_rules":    generation_rules,
        "validation_rules": [
            "Mathematics must be correct.",
            "Answer must match explanation.",
            "Options must be unique.",
            "Question must not be duplicated.",
            "Difficulty should match requested level.",
            "Topic should match requested topic.",
            "Grammar must be correct."
        ]
    }
    write_file(base / "pattern.json", json.dumps(pattern, indent=2))

    # ---- topic CSVs ----
    apt_topics  = APTITUDE_TOPICS.get(industry, APTITUDE_TOPICS["IT Services"])
    log_topics  = LOGICAL_TOPICS.get(industry,  LOGICAL_TOPICS["IT Services"])
    ver_topics  = VERBAL_TOPICS.get(industry,   VERBAL_TOPICS["IT Services"])

    write_file(base / "aptitude_topics.csv", topics_to_csv_content(apt_topics))
    write_file(base / "logical_topics.csv",  topics_to_csv_content(log_topics))
    write_file(base / "verbal_topics.csv",   topics_to_csv_content(ver_topics))

    # ---- company_pattern.csv ----
    pattern_rows = ["Section,Topic,Difficulty,Priority"]
    for (t, p, d, _) in apt_topics[:5]:
        pattern_rows.append(f"Quantitative Aptitude,{t},{d},{p}")
    for (t, p, d, _) in log_topics[:5]:
        pattern_rows.append(f"Logical Reasoning,{t},{d},{p}")
    for (t, p, d, _) in ver_topics[:5]:
        pattern_rows.append(f"Verbal Ability,{t},{d},{p}")
    write_file(base / "company_pattern.csv", "\n".join(pattern_rows))

    return folder_key


def main():
    print("=" * 60)
    print("KNOWLEDGE SEEDER")
    print(f"Seeding {len(COMPANIES)} companies...")
    print("=" * 60)

    seeded = []
    for folder_key, meta in COMPANIES.items():
        try:
            seed_company(folder_key, meta)
            seeded.append(folder_key)
        except Exception as e:
            print(f"  [FAIL] {folder_key}: {e}")

    print("\n" + "=" * 60)
    print(f"Done. {len(seeded)}/{len(COMPANIES)} companies seeded.")
    print("=" * 60)


if __name__ == "__main__":
    main()

import requests
import pandas as pd
import joblib

from bs4 import BeautifulSoup

# =========================
# LOAD MODEL
# =========================

model, feature_names = joblib.load(
    "con.pkl"
)

# =========================
# CONTENT FEATURE EXTRACTION
# =========================

def extract_content_features(url):

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=5
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        html = response.text.lower()

        data = {}

        # =========================
        # CONTENT FEATURES
        # =========================

        data["forms"] = len(
            soup.find_all("form")
        )

        data["iframes"] = len(
            soup.find_all("iframe")
        )

        data["scripts"] = len(
            soup.find_all("script")
        )

        data["external_links"] = len([
            a for a in soup.find_all("a", href=True)
            if "http" in a["href"]
        ])

        data["password_fields"] = len(
            soup.find_all("input", {"type": "password"})
        )

        # =========================
        # NLP FEATURES
        # =========================

        suspicious_words = [
            "login",
            "verify",
            "account",
            "bank",
            "secure",
            "signin",
            "password",
            "paypal",
            "update"
        ]

        suspicious_count = 0

        for word in suspicious_words:

            if word in html:
                suspicious_count += 1

        data["suspicious_words"] = suspicious_count

        return pd.DataFrame([data])

    except:

        return None

# =========================
# RULE-BASED DETECTION
# =========================

def rule_based_detection(url):

    score = 0

    suspicious_keywords = [
        "login",
        "verify",
        "secure",
        "update",
        "signin",
        "bank",
        "paypal",
        "account"
    ]

    url_lower = url.lower()

    for word in suspicious_keywords:

        if word in url_lower:
            score += 1

    if any(char.isdigit() for char in url):
        score += 1

    if "-" in url:
        score += 1

    if len(url) > 30:
        score += 1

    return score

# =========================
# INPUT
# =========================

url = input("Enter URL: ")

if not url.startswith("http"):
    url = "http://" + url

print("\nScanning Website...")

# =========================
# RULE SCORE
# =========================

rule_score = rule_based_detection(url)

# =========================
# CONTENT FEATURES
# =========================

features = extract_content_features(url)

# =========================
# INVALID DOMAIN
# =========================

if features is None:

    print("\nWebsite unreachable or invalid !!!!")

    if rule_score >= 2:
        print("Suspicious URL Pattern !!!!")

    exit()

# =========================
# FILL MISSING COLUMNS
# =========================

for col in feature_names:

    if col not in features:
        features[col] = 0

features = features[feature_names]

# =========================
# ML PREDICTION
# =========================

prediction = model.predict(features)[0]

probability = model.predict_proba(
    features
).max() * 100

# =========================
# FINAL SCORE
# =========================

final_score = probability

if rule_score >= 2:
    final_score += 15

if final_score > 100:
    final_score = 100

# =========================
# FINAL RESULT
# =========================

print("\n========================")
print("PHISHING SCAN RESULT")
print("========================")

print("Risk Score:", round(final_score, 2), "%")

if prediction == 1 or final_score >= 60:

    print("PHISHING WEBSITE !!!!")

else:

    print("SAFE WEBSITE")
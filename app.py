from flask import Flask, render_template, request
import joblib
import pandas as pd
import requests
import math
from urllib.parse import urlparse
from bs4 import BeautifulSoup

app = Flask(__name__)

# =========================
# LOAD MODEL
# =========================

model, feature_names = joblib.load("url.pkl")

# =========================
# ENTROPY FUNCTION
# =========================

def calculate_entropy(text):

    if len(text) == 0:
        return 0

    prob = [
        float(text.count(c)) / len(text)
        for c in dict.fromkeys(list(text))
    ]

    entropy = -sum(
        [p * math.log(p) / math.log(2.0) for p in prob]
    )

    return entropy

# =========================
# LIVE CHECK
# =========================

def is_live(url):

    try:

        if not url.startswith("http"):
            url = "http://" + url

        requests.get(url, timeout=3)

        return True

    except:

        return False

# =========================
# FEATURE EXTRACTION
# =========================

def extract_features(url):

    if not url.startswith("http"):
        url = "http://" + url

    parsed = urlparse(url)

    domain = parsed.netloc
    path = parsed.path

    data = {}

    special_chars = "!@#$%^&*()_+=[]{}|;:,.<>?/"

    # ================= URL FEATURES =================

    data['url_length'] = len(url)
    data['number_of_dots_in_url'] = url.count('.')
    data['having_repeated_digits_in_url'] = 1 if any(url.count(d) > 1 for d in "0123456789") else 0
    data['number_of_digits_in_url'] = sum(c.isdigit() for c in url)
    data['number_of_special_char_in_url'] = sum(c in special_chars for c in url)
    data['number_of_hyphens_in_url'] = url.count('-')
    data['number_of_underline_in_url'] = url.count('_')
    data['number_of_slash_in_url'] = url.count('/')
    data['number_of_questionmark_in_url'] = url.count('?')
    data['number_of_equal_in_url'] = url.count('=')
    data['number_of_at_in_url'] = url.count('@')
    data['number_of_dollar_in_url'] = url.count('$')
    data['number_of_exclamation_in_url'] = url.count('!')
    data['number_of_hashtag_in_url'] = url.count('#')
    data['number_of_percent_in_url'] = url.count('%')

    # ================= DOMAIN =================

    data['domain_length'] = len(domain)
    data['number_of_dots_in_domain'] = domain.count('.')
    data['number_of_hyphens_in_domain'] = domain.count('-')
    data['having_special_characters_in_domain'] = 1 if any(c in special_chars for c in domain) else 0
    data['number_of_special_characters_in_domain'] = sum(c in special_chars for c in domain)
    data['having_digits_in_domain'] = 1 if any(c.isdigit() for c in domain) else 0
    data['number_of_digits_in_domain'] = sum(c.isdigit() for c in domain)

    # ================= SUBDOMAIN =================

    subdomains = domain.split('.')[:-2]

    data['number_of_subdomains'] = len(subdomains)

    sub_text = ''.join(subdomains)

    data['having_dot_in_subdomain'] = 1 if '.' in sub_text else 0
    data['having_hyphen_in_subdomain'] = 1 if '-' in sub_text else 0

    if len(subdomains) > 0:
        data['average_subdomain_length'] = sum(len(s) for s in subdomains) / len(subdomains)
    else:
        data['average_subdomain_length'] = 0

    data['average_number_of_dots_in_subdomain'] = sub_text.count('.')
    data['average_number_of_hyphens_in_subdomain'] = sub_text.count('-')

    data['having_special_characters_in_subdomain'] = 1 if any(c in special_chars for c in sub_text) else 0
    data['number_of_special_characters_in_subdomain'] = sum(c in special_chars for c in sub_text)
    data['having_digits_in_subdomain'] = 1 if any(c.isdigit() for c in sub_text) else 0
    data['number_of_digits_in_subdomain'] = sum(c.isdigit() for c in sub_text)

    # ================= PATH =================

    data['having_path'] = 1 if path else 0
    data['path_length'] = len(path)

    # ================= QUERY =================

    data['having_query'] = 1 if parsed.query else 0
    data['having_fragment'] = 1 if parsed.fragment else 0
    data['having_anchor'] = 1 if "#" in url else 0

    # ================= ENTROPY =================

    data['entropy_of_url'] = calculate_entropy(url)
    data['entropy_of_domain'] = calculate_entropy(domain)

    df = pd.DataFrame([data])

    # align columns
    for col in feature_names:
        if col not in df:
            df[col] = 0

    df = df[feature_names]

    return df

# =========================
# HOME ROUTE
# =========================

@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    confidence = None

    if request.method == "POST":

        url = request.form["url"]

        # LIVE CHECK
        live = is_live(url)

        if not live:

            result = "⚠️ Website Not Reachable / Suspicious Domain"
            confidence = "0"

            return render_template(
                "index.html",
                result=result,
                confidence=confidence
            )

        # FEATURES
        features = extract_features(url)

        # PREDICT
        prediction = model.predict(features)[0]

        probability = round(
            model.predict_proba(features).max() * 100,
            2
        )

        # RESULT
        if prediction == 1:
            result = "⚠️ Phishing Website"
        else:
            result = "✅ Safe Website"

        confidence = probability

    return render_template(
        "index.html",
        result=result,
        confidence=confidence
    )

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)
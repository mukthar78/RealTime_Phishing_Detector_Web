import joblib
import pandas as pd
import math
from urllib.parse import urlparse

# Load model
model, feature_names = joblib.load("url.pkl")

# =========================
# ENTROPY FUNCTION
# =========================
def calculate_entropy(text):

    prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]

    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])

    return entropy

# =========================
# FEATURE EXTRACTION
# =========================
def extract_features(url):

    # Add scheme if missing
    if not url.startswith("http"):
        url = "http://" + url

    parsed = urlparse(url)

    domain = parsed.netloc
    path = parsed.path

    data = {}

    # URL FEATURES
    data['url_length'] = len(url)
    data['number_of_dots_in_url'] = url.count('.')
    data['having_repeated_digits_in_url'] = 1 if any(url.count(digit) > 1 for digit in '0123456789') else 0
    data['number_of_digits_in_url'] = sum(c.isdigit() for c in url)

    special_chars = "!@#$%^&*()_+=[]{}|;:,.<>?/"

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

    # DOMAIN FEATURES
    data['domain_length'] = len(domain)
    data['number_of_dots_in_domain'] = domain.count('.')
    data['number_of_hyphens_in_domain'] = domain.count('-')

    data['having_special_characters_in_domain'] = 1 if any(c in special_chars for c in domain) else 0

    data['number_of_special_characters_in_domain'] = sum(c in special_chars for c in domain)

    data['having_digits_in_domain'] = 1 if any(c.isdigit() for c in domain) else 0

    data['number_of_digits_in_domain'] = sum(c.isdigit() for c in domain)

    data['having_repeated_digits_in_domain'] = 1 if any(domain.count(digit) > 1 for digit in '0123456789') else 0

    # SUBDOMAIN FEATURES
    subdomains = domain.split('.')[:-2]

    data['number_of_subdomains'] = len(subdomains)

    subdomain_text = ''.join(subdomains)

    data['having_dot_in_subdomain'] = 1 if '.' in subdomain_text else 0
    data['having_hyphen_in_subdomain'] = 1 if '-' in subdomain_text else 0

    if len(subdomains) > 0:
        data['average_subdomain_length'] = sum(len(s) for s in subdomains) / len(subdomains)
    else:
        data['average_subdomain_length'] = 0

    data['average_number_of_dots_in_subdomain'] = subdomain_text.count('.')

    data['average_number_of_hyphens_in_subdomain'] = subdomain_text.count('-')

    data['having_special_characters_in_subdomain'] = 1 if any(c in special_chars for c in subdomain_text) else 0

    data['number_of_special_characters_in_subdomain'] = sum(c in special_chars for c in subdomain_text)

    data['having_digits_in_subdomain'] = 1 if any(c.isdigit() for c in subdomain_text) else 0

    data['number_of_digits_in_subdomain'] = sum(c.isdigit() for c in subdomain_text)

    data['having_repeated_digits_in_subdomain'] = 1 if any(subdomain_text.count(digit) > 1 for digit in '0123456789') else 0

    # PATH FEATURES
    data['having_path'] = 1 if path else 0
    data['path_length'] = len(path)

    # QUERY / FRAGMENT
    data['having_query'] = 1 if parsed.query else 0
    data['having_fragment'] = 1 if parsed.fragment else 0
    data['having_anchor'] = 1 if '#' in url else 0

    # ENTROPY
    data['entropy_of_url'] = calculate_entropy(url)
    data['entropy_of_domain'] = calculate_entropy(domain)

    # Create dataframe
    df = pd.DataFrame([data])

    # Correct order
    df = df[feature_names]

    return df

# =========================
# INPUT
# =========================
url = input("Enter URL: ")

# Extract features
features = extract_features(url)

# Predict
prediction = model.predict(features)[0]

# Probability
probability = model.predict_proba(features).max() * 100

# Result
print("\n========================")

if prediction == 1:
    print("⚠️ Phishing Website")
else:
    print("✅ Safe Website")

print("Confidence:", round(probability, 2), "%")
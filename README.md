# 🛡️ HPD - Hybrid Phishing Detection System

A Machine Learning based phishing detection system that identifies malicious websites using URL Analysis, Website Content Analysis, and Rule-Based Detection.

## 🚀 Features

- URL-Based Phishing Detection
- Content-Based Phishing Detection
- Real-Time Website Scanning
- Machine Learning Classification
- Rule-Based Threat Detection
- Risk Score Generation
- Flask Web Application
- Live Website Availability Check
- Confidence Score Prediction
- Future Support for QR Code Phishing Detection

---

## 🏗️ Project Architecture

User URL
↓
Feature Extraction
↓
Machine Learning Models
↓
Rule-Based Analysis
↓
Risk Score Calculation
↓
Final Verdict

---

## 📂 Project Structure

```text
HPD/
│
├── app.py                 # Flask Web Application
├── urlmodel.py            # URL Model Training
├── urltest.py             # URL Prediction
├── conmodel.py            # Content Model Training
├── contest.py             # Content Prediction
├── url.pkl                # Trained URL Model
├── con.pkl                # Trained Content Model
├── train_url.csv          # URL Dataset
├── train_con.csv          # Content Dataset
│
├── templates/
│   └── index.html
│
└── README.md
```

---

## 🔍 URL Features Used

- URL Length
- Domain Length
- Number of Dots
- Number of Digits
- Number of Special Characters
- Hyphens
- Subdomains
- Query Parameters
- Path Length
- Entropy Score
- Fragment Detection
- Anchor Detection

Total Features: **41+**

---

## 🌐 Content Features Used

- Number of Forms
- Number of Iframes
- Number of Scripts
- External Links
- Password Fields
- Suspicious Keywords Detection
- HTML Structure Analysis

---

## 🤖 Machine Learning

### URL Detection Model

- Random Forest Classifier
- Accuracy: **96.21%**

### Content Detection Model

- Random Forest Classifier
- Accuracy: **95%+**

---

## 🛠️ Technologies Used

- Python
- Flask
- Pandas
- Scikit-Learn
- Joblib
- BeautifulSoup
- Requests
- HTML
- CSS

---

## 📸 Web Interface

The system provides a modern web dashboard where users can:

- Enter a URL
- Scan websites in real time
- View phishing prediction
- View confidence score
- Detect suspicious websites instantly

---

## 🔮 Future Enhancements

- QR Code Phishing Detection
- Email Phishing Detection
- Screenshot-Based Detection
- Browser Extension
- Deep Learning Integration
- Threat Intelligence Integration
- SIEM Integration (Splunk/Wazuh)

---

## 🎯 Use Cases

- Cybersecurity Awareness
- Phishing Detection
- Security Research
- Educational Projects
- SOC Analyst Training
- VAPT Demonstrations

---

## 👨‍💻 Author

**Mohammed Mukthar A**

Cybersecurity Student | SOC Analyst Aspirant | VAPT Enthusiast

---

## 📜 License

This project is developed for educational and research purposes.

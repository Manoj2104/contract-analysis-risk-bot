
 📑 Contract Analysis & Risk Assessment Bot for SMEs

**Career Carnival Hackathon 2026 – Data Science**



 🚀 Project Overview

Small and Medium Enterprises (SMEs) frequently enter into legal contracts such as employment agreements, vendor contracts, lease agreements, partnership deeds, and service contracts without fully understanding complex legal language, hidden risks, or unfavorable clauses.

This project is a **GenAIpowered Contract Analysis & Risk Assessment Bot** that helps SME owners:

* Understand contracts in **plain business language**
* Identify **legal and financial risks**
* Get **actionable renegotiation suggestions**
* Make informed decisions **before signing contracts**

The solution is designed to be **SMEfriendly**, **confidential**, and **fully compliant with hackathon rules**.



 🎯 Problem Statement

Legal contracts are difficult for nonlegal professionals to interpret. This often results in:

* Acceptance of onesided clauses
* Exposure to unlimited liability
* Longterm lockins and penalties
* Dependency on costly legal consultations

The objective of this project is to **democratize contract understanding** using AI, while maintaining transparency, explainability, and simplicity.



 🧠 Key Features

* 📄 Upload contracts in **PDF, DOCX, or TXT**
* 🖼 OCR support for **scanned/imagebased PDFs**
* 🌐 Multilingual support (**English & Hindi**)
* 🔍 Automatic **contract type classification**
* 🧩 Clause & subclause extraction
* 🏷 Named Entity Recognition:

  * Parties
  * Dates
  * Financial amounts
  * Jurisdiction
* ⚖️ Obligation vs Right vs Prohibition identification
* 🚨 **Clauselevel risk scoring** (Low / Medium / High)
* ❗ Detection of:

  * Penalty clauses
  * Indemnity clauses
  * Unilateral termination clauses
  * Arbitration & jurisdiction clauses
  * Autorenewal & lockin periods
  * Noncompete & IP transfer clauses
* 🧠 PlainEnglish clause explanations
* 🔄 SMEfriendly alternative clause suggestions
* 📊 Overall contract risk score
* 📑 Downloadable **PDF risk assessment report**
* 🔐 Confidential processing with local audit logs
* 🧪 Extensive automated test coverage



 ⚙️ System Workflow

1. User uploads a contract (PDF / DOCX / TXT)
2. Text extraction is performed

   * OCR is applied if the document is scanned
3. Language detection (English / Hindi)
4. Hindi contracts are internally normalized to English
5. NLP pipeline performs:

   * Contract classification
   * Clause extraction
   * Entity recognition
   * Obligation and risk detection
6. LLM generates explanations and safer alternatives
7. Risk scores and summaries are aggregated
8. Final report is generated and exported as PDF



 🛠️ Technology Stack

| Layer   | Technology                        |
|  |  |
| UI      | Streamlit                         |
| OCR     | Tesseract OCR                     |
| NLP     | spaCy, NLTK                       |
| ML      | Scikitlearn                      |
| LLM     | GPT4 / Claude 3 (reasoning only) |
| Storage | Local JSON audit logs             |
| Export  | PDF report generation             |
| Testing | PyTest                            |

⚠️ **No external legal databases, statutes, or APIs are used**, in compliance with hackathon rules.



 📂 Project Structure (Detailed)

```
contractriskbot/
├── README.md
├── requirements.txt
├── run.bat
├── AI_Contract_Risk_Report.pdf
├── .gitignore
├── .pytest_cache/
│
├── app/
│   ├── app.py
│   ├── styles/
│   │   └── theme.css
│   ├── modules/
│   │   ├── ambiguity_detector.py
│   │   ├── clause_explainer.py
│   │   ├── clause_extractor.py
│   │   ├── clause_rewriter.py
│   │   ├── clause_risk.py
│   │   ├── contract_classifier.py
│   │   ├── contract_entity_normalizer.py
│   │   ├── contract_intelligence.py
│   │   ├── contract_risk_aggregator.py
│   │   ├── decision_engine.py
│   │   ├── executive_summary.py
│   │   ├── hindi_normalizer.py
│   │   ├── indian_law_checker.py
│   │   ├── language_detector.py
│   │   ├── missing_clause_detector.py
│   │   ├── missing_clause_severity.py
│   │   ├── name_redactor.py
│   │   ├── ner.py
│   │   ├── obligation_detector.py
│   │   ├── obligation_tagger.py
│   │   ├── pdf_report.py
│   │   ├── penalty_detector.py
│   │   ├── plain_english.py
│   │   ├── risk_rules.py
│   │   ├── risk_tags.py
│   │   ├── simple_explainer.py
│   │   ├── unilateral_detector.py
│   │   └── utils.py
│
├── assets/
│   ├── demo/
│   └── screenshots/
│
├── data/
│   ├── samples/
│   └── outputs/
│
├── logs/
│
├── tests/
│   ├── test_ambiguity_detector.py
│   ├── test_clause_risk_assessment.py
│   ├── test_clauses.py
│   ├── test_contract_classifier.py
│   ├── test_contract_risk_aggregator.py
│   ├── test_decision_engine.py
│   ├── test_missing_clause_detector.py
│   ├── test_ner.py
│   ├── test_obligation_tagger.py
│   ├── test_ocr.py
│   └── test_risk_rules.py
```



 🔧 OCR SETUP – TESSERACT (WINDOWS)

 1️⃣ Download Tesseract OCR

Download from:
[https://github.com/UBMannheim/tesseract/wiki](https://github.com/UBMannheim/tesseract/wiki)

Recommended installer: **tesseractocrw64setup.exe**



 2️⃣ Install Location

```
C:\Program Files\TesseractOCR\
```

Ensure the file exists:

```
C:\Program Files\TesseractOCR\tesseract.exe
```



 3️⃣ Add Tesseract to PATH

1. Open **Environment Variables**
2. Under **System Variables → Path → Edit**
3. Add:

```
C:\Program Files\TesseractOCR\
```

4. Restart system



 4️⃣ Verify Installation

```bash
tesseract version
```



 5️⃣ Install OCR Python Dependencies

```bash
pip install pytesseract pillow pdf2image
```



 6️⃣ Configure Tesseract Path in Code

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\TesseractOCR\tesseract.exe"
```



 7️⃣ Install Poppler (For PDF OCR)

Download from:
[https://github.com/oschwartz10612/popplerwindows/releases](https://github.com/oschwartz10612/popplerwindows/releases)

Add Poppler `bin` folder to PATH, example:

```
C:\poppler\Library\bin
```

Verify:

```bash
pdfinfo v
```



 📦 requirements.txt (Sample)

```
streamlit
pytesseract
pdf2image
pillow
PyPDF2
pythondocx
spacy
nltk
scikitlearn
reportlab
langdetect
pytest
```



 ▶️ How to Run the Application

```bash
git clone https://github.com/Manoj2104/contractriskbot.git
cd contractriskbot
pip install r requirements.txt
streamlit run app/app.py
```



 🌐 Live Demo

**Live Application URL:**
(https://contract-analysis-risk-bot-s.streamlit.app/)



 🎥 Demo Video

**Demo Video Link:**
(https://drive.google.com/file/d/1s8fPuFEKkj2JeBNKtCWtPMaQIQhEyo3J/view?usp=sharing)



 👨‍💻 Author

**Manoj S**
Career Carnival Hackathon 2026 – Data Science



 🏁 Conclusion

This project showcases how **GenAI, OCR, and NLP** can be combined to solve realworld legal understanding challenges faced by SMEs. By transforming complex legal contracts into **clear, actionable insights**, the system empowers users to reduce risk and make smarter business decisions.


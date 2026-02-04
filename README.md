# 📊 InsightStream

[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io/)  
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://www.python.org/)  

**InsightStream** is an AI-powered data analytics platform built with **Streamlit**, **Pandas**, and **Plotly**.  
It enables users to upload CSV datasets, ask natural language questions, and instantly generate:

- 📈 Interactive visualizations (charts, trends, comparisons)  
- 📊 Summary tables  
- 💡 Automated business insights  

The app includes **prompt-injection protection** and an **offline fallback mode** when AI is unavailable.

---

## 🌟 Features

1. **AI-Powered Analytics**
   - Ask natural language questions about your dataset.
   - Generates Python code automatically and executes it safely.
   - Provides actionable business insights.

2. **Rich Visualizations**
   - Line charts, scatter plots, bar charts, and heatmaps with **Plotly**.
   - Monthly trends, correlations, comparisons, and distributions.

3. **Offline Mode**
   - Works even if AI service is unavailable or quota exceeded.
   - Provides correlation heatmaps and simple trend charts.

4. **Prompt-Injection Protection**
   - Queries are sanitized to prevent unsafe code execution.
   - Blocks access to system files, environment variables, or shell commands.

5. **Mobile-Friendly**
   - Responsive layout adapts to mobile devices.
   - Charts are scrollable and touch-friendly.

---

## ⚡ Demo

👉 [Insert link to your deployed Streamlit app here]

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/himanshu-jadhav108/insightstream.git
cd insightstream

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 🔑 Configuration

Add your **Gemini API key**:

```python
# In app.py:
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
```

Or in **Streamlit Cloud Secrets**:

```
GEMINI_API_KEY = "your_api_key_here"
```

Optional settings in `app.py`:

- `AI_MODE`: `"ONLINE"` or `"OFFLINE"`
- `GEMINI_MODEL`: `"models/gemini-2.5-flash-lite"` (default)

---

## 🧩 Usage Examples

| Question                            | Output                             |
| ----------------------------------- | ---------------------------------- |
| Show monthly sales trend            | Line chart with sales over time    |
| Compare sales and marketing spend   | Multi-line chart comparing columns |
| Correlation between numeric columns | Correlation heatmap                |

---

## 📦 Requirements

- Python 3.10+  
- Streamlit  
- Pandas  
- Plotly  
- Google Generative AI SDK (`google-generativeai`)

Example `requirements.txt`:

```
streamlit
pandas
plotly
google-generativeai
```

---

## 🔒 Security

- Queries are sanitized to prevent **prompt injection**.  
- AI code execution is sandboxed.  
- No sensitive data or environment variables are exposed.  

---

## 📡 Deployment

Deploy easily on:

- **Streamlit Community Cloud** (free)  
- Any cloud service supporting Python/Streamlit  

Steps:

1. Push the repo to GitHub.  
2. Go to [Streamlit Cloud](https://share.streamlit.io/), connect your repo.  
3. Specify `app.py` as the entry point.  
4. Add API key in **Secrets**.  
5. Deploy and share the link.  

---

## 👨‍💻 About the Maintainer

**Himanshu Jadhav**  
Second-Year Engineering Student (AI & Data Science)

### Connect with me:

[![GitHub](https://img.shields.io/badge/GitHub-himanshu--jadhav108-black?style=flat-square&logo=github)](https://github.com/himanshu-jadhav108)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-himanshu--jadhav-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/himanshu-jadhav-328082339?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
[![Instagram](https://img.shields.io/badge/Instagram-himanshu__jadhav__108-purple?style=flat-square&logo=instagram)](https://www.instagram.com/himanshu_jadhav_108?igsh=MWYxamppcTBlY3Rl)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit%20Now-yellow?style=flat-square)](https://himanshu-jadhav-portfolio.vercel.app/)

---
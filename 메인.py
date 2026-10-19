
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #F4F7FB;
    --surface: #FFFFFF;
    --blue: #E5EDF8;
    --blue-strong: #6687B4;
    --mint: #DDECE8;
    --text: #293B52;
    --muted: #718096;
    --border: #E1E7EF;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

html, body, [class*="css"] {
    font-family: 'Pretendard', sans-serif;
}

.block-container {
    max-width: 1120px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: var(--text);
    letter-spacing: -0.035em;
}

h1 {
    font-weight: 800;
}

h2, h3 {
    font-weight: 650;
}

[data-testid="stSidebar"] {
    background: #EDF2F8;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] h1 {
    font-size: 1.35rem;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    border-radius: 10px;
}

.hero {
    background: linear-gradient(120deg, #E5EDF8 0%, #EAF1F7 65%, #DDECE8 100%);
    border: 1px solid #DEE7F0;
    border-radius: 22px;
    padding: 34px;
    margin-bottom: 28px;
}

.hero h1 {
    color: #293F5B;
    font-size: 2.1rem;
    margin-bottom: 12px;
}

.hero p {
    color: #586D84;
    font-size: 1rem;
    line-height: 1.8;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface);
    border-color: var(--border) !important;
    border-radius: 17px;
}

div.stButton > button,
div.stLinkButton > a {
    border-radius: 11px;
    font-weight: 600;
    transition: all 0.2s ease;
}

div.stButton > button {
    border: 1px solid #D7E1EE;
    background: #F1F5FA;
    color: #344D6B;
}

div.stButton > button:hover {
    border-color: #9DB4D2;
    background: #E5EDF8;
    color: #263D59;
}

div.stLinkButton > a {
    border: 1px solid #D7E1EE;
    background: #FFFFFF;
    color: #405B7C;
}

div.stLinkButton > a:hover {
    background: #EAF1F8;
    border-color: #A8BCD4;
}

[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 13px;
    overflow: hidden;
}

[data-testid="stTextInput"] input {
    border-radius: 11px;
    border-color: #D8E1EB;
    background: #FFFFFF;
}

[data-testid="stProgressBar"] > div > div {
    background: #7798B8;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 15px;
}

hr {
    border-color: #E1E7EF;
}

.small-note {
    color: var(--muted);
    font-size: 0.9rem;
}

@media (max-width: 640px) {
    .block-container {
        padding: 1.2rem 1rem 2rem;
    }

    .hero {
        padding: 23px;
        border-radius: 17px;
    }

    .hero h1 {
        font-size: 1.65rem;
    }
}
</style>
""", unsafe_allow_html=True)

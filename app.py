import streamlit as st
import urllib.request
import urllib.parse
import json
import re
from datetime import datetime
import xml.etree.ElementTree as ET

st.set_page_config(
    page_title="SentimentEdge — Indian Stock Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Indian Stocks ─────────────────────────────────────────────────────────────
INDIAN_STOCKS = {
    "Reliance Industries": "RELIANCE.NS","TCS": "TCS.NS","HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS","ICICI Bank": "ICICIBANK.NS","Hindustan Unilever": "HINDUNILVR.NS",
    "ITC": "ITC.NS","State Bank of India": "SBIN.NS","Bharti Airtel": "BHARTIARTL.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS","Bajaj Finance": "BAJFINANCE.NS",
    "HCL Technologies": "HCLTECH.NS","Asian Paints": "ASIANPAINT.NS","Axis Bank": "AXISBANK.NS",
    "Larsen & Toubro": "LT.NS","Sun Pharmaceutical": "SUNPHARMA.NS",
    "UltraTech Cement": "ULTRACEMCO.NS","Maruti Suzuki": "MARUTI.NS","Titan Company": "TITAN.NS",
    "Wipro": "WIPRO.NS","Nestle India": "NESTLEIND.NS","Power Grid": "POWERGRID.NS",
    "NTPC": "NTPC.NS","Tech Mahindra": "TECHM.NS","Bajaj Finserv": "BAJAJFINSV.NS",
    "JSW Steel": "JSWSTEEL.NS","Tata Steel": "TATASTEEL.NS","ONGC": "ONGC.NS",
    "Coal India": "COALINDIA.NS","Adani Enterprises": "ADANIENT.NS","Adani Ports": "ADANIPORTS.NS",
    "Adani Green Energy": "ADANIGREEN.NS","Tata Motors": "TATAMOTORS.NS",
    "Mahindra & Mahindra": "M&M.NS","Hero MotoCorp": "HEROMOTOCO.NS","Bajaj Auto": "BAJAJ-AUTO.NS",
    "Eicher Motors": "EICHERMOT.NS","IndusInd Bank": "INDUSINDBK.NS","Cipla": "CIPLA.NS",
    "Dr. Reddy's Laboratories": "DRREDDY.NS","Divi's Laboratories": "DIVISLAB.NS",
    "Apollo Hospitals": "APOLLOHOSP.NS","Grasim Industries": "GRASIM.NS",
    "Havells India": "HAVELLS.NS","Pidilite Industries": "PIDILITIND.NS",
    "Muthoot Finance": "MUTHOOTFIN.NS","Torrent Pharmaceuticals": "TORNTPHARM.NS",
    "Bharat Electronics": "BEL.NS","HAL": "HAL.NS","DLF": "DLF.NS",
    "BHEL": "BHEL.NS","SAIL": "SAIL.NS","GAIL": "GAIL.NS","Indian Oil": "IOC.NS",
    "BPCL": "BPCL.NS","Bank of Baroda": "BANKBARODA.NS","Punjab National Bank": "PNB.NS",
    "Canara Bank": "CANBK.NS","Zomato": "ZOMATO.NS","Paytm": "PAYTM.NS","Nykaa": "NYKAA.NS",
    "Delhivery": "DELHIVERY.NS","Info Edge (Naukri)": "NAUKRI.NS","IRCTC": "IRCTC.NS",
    "IRFC": "IRFC.NS","REC Limited": "RECLTD.NS","PFC": "PFC.NS",
    "HDFC Life Insurance": "HDFCLIFE.NS","SBI Life Insurance": "SBILIFE.NS",
    "SBI Cards": "SBICARD.NS","Cholamandalam Investment": "CHOLAFIN.NS",
    "AU Small Finance Bank": "AUBANK.NS","IDFC First Bank": "IDFCFIRSTB.NS",
    "Federal Bank": "FEDERALBNK.NS","Bandhan Bank": "BANDHANBNK.NS","Yes Bank": "YESBANK.NS",
    "Biocon": "BIOCON.NS","Lupin": "LUPIN.NS","Glenmark Pharmaceuticals": "GLENMARK.NS",
    "UPL": "UPL.NS","PI Industries": "PIIND.NS","Tata Chemicals": "TATACHEM.NS",
    "Tata Power": "TATAPOWER.NS","Adani Power": "ADANIPOWER.NS","IndiGo": "INDIGO.NS",
    "Vedanta": "VEDL.NS","Hindalco": "HINDALCO.NS","Hindustan Zinc": "HINDZINC.NS",
    "Jindal Steel & Power": "JINDALSTEL.NS","Tata Consumer Products": "TATACONSUM.NS",
    "Varun Beverages": "VBL.NS","Jubilant FoodWorks": "JUBLFOOD.NS",
    "Page Industries": "PAGEIND.NS","LTIMindtree": "LTIM.NS",
    "Mankind Pharma": "MANKIND.NS","Dixon Technologies": "DIXON.NS",
    "Polycab India": "POLYCAB.NS","Siemens India": "SIEMENS.NS","ABB India": "ABB.NS",
    "Ashok Leyland": "ASHOKLEY.NS","TVS Motor": "TVSMOTOR.NS","Bharti Forge": "BHARATFORG.NS",
    "Dabur India": "DABUR.NS","Marico": "MARICO.NS","Colgate-Palmolive India": "COLPAL.NS",
    "Godrej Properties": "GODREJPROP.NS","Oberoi Realty": "OBEROIRLTY.NS",
    "Shriram Finance": "SHRIRAMFIN.NS","L&T Finance": "L&TFH.NS",
    "National Aluminium": "NATIONALUM.NS","Deepak Nitrite": "DEEPAKNTR.NS",
    "SRF": "SRF.NS","Aarti Industries": "AARTIIND.NS","Raymond": "RAYMOND.NS",
    "Container Corporation": "CONCOR.NS","RBL Bank": "RBLBANK.NS",
}

# sentiment words
POSITIVE_WORDS = {"growth","profit","surge","rally","strong","gain","rise","bullish","buy","positive","boost"}
NEGATIVE_WORDS = {"loss","decline","fall","drop","weak","bearish","risk","crash","fraud","investigation"}

def simple_sentiment(text):
    words = re.findall(r'\b\w+\b', text.lower())
    pos = sum(1 for w in words if w in POSITIVE_WORDS)
    neg = sum(1 for w in words if w in NEGATIVE_WORDS)
    total = pos + neg
    if total == 0:
        return 0.0, "neutral"
    score = (pos - neg) / total
    return score, "positive" if score > 0 else "negative"

def fetch_yahoo(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    try:
        data = json.loads(urllib.request.urlopen(url).read())
        price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        return price
    except:
        return None

def fetch_news(company):
    query = urllib.parse.quote(company)
    url = f"https://news.google.com/rss/search?q={query}"
    articles = []
    try:
        raw = urllib.request.urlopen(url).read()
        root = ET.fromstring(raw)
        for item in root.findall(".//item")[:5]:
            title = item.findtext("title")
            score, label = simple_sentiment(title)
            articles.append((title, label))
    except:
        pass
    return articles

def main():
    st.title("📊 AI Stock Sentiment Analyzer")

    col1, col2 = st.columns([4,1])

    with col1:
        user_input = st.text_input("Search company")
        chosen = st.selectbox("Or select", list(INDIAN_STOCKS.keys()))

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        go = st.button("Analyse")

    if not go:
        return

    selected_company = None

    if user_input:
        for name in INDIAN_STOCKS:
            if user_input.lower() in name.lower():
                selected_company = name
                break

    if not selected_company:
        selected_company = chosen

    ticker = INDIAN_STOCKS[selected_company]

    st.subheader(selected_company)

    price = fetch_yahoo(ticker)
    if price:
        st.success(f"Current Price: ₹{price}")

    news = fetch_news(selected_company)
    st.write("### News Sentiment")
    for n in news:
        st.write(f"{n[0]} → {n[1]}")

if __name__ == "__main__":
    main()

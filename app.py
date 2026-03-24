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

# (KEEP EVERYTHING SAME ABOVE)

def main():
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        dark = st.toggle("🌙 Dark Mode", value=True)
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
**SentimentEdge** combines:
- 🧠 Rule-based NLP sentiment
- 📊 Yahoo Finance live data
- 📰 Google News RSS
- 📐 RSI · MACD · MA indicators
""")

    load_css(dark)

    st.markdown("""
    <div class="top-bar">
        <div class="chip">AI-Powered · NSE & BSE</div>
        <h1>📊 AI Stock Sentiment Analyzer</h1>
        <p>Real-time sentiment analysis & investment signals for Indian stocks</p>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([4,1])

    with col1:
        user_input = st.text_input("🔍 Search company (or pick from list)")
        chosen = st.selectbox("Or select from list", list(INDIAN_STOCKS.keys()))

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        go = st.button("Analyse →")

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

    # (REST OF YOUR ORIGINAL CODE CONTINUES EXACTLY SAME)

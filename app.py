import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import feedparser
import urllib.parse
import warnings
warnings.filterwarnings('ignore')

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SentimentEdge — Indian Stock Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Indian Stocks Database (NSE + BSE) ───────────────────────────────────────
INDIAN_STOCKS = {
    # NIFTY 50
    "Reliance Industries": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "ITC": "ITC.NS",
    "State Bank of India": "SBIN.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "LTIMindtree": "LTIM.NS",
    "HCL Technologies": "HCLTECH.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Axis Bank": "AXISBANK.NS",
    "Larsen & Toubro": "LT.NS",
    "Sun Pharmaceutical": "SUNPHARMA.NS",
    "UltraTech Cement": "ULTRACEMCO.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Titan Company": "TITAN.NS",
    "Wipro": "WIPRO.NS",
    "Nestle India": "NESTLEIND.NS",
    "Power Grid": "POWERGRID.NS",
    "NTPC": "NTPC.NS",
    "Tech Mahindra": "TECHM.NS",
    "Bajaj Finserv": "BAJAJFINSV.NS",
    "JSW Steel": "JSWSTEEL.NS",
    "Tata Steel": "TATASTEEL.NS",
    "ONGC": "ONGC.NS",
    "Coal India": "COALINDIA.NS",
    "Adani Enterprises": "ADANIENT.NS",
    "Adani Ports": "ADANIPORTS.NS",
    "Adani Green Energy": "ADANIGREEN.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Tata Consultancy Services": "TCS.NS",
    "Mahindra & Mahindra": "M&M.NS",
    "Hero MotoCorp": "HEROMOTOCO.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "Eicher Motors": "EICHERMOT.NS",
    "IndusInd Bank": "INDUSINDBK.NS",
    "Cipla": "CIPLA.NS",
    "Dr. Reddy's Laboratories": "DRREDDY.NS",
    "Divi's Laboratories": "DIVISLAB.NS",
    "Apollo Hospitals": "APOLLOHOSP.NS",
    "Grasim Industries": "GRASIM.NS",
    "Shree Cement": "SHREECEM.NS",
    "Havells India": "HAVELLS.NS",
    "Pidilite Industries": "PIDILITIND.NS",
    "Muthoot Finance": "MUTHOOTFIN.NS",
    "Torrent Pharmaceuticals": "TORNTPHARM.NS",
    # NIFTY Next 50
    "Bharat Electronics": "BEL.NS",
    "HAL": "HAL.NS",
    "DLF": "DLF.NS",
    "Godrej Consumer Products": "GODREJCP.NS",
    "Vodafone Idea": "IDEA.NS",
    "BHEL": "BHEL.NS",
    "SAIL": "SAIL.NS",
    "GAIL": "GAIL.NS",
    "Indian Oil": "IOC.NS",
    "BPCL": "BPCL.NS",
    "Hindustan Petroleum": "HINDPETRO.NS",
    "Bank of Baroda": "BANKBARODA.NS",
    "Punjab National Bank": "PNB.NS",
    "Canara Bank": "CANBK.NS",
    "Union Bank": "UNIONBANK.NS",
    "Bosch": "BOSCHLTD.NS",
    "Siemens India": "SIEMENS.NS",
    "ABB India": "ABB.NS",
    "Cummins India": "CUMMINSIND.NS",
    "Ashok Leyland": "ASHOKLEY.NS",
    "TVS Motor": "TVSMOTOR.NS",
    "Motherson Sumi": "MOTHERSON.NS",
    "Bharat Forge": "BHARATFORG.NS",
    "Exide Industries": "EXIDEIND.NS",
    "Amara Raja Batteries": "AMARAJABAT.NS",
    "Dabur India": "DABUR.NS",
    "Marico": "MARICO.NS",
    "Colgate-Palmolive India": "COLPAL.NS",
    "Emami": "EMAMILTD.NS",
    "Godrej Properties": "GODREJPROP.NS",
    "Oberoi Realty": "OBEROIRLTY.NS",
    "Prestige Estates": "PRESTIGE.NS",
    "Crompton Greaves": "CROMPTON.NS",
    "Voltas": "VOLTAS.NS",
    "Blue Star": "BLUESTARCO.NS",
    "Whirlpool India": "WHIRLPOOL.NS",
    "Dixon Technologies": "DIXON.NS",
    "Amber Enterprises": "AMBER.NS",
    "Polycab India": "POLYCAB.NS",
    "KEI Industries": "KEI.NS",
    "Tata Power": "TATAPOWER.NS",
    "Adani Power": "ADANIPOWER.NS",
    "JSW Energy": "JSWENERGY.NS",
    "Torrent Power": "TORNTPOWER.NS",
    "CESC": "CESC.NS",
    "Interglobe Aviation (IndiGo)": "INDIGO.NS",
    "SpiceJet": "SPICEJET.NS",
    "Container Corporation": "CONCOR.NS",
    "Gateway Distriparks": "GDL.NS",
    "Zomato": "ZOMATO.NS",
    "Paytm (One97 Communications)": "PAYTM.NS",
    "Nykaa (FSN E-Commerce)": "NYKAA.NS",
    "PB Fintech (Policybazaar)": "POLICYBZR.NS",
    "Delhivery": "DELHIVERY.NS",
    "Nazara Technologies": "NAZARA.NS",
    "Info Edge (Naukri)": "NAUKRI.NS",
    "Just Dial": "JUSTDIAL.NS",
    "Indiamart Intermesh": "INDIAMART.NS",
    "CarTrade Tech": "CARTRADE.NS",
    "Easy Trip Planners (EaseMyTrip)": "EASEMYTRIP.NS",
    "Irctc": "IRCTC.NS",
    "RITES": "RITES.NS",
    "IRFC": "IRFC.NS",
    "REC Limited": "RECLTD.NS",
    "PFC": "PFC.NS",
    "HUDCO": "HUDCO.NS",
    "LIC Housing Finance": "LICHSGFIN.NS",
    "HDFC Life Insurance": "HDFCLIFE.NS",
    "SBI Life Insurance": "SBILIFE.NS",
    "ICICI Prudential Life": "ICICIPRULI.NS",
    "Max Financial Services": "MFSL.NS",
    "General Insurance": "GICRE.NS",
    "New India Assurance": "NIACL.NS",
    "Star Health Insurance": "STARHEALTH.NS",
    "SBI Cards": "SBICARD.NS",
    "Cholamandalam Investment": "CHOLAFIN.NS",
    "Mahindra Finance": "M&MFIN.NS",
    "Shriram Finance": "SHRIRAMFIN.NS",
    "Sundaram Finance": "SUNDARMFIN.NS",
    "L&T Finance Holdings": "L&TFH.NS",
    "Aavas Financiers": "AAVAS.NS",
    "Home First Finance": "HOMEFIRST.NS",
    "Five Star Business Finance": "FIVESTAR.NS",
    "Ujjivan Small Finance Bank": "UJJIVANSFB.NS",
    "AU Small Finance Bank": "AUBANK.NS",
    "Equitas Small Finance Bank": "EQUITASBNK.NS",
    "IDFC First Bank": "IDFCFIRSTB.NS",
    "Federal Bank": "FEDERALBNK.NS",
    "Karnataka Bank": "KTKBANK.NS",
    "South Indian Bank": "SOUTHBANK.NS",
    "City Union Bank": "CUB.NS",
    "Karur Vysya Bank": "KARURVYSYA.NS",
    "Bandhan Bank": "BANDHANBNK.NS",
    "RBL Bank": "RBLBANK.NS",
    "Yes Bank": "YESBANK.NS",
    "Biocon": "BIOCON.NS",
    "Lupin": "LUPIN.NS",
    "Alkem Laboratories": "ALKEM.NS",
    "Ipca Laboratories": "IPCALAB.NS",
    "Natco Pharma": "NATCOPHARM.NS",
    "Glenmark Pharmaceuticals": "GLENMARK.NS",
    "Mankind Pharma": "MANKIND.NS",
    "Granules India": "GRANULES.NS",
    "Suven Pharmaceuticals": "SUVEN.NS",
    "Astrazeneca India": "ASTRAZEN.NS",
    "Pfizer India": "PFIZER.NS",
    "Abbott India": "ABBOTINDIA.NS",
    "Sanofi India": "SANOFI.NS",
    "Tata Chemicals": "TATACHEM.NS",
    "UPL": "UPL.NS",
    "PI Industries": "PIIND.NS",
    "Coromandel International": "COROMANDEL.NS",
    "Chambal Fertilizers": "CHAMBLFERT.NS",
    "Gujarat Fluorochemicals": "FLUOROCHEM.NS",
    "SRF": "SRF.NS",
    "Navin Fluorine": "NAVINFLUOR.NS",
    "Deepak Nitrite": "DEEPAKNTR.NS",
    "Aarti Industries": "AARTIIND.NS",
    "Vinati Organics": "VINATIORGA.NS",
    "Galaxy Surfactants": "GALAXYSURF.NS",
    "Tata Consumer Products": "TATACONSUM.NS",
    "Varun Beverages": "VBL.NS",
    "United Spirits": "MCDOWELL-N.NS",
    "United Breweries": "UBL.NS",
    "Jubilant FoodWorks": "JUBLFOOD.NS",
    "Devyani International": "DEVYANI.NS",
    "Sapphire Foods": "SAPPHIRE.NS",
    "Restaurant Brands Asia": "RBA.NS",
    "Westlife Foodworld": "WESTLIFE.NS",
    "Trident": "TRIDENT.NS",
    "Welspun India": "WELSPUNIND.NS",
    "Raymond": "RAYMOND.NS",
    "Arvind": "ARVIND.NS",
    "Page Industries": "PAGEIND.NS",
    "Lux Industries": "LUXIND.NS",
    "Vedanta": "VEDL.NS",
    "Hindalco": "HINDALCO.NS",
    "National Aluminium": "NATIONALUM.NS",
    "Hindustan Zinc": "HINDZINC.NS",
    "Sterlite Technologies": "STLTECH.NS",
    "Jindal Steel & Power": "JINDALSTEL.NS",
    "Jindal Stainless": "JSL.NS",
    "APL Apollo Tubes": "APLAPOLLO.NS",
    "Ratnamani Metals": "RATNAMANI.NS",
    "Man Infraconstruction": "MANINFRA.NS",
}

# ─── Custom CSS ───────────────────────────────────────────────────────────────
def load_css(dark_mode):
    if dark_mode:
        bg_primary = "#0A0E1A"
        bg_secondary = "#111827"
        bg_card = "#1A2332"
        text_primary = "#F0F4FF"
        text_secondary = "#94A3B8"
        accent = "#00D4FF"
        accent2 = "#7C3AED"
        border = "#1E2D45"
        positive = "#10B981"
        negative = "#EF4444"
        warning = "#F59E0B"
    else:
        bg_primary = "#F8FAFF"
        bg_secondary = "#EEF2FF"
        bg_card = "#FFFFFF"
        text_primary = "#0F172A"
        text_secondary = "#475569"
        accent = "#0066CC"
        accent2 = "#7C3AED"
        border = "#E2E8F0"
        positive = "#059669"
        negative = "#DC2626"
        warning = "#D97706"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Space Grotesk', sans-serif;
    }}

    .stApp {{
        background-color: {bg_primary};
        color: {text_primary};
    }}

    /* Header */
    .main-header {{
        background: linear-gradient(135deg, {bg_secondary} 0%, {bg_card} 100%);
        border: 1px solid {border};
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }}
    .main-header::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, {accent}, {accent2});
    }}
    .main-header h1 {{
        font-size: 2.2rem;
        font-weight: 700;
        color: {text_primary};
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }}
    .main-header p {{
        color: {text_secondary};
        margin: 0;
        font-size: 0.95rem;
    }}
    .badge {{
        display: inline-block;
        background: linear-gradient(135deg, {accent}22, {accent2}22);
        border: 1px solid {accent}44;
        color: {accent};
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 10px;
    }}

    /* Metric cards */
    .metric-card {{
        background: {bg_card};
        border: 1px solid {border};
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px {accent}22;
    }}
    .metric-label {{
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: {text_secondary};
        margin-bottom: 8px;
    }}
    .metric-value {{
        font-size: 1.6rem;
        font-weight: 700;
        color: {text_primary};
        font-family: 'JetBrains Mono', monospace;
    }}
    .metric-delta {{
        font-size: 0.8rem;
        margin-top: 4px;
        font-family: 'JetBrains Mono', monospace;
    }}
    .positive {{ color: {positive}; }}
    .negative {{ color: {negative}; }}
    .neutral {{ color: {warning}; }}

    /* Section headers */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 28px 0 16px 0;
        padding-bottom: 10px;
        border-bottom: 1px solid {border};
    }}
    .section-header h3 {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {text_primary};
        margin: 0;
    }}
    .section-dot {{
        width: 8px; height: 8px;
        border-radius: 50%;
        background: linear-gradient(135deg, {accent}, {accent2});
    }}

    /* Sentiment gauge */
    .sentiment-container {{
        background: {bg_card};
        border: 1px solid {border};
        border-radius: 16px;
        padding: 28px;
        text-align: center;
    }}
    .verdict-box {{
        background: linear-gradient(135deg, {bg_secondary}, {bg_card});
        border: 1px solid {border};
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin-top: 16px;
    }}
    .verdict-text {{
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }}

    /* News cards */
    .news-card {{
        background: {bg_card};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 10px;
        transition: border-color 0.2s;
    }}
    .news-card:hover {{
        border-color: {accent}66;
    }}
    .news-title {{
        font-size: 0.9rem;
        font-weight: 600;
        color: {text_primary};
        margin-bottom: 6px;
        line-height: 1.4;
    }}
    .news-meta {{
        font-size: 0.75rem;
        color: {text_secondary};
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
    }}
    .sentiment-pill {{
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
    }}
    .pill-positive {{ background: {positive}22; color: {positive}; border: 1px solid {positive}44; }}
    .pill-negative {{ background: {negative}22; color: {negative}; border: 1px solid {negative}44; }}
    .pill-neutral {{ background: {warning}22; color: {warning}; border: 1px solid {warning}44; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: {bg_secondary};
        border-right: 1px solid {border};
    }}

    /* Streamlit overrides */
    .stSelectbox > div > div {{
        background: {bg_card};
        border-color: {border};
        color: {text_primary};
    }}
    div[data-testid="stMetric"] {{
        background: {bg_card};
        border: 1px solid {border};
        border-radius: 12px;
        padding: 16px;
    }}
    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, {accent}, {accent2});
    }}
    div.stButton > button {{
        background: linear-gradient(135deg, {accent}, {accent2});
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 24px;
        font-family: 'Space Grotesk', sans-serif;
    }}
    div.stButton > button:hover {{
        opacity: 0.9;
        transform: translateY(-1px);
    }}
    </style>
    """, unsafe_allow_html=True)

# ─── Data Fetching Functions ───────────────────────────────────────────────────

@st.cache_data(ttl=300)
def get_stock_data(ticker, period="6mo"):
    """Fetch stock data from Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        info = stock.info
        return hist, info
    except Exception as e:
        return None, {}

def get_news_sentiment(company_name, ticker):
    """Fetch news from Google News RSS and analyze sentiment."""
    analyzer = SentimentIntensityAnalyzer()
    news_items = []
    queries = [
        f"{company_name} stock",
        f"{company_name} NSE BSE",
        f"{ticker.replace('.NS','').replace('.BO','')} share price"
    ]
    for query in queries[:2]:
        encoded = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={encoded}+when:7d&hl=en-IN&gl=IN&ceid=IN:en"
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:8]:
                title = entry.get('title', '')
                summary = entry.get('summary', '')
                text = f"{title} {summary}"
                text_clean = re.sub('<[^<]+?>', '', text)
                # VADER sentiment
                vader_score = analyzer.polarity_scores(text_clean)
                # TextBlob sentiment
                blob = TextBlob(text_clean)
                compound = vader_score['compound']
                if compound >= 0.05:
                    sentiment = "positive"
                elif compound <= -0.05:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
                published = entry.get('published', 'Recent')
                source = entry.get('source', {}).get('title', 'News Source') if hasattr(entry.get('source', ''), 'get') else 'Google News'
                news_items.append({
                    'title': title[:120] + '...' if len(title) > 120 else title,
                    'summary': text_clean[:200] + '...' if len(text_clean) > 200 else text_clean,
                    'sentiment': sentiment,
                    'score': round(compound, 3),
                    'subjectivity': round(blob.sentiment.subjectivity, 3),
                    'published': published,
                    'source': source,
                    'url': entry.get('link', '#')
                })
        except:
            continue
    # Deduplicate
    seen = set()
    unique_news = []
    for item in news_items:
        if item['title'] not in seen:
            seen.add(item['title'])
            unique_news.append(item)
    return unique_news[:15]

def calculate_overall_sentiment(news_items):
    """Calculate weighted overall sentiment score."""
    if not news_items:
        return 0, "neutral", 0, 0, 0
    scores = [item['score'] for item in news_items]
    avg_score = np.mean(scores)
    positive = sum(1 for s in scores if s >= 0.05)
    negative = sum(1 for s in scores if s <= -0.05)
    neutral = len(scores) - positive - negative
    if avg_score >= 0.15:
        sentiment = "positive"
    elif avg_score <= -0.15:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return round(avg_score, 3), sentiment, positive, negative, neutral

def get_technical_indicators(hist):
    """Calculate basic technical indicators."""
    if hist is None or len(hist) < 20:
        return {}
    close = hist['Close']
    # Moving averages
    ma20 = close.rolling(20).mean().iloc[-1]
    ma50 = close.rolling(50).mean().iloc[-1] if len(close) >= 50 else None
    # RSI
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss
    rsi = (100 - (100 / (1 + rs))).iloc[-1]
    # MACD
    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    macd = (ema12 - ema26).iloc[-1]
    # Bollinger Bands
    std20 = close.rolling(20).std().iloc[-1]
    upper_band = ma20 + (2 * std20)
    lower_band = ma20 - (2 * std20)
    current_price = close.iloc[-1]
    # Volume trend
    avg_vol = hist['Volume'].rolling(20).mean().iloc[-1]
    curr_vol = hist['Volume'].iloc[-1]
    return {
        'current_price': round(current_price, 2),
        'ma20': round(ma20, 2),
        'ma50': round(ma50, 2) if ma50 else None,
        'rsi': round(rsi, 1),
        'macd': round(macd, 2),
        'upper_band': round(upper_band, 2),
        'lower_band': round(lower_band, 2),
        'vol_ratio': round(curr_vol / avg_vol, 2) if avg_vol > 0 else 1.0
    }

def generate_investment_verdict(sentiment_score, sentiment_label, tech, info):
    """Generate a comprehensive investment recommendation."""
    score = 50  # Base score
    reasons = []
    risks = []

    # Sentiment component (30%)
    sent_score = (sentiment_score + 1) / 2 * 30
    score = score - 15 + sent_score
    if sentiment_score > 0.2:
        reasons.append("📰 Strong positive news sentiment")
    elif sentiment_score < -0.2:
        risks.append("📰 Negative news flow detected")

    # Technical indicators (40%)
    if tech:
        cp = tech.get('current_price', 0)
        ma20 = tech.get('ma20', 0)
        ma50 = tech.get('ma50', 0)
        rsi = tech.get('rsi', 50)
        macd = tech.get('macd', 0)

        if cp > ma20:
            score += 8
            reasons.append("📈 Price above 20-day moving average")
        else:
            score -= 5
            risks.append("📉 Price below 20-day MA (bearish signal)")

        if ma50 and cp > ma50:
            score += 7
            reasons.append("📊 Trading above 50-day moving average")
        elif ma50:
            score -= 5
            risks.append("📊 Below 50-day MA (longer-term weakness)")

        if 30 <= rsi <= 70:
            score += 5
            reasons.append(f"⚖️ RSI at {rsi:.1f} (healthy zone)")
        elif rsi < 30:
            score += 8
            reasons.append(f"🔄 RSI oversold ({rsi:.1f}) — potential reversal")
        elif rsi > 70:
            score -= 8
            risks.append(f"⚠️ RSI overbought ({rsi:.1f}) — caution advised")

        if macd > 0:
            score += 5
            reasons.append("✅ MACD positive (bullish momentum)")
        else:
            score -= 3
            risks.append("🔻 MACD negative (bearish momentum)")

    # Fundamental data (30%)
    pe = info.get('trailingPE', None)
    pb = info.get('priceToBook', None)
    div_yield = info.get('dividendYield', 0) or 0

    if pe:
        if 0 < pe < 25:
            score += 10
            reasons.append(f"💰 Attractive P/E ratio ({pe:.1f})")
        elif pe > 50:
            score -= 5
            risks.append(f"⚠️ High P/E ratio ({pe:.1f}) — expensive valuation")

    if div_yield and div_yield > 0.02:
        score += 5
        reasons.append(f"💵 Decent dividend yield ({div_yield*100:.1f}%)")

    # Clamp score
    score = max(0, min(100, score))

    if score >= 70:
        verdict = "STRONG BUY"
        verdict_color = "positive"
        verdict_emoji = "🚀"
        summary = "Multiple bullish indicators align. Strong candidate for investment consideration."
    elif score >= 55:
        verdict = "BUY"
        verdict_color = "positive"
        verdict_emoji = "✅"
        summary = "Favorable signals with moderate confidence. Consider adding to your watchlist."
    elif score >= 40:
        verdict = "HOLD / WATCH"
        verdict_color = "neutral"
        verdict_emoji = "⏳"
        summary = "Mixed signals. Wait for clearer direction before making a move."
    elif score >= 25:
        verdict = "SELL"
        verdict_color = "negative"
        verdict_emoji = "⚠️"
        summary = "More bearish signals than bullish. Review your position carefully."
    else:
        verdict = "STRONG SELL"
        verdict_color = "negative"
        verdict_emoji = "🔴"
        summary = "Strong bearish signals across multiple indicators. High risk."

    return verdict, verdict_color, verdict_emoji, summary, score, reasons, risks

# ─── Chart Functions ──────────────────────────────────────────────────────────

def plot_candlestick(hist, ticker, dark_mode):
    bg = "#0A0E1A" if dark_mode else "#FFFFFF"
    grid = "#1E2D45" if dark_mode else "#E2E8F0"
    text_color = "#F0F4FF" if dark_mode else "#0F172A"

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.04, row_heights=[0.7, 0.3])
    fig.add_trace(go.Candlestick(
        x=hist.index, open=hist['Open'], high=hist['High'],
        low=hist['Low'], close=hist['Close'],
        increasing_line_color='#10B981', decreasing_line_color='#EF4444',
        name='Price'
    ), row=1, col=1)

    ma20 = hist['Close'].rolling(20).mean()
    ma50 = hist['Close'].rolling(50).mean()
    fig.add_trace(go.Scatter(x=hist.index, y=ma20, name='MA20',
                             line=dict(color='#00D4FF', width=1.5), opacity=0.8), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=ma50, name='MA50',
                             line=dict(color='#F59E0B', width=1.5), opacity=0.8), row=1, col=1)
    fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume',
                         marker_color='#7C3AED', opacity=0.6), row=2, col=1)

    fig.update_layout(
        paper_bgcolor=bg, plot_bgcolor=bg,
        font=dict(color=text_color, family='Space Grotesk'),
        xaxis_rangeslider_visible=False,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, bgcolor='rgba(0,0,0,0)'),
        margin=dict(t=10, b=10, l=10, r=10),
        height=420,
        xaxis2=dict(gridcolor=grid, showgrid=True),
        xaxis=dict(gridcolor=grid, showgrid=True),
        yaxis=dict(gridcolor=grid, showgrid=True),
        yaxis2=dict(gridcolor=grid, showgrid=True, title='Volume'),
    )
    return fig

def plot_sentiment_gauge(score, dark_mode):
    bg = "#0A0E1A" if dark_mode else "#FFFFFF"
    text_color = "#F0F4FF" if dark_mode else "#0F172A"
    normalized = (score + 1) / 2 * 100
    color = "#10B981" if score > 0.05 else ("#EF4444" if score < -0.05 else "#F59E0B")

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=normalized,
        delta={'reference': 50, 'increasing': {'color': "#10B981"}, 'decreasing': {'color': "#EF4444"}},
        number={'suffix': '%', 'font': {'size': 32, 'color': text_color, 'family': 'JetBrains Mono'}},
        gauge={
            'axis': {'range': [0, 100], 'tickfont': {'color': text_color}},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': 'rgba(0,0,0,0)',
            'bordercolor': 'rgba(0,0,0,0)',
            'steps': [
                {'range': [0, 33], 'color': '#EF444422'},
                {'range': [33, 66], 'color': '#F59E0B22'},
                {'range': [66, 100], 'color': '#10B98122'}
            ],
            'threshold': {'line': {'color': color, 'width': 3}, 'value': normalized}
        }
    ))
    fig.update_layout(
        paper_bgcolor=bg,
        font=dict(color=text_color, family='Space Grotesk'),
        height=220, margin=dict(t=20, b=20, l=30, r=30)
    )
    return fig

def plot_sentiment_breakdown(pos, neg, neu, dark_mode):
    bg = "#0A0E1A" if dark_mode else "#FFFFFF"
    text_color = "#F0F4FF" if dark_mode else "#0F172A"
    labels = ['Positive', 'Negative', 'Neutral']
    values = [pos, neg, neu]
    colors = ['#10B981', '#EF4444', '#F59E0B']
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.65,
        marker=dict(colors=colors, line=dict(color=bg, width=3)),
        textfont=dict(color=text_color),
    ))
    fig.update_layout(
        paper_bgcolor=bg,
        font=dict(color=text_color, family='Space Grotesk'),
        height=220, margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(font=dict(color=text_color), bgcolor='rgba(0,0,0,0)', orientation='h', y=-0.1),
        showlegend=True,
    )
    return fig

# ─── Main App ─────────────────────────────────────────────────────────────────

def main():
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        dark_mode = st.toggle("🌙 Dark Mode", value=True)
        st.markdown("---")
        st.markdown("### 📈 Chart Period")
        period_map = {"1 Month": "1mo", "3 Months": "3mo",
                      "6 Months": "6mo", "1 Year": "1y", "2 Years": "2y"}
        period_label = st.selectbox("", list(period_map.keys()), index=2)
        period = period_map[period_label]
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        **SentimentEdge** uses:
        - 🧠 VADER + TextBlob NLP
        - 📊 Yahoo Finance data
        - 📰 Google News RSS
        - 📐 Technical Indicators

        *For educational purposes only. Not financial advice.*
        """)
        st.markdown("---")
        st.caption("Built for MBA AI & FinTech Project · 2025")

    load_css(dark_mode)

    # Header
    st.markdown("""
    <div class="main-header">
        <div class="badge">AI-Powered Stock Intelligence</div>
        <h1>📈 SentimentEdge</h1>
        <p>Real-time sentiment analysis & technical insights for Indian stocks (NSE & BSE)</p>
    </div>
    """, unsafe_allow_html=True)

    # Search
    col_search, col_btn = st.columns([4, 1])
    with col_search:
        stock_names = list(INDIAN_STOCKS.keys())
        selected_stock = st.selectbox(
            "🔍 Search for a company",
            stock_names,
            index=0,
            help="Type to search from 150+ NSE/BSE listed companies"
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("Analyze →", use_container_width=True)

    if selected_stock:
        ticker = INDIAN_STOCKS[selected_stock]
        st.markdown(f"**Selected:** `{selected_stock}` · `{ticker}`")

    if analyze_btn or selected_stock:
        ticker = INDIAN_STOCKS[selected_stock]

        with st.spinner(f"Fetching data for {selected_stock}..."):
            hist, info = get_stock_data(ticker, period)
            news_items = get_news_sentiment(selected_stock, ticker)
            tech = get_technical_indicators(hist)
            sent_score, sent_label, pos_count, neg_count, neu_count = calculate_overall_sentiment(news_items)
            verdict, v_color, v_emoji, summary, conf_score, reasons, risks = generate_investment_verdict(
                sent_score, sent_label, tech, info
            )

        # ── Price Metrics Row ─────────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <div class="section-dot"></div>
            <h3>Live Market Data (Yahoo Finance)</h3>
        </div>
        """, unsafe_allow_html=True)

        if tech and info:
            cp = tech.get('current_price', 0)
            prev = info.get('previousClose', cp)
            change = cp - prev
            change_pct = (change / prev * 100) if prev else 0
            delta_class = "positive" if change >= 0 else "negative"
            delta_sign = "+" if change >= 0 else ""

            c1, c2, c3, c4, c5, c6 = st.columns(6)
            metrics = [
                (c1, "Current Price", f"₹{cp:,.2f}", f"{delta_sign}{change:.2f} ({delta_sign}{change_pct:.2f}%)", delta_class),
                (c2, "52W High", f"₹{info.get('fiftyTwoWeekHigh', 'N/A')}", "", ""),
                (c3, "52W Low", f"₹{info.get('fiftyTwoWeekLow', 'N/A')}", "", ""),
                (c4, "Market Cap", f"₹{info.get('marketCap', 0)/1e9:.1f}B" if info.get('marketCap') else "N/A", "", ""),
                (c5, "P/E Ratio", f"{info.get('trailingPE', 'N/A'):.1f}" if isinstance(info.get('trailingPE'), float) else str(info.get('trailingPE', 'N/A')), "", ""),
                (c6, "Dividend Yield", f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "0.00%", "", ""),
            ]
            for col, label, val, delta, dc in metrics:
                with col:
                    delta_html = f'<div class="metric-delta {dc}">{delta}</div>' if delta else ""
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value">{val}</div>
                        {delta_html}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Could not fetch live price data. Yahoo Finance may be rate-limiting. Try again in a few seconds.")

        # ── Chart ─────────────────────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <div class="section-dot"></div>
            <h3>Price Chart & Volume</h3>
        </div>
        """, unsafe_allow_html=True)
        if hist is not None and not hist.empty:
            st.plotly_chart(plot_candlestick(hist, ticker, dark_mode), use_container_width=True)
        else:
            st.info("Chart data unavailable. Please check your internet connection.")

        # ── Technical Indicators ──────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <div class="section-dot"></div>
            <h3>Technical Indicators</h3>
        </div>
        """, unsafe_allow_html=True)
        if tech:
            t1, t2, t3, t4 = st.columns(4)
            rsi = tech.get('rsi', 50)
            rsi_label = "Oversold 🟢" if rsi < 30 else ("Overbought 🔴" if rsi > 70 else "Neutral ⚪")
            macd = tech.get('macd', 0)
            macd_label = "Bullish ↑" if macd > 0 else "Bearish ↓"
            vol_r = tech.get('vol_ratio', 1)
            vol_label = "High 🔥" if vol_r > 1.5 else ("Low 📉" if vol_r < 0.7 else "Normal")

            with t1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">RSI (14)</div>
                    <div class="metric-value">{rsi}</div>
                    <div class="metric-delta">{rsi_label}</div>
                </div>""", unsafe_allow_html=True)
            with t2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">MACD</div>
                    <div class="metric-value">{macd}</div>
                    <div class="metric-delta">{macd_label}</div>
                </div>""", unsafe_allow_html=True)
            with t3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">MA 20-Day</div>
                    <div class="metric-value">₹{tech.get('ma20', 'N/A')}</div>
                    <div class="metric-delta">Moving Avg</div>
                </div>""", unsafe_allow_html=True)
            with t4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Volume Ratio</div>
                    <div class="metric-value">{vol_r}x</div>
                    <div class="metric-delta">{vol_label}</div>
                </div>""", unsafe_allow_html=True)

        # ── Sentiment Analysis ────────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <div class="section-dot"></div>
            <h3>Sentiment Analysis</h3>
        </div>
        """, unsafe_allow_html=True)

        sa_col, sb_col = st.columns([1, 1])
        with sa_col:
            st.markdown('<div class="sentiment-container">', unsafe_allow_html=True)
            st.markdown("**Overall Sentiment Score**")
            st.plotly_chart(plot_sentiment_gauge(sent_score, dark_mode), use_container_width=True)
            sent_class = "positive" if sent_label == "positive" else ("negative" if sent_label == "negative" else "neutral")
            st.markdown(f'<div class="metric-delta {sent_class}" style="font-size:1rem;text-align:center;">Sentiment: {sent_label.upper()} ({sent_score:+.3f})</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with sb_col:
            st.markdown('<div class="sentiment-container">', unsafe_allow_html=True)
            st.markdown("**News Breakdown**")
            total = pos_count + neg_count + neu_count
            if total > 0:
                st.plotly_chart(plot_sentiment_breakdown(pos_count, neg_count, neu_count, dark_mode), use_container_width=True)
                st.markdown(f"<div style='text-align:center;font-size:0.85rem;'>Analyzed <b>{total}</b> recent articles</div>", unsafe_allow_html=True)
            else:
                st.info("No news data found for this stock.")
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Investment Verdict ────────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <div class="section-dot"></div>
            <h3>AI Investment Signal</h3>
        </div>
        """, unsafe_allow_html=True)

        v1, v2 = st.columns([1, 2])
        with v1:
            verdict_color_hex = "#10B981" if v_color == "positive" else ("#EF4444" if v_color == "negative" else "#F59E0B")
            st.markdown(f"""
            <div class="verdict-box">
                <div style="font-size:2.5rem;">{v_emoji}</div>
                <div class="verdict-text" style="color:{verdict_color_hex};">{verdict}</div>
                <div style="margin:12px 0;font-size:0.85rem;color:var(--text-secondary);">Confidence Score</div>
                <div style="font-size:1.8rem;font-weight:700;font-family:'JetBrains Mono',monospace;">{conf_score:.0f}/100</div>
                <div style="margin-top:12px;font-size:0.8rem;line-height:1.5;">{summary}</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(conf_score / 100)

        with v2:
            if reasons:
                st.markdown("**✅ Bullish Signals**")
                for r in reasons:
                    st.markdown(f"- {r}")
            if risks:
                st.markdown("**⚠️ Risk Factors**")
                for r in risks:
                    st.markdown(f"- {r}")
            st.info("⚠️ **Disclaimer:** This is an educational AI tool. Always do your own research (DYOR) before investing. Past performance is not indicative of future results.")

        # ── News Feed ─────────────────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <div class="section-dot"></div>
            <h3>Recent News & Articles</h3>
        </div>
        """, unsafe_allow_html=True)

        if news_items:
            for item in news_items:
                pill_class = f"pill-{item['sentiment']}"
                pill_text = item['sentiment'].upper()
                score_display = f"{item['score']:+.3f}"
                st.markdown(f"""
                <div class="news-card">
                    <div class="news-title">{item['title']}</div>
                    <div class="news-meta">
                        <span class="sentiment-pill {pill_class}">{pill_text}</span>
                        <span>Score: {score_display}</span>
                        <span>📅 {item['published'][:16] if len(item['published']) > 10 else item['published']}</span>
                        <span>📰 {item['source']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 No recent news found. Try searching Google News for this company manually.")

        # ── Company Info ──────────────────────────────────────────────────
        if info:
            with st.expander("📋 Company Information"):
                ic1, ic2 = st.columns(2)
                with ic1:
                    st.markdown(f"**Sector:** {info.get('sector', 'N/A')}")
                    st.markdown(f"**Industry:** {info.get('industry', 'N/A')}")
                    st.markdown(f"**Exchange:** {info.get('exchange', 'N/A')}")
                    st.markdown(f"**Currency:** {info.get('currency', 'INR')}")
                with ic2:
                    st.markdown(f"**EPS:** {info.get('trailingEps', 'N/A')}")
                    st.markdown(f"**Beta:** {info.get('beta', 'N/A')}")
                    st.markdown(f"**Avg Volume:** {info.get('averageVolume', 'N/A'):,}" if isinstance(info.get('averageVolume'), int) else f"**Avg Volume:** N/A")
                    st.markdown(f"**Float Shares:** {info.get('floatShares', 'N/A')}")
                desc = info.get('longBusinessSummary', '')
                if desc:
                    st.markdown("**About the Company:**")
                    st.markdown(desc[:600] + "..." if len(desc) > 600 else desc)

if __name__ == "__main__":
    main()

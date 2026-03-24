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

# ── VADER-lite: built-in lexicon, no install needed ──────────────────────────
POSITIVE_WORDS = {
    "growth","profit","surge","rally","strong","beat","record","gain","rise","up","bullish",
    "outperform","upgrade","buy","positive","boost","soar","jump","high","good","great",
    "excellent","opportunity","recovery","success","win","advance","expand","improve",
    "revenue","earnings","dividend","acquisition","innovation","launch","partnership",
    "approval","milestone","target","exceed","robust","solid","optimistic","confident",
    "increase","higher","better","best","boom","breakout","momentum","upside","attractive",
    "potential","deliver","achieve","order","contract","invest","fund","grow","benefit",
    "reward","leader","dominant","efficient","quality","value","returns","recommend",
}
NEGATIVE_WORDS = {
    "loss","decline","fall","drop","weak","miss","disappoint","sell","bearish","risk",
    "concern","worry","debt","crisis","cut","reduce","lower","poor","bad","negative",
    "slow","down","downturn","underperform","downgrade","crash","plunge","slump","trouble",
    "problem","issue","challenge","threat","uncertainty","volatile","warning","alert",
    "default","penalty","fine","fraud","scam","probe","investigation","lawsuit","recall",
    "ban","restrict","delay","cancel","fail","exit","close","layoff","resign","resign",
    "pressure","squeeze","margin","competition","dilute","expensive","overvalued","bubble",
}

def simple_sentiment(text):
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    pos = sum(1 for w in words if w in POSITIVE_WORDS)
    neg = sum(1 for w in words if w in NEGATIVE_WORDS)
    total = pos + neg
    if total == 0:
        return 0.0, "neutral"
    score = (pos - neg) / (total + len(words) * 0.1)
    score = max(-1.0, min(1.0, score * 3))
    if score > 0.05:
        return round(score, 3), "positive"
    elif score < -0.05:
        return round(score, 3), "negative"
    return 0.0, "neutral"

# ── Yahoo Finance (no library — direct API call) ───────────────────────────
def fetch_yahoo(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(ticker)}?interval=1d&range=6mo"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        result = data["chart"]["result"][0]
        meta = result["meta"]
        timestamps = result.get("timestamp", [])
        closes = result["indicators"]["quote"][0].get("close", [])
        highs  = result["indicators"]["quote"][0].get("high", [])
        lows   = result["indicators"]["quote"][0].get("low", [])
        opens  = result["indicators"]["quote"][0].get("open", [])
        volumes= result["indicators"]["quote"][0].get("volume", [])
        dates  = [datetime.utcfromtimestamp(t).strftime("%Y-%m-%d") for t in timestamps]
        hist = {"dates": dates, "close": closes, "high": highs,
                "low": lows, "open": opens, "volume": volumes}
        info = {
            "currentPrice": meta.get("regularMarketPrice", 0),
            "previousClose": meta.get("previousClose") or meta.get("chartPreviousClose", 0),
            "fiftyTwoWeekHigh": meta.get("fiftyTwoWeekHigh", 0),
            "fiftyTwoWeekLow": meta.get("fiftyTwoWeekLow", 0),
            "currency": meta.get("currency", "INR"),
            "symbol": meta.get("symbol", ticker),
            "exchange": meta.get("exchangeName", "NSE/BSE"),
        }
        return hist, info
    except Exception as e:
        return None, {}

def fetch_news(company, ticker):
    symbol = ticker.replace(".NS","").replace(".BO","")
    query = urllib.parse.quote(f"{company} stock India")
    url = f"https://news.google.com/rss/search?q={query}+when:7d&hl=en-IN&gl=IN&ceid=IN:en"
    articles = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            raw = r.read()
        root = ET.fromstring(raw)
        channel = root.find("channel")
        items = channel.findall("item") if channel else []
        for item in items[:12]:
            title = item.findtext("title","")
            title = re.sub(r'\s*-\s*\S+$', '', title)  # remove source suffix
            pub   = item.findtext("pubDate","")[:16]
            link  = item.findtext("link","#")
            score, label = simple_sentiment(title)
            articles.append({"title": title, "published": pub,
                              "score": score, "sentiment": label, "link": link})
    except:
        pass
    return articles

def calc_technicals(hist):
    closes = [c for c in hist["close"] if c is not None]
    vols   = [v for v in hist["volume"] if v is not None]
    if len(closes) < 20:
        return {}
    def ma(n):
        return sum(closes[-n:]) / n if len(closes) >= n else None
    # RSI
    deltas = [closes[i]-closes[i-1] for i in range(1,len(closes))]
    gains  = [d if d>0 else 0 for d in deltas[-14:]]
    losses = [-d if d<0 else 0 for d in deltas[-14:]]
    avg_g  = sum(gains)/14
    avg_l  = sum(losses)/14
    rsi    = 100 - (100/(1+(avg_g/avg_l))) if avg_l>0 else 100
    # MACD
    def ema(data, span):
        k = 2/(span+1); v = data[0]
        for d in data[1:]: v = d*k + v*(1-k)
        return v
    macd = ema(closes[-26:], 12) - ema(closes[-26:], 26) if len(closes) >= 26 else 0
    # Volume
    avg_vol = sum(vols[-20:])/20 if vols else 0
    curr_vol = vols[-1] if vols else 0
    return {
        "current": round(closes[-1], 2),
        "ma20": round(ma(20), 2),
        "ma50": round(ma(50), 2) if len(closes)>=50 else None,
        "rsi": round(rsi, 1),
        "macd": round(macd, 2),
        "vol_ratio": round(curr_vol/avg_vol, 2) if avg_vol else 1.0,
    }

def investment_signal(sent_score, tech, articles):
    score = 50
    reasons, risks = [], []
    # Sentiment (30%)
    score += sent_score * 30
    if sent_score > 0.15: reasons.append("📰 Positive news momentum")
    elif sent_score < -0.15: risks.append("📰 Negative news flow")
    # Technicals (50%)
    if tech:
        cp, ma20 = tech.get("current",0), tech.get("ma20",0)
        ma50, rsi, macd = tech.get("ma50"), tech.get("rsi",50), tech.get("macd",0)
        if cp > ma20: score+=8; reasons.append("📈 Above 20-day moving average")
        else: score-=5; risks.append("📉 Below 20-day moving average")
        if ma50:
            if cp > ma50: score+=7; reasons.append("📊 Above 50-day moving average")
            else: score-=5; risks.append("📊 Below 50-day moving average")
        if rsi < 30: score+=8; reasons.append(f"🔄 RSI oversold ({rsi}) — potential bounce")
        elif rsi > 70: score-=8; risks.append(f"⚠️ RSI overbought ({rsi}) — caution")
        else: score+=4; reasons.append(f"⚖️ RSI healthy ({rsi})")
        if macd > 0: score+=5; reasons.append("✅ MACD bullish")
        else: score-=3; risks.append("🔻 MACD bearish")
        vr = tech.get("vol_ratio",1)
        if vr > 1.5: score+=3; reasons.append(f"🔥 High trading volume ({vr}x avg)")
    score = max(0, min(100, score))
    if score >= 70: return "STRONG BUY","#10B981","🚀", score, reasons, risks
    if score >= 55: return "BUY","#22C55E","✅", score, reasons, risks
    if score >= 40: return "HOLD / WATCH","#F59E0B","⏳", score, reasons, risks
    if score >= 25: return "SELL","#F97316","⚠️", score, reasons, risks
    return "STRONG SELL","#EF4444","🔴", score, reasons, risks

# ── Inline sparkline (SVG) ────────────────────────────────────────────────────
def sparkline_svg(values, color="#00D4FF", width=300, height=60):
    vals = [v for v in values if v is not None]
    if len(vals) < 2: return ""
    mn, mx = min(vals), max(vals)
    rng = mx - mn or 1
    pts = []
    for i, v in enumerate(vals):
        x = i/(len(vals)-1)*width
        y = height - (v-mn)/rng*(height-4) - 2
        pts.append(f"{x:.1f},{y:.1f}")
    polyline = " ".join(pts)
    first_x,first_y = pts[0].split(",")
    last_x,last_y   = pts[-1].split(",")
    fill_pts = f"{first_x},{height} " + polyline + f" {last_x},{height}"
    return f"""
    <svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:70px">
      <defs>
        <linearGradient id="sg" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="{color}" stop-opacity="0.3"/>
          <stop offset="100%" stop-color="{color}" stop-opacity="0"/>
        </linearGradient>
      </defs>
      <polygon points="{fill_pts}" fill="url(#sg)"/>
      <polyline points="{polyline}" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>
    </svg>"""

# ── CSS ───────────────────────────────────────────────────────────────────────
def load_css(dark):
    bp  = "#0A0E1A" if dark else "#F0F4FF"
    bs  = "#111827" if dark else "#E8EEFF"
    bc  = "#1A2332" if dark else "#FFFFFF"
    tp  = "#F0F4FF" if dark else "#0F172A"
    ts  = "#94A3B8" if dark else "#475569"
    brd = "#1E2D45" if dark else "#DDE4F0"
    acc = "#00D4FF"
    pos = "#10B981"; neg = "#EF4444"; wrn = "#F59E0B"
    st.markdown(f"""<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
    html,body,[class*="css"]{{font-family:'DM Sans',sans-serif;}}
    .stApp{{background:{bp};color:{tp};}}
    section[data-testid="stSidebar"]{{background:{bs};border-right:1px solid {brd};}}
    .top-bar{{background:linear-gradient(135deg,{bs},{bc});border:1px solid {brd};border-radius:14px;
        padding:24px 30px;margin-bottom:20px;position:relative;overflow:hidden;}}
    .top-bar::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;
        background:linear-gradient(90deg,{acc},#7C3AED);}}
    .top-bar h1{{font-size:2rem;font-weight:700;margin:4px 0;color:{tp};letter-spacing:-0.5px;}}
    .top-bar p{{color:{ts};font-size:0.9rem;margin:0;}}
    .chip{{display:inline-block;background:{acc}18;border:1px solid {acc}44;color:{acc};
        font-size:0.65rem;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;
        padding:3px 9px;border-radius:20px;margin-bottom:8px;}}
    .card{{background:{bc};border:1px solid {brd};border-radius:12px;padding:18px;
        transition:box-shadow .2s;}}
    .card:hover{{box-shadow:0 6px 20px {acc}18;}}
    .mlabel{{font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:1px;
        color:{ts};margin-bottom:6px;}}
    .mval{{font-size:1.45rem;font-weight:700;color:{tp};font-family:'JetBrains Mono',monospace;}}
    .mdelta{{font-size:0.78rem;margin-top:3px;font-family:'JetBrains Mono',monospace;}}
    .pos{{color:{pos};}} .neg{{color:{neg};}} .neu{{color:{wrn};}}
    .sec{{display:flex;align-items:center;gap:8px;margin:22px 0 12px;
        padding-bottom:8px;border-bottom:1px solid {brd};}}
    .sec h3{{font-size:1rem;font-weight:600;color:{tp};margin:0;}}
    .dot{{width:7px;height:7px;border-radius:50%;background:linear-gradient(135deg,{acc},#7C3AED);}}
    .verdict-box{{background:linear-gradient(135deg,{bs},{bc});border:1px solid {brd};
        border-radius:14px;padding:24px;text-align:center;}}
    .news-item{{background:{bc};border:1px solid {brd};border-radius:9px;
        padding:13px 15px;margin-bottom:8px;}}
    .news-item:hover{{border-color:{acc}55;}}
    .ntitle{{font-size:0.88rem;font-weight:500;color:{tp};line-height:1.4;margin-bottom:5px;}}
    .nmeta{{font-size:0.72rem;color:{ts};display:flex;gap:10px;flex-wrap:wrap;align-items:center;}}
    .pill{{padding:2px 7px;border-radius:20px;font-size:0.68rem;font-weight:700;}}
    .pp{{background:{pos}20;color:{pos};border:1px solid {pos}44;}}
    .np{{background:{neg}20;color:{neg};border:1px solid {neg}44;}}
    .neup{{background:{wrn}20;color:{wrn};border:1px solid {wrn}44;}}
    .bar-track{{background:{brd};border-radius:99px;height:8px;margin:6px 0;}}
    .bar-fill{{height:8px;border-radius:99px;background:linear-gradient(90deg,{acc},#7C3AED);}}
    div.stButton>button{{background:linear-gradient(135deg,{acc},#7C3AED);color:#fff;
        border:none;border-radius:8px;font-weight:600;font-family:'DM Sans',sans-serif;
        padding:10px 22px;width:100%;}}
    div.stButton>button:hover{{opacity:.88;transform:translateY(-1px);}}
    </style>""", unsafe_allow_html=True)

# ── App ───────────────────────────────────────────────────────────────────────
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
        st.markdown("---")

    load_css(dark)
    bp="#0A0E1A" if dark else "#F0F4FF"
    pos_c="#10B981"; neg_c="#EF4444"; neu_c="#F59E0B"; acc="#00D4FF"

    st.markdown("""
    <div class="top-bar">
        <div class="chip">AI-Powered · NSE & BSE</div>
        <h1>📈 SentimentEdge</h1>
        <p>Real-time sentiment analysis &amp; investment signals for Indian stocks</p>
    </div>""", unsafe_allow_html=True)

   col1, col2 = st.columns([4,1])

with col1:
    user_input = st.text_input("🔍 Search company (or pick from list)")
    selected_company = st.selectbox("Or select from list", list(INDIAN_STOCKS.keys()))

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    go = st.button("Analyse →")

   if not go:
    return

   selected_company = None

# Priority: typed input > dropdown
if user_input:
    for name in INDIAN_STOCKS:
        if user_input.lower() in name.lower():
            selected_company = name
            break

if not selected_company:
    selected_company = chosen

ticker = INDIAN_STOCKS[selected_company]

    with st.spinner("Fetching live market data…"):
        hist, info = fetch_yahoo(ticker)
    with st.spinner("Reading latest news…"):
        articles = fetch_news(chosen, ticker)

    tech = calc_technicals(hist) if hist else {}
    pos_news = [a for a in articles if a["sentiment"]=="positive"]
    neg_news = [a for a in articles if a["sentiment"]=="negative"]
    neu_news = [a for a in articles if a["sentiment"]=="neutral"]
    avg_sent = sum(a["score"] for a in articles)/len(articles) if articles else 0
    verdict, v_color, v_emoji, conf, reasons, risks = investment_signal(avg_sent, tech, articles)

    # ── Price strip ──────────────────────────────────────────────────────
    st.markdown('<div class="sec"><div class="dot"></div><h3>Live Market Data</h3></div>', unsafe_allow_html=True)
    if info:
        cp   = info.get("currentPrice", 0) or 0
        prev = info.get("previousClose", cp) or cp
        chg  = cp - prev
        chg_pct = (chg/prev*100) if prev else 0
        dc   = "pos" if chg>=0 else "neg"
        sign = "+" if chg>=0 else ""
        w52h = info.get("fiftyTwoWeekHigh",0) or 0
        w52l = info.get("fiftyTwoWeekLow",0) or 0
        exch = info.get("exchange","NSE")

        c1,c2,c3,c4 = st.columns(4)
        def mcard(col, label, val, delta="", dc_=""):
            delta_html = f'<div class="mdelta {dc_}">{delta}</div>' if delta else ""
            col.markdown(f'<div class="card"><div class="mlabel">{label}</div>'
                         f'<div class="mval">{val}</div>{delta_html}</div>', unsafe_allow_html=True)
        mcard(c1,"Current Price",f"₹{cp:,.2f}",f"{sign}{chg:.2f} ({sign}{chg_pct:.2f}%)",dc)
        mcard(c2,"52W High",f"₹{w52h:,.2f}")
        mcard(c3,"52W Low", f"₹{w52l:,.2f}")
        mcard(c4,"Exchange", exch)
    else:
        st.warning("⚠️ Could not fetch live price. Yahoo Finance may be rate-limiting — wait 30 sec and retry.")

    # ── Sparkline chart ──────────────────────────────────────────────────
    if hist:
        closes = [c for c in hist["close"] if c is not None]
        chg_overall = closes[-1]-closes[0] if len(closes)>=2 else 0
        chart_color = pos_c if chg_overall>=0 else neg_c
        st.markdown('<div class="sec"><div class="dot"></div><h3>6-Month Price Trend</h3></div>', unsafe_allow_html=True)
        svg = sparkline_svg(closes, chart_color)
        st.markdown(f'<div class="card">{svg}</div>', unsafe_allow_html=True)

        # show first/last date labels
        dates = hist.get("dates",[])
        if dates:
            d1,d2 = st.columns(2)
            d1.caption(f"📅 {dates[0]}")
            d2.caption(f"📅 {dates[-1]}" if len(dates)>1 else "")

    # ── Technical indicators ─────────────────────────────────────────────
    if tech:
        st.markdown('<div class="sec"><div class="dot"></div><h3>Technical Indicators</h3></div>', unsafe_allow_html=True)
        t1,t2,t3,t4 = st.columns(4)
        rsi = tech.get("rsi",50)
        rsi_lbl = "🟢 Oversold" if rsi<30 else ("🔴 Overbought" if rsi>70 else "⚪ Neutral")
        macd = tech.get("macd",0)
        macd_lbl = "↑ Bullish" if macd>0 else "↓ Bearish"
        vr = tech.get("vol_ratio",1)
        vr_lbl = "🔥 High" if vr>1.5 else ("📉 Low" if vr<0.7 else "Normal")
        def tcard(col, label, val, sub):
            col.markdown(f'<div class="card"><div class="mlabel">{label}</div>'
                         f'<div class="mval">{val}</div><div class="mdelta neu">{sub}</div></div>',
                         unsafe_allow_html=True)
        tcard(t1,"RSI (14)", rsi, rsi_lbl)
        tcard(t2,"MACD", macd, macd_lbl)
        tcard(t3,"MA 20-Day", f"₹{tech.get('ma20','—')}", "Moving avg")
        tcard(t4,"Vol Ratio", f"{vr}x", vr_lbl)

    # ── Sentiment ────────────────────────────────────────────────────────
    st.markdown('<div class="sec"><div class="dot"></div><h3>News Sentiment Analysis</h3></div>', unsafe_allow_html=True)
    s1,s2 = st.columns(2)
    sent_pct = int((avg_sent+1)/2*100)
    sent_lbl = "POSITIVE" if avg_sent>0.05 else ("NEGATIVE" if avg_sent<-0.05 else "NEUTRAL")
    sent_cls  = "pos" if avg_sent>0.05 else ("neg" if avg_sent<-0.05 else "neu")
    total_arts = len(articles)
    with s1:
        st.markdown(f"""
        <div class="card" style="text-align:center;padding:24px;">
            <div class="mlabel">Overall Sentiment</div>
            <div style="font-size:3rem;font-weight:800;font-family:'JetBrains Mono',monospace;
                margin:10px 0;" class="{sent_cls}">{sent_pct}%</div>
            <div class="bar-track"><div class="bar-fill" style="width:{sent_pct}%"></div></div>
            <div class="mdelta {sent_cls}" style="margin-top:8px;font-size:1rem;">{sent_lbl}</div>
            <div style="color:#94A3B8;font-size:0.78rem;margin-top:6px;">
                Based on {total_arts} articles</div>
        </div>""", unsafe_allow_html=True)
    with s2:
        pp = len(pos_news); np_ = len(neg_news); np2 = len(neu_news)
        tot = pp+np_+np2 or 1
        st.markdown(f"""
        <div class="card" style="padding:24px;">
            <div class="mlabel">Article Breakdown</div>
            <div style="margin-top:14px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span class="pos">✅ Positive</span><b class="pos">{pp}</b></div>
                <div class="bar-track"><div style="height:8px;border-radius:99px;
                    background:{pos_c};width:{pp/tot*100:.0f}%"></div></div>
                <div style="display:flex;justify-content:space-between;margin:10px 0 4px;">
                    <span class="neg">❌ Negative</span><b class="neg">{np_}</b></div>
                <div class="bar-track"><div style="height:8px;border-radius:99px;
                    background:{neg_c};width:{np_/tot*100:.0f}%"></div></div>
                <div style="display:flex;justify-content:space-between;margin:10px 0 4px;">
                    <span class="neu">⚪ Neutral</span><b class="neu">{np2}</b></div>
                <div class="bar-track"><div style="height:8px;border-radius:99px;
                    background:{neu_c};width:{np2/tot*100:.0f}%"></div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── Verdict ──────────────────────────────────────────────────────────
    st.markdown('<div class="sec"><div class="dot"></div><h3>AI Investment Signal</h3></div>', unsafe_allow_html=True)
    v1,v2 = st.columns([1,2])
    with v1:
        bar_w = int(conf)
        st.markdown(f"""
        <div class="verdict-box">
            <div style="font-size:2.8rem;">{v_emoji}</div>
            <div style="font-size:1.8rem;font-weight:800;color:{v_color};
                letter-spacing:-0.5px;margin:8px 0;">{verdict}</div>
            <div class="mlabel">Confidence Score</div>
            <div style="font-size:2rem;font-weight:700;font-family:'JetBrains Mono',monospace;
                color:{v_color};">{conf:.0f}<span style="font-size:1rem">/100</span></div>
            <div class="bar-track" style="margin-top:10px;">
                <div style="height:8px;border-radius:99px;background:{v_color};
                    width:{bar_w}%"></div></div>
        </div>""", unsafe_allow_html=True)
    with v2:
        if reasons:
            st.markdown("**✅ Bullish Signals**")
            for r in reasons: st.markdown(f"- {r}")
        if risks:
            st.markdown("**⚠️ Risk Factors**")
            for r in risks: st.markdown(f"- {r}")

    # ── News feed ────────────────────────────────────────────────────────
    st.markdown('<div class="sec"><div class="dot"></div><h3>Recent News</h3></div>', unsafe_allow_html=True)
    if articles:
        for a in articles:
            pill_cls = "pp" if a["sentiment"]=="positive" else ("np" if a["sentiment"]=="negative" else "neup")
            pill_txt = a["sentiment"].upper()
            score_txt = f"{a['score']:+.2f}"
            st.markdown(f"""
            <div class="news-item">
                <div class="ntitle">{a['title']}</div>
                <div class="nmeta">
                    <span class="pill {pill_cls}">{pill_txt}</span>
                    <span>Score: {score_txt}</span>
                    <span>📅 {a['published']}</span>
                </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("📭 No recent news found. Try again in a moment.")

if __name__ == "__main__":
    main()

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="E-Commerce Profit Calculator",
    page_icon="📦",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Currency exchange rates (base: USD)
CURRENCY_RATES = {
    "USD": 1.0, "EUR": 0.92, "GBP": 0.79, "INR": 83.12, "JPY": 149.50,
    "CNY": 7.24, "AUD": 1.52, "CAD": 1.36, "SGD": 1.34, "AED": 3.67
}

# Courier services
COURIER_SERVICES = {
    "India Post": {"rate": 2.5, "desc": "Most budget-friendly"},
    "EMS": {"rate": 8.0, "desc": "Postal express service"},
    "Aramex": {"rate": 10.0, "desc": "Middle East & Asia"},
    "UPS Worldwide": {"rate": 13.8, "desc": "Global network"},
    "FedEx International": {"rate": 14.5, "desc": "Reliable delivery"},
    "DHL Express": {"rate": 15.0, "desc": "Fastest shipping"}
}

def convert_currency(amount, from_curr, to_curr="USD"):
    if from_curr == to_curr:
        return amount
    return (amount / CURRENCY_RATES[from_curr]) * CURRENCY_RATES[to_curr]

def calculate_shipping(weight_kg, courier):
    rate = COURIER_SERVICES[courier]["rate"]
    if weight_kg <= 1:
        return rate * weight_kg
    elif weight_kg <= 5:
        return rate * weight_kg * 1.1
    elif weight_kg <= 10:
        return rate * weight_kg * 1.2
    return rate * weight_kg * 1.3

# Header
st.markdown('<div class="main-header">📦 E-Commerce Profit Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Calculate profits with multi-currency, shipping, and percentage-based customs duties</div>', unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    # Product Information
    st.markdown("### 📋 Product Information")
    
    prod_curr = st.selectbox("💱 Product Currency", list(CURRENCY_RATES.keys()), index=3)
    prod_price = st.number_input(f"💰 Base Product Price ({prod_curr})", min_value=0.0, value=100.0, step=10.0)
    
    st.markdown("**Weight**")
    weight_cols = st.columns([1, 2])
    with weight_cols[0]:
        weight_unit = st.radio("Unit", ["kg", "g"], horizontal=True, label_visibility="collapsed")
    with weight_cols[1]:
        weight_val = st.number_input(
            "Weight value", 
            min_value=0.0, 
            value=500.0 if weight_unit == "g" else 0.5, 
            step=10.0 if weight_unit == "g" else 0.1,
            label_visibility="collapsed"
        )
    
    weight_kg = weight_val / 1000 if weight_unit == "g" else weight_val
    
    st.markdown("---")
    
    # Shipping
    st.markdown("### 🚚 Shipping Details")
    courier = st.selectbox("📦 Courier Service", list(COURIER_SERVICES.keys()))
    st.caption(f"💡 {COURIER_SERVICES[courier]['desc']}")

with col2:
    # Tariffs
    st.markdown("### 🌍 Customs Duties & Tariffs")
    st.info("💡 Tariffs are **percentage (%)** of product base price")
    
    num_legs = st.number_input("🔢 Number of Transit Legs", min_value=1, max_value=10, value=1, step=1)
    
    tariff_legs = []
    prod_price_usd = convert_currency(prod_price, prod_curr)
    total_tariffs_usd = 0
    
    for i in range(num_legs):
        with st.expander(f"**Leg {i+1}** Details", expanded=True):
            tc1, tc2 = st.columns(2)
            with tc1:
                from_country = st.text_input("From", value=f"Country {chr(65+i)}", key=f"from_{i}", label_visibility="collapsed", placeholder="From Country")
            with tc2:
                to_country = st.text_input("To", value=f"Country {chr(66+i)}", key=f"to_{i}", label_visibility="collapsed", placeholder="To Country")
            
            tariff_pct = st.slider(
                f"Tariff Rate (%)", 
                min_value=0.0, 
                max_value=100.0, 
                value=10.0, 
                step=0.5,
                key=f"tariff_{i}"
            )
            
            tariff_amt = prod_price_usd * (tariff_pct / 100)
            total_tariffs_usd += tariff_amt
            
            st.caption(f"💵 {from_country} → {to_country}: **${tariff_amt:.2f}** ({tariff_pct}% of ${prod_price_usd:.2f})")
            
            tariff_legs.append({
                "from": from_country,
                "to": to_country,
                "pct": tariff_pct,
                "amt_usd": tariff_amt
            })
    
    st.markdown("---")
    
    # Selling Price
    st.markdown("### 💵 Selling Price")
    sell_curr = st.selectbox("💱 Selling Currency", list(CURRENCY_RATES.keys()), index=3)
    sell_price = st.number_input(f"💰 Your Selling Price ({sell_curr})", min_value=0.0, value=200.0, step=10.0)

# Calculations
st.markdown("---")
st.markdown("## 📊 Profit/Loss Analysis")

shipping_usd = calculate_shipping(weight_kg, courier)
sell_price_usd = convert_currency(sell_price, sell_curr)
total_cost = prod_price_usd + shipping_usd + total_tariffs_usd
profit = sell_price_usd - total_cost
margin_pct = (profit / sell_price_usd * 100) if sell_price_usd > 0 else 0

# Results
res_cols = st.columns(4)

with res_cols[0]:
    st.metric(
        "💸 Total Cost",
        f"${total_cost:.2f}",
        help="Product + Shipping + Tariffs"
    )
    st.caption(f"Product: ${prod_price_usd:.2f}")
    st.caption(f"Shipping: ${shipping_usd:.2f}")
    st.caption(f"Tariffs: ${total_tariffs_usd:.2f}")

with res_cols[1]:
    st.metric(
        "💰 Selling Price",
        f"${sell_price_usd:.2f}",
        help=f"{sell_price:.2f} {sell_curr}"
    )

with res_cols[2]:
    st.metric(
        "📈 Profit/Loss",
        f"${profit:.2f}",
        delta=f"{margin_pct:.1f}%",
        delta_color="normal" if profit >= 0 else "inverse"
    )

with res_cols[3]:
    margin_status = "🟢 Healthy" if margin_pct >= 20 else "🟡 Moderate" if margin_pct >= 10 else "🔴 Low"
    st.metric(
        "📊 Profit Margin",
        f"{margin_pct:.1f}%",
        help=margin_status
    )
    st.caption(margin_status)

# Detailed breakdown
st.markdown("---")
with st.expander("📋 **Detailed Cost Breakdown**"):
    st.markdown("#### 🌍 Tariff Route")
    for i, leg in enumerate(tariff_legs):
        st.write(f"**Leg {i+1}:** {leg['from']} → {leg['to']} | {leg['pct']}% = ${leg['amt_usd']:.2f}")
    
    st.markdown("#### 💵 Cost Summary (USD)")
    st.write(f"• Base Product: **${prod_price_usd:.2f}**")
    st.write(f"• Shipping ({courier}): **${shipping_usd:.2f}**")
    st.write(f"• Total Tariffs: **${total_tariffs_usd:.2f}**")
    st.write(f"• **TOTAL COST: ${total_cost:.2f}**")
    st.write(f"• Selling Price: **${sell_price_usd:.2f}**")
    
    profit_color = "green" if profit >= 0 else "red"
    st.markdown(f"• **NET PROFIT/LOSS:** :{profit_color}[**${profit:.2f}** ({margin_pct:.1f}%)]")

# Insights
if margin_pct < 10:
    st.warning("⚠️ **Low Profit Margin** - Consider increasing your selling price or finding cheaper shipping/tariff routes")
elif margin_pct < 20:
    st.info("💡 **Moderate Margin** - You have room for optimization. Try negotiating better shipping rates or tariffs")
else:
    st.success("✅ **Healthy Profit Margin** - Great job! Your pricing is competitive")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #9ca3af; padding: 1rem;'>"
    "Built with Streamlit | 📦 E-Commerce Calculator v2.0"
    "</div>",
    unsafe_allow_html=True
)
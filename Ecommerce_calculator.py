import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="E-Commerce Profit Calculator",
    page_icon="📦",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stNumberInput input {
        font-size: 1.1rem;
        font-weight: 500;
    }
    .profit-positive {
        color: #10b981;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .profit-negative {
        color: #ef4444;
        font-weight: bold;
        font-size: 1.5rem;
    }
    h1 {
        color: #1f2937;
        font-weight: 700;
    }
    h3 {
        color: #374151;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .stSelectbox label, .stNumberInput label {
        font-weight: 600;
        color: #4b5563;
    }
    .exchange-rate-box {
        background: #f0f9ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Available currencies
AVAILABLE_CURRENCIES = ["INR", "USD", "EUR", "GBP", "JPY", "CNY", "AUD", "CAD", "SGD", "AED"]

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_exchange_rate(from_currency="INR", to_currency="USD"):
    """
    Fetch real-time exchange rate from INR to target currency
    Uses exchangerate-api.com (free tier: 1500 requests/month)
    """
    try:
        # Free API - no key required for basic usage
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            rate = data['rates'].get(to_currency, 1.0)
            last_update = data.get('date', 'Unknown')
            return rate, last_update, True
        else:
            return None, None, False
    except Exception as e:
        return None, None, False

# Fallback rates (in case API fails) - Base: INR
FALLBACK_RATES = {
    "INR": 1.0,
    "USD": 0.012,
    "EUR": 0.011,
    "GBP": 0.0095,
    "JPY": 1.80,
    "CNY": 0.087,
    "AUD": 0.018,
    "CAD": 0.016,
    "SGD": 0.016,
    "AED": 0.044
}

# Header
st.title("📦 E-Commerce Profit Calculator")
st.markdown("**Professional profit/loss calculator for e-commerce businesses**")
st.markdown("---")

# Currency Selection
st.markdown("### 💱 Currency")
currency = st.selectbox(
    "Select your currency (all calculations will use live exchange rates from INR)",
    AVAILABLE_CURRENCIES,
    index=0,  # Default to INR
    help="INR is the base currency. If you select another currency, live exchange rates will be fetched."
)

# Get exchange rate
if currency == "INR":
    exchange_rate = 1.0
    rate_status = "live"
    last_update = datetime.now().strftime("%Y-%m-%d")
else:
    exchange_rate, last_update, rate_status = get_exchange_rate("INR", currency)
    
    # Use fallback if API fails
    if not rate_status:
        exchange_rate = FALLBACK_RATES.get(currency, 1.0)
        rate_status = "fallback"
        last_update = "Offline"

# Display exchange rate info
if currency != "INR":
    st.markdown(f"""
    <div class="exchange-rate-box">
        <strong>💹 Exchange Rate:</strong> 1 INR = {exchange_rate:.6f} {currency}<br>
        <small>📅 Last updated: {last_update} | 
        {'✅ Live rate' if rate_status == 'live' else '⚠️ Using fallback rate (API unavailable)'}</small>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Refresh Exchange Rate"):
        st.cache_data.clear()
        st.rerun()

st.markdown("---")

# Product Base Price
st.markdown("### 💰 Base Product Price")
base_price = st.number_input(
    f"Enter base product cost ({currency})",
    min_value=0.0,
    value=100.0 if currency == "INR" else round(100.0 * exchange_rate, 2),
    step=10.0 if currency == "INR" else round(10.0 * exchange_rate, 2),
    format="%.2f"
)

# Convert to INR for internal calculations
base_price_inr = base_price / exchange_rate

# Delivery Charges
st.markdown("### 🚚 Delivery Charges")
delivery_charge = st.number_input(
    f"Enter shipping/delivery cost ({currency})",
    min_value=0.0,
    value=50.0 if currency == "INR" else round(50.0 * exchange_rate, 2),
    step=5.0 if currency == "INR" else round(5.0 * exchange_rate, 2),
    format="%.2f",
    help="Total cost to ship this product to the final destination"
)

# Convert to INR
delivery_charge_inr = delivery_charge / exchange_rate

# Custom Duties/Tariffs
st.markdown("### 🌍 Custom Duties & Tariffs")
st.info("💡 Enter tariff as **percentage (%)** of base product price")

num_legs = st.number_input(
    "Number of transit legs",
    min_value=1,
    max_value=10,
    value=1,
    step=1,
    help="Example: China → India → USA = 2 legs"
)

tariff_legs = []
total_tariff_amount = 0
total_tariff_amount_inr = 0

for i in range(num_legs):
    st.markdown(f"#### Leg {i+1}")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        from_country = st.text_input(
            "From",
            value=f"Country {chr(65+i)}",
            key=f"from_{i}"
        )
    
    with col2:
        to_country = st.text_input(
            "To",
            value=f"Country {chr(66+i)}",
            key=f"to_{i}"
        )
    
    with col3:
        tariff_pct = st.number_input(
            "Tariff %",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=0.5,
            format="%.2f",
            key=f"tariff_{i}"
        )
    
    # Calculate tariff amount in selected currency
    tariff_amount = base_price * (tariff_pct / 100)
    tariff_amount_inr = base_price_inr * (tariff_pct / 100)
    
    total_tariff_amount += tariff_amount
    total_tariff_amount_inr += tariff_amount_inr
    
    st.caption(f"💵 {from_country} → {to_country}: **{tariff_pct}%** = **{tariff_amount:.2f} {currency}** (₹{tariff_amount_inr:.2f})")
    
    tariff_legs.append({
        "from": from_country,
        "to": to_country,
        "percentage": tariff_pct,
        "amount": tariff_amount,
        "amount_inr": tariff_amount_inr
    })
    
    if i < num_legs - 1:
        st.markdown("---")

st.markdown("---")

# Selling Price
st.markdown("### 💵 Selling Price")
selling_price = st.number_input(
    f"Your selling price ({currency})",
    min_value=0.0,
    value=200.0 if currency == "INR" else round(200.0 * exchange_rate, 2),
    step=10.0 if currency == "INR" else round(10.0 * exchange_rate, 2),
    format="%.2f",
    help="The price at which you will sell this product"
)

# Convert to INR
selling_price_inr = selling_price / exchange_rate

st.markdown("---")
st.markdown("---")

# CALCULATIONS (All done in INR, then converted back to selected currency)
total_cost_inr = base_price_inr + delivery_charge_inr + total_tariff_amount_inr
profit_loss_inr = selling_price_inr - total_cost_inr
profit_loss_percentage = (profit_loss_inr / selling_price_inr * 100) if selling_price_inr > 0 else 0
profit_multiple = profit_loss_inr / base_price_inr if base_price_inr > 0 else 0

# Convert back to selected currency for display
total_cost = total_cost_inr * exchange_rate
profit_loss = profit_loss_inr * exchange_rate

# Results Section
st.markdown("## 📊 Profit/Loss Analysis")

# Main metrics in colored boxes
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="💸 Total Cost",
        value=f"{total_cost:.2f} {currency}",
        help="Base Price + Delivery + Tariffs"
    )
    if currency != "INR":
        st.caption(f"₹{total_cost_inr:.2f} INR")

with col2:
    st.metric(
        label="💰 Selling Price",
        value=f"{selling_price:.2f} {currency}"
    )
    if currency != "INR":
        st.caption(f"₹{selling_price_inr:.2f} INR")

with col3:
    profit_color = "normal" if profit_loss >= 0 else "inverse"
    st.metric(
        label="📈 Profit/Loss",
        value=f"{profit_loss:.2f} {currency}",
        delta=f"{profit_loss_percentage:.2f}%",
        delta_color=profit_color
    )
    if currency != "INR":
        st.caption(f"₹{profit_loss_inr:.2f} INR")

# Detailed breakdown
st.markdown("---")
st.markdown("### 📋 Detailed Breakdown")

breakdown_col1, breakdown_col2 = st.columns(2)

with breakdown_col1:
    st.markdown("**Cost Components:**")
    st.write(f"• Base Product Price: **{base_price:.2f} {currency}**")
    if currency != "INR":
        st.write(f"  (₹{base_price_inr:.2f} INR)")
    
    st.write(f"• Delivery Charges: **{delivery_charge:.2f} {currency}**")
    if currency != "INR":
        st.write(f"  (₹{delivery_charge_inr:.2f} INR)")
    
    st.write(f"• Total Custom Duties: **{total_tariff_amount:.2f} {currency}**")
    if currency != "INR":
        st.write(f"  (₹{total_tariff_amount_inr:.2f} INR)")
    
    st.markdown(f"**Total Cost: {total_cost:.2f} {currency}**")
    if currency != "INR":
        st.markdown(f"**(₹{total_cost_inr:.2f} INR)**")

with breakdown_col2:
    st.markdown("**Tariff Route:**")
    for i, leg in enumerate(tariff_legs):
        st.write(f"• Leg {i+1}: {leg['from']} → {leg['to']}")
        st.write(f"  {leg['percentage']}% = {leg['amount']:.2f} {currency}")
        if currency != "INR":
            st.write(f"  (₹{leg['amount_inr']:.2f} INR)")

# Profit Analysis
st.markdown("---")
st.markdown("### 💡 Profit Analysis")

analysis_col1, analysis_col2, analysis_col3 = st.columns(3)

with analysis_col1:
    profit_class = "profit-positive" if profit_loss >= 0 else "profit-negative"
    st.markdown(f"**Profit/Loss Amount:**")
    st.markdown(f"<div class='{profit_class}'>{profit_loss:+.2f} {currency}</div>", unsafe_allow_html=True)
    if currency != "INR":
        st.markdown(f"<div style='font-size: 0.9rem; color: #6b7280;'>₹{profit_loss_inr:+.2f} INR</div>", unsafe_allow_html=True)

with analysis_col2:
    st.markdown("**Profit/Loss Percentage:**")
    pct_class = "profit-positive" if profit_loss_percentage >= 0 else "profit-negative"
    st.markdown(f"<div class='{pct_class}'>{profit_loss_percentage:+.2f}%</div>", unsafe_allow_html=True)

with analysis_col3:
    st.markdown("**Profit Multiple:**")
    mult_class = "profit-positive" if profit_multiple >= 0 else "profit-negative"
    st.markdown(f"<div class='{mult_class}'>{profit_multiple:+.2f}x</div>", unsafe_allow_html=True)
    st.caption("(Profit as multiple of base price)")

# Formula explanation
with st.expander("📐 Calculation Formula"):
    st.markdown(f"""
    **All calculations are done in INR and converted to {currency} using live exchange rate:**
    
    **Exchange Rate:** 1 INR = {exchange_rate:.6f} {currency}
    
    ```
    Total Cost (INR) = Base Price + Delivery + Custom Duties
    Total Cost (INR) = ₹{base_price_inr:.2f} + ₹{delivery_charge_inr:.2f} + ₹{total_tariff_amount_inr:.2f}
    Total Cost (INR) = ₹{total_cost_inr:.2f}
    Total Cost ({currency}) = {total_cost:.2f} {currency}
    
    Profit/Loss (INR) = Selling Price - Total Cost
    Profit/Loss (INR) = ₹{selling_price_inr:.2f} - ₹{total_cost_inr:.2f}
    Profit/Loss (INR) = ₹{profit_loss_inr:.2f}
    Profit/Loss ({currency}) = {profit_loss:.2f} {currency}
    
    Profit Percentage = (Profit/Loss ÷ Selling Price) × 100
    Profit Percentage = (₹{profit_loss_inr:.2f} ÷ ₹{selling_price_inr:.2f}) × 100 = {profit_loss_percentage:.2f}%
    
    Profit Multiple = Profit/Loss ÷ Base Price
    Profit Multiple = ₹{profit_loss_inr:.2f} ÷ ₹{base_price_inr:.2f} = {profit_multiple:.2f}x
    ```
    """)

# Recommendations
st.markdown("---")
if profit_loss < 0:
    st.error(f"⚠️ **Loss Alert**: You're losing **{abs(profit_loss):.2f} {currency}** (₹{abs(profit_loss_inr):.2f}) per unit. Consider increasing your selling price or reducing costs.")
elif profit_loss_percentage < 10:
    st.warning(f"💡 **Low Margin**: Your profit margin is only **{profit_loss_percentage:.2f}%**. Consider optimizing your costs or pricing.")
elif profit_loss_percentage < 20:
    st.info(f"📊 **Moderate Margin**: Your profit margin is **{profit_loss_percentage:.2f}%**. Room for improvement!")
else:
    st.success(f"✅ **Healthy Margin**: Excellent! Your profit margin is **{profit_loss_percentage:.2f}%**")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #9ca3af; padding: 1rem;'>"
    "📦 E-Commerce Profit Calculator | Built with Streamlit<br>"
    "<small>Base Currency: INR | Live exchange rates powered by exchangerate-api.com</small>"
    "</div>",
    unsafe_allow_html=True
)
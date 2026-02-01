import streamlit as st

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
</style>
""", unsafe_allow_html=True)

# Currency exchange rates (base: USD)
CURRENCY_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "INR": 83.12,
    "JPY": 149.50,
    "CNY": 7.24,
    "AUD": 1.52,
    "CAD": 1.36,
    "SGD": 1.34,
    "AED": 3.67
}

# Header
st.title("📦 E-Commerce Profit Calculator")
st.markdown("**Professional profit/loss calculator for e-commerce businesses**")
st.markdown("---")

# Currency Selection
st.markdown("### 💱 Currency")
currency = st.selectbox(
    "Select your currency (applies to all fields)",
    list(CURRENCY_RATES.keys()),
    index=3,  # Default to INR
    help="This currency will be used for base price, selling price, and delivery charges"
)

st.markdown("---")

# Product Base Price
st.markdown("### 💰 Base Product Price")
base_price = st.number_input(
    f"Enter base product cost ({currency})",
    min_value=0.0,
    value=100.0,
    step=10.0,
    format="%.2f"
)

# Delivery Charges
st.markdown("### 🚚 Delivery Charges")
delivery_charge = st.number_input(
    f"Enter shipping/delivery cost ({currency})",
    min_value=0.0,
    value=50.0,
    step=5.0,
    format="%.2f",
    help="Total cost to ship this product to the final destination"
)

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
    total_tariff_amount += tariff_amount
    
    st.caption(f"💵 {from_country} → {to_country}: **{tariff_pct}%** = **{tariff_amount:.2f} {currency}**")
    
    tariff_legs.append({
        "from": from_country,
        "to": to_country,
        "percentage": tariff_pct,
        "amount": tariff_amount
    })
    
    if i < num_legs - 1:
        st.markdown("---")

st.markdown("---")

# Selling Price
st.markdown("### 💵 Selling Price")
selling_price = st.number_input(
    f"Your selling price ({currency})",
    min_value=0.0,
    value=200.0,
    step=10.0,
    format="%.2f",
    help="The price at which you will sell this product"
)

st.markdown("---")
st.markdown("---")

# CALCULATIONS
total_cost = base_price + delivery_charge + total_tariff_amount
profit_loss = selling_price - total_cost
profit_loss_percentage = (profit_loss / selling_price * 100) if selling_price > 0 else 0
profit_multiple = profit_loss / base_price if base_price > 0 else 0

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

with col2:
    st.metric(
        label="💰 Selling Price",
        value=f"{selling_price:.2f} {currency}"
    )

with col3:
    profit_color = "normal" if profit_loss >= 0 else "inverse"
    st.metric(
        label="📈 Profit/Loss",
        value=f"{profit_loss:.2f} {currency}",
        delta=f"{profit_loss_percentage:.2f}%",
        delta_color=profit_color
    )

# Detailed breakdown
st.markdown("---")
st.markdown("### 📋 Detailed Breakdown")

breakdown_col1, breakdown_col2 = st.columns(2)

with breakdown_col1:
    st.markdown("**Cost Components:**")
    st.write(f"• Base Product Price: **{base_price:.2f} {currency}**")
    st.write(f"• Delivery Charges: **{delivery_charge:.2f} {currency}**")
    st.write(f"• Total Custom Duties: **{total_tariff_amount:.2f} {currency}**")
    st.markdown(f"**Total Cost: {total_cost:.2f} {currency}**")

with breakdown_col2:
    st.markdown("**Tariff Route:**")
    for i, leg in enumerate(tariff_legs):
        st.write(f"• Leg {i+1}: {leg['from']} → {leg['to']}")
        st.write(f"  {leg['percentage']}% = {leg['amount']:.2f} {currency}")

# Profit Analysis
st.markdown("---")
st.markdown("### 💡 Profit Analysis")

analysis_col1, analysis_col2, analysis_col3 = st.columns(3)

with analysis_col1:
    profit_class = "profit-positive" if profit_loss >= 0 else "profit-negative"
    st.markdown(f"**Profit/Loss Amount:**")
    st.markdown(f"<div class='{profit_class}'>{profit_loss:+.2f} {currency}</div>", unsafe_allow_html=True)

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
    st.markdown("""
    **Profit/Loss Calculation:**
    
    ```
    Total Cost = Base Price + Delivery Charge + Custom Duties
    Total Cost = {:.2f} + {:.2f} + {:.2f} = {:.2f} {}
    
    Profit/Loss = Selling Price - Total Cost
    Profit/Loss = {:.2f} - {:.2f} = {:.2f} {}
    
    Profit Percentage = (Profit/Loss ÷ Selling Price) × 100
    Profit Percentage = ({:.2f} ÷ {:.2f}) × 100 = {:.2f}%
    
    Profit Multiple = Profit/Loss ÷ Base Price
    Profit Multiple = {:.2f} ÷ {:.2f} = {:.2f}x
    ```
    """.format(
        base_price, delivery_charge, total_tariff_amount, total_cost, currency,
        selling_price, total_cost, profit_loss, currency,
        profit_loss, selling_price, profit_loss_percentage,
        profit_loss, base_price, profit_multiple
    ))

# Recommendations
st.markdown("---")
if profit_loss < 0:
    st.error(f"⚠️ **Loss Alert**: You're losing **{abs(profit_loss):.2f} {currency}** per unit. Consider increasing your selling price or reducing costs.")
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
    "📦 E-Commerce Profit Calculator | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)
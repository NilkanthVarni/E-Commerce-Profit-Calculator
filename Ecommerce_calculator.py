import streamlit as st
import anthropic
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="E-Commerce Profit Calculator",
    page_icon="📦",
    layout="wide"
)

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

# Courier services with base rates (per kg in USD)
COURIER_SERVICES = {
    "India Post": {
        "base_rate": 2.5,
        "description": "Most budget-friendly option"
    },
    "DHL Express": {
        "base_rate": 15.0,
        "description": "Fast international shipping"
    },
    "FedEx International": {
        "base_rate": 14.5,
        "description": "Reliable worldwide delivery"
    },
    "UPS Worldwide": {
        "base_rate": 13.8,
        "description": "Global shipping network"
    },
    "Aramex": {
        "base_rate": 10.0,
        "description": "Middle East & Asia specialist"
    },
    "TNT Express": {
        "base_rate": 12.5,
        "description": "European coverage"
    },
    "EMS (Express Mail Service)": {
        "base_rate": 8.0,
        "description": "Postal express service"
    }
}

def convert_currency(amount, from_currency, to_currency="USD"):
    """Convert amount from one currency to another via USD"""
    if from_currency == to_currency:
        return amount
    usd_amount = amount / CURRENCY_RATES[from_currency]
    return usd_amount * CURRENCY_RATES[to_currency]

def calculate_shipping_cost(weight_kg, courier_service):
    """Calculate shipping cost based on weight and courier"""
    base_rate = COURIER_SERVICES[courier_service]["base_rate"]
    # Progressive pricing: higher rates for heavier items
    if weight_kg <= 1:
        return base_rate * weight_kg
    elif weight_kg <= 5:
        return base_rate * weight_kg * 1.1
    elif weight_kg <= 10:
        return base_rate * weight_kg * 1.2
    else:
        return base_rate * weight_kg * 1.3

def get_ai_pricing_suggestion(product_cost, shipping_cost, total_tariffs, current_price, api_key):
    """Get AI-powered pricing suggestions using Claude"""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        total_cost = product_cost + shipping_cost + total_tariffs
        profit_margin = ((current_price - total_cost) / current_price * 100) if current_price > 0 else 0
        
        prompt = f"""You are an e-commerce pricing expert. Analyze this product's cost structure and provide pricing recommendations.

Product Cost Breakdown:
- Base Product Cost: ${product_cost:.2f}
- Shipping Cost: ${shipping_cost:.2f}
- Total Tariffs/Duties: ${total_tariffs:.2f}
- Total Cost: ${total_cost:.2f}
- Current Selling Price: ${current_price:.2f}
- Current Profit Margin: {profit_margin:.2f}%

Please provide:
1. Recommended selling price range (with reasoning)
2. Optimal profit margin for this product category
3. Competitive positioning advice
4. Risk assessment of current pricing

Keep your response concise and actionable."""

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    except Exception as e:
        return f"Error getting AI suggestion: {str(e)}\n\nPlease check your API key in the sidebar."

# Main App
st.title("📦 E-Commerce Profit Calculator")
st.markdown("**Calculate profits with multi-currency, shipping, and tariff support + AI pricing recommendations**")

# Sidebar for API Key
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Anthropic API Key", type="password", help="Get your free API key from https://console.anthropic.com/")
    st.markdown("---")
    st.markdown("### 📚 Quick Guide")
    st.markdown("""
    1. Enter product details
    2. Add shipping info
    3. Configure tariffs (multi-leg)
    4. View profit/loss analysis
    5. Get AI pricing suggestions
    """)
    st.markdown("---")
    st.markdown("💡 **Tip**: India Post offers the most budget-friendly rates!")

# Create tabs
tab1, tab2 = st.tabs(["💰 Calculator", "🤖 AI Recommendations"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Product Information")
        
        # Product base price
        product_currency = st.selectbox("Currency", list(CURRENCY_RATES.keys()), key="product_currency")
        product_price = st.number_input(f"Base Product Price ({product_currency})", min_value=0.0, value=100.0, step=1.0)
        
        # Weight
        weight_unit = st.radio("Weight Unit", ["Grams", "Kilograms"], horizontal=True)
        weight_value = st.number_input(f"Product Weight ({weight_unit})", min_value=0.0, value=500.0 if weight_unit == "Grams" else 0.5, step=1.0 if weight_unit == "Grams" else 0.1)
        
        # Convert to kg for calculations
        weight_kg = weight_value / 1000 if weight_unit == "Grams" else weight_value
        
        st.subheader("🚚 Shipping Details")
        courier = st.selectbox(
            "Courier Service",
            list(COURIER_SERVICES.keys()),
            help="India Post is the most budget-friendly option"
        )
        st.caption(f"📝 {COURIER_SERVICES[courier]['description']}")
        
    with col2:
        st.subheader("🌍 Tariffs & Duties (Multi-Leg)")
        
        num_legs = st.number_input("Number of Transit Legs", min_value=1, max_value=10, value=1, step=1, help="E.g., China → India → USA = 2 legs")
        
        tariff_legs = []
        total_tariffs_usd = 0
        
        for i in range(num_legs):
            with st.expander(f"Leg {i+1} Tariff", expanded=(i==0)):
                col_a, col_b = st.columns(2)
                with col_a:
                    from_country = st.text_input(f"From (Leg {i+1})", value="Country A" if i == 0 else f"Country {chr(66+i)}", key=f"from_{i}")
                    tariff_currency = st.selectbox(f"Currency (Leg {i+1})", list(CURRENCY_RATES.keys()), key=f"currency_{i}")
                with col_b:
                    to_country = st.text_input(f"To (Leg {i+1})", value=f"Country {chr(66+i)}", key=f"to_{i}")
                    tariff_amount = st.number_input(f"Tariff Amount ({tariff_currency})", min_value=0.0, value=10.0, step=1.0, key=f"tariff_{i}")
                
                tariff_usd = convert_currency(tariff_amount, tariff_currency, "USD")
                total_tariffs_usd += tariff_usd
                
                tariff_legs.append({
                    "from": from_country,
                    "to": to_country,
                    "amount": tariff_amount,
                    "currency": tariff_currency,
                    "amount_usd": tariff_usd
                })
        
        st.subheader("💵 Selling Price")
        selling_currency = st.selectbox("Selling Currency", list(CURRENCY_RATES.keys()), key="selling_currency")
        selling_price = st.number_input(f"Your Selling Price ({selling_currency})", min_value=0.0, value=200.0, step=1.0)

    # Calculations
    st.markdown("---")
    st.subheader("📊 Profit/Loss Analysis")
    
    # Convert everything to USD for calculation
    product_price_usd = convert_currency(product_price, product_currency, "USD")
    shipping_cost_usd = calculate_shipping_cost(weight_kg, courier)
    selling_price_usd = convert_currency(selling_price, selling_currency, "USD")
    
    total_cost_usd = product_price_usd + shipping_cost_usd + total_tariffs_usd
    profit_loss_usd = selling_price_usd - total_cost_usd
    profit_loss_percentage = (profit_loss_usd / selling_price_usd * 100) if selling_price_usd > 0 else 0
    
    # Display results
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cost (USD)", f"${total_cost_usd:.2f}")
        st.caption(f"Product: ${product_price_usd:.2f}")
        st.caption(f"Shipping: ${shipping_cost_usd:.2f}")
        st.caption(f"Tariffs: ${total_tariffs_usd:.2f}")
    
    with col2:
        st.metric("Selling Price (USD)", f"${selling_price_usd:.2f}")
        st.caption(f"Original: {selling_price:.2f} {selling_currency}")
    
    with col3:
        profit_color = "normal" if profit_loss_usd >= 0 else "inverse"
        st.metric("Profit/Loss", f"${profit_loss_usd:.2f}", delta=f"{profit_loss_percentage:.1f}%", delta_color=profit_color)
    
    with col4:
        margin_color = "🟢" if profit_loss_percentage >= 20 else "🟡" if profit_loss_percentage >= 10 else "🔴"
        st.metric("Profit Margin", f"{profit_loss_percentage:.1f}%")
        st.caption(f"{margin_color} Margin Status")
    
    # Detailed breakdown
    with st.expander("📋 Detailed Cost Breakdown"):
        st.write("**Tariff Route:**")
        for i, leg in enumerate(tariff_legs):
            st.write(f"Leg {i+1}: {leg['from']} → {leg['to']}: {leg['amount']:.2f} {leg['currency']} (${leg['amount_usd']:.2f} USD)")
        
        st.write("\n**Summary in USD:**")
        st.write(f"- Base Product Cost: ${product_price_usd:.2f}")
        st.write(f"- Shipping Cost ({courier}): ${shipping_cost_usd:.2f}")
        st.write(f"- Total Tariffs: ${total_tariffs_usd:.2f}")
        st.write(f"- **Total Cost: ${total_cost_usd:.2f}**")
        st.write(f"- Selling Price: ${selling_price_usd:.2f}")
        st.write(f"- **Net Profit/Loss: ${profit_loss_usd:.2f} ({profit_loss_percentage:.1f}%)**")

with tab2:
    st.subheader("🤖 AI-Powered Pricing Recommendations")
    
    if not api_key:
        st.warning("⚠️ Please enter your Anthropic API Key in the sidebar to use AI recommendations.")
        st.info("""
        **How to get your API key:**
        1. Visit https://console.anthropic.com/
        2. Sign up for a free account (get $5 free credit)
        3. Go to API Keys section
        4. Create a new key and paste it in the sidebar
        """)
    else:
        if st.button("🎯 Get AI Pricing Suggestion", type="primary"):
            with st.spinner("Analyzing your product pricing..."):
                suggestion = get_ai_pricing_suggestion(
                    product_price_usd,
                    shipping_cost_usd,
                    total_tariffs_usd,
                    selling_price_usd,
                    api_key
                )
                
                st.markdown("### 💡 AI Recommendation")
                st.markdown(suggestion)
                
                # Additional insights
                st.markdown("---")
                st.markdown("### 📈 Current Status")
                col1, col2 = st.columns(2)
                with col1:
                    if profit_loss_percentage < 10:
                        st.error("⚠️ Low profit margin - consider repricing")
                    elif profit_loss_percentage < 20:
                        st.warning("⚡ Moderate margin - room for optimization")
                    else:
                        st.success("✅ Healthy profit margin")
                
                with col2:
                    markup = ((selling_price_usd - product_price_usd) / product_price_usd * 100) if product_price_usd > 0 else 0
                    st.info(f"📊 Current Markup: {markup:.1f}%")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with Streamlit | Powered by Claude AI | 📦 E-Commerce Calculator v1.0</p>
</div>
""", unsafe_allow_html=True)

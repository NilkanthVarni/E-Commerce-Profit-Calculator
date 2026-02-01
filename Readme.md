# 📦 E-Commerce Profit Calculator

A powerful Streamlit web app for calculating e-commerce profits with multi-currency support, multiple courier options, and percentage-based multi-leg tariff calculations.

## ✨ Features

- **Multi-Currency Support**: Calculate costs in 10+ major currencies (USD, EUR, GBP, INR, JPY, CNY, AUD, CAD, SGD, AED)
- **Flexible Weight Units**: Input weight in grams or kilograms
- **7 Courier Services**: Including India Post (most budget-friendly), DHL, FedEx, UPS, Aramex, TNT, and EMS
- **Percentage-Based Tariffs**: Real-world customs duty calculations based on product value
- **Multi-Leg Tariff Calculation**: Handle complex shipping routes (e.g., China → India → USA)
- **Real-Time Profit/Loss Analysis**: Instant calculations with visual metrics
- **Clean, Modern UI**: Built with Streamlit for a professional look

## 🚀 Quick Start (Local Testing)

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the app:**
```bash
streamlit run ecommerce_calculator.py
```

3. **Open in browser:** The app will automatically open at `http://localhost:8501`

## 🌐 Deploy to Streamlit Cloud (FREE!)

### Step 1: Prepare Your Repository

1. Create a new GitHub repository
2. Upload these files:
   - `ecommerce_calculator.py`
   - `requirements.txt`
   - `README.md` (this file)

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch (main), and main file (`ecommerce_calculator.py`)
5. Click "Deploy"
6. Wait 2-3 minutes for deployment

That's it! Your calculator is now live and accessible to anyone! 🎉

## 📖 How to Use

### Basic Calculation

1. **Product Information**:
   - Select your currency
   - Enter base product price
   - Choose weight unit (grams/kg) and enter weight

2. **Shipping Details**:
   - Select courier service
   - India Post recommended for budget-friendly shipping

3. **Tariffs & Duties** (Percentage-Based):
   - Set number of transit legs (e.g., 2 for China → India → USA)
   - For each leg, enter:
     - From country
     - To country
     - Tariff percentage (% of product base price)
   - Example: If product costs $100 and tariff is 15%, duty = $15

4. **Selling Price**:
   - Enter your intended selling price and currency

5. **View Results**:
   - Total cost breakdown
   - Profit/loss amount and percentage
   - Profit margin status (color-coded)

### Understanding Percentage-Based Tariffs

**Real-world example:**
- **Product**: Smartphone at ¥500 CNY (~$69 USD)
- **Route**: China → India → USA
  - China to India: 18% tariff = $12.42
  - India to USA: 25% tariff = $17.25
- **Total Tariffs**: $29.67

This reflects how actual customs duties work - they're calculated as a percentage of the product value, not fixed amounts.

## 💰 Courier Services Comparison

| Courier | Best For | Relative Cost |
|---------|----------|---------------|
| India Post | Budget-conscious shipping | 💰 (Cheapest) |
| EMS | Balanced speed & cost | 💰💰 |
| Aramex | Middle East & Asia | 💰💰💰 |
| UPS | Global reliability | 💰💰💰💰 |
| TNT | European markets | 💰💰💰💰 |
| FedEx | Premium service | 💰💰💰💰 |
| DHL | Fastest delivery | 💰💰💰💰💰 |

## 🔧 Configuration

### Currency Exchange Rates

The app uses real-world approximate rates (base: USD). Rates are embedded in the code and can be updated in `CURRENCY_RATES` dictionary.

### Courier Pricing

Courier costs are calculated per kg with progressive pricing:
- 0-1 kg: Base rate
- 1-5 kg: Base rate × 1.1
- 5-10 kg: Base rate × 1.2
- 10+ kg: Base rate × 1.3

### Tariff Calculations

Tariffs are calculated as **percentages of the product base price**:
- Each leg's tariff = Product Price × (Tariff % / 100)
- All tariffs are converted to USD for total cost calculation
- Reflects real-world customs duty practices

## 🎯 Example Use Case

**Scenario**: You're selling electronics from China to USA via India

- **Product**: Smartphone
- **Base Price**: ¥500 CNY (~$69 USD)
- **Weight**: 200 grams
- **Route**: 
  - China → India (18% tariff = $12.42)
  - India → USA (25% tariff = $17.25)
- **Courier**: India Post ($0.55 for 0.2kg)
- **Total Cost**: $69 + $0.55 + $29.67 = $99.22
- **Selling Price**: $150 USD
- **Profit**: $50.78 (33.9% margin)

## 📱 Browser Compatibility

Works on all modern browsers:
- Chrome
- Firefox
- Safari
- Edge

Mobile-responsive design works great on phones and tablets!

## 🔐 Privacy & Security

- No external API calls required
- All calculations happen locally in your browser
- No data is saved or transmitted to third parties
- Streamlit Cloud hosting is secure and HTTPS-enabled

## 📄 License

Free to use and modify for personal and commercial purposes.

## 🆘 Support

Having issues? Check:
1. All required fields are filled
2. Tariff percentages are entered correctly (0-100%)
3. Browser is up to date

## 🌟 Future Enhancements

Planned features:
- Historical profit tracking
- Bulk product calculations
- Export results to CSV/Excel
- Custom courier rate configuration
- Real-time currency rate updates via API
- Multi-language support
- Save/load product configurations

## 💡 Common Tariff Rates by Country

Here are some typical customs duty rates to help you get started:

- **USA**: 0-25% (varies by product category)
- **India**: 10-100% (electronics typically 18-25%)
- **China**: 0-35%
- **EU**: 0-17%
- **UK**: 0-12%
- **Australia**: 5-10%

*Note: Rates vary by product type and trade agreements. Check official customs websites for accurate rates.*

---

**Built with ❤️ using Streamlit**

Enjoy calculating your profits! 📈
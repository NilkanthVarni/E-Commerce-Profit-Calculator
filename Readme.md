# 📦 E-Commerce Profit Calculator

A powerful Streamlit web app for calculating e-commerce profits with multi-currency support, multiple courier options, multi-leg tariff calculations, and AI-powered pricing recommendations.

## ✨ Features

- **Multi-Currency Support**: Calculate costs in 10+ major currencies (USD, EUR, GBP, INR, JPY, CNY, AUD, CAD, SGD, AED)
- **Flexible Weight Units**: Input weight in grams or kilograms
- **7 Courier Services**: Including India Post (most budget-friendly), DHL, FedEx, UPS, Aramex, TNT, and EMS
- **Multi-Leg Tariff Calculation**: Handle complex shipping routes (e.g., China → India → USA)
- **Real-Time Profit/Loss Analysis**: Instant calculations with visual metrics
- **AI Pricing Recommendations**: Claude AI suggests optimal pricing based on your costs
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

### Step 3: Get Your Anthropic API Key

1. Visit [console.anthropic.com](https://console.anthropic.com/)
2. Sign up for a free account (includes $5 free credit)
3. Navigate to "API Keys"
4. Create a new key
5. Copy the key and paste it in the app's sidebar

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

3. **Tariffs & Duties**:
   - Set number of transit legs (e.g., 2 for China → India → USA)
   - For each leg, enter:
     - From country
     - To country
     - Tariff amount and currency

4. **Selling Price**:
   - Enter your intended selling price and currency

5. **View Results**:
   - Total cost breakdown
   - Profit/loss amount and percentage
   - Profit margin status (color-coded)

### AI Recommendations

1. Go to "AI Recommendations" tab
2. Click "Get AI Pricing Suggestion"
3. Receive personalized advice on:
   - Recommended selling price range
   - Optimal profit margins
   - Competitive positioning
   - Risk assessment

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

## 🎯 Example Use Case

**Scenario**: You're selling electronics from China to USA via India

- **Product**: Smartphone
- **Base Price**: ¥500 CNY
- **Weight**: 200 grams
- **Route**: China → India (₹800 tariff) → USA ($50 tariff)
- **Courier**: India Post
- **Selling Price**: $150 USD

The calculator will:
1. Convert all currencies to USD
2. Calculate shipping (India Post, 0.2 kg)
3. Add multi-leg tariffs
4. Show your profit/loss and margin
5. AI suggests optimal pricing

## 🤖 About AI Integration

The app uses Claude Sonnet 4 for intelligent pricing recommendations. Claude analyzes:
- Your cost structure
- Current profit margins
- Market positioning
- Competitive factors

All processing happens securely via Anthropic's API.

## 📱 Browser Compatibility

Works on all modern browsers:
- Chrome
- Firefox
- Safari
- Edge

Mobile-responsive design works great on phones and tablets!

## 🔐 Privacy & Security

- Your API key is only stored in your browser session
- No data is saved or transmitted to third parties
- All calculations happen in real-time
- Streamlit Cloud hosting is secure and HTTPS-enabled

## 📄 License

Free to use and modify for personal and commercial purposes.

## 🆘 Support

Having issues? Check:
1. API key is correctly entered
2. All required fields are filled
3. Browser is up to date

## 🌟 Future Enhancements

Planned features:
- Historical profit tracking
- Bulk product calculations
- Export results to CSV/Excel
- Custom courier rate configuration
- Real-time currency rate updates via API
- Multi-language support

---

**Built with ❤️ using Streamlit and Claude AI**

Enjoy calculating your profits! 📈

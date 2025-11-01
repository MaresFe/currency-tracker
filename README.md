# 💱 Currency Exchange Rate Tracker

A real-time currency exchange rate tracker with a modern GUI that displays live exchange rates, performs currency conversions, and exports data to Excel.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **Real-Time Exchange Rates**: Get live currency exchange rates from reliable API
- **12+ Currencies**: Track USD, EUR, GBP, JPY, CHF, CAD, AUD, CNY, TRY, INR, BRL, MXN, ZAR
- **Currency Converter**: Convert any amount between supported currencies
- **Auto-Refresh**: Automatic updates every 60 seconds (optional)
- **Excel Export**: Save exchange rates and history to Excel files
- **Modern GUI**: Clean and intuitive interface
- **Multiple Base Currencies**: Choose from USD, EUR, GBP, JPY, CHF, TRY
- **Free API**: Uses frankfurter.app - no API key required

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Internet connection

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/currency-tracker.git
cd currency-tracker
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

### Usage

1. Run the application:
```bash
python currency_tracker.py
```

2. Click "Refresh Rates" to get current exchange rates

3. Use the currency converter to convert between currencies

4. Enable "Auto-refresh" for automatic updates every 60 seconds

5. Export data to Excel using "Export to Excel" button

## 📊 Supported Currencies

- **EUR** - Euro
- **GBP** - British Pound
- **JPY** - Japanese Yen
- **CHF** - Swiss Franc
- **CAD** - Canadian Dollar
- **AUD** - Australian Dollar
- **CNY** - Chinese Yuan
- **TRY** - Turkish Lira
- **INR** - Indian Rupee
- **BRL** - Brazilian Real
- **MXN** - Mexican Peso
- **ZAR** - South African Rand

## 🛠️ Technical Details

### Libraries Used

- **requests**: HTTP requests to fetch exchange rates
- **tkinter**: GUI framework (built-in with Python)
- **pandas**: Data manipulation and Excel export
- **openpyxl**: Excel file creation

### API

This project uses the **Frankfurter API** (frankfurter.app), which is:
- ✅ Free to use
- ✅ No API key required
- ✅ No rate limits
- ✅ Reliable and up-to-date
- ✅ European Central Bank data

API Endpoint: `https://api.frankfurter.app/latest`

### How It Works

1. User selects base currency (default: USD)
2. Application sends GET request to Frankfurter API
3. API returns current exchange rates for all currencies
4. Data is displayed in the GUI table
5. User can convert currencies using the converter
6. Optional: Auto-refresh fetches new data every 60 seconds
7. All fetched data can be exported to Excel

## 📋 Features Explained

### Main Display
- Shows exchange rates for 12 popular currencies
- Rates are updated in real-time when refreshed
- Clean table format with currency names and rates

### Base Currency Selection
- Choose which currency to use as base
- Options: USD, EUR, GBP, JPY, CHF, TRY
- All other rates will be relative to your selected base

### Currency Converter
- Enter any amount
- Select source currency
- Select target currency
- Click "Convert" to see the result

### Auto-Refresh
- Enable to automatically update rates every 60 seconds
- Disable when you don't need continuous updates
- Saves bandwidth and API calls

### Excel Export
- Exports current rates to Excel
- Includes historical data (all refreshes in current session)
- Two sheets: "Current Rates" and "History"
- Filename includes timestamp

## 🔧 Customization

### Adding More Currencies

To add more currencies to the display, edit the `display_currencies` list in the `CurrencyTrackerGUI` class:

```python
self.display_currencies = ['EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD', 
                           'CNY', 'TRY', 'INR', 'BRL', 'MXN', 'ZAR',
                           'SEK', 'NOK', 'DKK']  # Add more here
```

### Changing Auto-Refresh Interval

To change the auto-refresh interval (default: 60 seconds), modify this line in `schedule_refresh()`:

```python
self.refresh_job = self.root.after(60000, self.schedule_refresh)  # 60000 = 60 seconds
```

### Currency Name Customization

To add or modify currency display names, edit the `currency_names` dictionary in `update_rates_display()`:

```python
currency_names = {
    'EUR': 'Euro (EUR)',
    'GBP': 'British Pound (GBP)',
    # Add more here
}
```

## 📸 Screenshots

### Main Interface
- Real-time exchange rates display
- Currency converter
- Status bar with last update time

### Excel Export
- Current rates and historical data
- Clean spreadsheet format
- Ready for analysis

## 🐛 Troubleshooting

**Problem**: "Network error"
- Check internet connection
- Verify firewall settings
- Try again in a few moments

**Problem**: "No rates to export"
- Click "Refresh Rates" first
- Wait for rates to load
- Then try exporting

**Problem**: Installation errors
- Ensure Python 3.8+ is installed
- Update pip: `pip install --upgrade pip`
- Install packages individually if needed

## 📝 Future Enhancements

- [ ] Historical charts and graphs
- [ ] Price alerts and notifications
- [ ] Multiple base currency comparison
- [ ] Cryptocurrency support
- [ ] Favorites/watchlist feature
- [ ] Dark mode
- [ ] Mobile responsive design
- [ ] API rate optimization

## ⚖️ API Usage & Limits

The Frankfurter API is free and has no strict rate limits, but please:
- Use auto-refresh responsibly (60s default is recommended)
- Don't make excessive requests
- Cache data when appropriate
- Be respectful of the free service

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new features
- Improve the UI/UX
- Add more currencies
- Fix bugs
- Improve documentation

## 📜 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Exchange rate data provided by **Frankfurter API**
- Data sourced from European Central Bank
- Built with Python and Tkinter

## 👤 Author

Yakamoz Demir
- GitHub: [@MaresFe](https://github.com/MaresFe)

---

⭐ If you find this project useful, please consider giving it a star!

## 💡 Use Cases

- **Travelers**: Check exchange rates before trips
- **Forex Traders**: Monitor currency movements
- **Online Shoppers**: Convert prices to your currency
- **Students**: Learn about foreign exchange markets
- **Businesses**: Track international currency rates
- **Personal Finance**: Manage multi-currency accounts

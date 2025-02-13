# Stock Market Dashboard

## Overview
The **Stock Market Dashboard** is a Tkinter-based desktop application that allows users to track live stock prices, manage their investment portfolio, and analyze stock performance. The application integrates with the **Yahoo Finance API** to fetch real-time stock data and stores portfolio information in an SQLite database.

## Features
- **Live Stock Updates:** Track real-time stock prices by entering a stock ticker.
- **Portfolio Management:** Add stocks to your portfolio with quantity and purchase price.
- **Database Storage:** Portfolio and stock history data are stored in an SQLite database.
- **Graphical Analysis:** Future enhancements include candlestick charts for stock visualization.
- **Stock News Sentiment Analysis (Planned):** Analyzing stock-related news for sentiment.

## Dependencies
Ensure you have the following dependencies installed before running the application:
```sh
pip install tkinter yfinance mplfinance sqlite3 pandas matplotlib textblob
```

## Installation & Setup
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-repo/stock-dashboard.git
   cd stock-dashboard
   ```
2. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the Application:**
   ```sh
   python stock_dashboard.py
   ```

## Database Setup
The application automatically sets up an SQLite database (`stocks.db`) on the first run. It includes:
- `portfolio`: Stores stock ticker, quantity, purchase price, and timestamp.
- `stock_history`: Logs historical stock price data.

## Usage Guide
- **Live Stock Updates:** Enter a stock ticker (e.g., `AAPL`) and start tracking real-time prices.
- **Manage Portfolio:**
  - Add stocks by entering ticker, quantity, and purchase price.
  - Remove stocks from the portfolio.
- **Data Persistence:** The portfolio remains saved between sessions.

## Future Enhancements
- **Candlestick Chart Visualization** for better stock analysis.
- **Automated Alerts** when stock prices reach a certain threshold.
- **Integration with News APIs** to fetch financial news related to tracked stocks.

## Contributing
If you'd like to contribute, feel free to fork the repository and submit a pull request!

## License
This project is licensed under the MIT License.


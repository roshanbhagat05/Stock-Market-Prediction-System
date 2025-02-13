import tkinter as tk
from tkinter import ttk
import requests
import yfinance as yf
import mplfinance as mpf
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import time
from textblob import TextBlob
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Cursor
import numpy as np

# Database Setup
def setup_database():
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT UNIQUE,
        price REAL,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT,
        price REAL,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

setup_database()

def fetch_stock_data(ticker, period="6mo"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist

def fetch_news():
    api_key = "dcc4933a14ae412bb499d53c46c4395b"
    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        return news_data.get("articles", [])[:5]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

def analyze_sentiment(news_text):
    return TextBlob(news_text).sentiment.polarity

def display_news():
    articles = fetch_news()
    news_text.config(state=tk.NORMAL)
    news_text.delete("1.0", tk.END)
    
    if not articles:
        news_text.insert(tk.END, "No news available.\n")
    else:
        for article in articles:
            sentiment = analyze_sentiment(article['title'])
            sentiment_label = "Positive" if sentiment > 0 else "Neutral" if sentiment == 0 else "Negative"
            news_text.insert(tk.END, f"{article['title']} ({sentiment_label})\n{article['url']}\n\n")
    
    news_text.config(state=tk.DISABLED)

def save_stock_history(ticker, price):
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO stock_history (ticker, price) VALUES (?, ?)", (ticker, price))
    conn.commit()
    conn.close()

def export_stock_history():
    conn = sqlite3.connect("stocks.db")
    df = pd.read_sql_query("SELECT * FROM stock_history", conn)
    df.to_csv("stock_history_export.csv", index=False)
    conn.close()

def display_stock_performance():
    ticker = stock_entry.get()
    data = fetch_stock_data(ticker, period="1y")
    
    if data.empty:
        stock_label.config(text="Invalid Ticker")
        return
    
    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[-2]
    one_month_ago = data['Close'].iloc[-21] if len(data) > 21 else prev_close
    six_months_ago = data['Close'].iloc[0]
    
    daily_change = ((last_close - prev_close) / prev_close) * 100
    monthly_change = ((last_close - one_month_ago) / one_month_ago) * 100
    six_months_change = ((last_close - six_months_ago) / six_months_ago) * 100
    
    stock_label.config(text=f"{ticker}: {last_close:.2f} USD\nDaily: {daily_change:.2f}%\nMonthly: {monthly_change:.2f}%\n6-Months: {six_months_change:.2f}%")
    save_stock_history(ticker, last_close)

def display_candlestick_chart():
    ticker = stock_entry.get()
    data = fetch_stock_data(ticker)
    
    if data.empty:
        return
    
    fig, ax = plt.subplots(figsize=(8, 5))
    mpf.plot(data, type='candle', style='charles', ax=ax, volume=False, mav=(10, 20))
    
    cursor = Cursor(ax, useblit=True, color='red', linewidth=1)
    
    for widget in chart_frame.winfo_children():
        widget.destroy()
    
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def add_to_portfolio():
    ticker = portfolio_entry.get()
    data = fetch_stock_data(ticker)
    if not data.empty:
        price = data['Close'].iloc[-1]
        conn = sqlite3.connect("stocks.db")
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO portfolio (ticker, price) VALUES (?, ?)", (ticker, price))
        conn.commit()
        conn.close()
        portfolio_list.insert(tk.END, f"{ticker}: {price:.2f} USD")

def auto_close():
    root.quit()

# Main Window
root = tk.Tk()
root.title("Stock Market Dashboard")
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Stock Analysis Tab
stock_tab = ttk.Frame(notebook)
notebook.add(stock_tab, text="Stock Analysis")
stock_entry = tk.Entry(stock_tab)
stock_entry.pack()
tk.Button(stock_tab, text="Fetch", command=display_stock_performance, height=3, width=28).pack()
stock_label = tk.Label(stock_tab, text="Enter a stock ticker")
stock_label.pack()

# Candlestick Chart Tab
chart_tab = ttk.Frame(notebook)
notebook.add(chart_tab, text="Candlestick Chart")
chart_frame = tk.Frame(chart_tab)
chart_frame.pack()
tk.Button(chart_tab, text="Show Chart", command=display_candlestick_chart, height=3, width=28).pack()

# Financial News Tab
news_tab = ttk.Frame(notebook)
notebook.add(news_tab, text="Financial News")
news_text = tk.Text(news_tab, state=tk.DISABLED, height=15, width=70)
news_text.pack()
tk.Button(news_tab, text="Refresh News", command=display_news, height=3, width=28).pack()

# Portfolio Tab
portfolio_tab = ttk.Frame(notebook)
notebook.add(portfolio_tab, text="Portfolio Management")
portfolio_entry = tk.Entry(portfolio_tab)
portfolio_entry.pack()
tk.Button(portfolio_tab, text="Add Stock", command=add_to_portfolio, height=3, width=28).pack()
portfolio_list = tk.Listbox(portfolio_tab)
portfolio_list.pack()
tk.Button(portfolio_tab, text="Export Data", command=export_stock_history, height=3, width=28).pack()

# Exit Tab
tab_exit = ttk.Frame(notebook)
notebook.add(tab_exit, text="Exit")
tk.Button(tab_exit, text="Exit Application", command=root.quit, height=3, width=28).pack()

root.after(60000, auto_close)
root.mainloop()
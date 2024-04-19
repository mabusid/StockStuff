import json
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# double output: used in below functions
def getData(input):
    # input from llm is an '[array]'
    data = json.loads(input)
    ticker, start, end = data[0], data[1], data[2]

    # get stock history (date format: "%yr-%mn-%dy")
    ticker_data = yf.download(ticker, start, end)
    days = ticker_data.shape[0]
    return_y = []
    for i in range(days):
        return_y.append(ticker_data.iloc[i]["Close"].round(5))
    return np.arange(1, days+1), return_y


# single output: specifically for tool
def allData(input):
    # input from llm is an '[array]'
    data = json.loads(input)
    ticker, start, end = data[0], data[1], data[2]

    # get stock history (date format: "%yr-%mn-%dy")
    ticker_data = yf.download(ticker, start, end)
    days = ticker_data.shape[0]
    return_y = []
    for i in range(days):
        return_y.append(str((ticker_data.iloc[i]["Close"].round(5))))
    return return_y

def createPlot(input):
    x,y = getData(input)

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#444444') 
    ax.set_facecolor('#555555') 

    ax.plot(x,y)
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    ax.set_xlabel('Days', color='white')
    ax.set_ylabel('Closing Price in Dollars', color='white')
    ax.set_title('Closing Prices', color='white')

    plt.savefig('test.jpeg')

    # st.pyplot(plt.gcf())

    return "Graph plotted"


def analyzeData(input):
    _days, closingPrices = getData(input)
    mean_y = np.mean(closingPrices)
    median_y = np.median(closingPrices)
    min_y = np.min(closingPrices)
    max_y = np.max(closingPrices)
    std_y = np.std(closingPrices)

    return f'''
    Mean closing price: {mean_y:.2f}
    Median closing price: {median_y:.2f}
    Minimum closing price: {min_y:.2f}
    Maximum closing price: {max_y:.2f}
    Standard deviation of closing prices: {std_y:.2f}
    '''


def newsUpdate(input_ticker):

    ticker = yf.Ticker(input_ticker)

    response = ""
    for i in range(len(ticker.news)):
        response += f'''
                    Article {i}
                    Title: {ticker.news[i]['title']}
                    Publisher: {ticker.news[i]['publisher']}
                    Link: {ticker.news[i]['link']}
                    '''
    
    return response

def peVisual(input_ticker):
    # to be replaced with searched competitors
    industry_tickers = ["MSFT","AAPL","NVDA","GOOG","AMZN","META"]

    if (input_ticker in industry_tickers):
        pass
    else:
        return "Industy PE values currently not available"

    ticker = yf.Ticker(input_ticker)
    pe_ratio = ticker.info.get('forwardPE', None)

    valuesPE = []
    for i in range(len(industry_tickers)):
        valuesPE.append(yf.Ticker(industry_tickers[i]).info.get('forwardPE', None))

    #plt.bar(industry_tickers, valuesPE)
    fig, ax = plt.subplots()
    plt.bar(industry_tickers, valuesPE, color='#1f77b4')
    ax.set_facecolor('#555555')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    plt.xlabel('Tickers', color='white')
    plt.ylabel('PE values', color='white')
    plt.title('PE Comparison', color='white')

    plt.gcf().set_facecolor('#444444')

    plt.savefig('test.jpeg')

    if pe_ratio is not None:
        return f"P/E ratio for {input_ticker} is: {pe_ratio}"
    else:
        return f"P/E ratio information not available for {input_ticker}"

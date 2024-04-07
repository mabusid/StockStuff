import numpy as np
import openai
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
import os
import requests

import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


#############################
## DEFINE FUNCS FOR AGENTS ##
#############################


def getData(ticker, start, end):
    # get stock history b/w start to end date (date format: "%yr-%mn-%dy")
    ticker_data = yf.download(ticker, start, end)
    days = ticker_data.shape[0]
    return_y = []
    for i in range(days):
        return_y.append(ticker_data.iloc[i]["Close"].round(5))
        #print(ticker_data.iloc[i]["Close"].round(5)) # day 1 of range, closing price
    return np.arange(1, days+1), return_y

def analyzeData(ticker, start, end):
    days, closingPrices = getData(ticker, start, end)
    mean_y = np.mean(closingPrices)
    median_y = np.median(closingPrices)
    min_y = np.min(closingPrices)
    max_y = np.max(closingPrices)
    std_y = np.std(closingPrices)

    return f'''
    Summary of Data:
    Mean closing price: {mean_y:.2f}
    Median closing price: {median_y:.2f}
    Minimum closing price: {min_y:.2f}
    Maximum closing price: {max_y:.2f}
    Standard deviation of closing prices: {std_y:.2f}
    '''


def createPlot(ticker, start, end):
    x,y = getData(ticker, start, end)

    plt.plot(x,y)
    plt.xlabel('Days')
    plt.ylabel('Closing Price ($)')
    plt.title('Closing Prices across Time Period')

    plt.show()
    return "Compelte"


###################
## CREATE AGENTS ##
###################


load_dotenv() # get key from .env

llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
    model_name="gpt-3.5-turbo"
)

from langchain.agents import tool
from langchain.agents import initialize_agent

@tool
def analyzeTicker(input_ticker: str):
    """A simple analyzing tool that outputs a summary of a stock's \
        performance for a provided stock ticker over the course of a year. \
        Do not pass untrusted input. The input should be a ticker in the \
        format of a string."""
    return analyzeData(input_ticker, "2023-01-01", "2024-01-01")

@tool
def visualizeTicker(input_ticker: str):
    """A simple visualization and plotting tool that outputs a trend graph \
        for a provided stock ticker over the course of a year. Do not \
        pass untrusted input. The input should be a ticker in the format \
        of a string."""
    return createPlot(input_ticker, "2023-01-01", "2024-01-01")

tools = [analyzeTicker, visualizeTicker]

zero_shot_agent = initialize_agent(
    agent="zero-shot-react-description",
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3
)

result = zero_shot_agent("Visualize the trend of the apple stock for this year.")
print(result)

'''
CURRENT WORKINGS
issue: can only take one input (currently tick)
temp. solution: only take ticker - show data for previous year

issue: after plotting, observe: None --> retries infinitely 
try: returning "complete" in plotting function
status: SOLVED

issue(?): Thought: "I should ALSO analyze/plot after analyzing/plotting"
question: Should I limit the model to one function or combine both?
'''
import os
import functions as funcs
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import tool, load_tools, initialize_agent


llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
    model_name="gpt-3.5-turbo"
)


@tool
def allData(stock_data: str):
    """A tool that provides the full summary of a stock. \
        Only take an input of an array with three elements. The input should be an array with \
        the first item being a ticker, the second a start date, and the thrid an end date. \
        The dates should be in the format of "%yr-%mn-%dy". If no dates are provided, use the most recently provided date OR \
        default to "2023-01-01" as the second item and "2024-01-01" as the third item.
        """
    return funcs.allData(stock_data)

@tool
def visualizeTicker(stock_data: str):
    """A simple visualizing and plotting tool that provides a trend graph \
        for a stock given its ticker, start date, and end date. \
        Only take an input of an array with three elements. \
        The first item being a ticker, the second a start date, and the thrid an end date. \
        The dates should be in the format of "%yr-%mn-%dy". If no dates are provided, \
        default to "2023-01-01" as the second item and "2024-01-01" as the third item.
        """
    return  funcs.createPlot(stock_data)

custom_tools = [visualizeTicker, allData]
basic_visual_answer = initialize_agent(
    agent="zero-shot-react-description",
    tools=custom_tools,
    llm=llm,
    verbose=True,
    max_iterations=4,
)


@tool
def keyValues(stock_data: str):
    """A tool that provides a stock graph's mean, median, min, max, and std \
        price for a given stock ticker given a start and end date. This should not be used \
        to find specific, more general values for the stock in the given time period. \
        Only take an input of an array with three elements. The input should be an array with \
        the first item being a ticker, the second a start date, and the thrid an end date. \
        The dates should be in the format of "%yr-%mn-%dy". If no dates are provided, \
        default to "2023-01-01" as the second item and "2024-01-01" as the third item.
        """
    return funcs.analyzeData(stock_data)

@tool 
def getNews(ticker: str):
    """A tool that provides recent news about a give company when provided \
        a stock ticker with a start and end date. \
        Only take an input of a single ticker as a string.
        """
    return funcs.newsUpdate(ticker)

@tool
def peAnalysis(ticker: str):
    """A tool that provides an analysis of PE ratios for a stock ticker. \
        Only take an input of a single ticker as a string.
        """
    return funcs.peVisual(ticker)


#Pe analysis, industry summary

custom_tools = [keyValues, peAnalysis, getNews]
analysis_answer = initialize_agent(
    agent="zero-shot-react-description",
    tools=custom_tools,
    llm=llm,
    verbose=True,
    max_iterations=4,
)

wiki = load_tools(["wikipedia"], llm=llm)

wiki_answer = initialize_agent(
    agent="zero-shot-react-description",
    tools=wiki,
    llm=llm,
    verbose=True,
    max_iterations=3,
)
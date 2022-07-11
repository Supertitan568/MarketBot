import requests
import yfinance as yh

def return_stock_price(time, *tickers):
    '''
    This function returns a tuple with the stock prices of all the
    company tickers passed into the function at the listed time
    '''
    #FIXME: If there is an invalid ticker, time, or yahoo finance doesn't load, it will crash the program

    #fetches company data from yahoo finance
    company_data = list()
    for ticker in tickers:
        stock = yh.Ticker(ticker)
        company_data.append(stock)


    if time == 'now':
        prices = list()
        for stock in company_data:
            info = stock.info
            current_price = info['currentPrice']
            prices.append(current_price)
            
        #company_data = [stock['currentPrice'] for stock.info in company_data]
        return tuple(prices)

    else:
        #FIXME: This can only find close prices in the last month
        company_data = [stock.history(period='1mo').at[time, 'Close'] for stock in company_data]
        return tuple(company_data)


def fetch_top_performers(start, end):
    '''
    This fetches some of the top performers of the S&P 500 in the last day from yahoo finance
    '''

    #FIXME:This only fetches the tickers in grey because of the beginning html piece I used
    html_code = requests.get("https://finance.yahoo.com/gainers/").text

    #Note: This is a terribly ineffcient way to parse html
    start_indexs_start = [i for i in range(len(html_code)) if html_code.startswith('<a data-test="quoteLink"', i)]

    start_indexs_end = list()
    for i in start_indexs_start:
        end_bracket_index = html_code[i:].find('>') + i
        start_indexs_end.append(end_bracket_index)

    end_indexes_start = list()
    for i in start_indexs_end:
        start_bracket_index = html_code[i:].find('<') + i
        end_indexes_start.append(start_bracket_index)
    
    tickers = list()
    for i in range(start, end):
        ticker = html_code[start_indexs_end[i] + 1: end_indexes_start[i]]
        tickers.append(ticker)
    
    return tickers
    







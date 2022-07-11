import investing_functions as invest_funcs
from random import randint
import sys


def make_investment(money_avalible):
    #picks 5 random stocks out of a list of 25 top gainers
    top_performers = invest_funcs.fetch_top_performers(1, 25)
    stock_picks = list()
    for stock in range(5):
        stock_picks.append(top_performers[randint(0, len(top_performers) - 1)])
    
    money_for_each = money_avalible // 5

    #Figures out how many shares it should invest from amount of money avalible for it
    shares_invested = dict()
    shares_invested['money_left'] = 0
    for stock in stock_picks:
        share_price = invest_funcs.return_stock_price("now", stock)
        amount_shares = int(money_for_each / share_price[0])

        if stock in shares_invested:
            shares_invested[stock] += amount_shares

        if amount_shares != 0:
            print("Ticker Symbol:", stock, "    Amount of shares to invest:", amount_shares)
            shares_invested[stock] = amount_shares

        shares_invested["money_left"] += (share_price[0] * amount_shares)

    shares_invested['money_left'] = money_avalible - shares_invested['money_left']
    return shares_invested


def sell_investment(shares_to_sell):
    stocks = {stock: shares_to_sell[stock] for stock in shares_to_sell if stock != 'money_left'}
    current_share_prices = dict()
    for stock in stocks:
        current_price = invest_funcs.return_stock_price("now", stock)
        current_share_prices[stock] = current_price[0]
    
    amount_returned = 0
    for stock in stocks:
        amount_returned += (current_share_prices[stock] * stocks[stock])
    
    return {'money_left': amount_returned + shares_to_sell['money_left']}


def make_report(money_avalible, shares_invested):
    current_share_prices = dict()
    amount_invested = 0
    for stock in shares_invested:
        share_price = invest_funcs.return_stock_price("now", stock)
        current_share_prices[stock] = share_price[0]
        amount_invested += (share_price[0] * shares_invested[stock])
    
    report = "Total Portfolio: " + str(amount_invested + money_avalible) 
    report += ("\nTotal Money Invested:" + str(amount_invested))
    report += ("\nTotal Money Not Invested: " + str(money_avalible))
    for stock in shares_invested:
        report += ("\nTicker Symbol: " + stock + "  Amount of Shares invested: " + str(shares_invested[stock]) + "  Total Money Invested: " + str(current_share_prices[stock] * shares_invested[stock]))

    return report


def write_log(shares_invested):
    log_file = open('log.txt', 'a')
    report = str()
    for stock in shares_invested:
        report += (stock + ':' + str(shares_invested[stock]) + ' ')
    report += '\n'

    log_file.write(report)

def main():
    log_file = open('log.txt', 'r')
    line = log_file.readlines()[-1]
    line = line.rstrip().split(' ')

    current_stock = dict()    
    for stock in line:
        if stock[:10] == 'money_left':
            current_stock[stock[:stock.index(':')]] = float(stock[stock.index(':') + 1:])
        else:
            current_stock[stock[:stock.index(':')]] = int(stock[stock.index(':') + 1:])

    if "buy_mode" in sys.argv:
        new_picks = make_investment(current_stock['money_left'])
        for stock in new_picks:
            if stock in current_stock:
                if stock != 'money_left':
                    current_stock[stock] += new_picks[stock]
            else:
                current_stock[stock] = new_picks[stock]
        current_stock['money_left'] = new_picks['money_left']
        write_log(current_stock)
        
    if "sell_mode" in sys.argv:
        current_stock = sell_investment(current_stock)
        write_log(current_stock)
    if "report_mode" in sys.argv:
        print(make_report(current_stock['money_left'], {stock: current_stock[stock] for stock in current_stock if stock != 'money_left'}))
    

if __name__ == "__main__":
    main()

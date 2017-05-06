
def initialize(context):
    """
    Called once at the start of the algorithm.
    """   
    # Rebalance every month, with a 4 day offset, 4 hours after market open
    schedule_function(my_rebalance, date_rules.month_start(days_offset = 4), time_rules.market_open(hours=4))
    #WM, GOOG, AMZN, FB, MCD, WEN
    context.securities_list = [sid(19181), sid(26578), sid(16841),sid(42950),sid(4707), sid(10293)]
    #BND
    context.bonds = sid(33652)

         

 
def before_trading_start(context, data):
    """
    Called every day before market open.
    """
    
    context.securities_traded_list = []
    #get the previous day's closing price for each security in the list
    context.securities_prev_close_list = []
    for security in context.securities_list:
        context.securities_prev_close_list.append(data.current(security, 'close'))

     

 
def my_rebalance(context,data):
    """
    Execute orders according to our schedule_function() timing. 
    """
    #leave 20% of portfolio as cash, divide the rest evenly between each security in the list
    
    #to-do: hold BND instead of cash, and sell as needed
    for security in context.securities_list:
        if data.can_trade(security):
            order_target_percent(security, (1-.2)/len(context.securities_list))


 
def handle_data(context,data):
    """
    Called every minute.
    """
    for i in range(len(context.securities_list)):
        #if the current price is down 2.5% from the previous day's close, buy and hold until the next monthly rebalance
        if data.can_trade(context.securities_list[i]):
            
            if (context.securities_prev_close_list[i] - data.current(context.securities_list[i], 'price'))/context.securities_prev_close_list[i] < -.025 and not context.securities_list[i] in context.securities_traded_list:
                order_value(context.securities_list[i], context.portfolio.cash*.5)
                #add the security to already-traded-list. only trade each security once per day
                context.securities_traded_list.append(context.securities_list[i])
            
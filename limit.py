class Strategy(StrategyBase):
    def __init__(self):
        # strategy attributes
        self.period = 60 * 60 
        self.subscribed_books = {
            'Binance': {
                'pairs': ['ETH-USDT'],
            },
        }
        self.options = {}

        # define your attributes here
        self.i = 0
        #pass

    def on_order_state_change(self,  order):
        pass

    def trade(self, candles):

        exchange, pair, base, quote = CA.get_exchange_pair()
        candles[exchange][pair] = candles[exchange][pair][:self.period]

        low_price_history = [candle['low'] for candle in candles[exchange][pair]]
        low_price_history.reverse()
        high_price_history = [candle['close'] for candle in candles[exchange][pair]]
        high_price_history.reverse()
        close_price_history = [candle['close'] for candle in candles[exchange][pair]]
        close_price_history.reverse()

        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available


        if len(low_price_history) <=4:
            CA.log('Not enough data yet')
            is_support = None
            is_resistance = None

            # amount=0.25
            # if available_quote_amount >= amount * close_price_history[2+self.i]:
            #     CA.buy(exchange, pair, amount, CA.OrderType.MARKET)
            

        else:    
            scond1 = low_price_history[2+self.i] < low_price_history[1+self.i]
            scond2 = low_price_history[2+self.i] < low_price_history[3+self.i]
            scond3 = low_price_history[3+self.i] < low_price_history[4+self.i]
            scond4 = low_price_history[1+self.i] < low_price_history[0+self.i]   
            is_support = scond1 and scond2 and scond3 and scond4
            
            rcond1 = low_price_history[2+self.i] > low_price_history[1+self.i]
            rcond2 = low_price_history[2+self.i] > low_price_history[3+self.i]
            rcond3 = low_price_history[3+self.i] > low_price_history[4+self.i]
            rcond4 = low_price_history[1+self.i] > low_price_history[0+self.i]   
            is_resistance = rcond1 and rcond2 and rcond3 and rcond4
            
            self.i +=1
           
            if is_support:
                CA.log('low price = '+str(low_price_history[2+self.i]))
                amount=np.round(available_quote_amount /high_price_history[2+self.i] , 3)
                CA.log('quote= ' +str(available_quote_amount))
                if available_quote_amount >= amount * close_price_history[2+self.i]:
                    CA.buy(exchange, pair, amount, CA.OrderType.LIMIT, low_price_history[2+self.i])
                else:
                    CA.log('資產不足')
            else:
                pass

            if is_resistance:
                CA.log('high price = '+str(high_price_history[2+self.i]))
                amount=np.round(available_quote_amount /high_price_history[2+self.i] , 3)
                CA.log('base = ' +str(available_base_amount))
                if available_base_amount > 0.01:
                    CA.sell(exchange, pair, amount, CA.OrderType.LIMIT, high_price_history[2+self.i])
                else:
                    CA.log('資產不足')
            else:
                pass

            #test=high_price_history
            #CA.log(str(test))

   
    



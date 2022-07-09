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
        self.cont_1 = False
        self.cont_2 = False
        self.case = 0
        #pass

    def on_order_state_change(self,  order):
        pass

    def trade(self, candles):

        exchange, pair, base, quote = CA.get_exchange_pair()
        candles[exchange][pair] = candles[exchange][pair][:self.period]

        low_price_history = [candle['low'] for candle in candles[exchange][pair]]
        low_price_history.reverse()
        high_price_history = [candle['high'] for candle in candles[exchange][pair]]
        high_price_history.reverse()
        close_price_history = [candle['close'] for candle in candles[exchange][pair]]
        close_price_history.reverse()

        base_balance = CA.get_balance(exchange, base)
        quote_balance = CA.get_balance(exchange, quote)
        available_base_amount = base_balance.available
        available_quote_amount = quote_balance.available

        if len(low_price_history) <= 9:
            CA.log('Not enough data yet')
            is_support = False
            is_resistance = False
            
        else:        
            if self.case == 1 or self.cont_1 == True:
                CA.log('case 1')
                if close_price_history[self.i-9] <= close_price_history[self.i-9-1]:
                    self.cont_1= True
                    amount=np.round(available_quote_amount /high_price_history[self.i-9] , 3)/5
                    CA.log('quote= ' +str(available_quote_amount))
                    if available_quote_amount >= amount * close_price_history[self.i-9]:
                        CA.buy(exchange, pair, amount, CA.OrderType.MARKET)
                    else:
                        CA.log('資產不足')
                else:
                    self.cont_1 = False
                self.case = 0
                
            elif self.case ==2 or self.cont_2 == True:
                CA.log('case 2')
                if close_price_history[self.i-9] >= close_price_history[self.i-9-1]:
                    self.cont_2 = True
                    amount=np.round(available_quote_amount /high_price_history[self.i-9] , 3)/5
                    CA.log('base = ' +str(available_base_amount))
                    if available_base_amount > 0.01:
                        CA.sell(exchange, pair, amount, CA.OrderType.MARKET)
                    else:
                        CA.log('資產不足')
                else:
                    self.cont_2 = False
                self.case = 0
            else:
                pass
                        
            is_support=False
            min_list=[]
            for k in range(self.i-9,self.i-4):
                low_range = low_price_history[k-5:k+4]
                low_range = np.array(low_range)
                current_min = low_range.min()
                if current_min not in min_list:
                    min_list = []
                min_list.append(current_min)
                if len(min_list)==5 :
                    is_support= True
                    
            is_resistance=False
            max_list=[]
            for k in range(self.i-9,self.i-4):
                high_range = high_price_history[k-5:k+4]
                high_range = np.array(high_range)
                current_max = high_range.min()
                if current_max not in max_list:
                    max_list = []
                max_list.append(current_max)
                if len(max_list)==5 :
                    is_resistance= True
        
            self.i +=1
           
            if is_support:
                self.case = 1
            else:
                pass

            if is_resistance:
                self.case = 2
            else:
                pass

            #test=high_price_history
            #CA.log(str(test))

   
    



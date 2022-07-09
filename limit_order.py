import backtrader as bt
# import bc_study.tushare_csv_datafeed as ts_df
from backtrader.order import Order

import yfinance as yf
# import matplotlib.dates as mpl_dates
# import pandas as pd
import backtrader.feeds as btfeeds
import datetime

# 基策略
class LimitOrderStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        pass

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # if order.status == order.Submitted:
            #     self.log('订单(oid={oid}) , Submitted'.format(oid=order.ref))
            # if order.status == order.Accepted:
            #     self.log('订单(oid={oid}) , Accepted'.format(oid=order.ref))
            return
        elif order.status in [order.Completed]:
            if order.isbuy():
                self.log('买单(oid={oid})执行, 执行价={ep}，数量={ea}'.format(oid=order.ref, ep=order.executed.price, ea=order.executed.size))
            elif order.issell():
                self.log('卖单(oid={oid})执行, 执行价={ep}，数量={ea}'.format(oid=order.ref, ep=order.executed.price, ea=order.executed.size))
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order(oid={oid}) Canceled/Margin/Rejected'.format(oid=order.ref))

    def next(self):
        # 第1天，4日BUY单，限价17.6，无法成交
        if len(self) == 1:
            order = self.buy(size=10, price=17.60, exectype=Order.Limit)
            if order:
                self.log("下单BUY单(oid={id}), price={p}".format(id=order.ref, p=order.price))
        if len(self) == 2:
            order = self.buy(size=10, price=20.00, exectype=Order.Limit)
            if order:
                self.log("下单BUY单(oid={id}), price={p}".format(id=order.ref, p=order.price))
        if len(self) == 3:
            order = self.sell(size=10, price=20.30, exectype=Order.Limit)
            if order:
                self.log("下单SELL单(oid={id}), price={p}".format(id=order.ref, p=order.price))


# def get_stock_price(symbol):
#     df = yf.download(symbol, start='2021-02-01', threads= False)
#     df['Date'] = pd.to_datetime(df.index)
#     df['Date'] = df['Date'].apply(mpl_dates.date2num)
#     df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
#     return df

# 启动回测
def engine_run():
    # 初始化引擎
    cerebro = bt.Cerebro()

    # 给Cebro引擎添加策略
    cerebro.addstrategy(LimitOrderStrategy)

    # 设置初始资金：
    cerebro.broker.setcash(200000.0)

    # 从csv文件加载数据
    # 仅3天数据
    data = bt.feeds.PandasData(dataname=yf.download('SPY', '2015-07-06', '2021-07-01', auto_adjust=True))

    cerebro.adddata(data)

    # symbol = 'COST'
    # df = get_stock_price(symbol)
    # cerebro.adddata(df)

    # 回测启动运行
    cerebro.run()
    
if __name__ == '__main__':
    engine_run()
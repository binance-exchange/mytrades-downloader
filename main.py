from binance.spot import Spot as Client
from lib.configer import Configer
from modules.trade import Trade
from modules.symbol_manager import SymbolManager

if __name__ == "__main__": 
  config = Configer()
  client = Client(key=config.get('BINANCE_API_KEY'), secret=config.get('BINANCE_SECRET_KEY'), show_weight_usage=True)

  sm = SymbolManager()
  sm.client = client
  sm.fetch_all_symbols()

  trade = Trade()
  trade.client = client
  trade.configuration = config
  trade.download_trades(sm.all_symbols)

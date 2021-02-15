from modules.base import Base

class SymbolManager(Base):
  def __init__(self):
    super().__init__()
    self._all_symbols = []

  @property
  def all_symbols(self):
      return self._all_symbols


  def fetch_all_symbols(self):
    '''
      get all symbols from exchange
    '''

    response = self.client.exchange_info()
    if 'data' in response:
      response = response['data']
    result = []
    for s in response['symbols']:
      result.append(s['symbol'])
    self._all_symbols = result

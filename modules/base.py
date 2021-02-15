from binance.spot import Spot as Client

class Base(object):
  def __init__(self):
    self._client = None
    self._configuration = None

  @property
  def client(self):
    return self._client

  @property
  def configuration(self):
      return self._configuration

  @client.setter
  def client(self, client_instance):
    self._client = client_instance

  @configuration.setter
  def configuration(self, config):
    self._configuration = config

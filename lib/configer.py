import configparser

class Configer(object):
    
    def __init__(self, config_file=None):
      if config_file is None:
        config_file = 'app.properties'
      self._config = configparser.ConfigParser()
      self._config.read(config_file)
    
    def get(self, property):
      _split_properties = property.split('.')
      if len(_split_properties) > 2:
        raise AttributeError("property only support as: <section>.<property>")
      
      if len(_split_properties) == 1:
        _section = 'DEFAULT'
        _prop = _split_properties[0]
      else:
        _section = _split_properties[0]
        _prop = _split_properties[1]
      
      val = self._config.get(_section, _prop)
      val = [e.strip() for e in val.split(',')]
      if len(val) > 1:
        return val
      return val[0]

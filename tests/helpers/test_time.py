
from helpers.time import timestamp_to_localize

def test_timestamp_to_localize():
  timestamp_to_localize(1613352845000, 'Europe/Amsterdam').should.equal('2021-02-15 12:34:05')

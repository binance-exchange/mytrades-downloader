import os
import logging
import time
import pandas as pd
from pathlib import Path
from modules.base import Base
from helpers.files import scan_files
from helpers.time import timestamp_to_localize

class Trade(Base):

  def __init__(self):
    super().__init__()

  def create_csv_file(self, destination_dir, symbol):
    return os.path.join(destination_dir, "{}-trades.csv".format(symbol.upper()))

  def get_record_id_from_df(self, df):
    return df.iat[0,3]

  def get_1m_weight_usage(self, weight_usage):
    return int(weight_usage['x-mbx-used-weight-1m'])

  def add_local_time(self, df):
    localTime = []
    side = []
    for index, row in df.iterrows():
      # local time
      localTime.append(timestamp_to_localize(row[9], self.configuration.get('TIME_ZONE')))

      # add side
      if row[10] == False:
        side.append("SELL")
      else:
        side.append("BUY")
    
    df = df.drop(columns=['isBuyer', 'isMaker', 'isBestMatch', 'time']) # remove isMarker, isBuyer, isBestMatch, timestamp
    df.insert(0, "Local Time", localTime, True)
    df.insert(2, "Side", side, True)
    return df
    # return df.assign(localTime = localTime)

  def download_trade_by_symbol(self, symbol):
    if not symbol:
      logging.warn("{} symbol is not valid".format(symbol))
       
    # destination directory: data/spot/trades/<symbol>/
    destination_dir = self.configuration.get('STORE_DIRECTORY') + "/mytrades/{}/".format(symbol.upper())

    # scan current data folder, find out the latest file
    data_files = scan_files(destination_dir)

    # if no trade is saved
    if len(data_files) == 0:
      csv_file = ""
    else:
      csv_file = self.create_csv_file(destination_dir, symbol)

    start_time = int(self.configuration.get('START_TIMESTAMP'))
    end_time = int(self.configuration.get('END_TIMESTAMP'))

    # try to read last saved file
    try:
        df = pd.read_csv(csv_file, header=None)
        last_record_id = self.get_record_id_from_df(df.tail(1))
        from_id = int(last_record_id) + 1

    except FileNotFoundError:
        # first time to fetch trades
        from_id = 0
        pass
    
    while True:
      if from_id == 0 and start_time:
        my_trades = self.client.my_trades(symbol,limit=1000, startTime=start_time)
      else:
        my_trades = self.client.my_trades(symbol,limit=1000, fromId=from_id)

      weight_usage = my_trades['weight_usage']
      df = pd.DataFrame(my_trades['data'])
      if (df.empty):
        print("Finished, no more data")
        break

      if self.get_1m_weight_usage(weight_usage) > 1110:
        print("too much request, cool down")
        time.sleep(10)
      
      # touch the folder
      Path(destination_dir).mkdir(parents=True, exist_ok=True)
      csv_file = self.create_csv_file(destination_dir, symbol)
      
      last_trade_id = df.tail(1).iat[0, 1]
      from_id = int(last_trade_id) + 1
      last_record_time = df.tail(1).iat[0, 9]
      if last_record_time > end_time:
        for index, row in df.iterrows():
          if row[9] >= end_time:
            df = df.drop(index=index)
        
        df = self.add_local_time(df)
        if len(df) > 0:
          df.to_csv(csv_file, mode='a', index=False, header=True)
        print("Reach the end of the time window")
        break
      else:
        df = self.add_local_time(df)
        df.to_csv(csv_file, mode='a', index=False, header=True)

  def download_trades(self, symbol_list):
    checked_number = 0
    for symbol in symbol_list:
      checked_number += 1
      print("[{}/{}] start to download trade on {}".format(checked_number, len(symbol_list), symbol))
      self.download_trade_by_symbol(symbol)

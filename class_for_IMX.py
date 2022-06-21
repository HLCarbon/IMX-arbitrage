
import pandas as pd
from functions import functions_for_class as fc
from os import path
import datetime as dt

#for book, in name do str.split('#')[0]

class game:
    def __init__(self, name:str):
        def get_name_from_address(self):
            response = fc.go_to_site(site_type = f'collections/{self.address}')
            return response['name']
    
        def get_address_from_name(self):
            if self.name == 'Gods Unchained':
                return '0xacb3c6a43d15b907e8433077b6d38ae40936fe2c'
            response = fc.go_to_site(site_type = 'collections')
            game_dic = {game['name']: game['address'] for game in response['result']}
            if self.name in game_dic:
                return game_dic[self.name]
            else:
                while response['cursor'] == True:
                    response = fc.go_to_site(site_type = 'collections', querystring = {'cursor': response['cursor']})
                    game_dic = {game['name']: game['address'] for game in response['result']}
                    if self.name in game_dic:
                        return game_dic[self.name]
                return 'You misspelled the name'
        if name[:5] == 'https' :
            name_lst = name.split('=')
            self.address = name_lst[1]
            self.name = get_name_from_address(self)
        elif len(name) == 42 and name[:2] =='0x':
            self.address = name
            self.name = get_name_from_address(self)   
        else:
            self.name = name
            self.address = get_address_from_name(self)
    
    def get_metadata_schema(self):
        response = fc.go_to_site(site_type = 'orders', querystring = {"status":"filled",
            "sell_token_address":self.address})
        token_id = response['result'][0]['sell']['data']['token_id']
        token_address = response['result'][0]['sell']['data']['token_address']
        response = fc.go_to_site(site_type = f'assets/{token_address}/{token_id}')
        metadata = response['metadata']
        print(metadata)
        df = pd.Series(metadata)
        df = pd.DataFrame(df)
        df.rename(columns = {0:'Values'}, inplace = True)

        self.metadata = df
        return df
    def download_filled_trades(self, number_of_days:int):
        self.days = number_of_days
        self.prior_trades = fc.get_filled_trades_from_start_day(self.days, self.address)
        return self.prior_trades
    def download_active_trades(self):
        self.active_trades = fc.get_all_orders(self.address)
        return self.active_trades
    def get_filled_trades(self, number_of_days:int):
        if path.exists(f'csvs/some_filled_trades_{self.address}.csv'):
            self.prior_trades = pd.read_csv(f'csvs/some_filled_trades_{self.address}.csv', encoding = 'utf-8-sig', sep =';')
            self.days = number_of_days
            first_trade = dt.datetime.strptime(self.prior_trades['updated_timestamp'].iloc[0], "%Y-%m-%dT%H:%M:%S.%fZ")
            last_trade = dt.datetime.strptime(self.prior_trades['updated_timestamp'].iloc[-1], "%Y-%m-%dT%H:%M:%S.%fZ")
            difference = last_trade-first_trade
            if difference.days < self.days:
                print('The filled trades file has less recorded days than the ones that were requested.\nPlease choose a lower number or download the filled trades again with more days.')
            return self.prior_trades
        else:
            print('There is no filled trades csv.\nPlease use the download_filled_trades function first.')
    def get_active_trades(self):
        if path.exists(f'csvs/active_trades_for_sale_{self.address}.csv'):
            self.active_trades = pd.read_csv(f'csvs/active_trades_for_sale_{self.address}.csv', encoding = 'utf-8-sig', sep =';')
            return self.active_trades
        else:
            print('There is no active trades csv.\nPlease use the download_active_trades function first.')

    
    





#print(gogh.get_metadata_schema())

    

    #def sold_items_last_days(self, days):
        
    
            

import pandas as pd
from functions import functions_for_class as fc
from os import path
import datetime as dt

#for book, in name do str.split('#')[0]

class game:
    

    def __init__(self, name:str):
        self.defining_attributes = ['image_url']
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
    
    def change_defining_attributes(self, new_attributes:list):
        self.defining_attributes = new_attributes
    def get_metadata_schema(self):
        response = fc.go_to_site(site_type = 'orders', sell_token_address = self.address)
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
        self.filled_trades = fc.get_filled_trades_from_start_day(self.days,self.defining_attributes, self.address, )
        return self.filled_trades
    def download_active_trades(self):
        self.active_trades = fc.get_all_orders(self.defining_attributes, self.address)
        return self.active_trades
    def load_filled_trades(self, number_of_days:int):
        if path.exists(f'csvs/some_filled_trades_{self.address}.csv'):
            self.filled_trades = pd.read_csv(f'csvs/some_filled_trades_{self.address}.csv', encoding = 'utf-8-sig', sep =';')
            self.days = number_of_days
            first_trade = dt.datetime.strptime(self.filled_trades['updated_timestamp'].iloc[0], "%Y-%m-%dT%H:%M:%S.%fZ")
            last_trade = dt.datetime.now()
            difference = last_trade-first_trade
            if difference.days < self.days:
                print(f'The filled trades file has less recorded days than the ones that were requested ({difference} compared to {number_of_days}).\nPlease choose a lower number or download the filled trades again with more days.')
            return self.filled_trades
        else:
            print('There is no filled trades csv.\nPlease use the download_filled_trades function first.')
    def load_active_trades(self):
        if path.exists(f'csvs/active_trades_for_sale_{self.address}.csv'):
            self.active_trades = pd.read_csv(f'csvs/active_trades_for_sale_{self.address}.csv', encoding = 'utf-8-sig', sep =';')
            return self.active_trades
        else:
            print('There is no active trades csv.\nPlease use the download_active_trades function first.')
    def determine_arbitrage(self, coin_to_buy, coin_to_sell, daily_market_percentage = 0.2):
        try:
            self.coin_to_buy = coin_to_buy
            self.coin_to_sell = coin_to_sell
            coin_to_buy_usd = fc.get_current_data(coin_to_buy)
            coin_to_sell_usd = fc.get_current_data(coin_to_sell)
            coin_price_dict = {coin_to_buy:coin_to_buy_usd, coin_to_sell:coin_to_sell_usd}
            self.arbitrage_table = fc.get_arbitrage_from_2_currencies(coin_to_buy, coin_to_sell, self.active_trades, self.filled_trades,
            coin_price_dict, self.defining_attributes, self.days, market_percentage=daily_market_percentage)
            return self.arbitrage_table
        except AttributeError:
            print('Please get both the active trades and the filled trades dataframes before attempting to get the arbitrage table.\n')
    def execute_arbitrage(self, percentage_above = 20, price_reduction = 0.005, number_of_cards=0, cards_each_time=10):
        try:
            fc.execute_trades(self.arbitrage_table, self.coin_to_buy, self.coin_to_sell, 
        number_of_total_cards=number_of_cards, cards_each_time=cards_each_time, percentage_above=percentage_above,
        price_reduction=price_reduction)
        except AttributeError:
            print('Please get the arbitrage table first by executing the function "determine_arbitrage".')


    





        
    
            
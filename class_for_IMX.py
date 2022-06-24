
import pandas as pd
from functions import functions_for_class as fc
from os import path
import datetime as dt
import sys

class game:
    

    def __init__(self, name:str):
        #The attribute used for grouping the NFT's
        self.defining_attributes = ['image_url']
        def get_name_from_address(self):
            #If you give an address, it goes and gets the name of the game. Preferred way of doing this.
            response = fc.go_to_site(site_type = f'collections/{self.address}')
            return response['name']
    
        def get_address_from_name(self):
            #If you give a name, it goes and gets the address of the game. The problem rises when there are multiple games with the same name.
            #For example, there are at least Gods Unchained names. So I had to add an exemption because you can't determine which Gods Unchained 
            #is the correct one. This may happen with other games. for safety, always give the address instead of the name.
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
        #Changes the attribute used for grouping the NFT's
        self.defining_attributes = new_attributes
    def get_nft_properties(self)-> pd.DataFrame:
        #Gives you the attributes that you can use to group the NFT's
        response = fc.go_to_site(site_type = 'orders', sell_token_address = self.address, status = 'active')
        properties= response['result'][0]['sell']['data']['properties']
        df = pd.Series(properties)
        df = df.drop('collection')
        df = pd.DataFrame(df)
        df.rename(columns = {0:'Values'}, inplace = True)

        self.metadata = df
        return df

    def get_value_counts(self):
        #Gives you a table with the coins used for selling the NFT's in the last self.days 
        try: 
            print(f'In the last {self.days}, the coins used were:')
            print(self.filled_trades.coin.value_counts())
        except AttributeError:
            print('Please load/download the filled trades.')
    def download_filled_trades(self, number_of_days:int) -> pd.DataFrame:
        #Downloads the filled executed in the last self.days and saves them in a csv.
        self.days = number_of_days
        self.filled_trades = fc.get_filled_trades_from_start_day(self.days,self.defining_attributes, self.address, )
        return self.filled_trades
    def download_active_trades(self) -> pd.DataFrame:
        #Downloads the filled executed in the last self.days and saves them in a csv.
        self.active_trades = fc.get_all_orders(self.defining_attributes, self.address)
        return self.active_trades
    def load_filled_trades(self, number_of_days:int):
        #If you already have a csv with the filled trades, it goes and gets it.
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
        #If you already have a csv with the active trades, it goes and gets it.
        if path.exists(f'csvs/active_trades_for_sale_{self.address}.csv'):
            self.active_trades = pd.read_csv(f'csvs/active_trades_for_sale_{self.address}.csv', encoding = 'utf-8-sig', sep =';')
            return self.active_trades
        else:
            print('There is no active trades csv.\nPlease use the download_active_trades function first.')
    def determine_arbitrage(self, coin_to_buy:str, coin_to_sell:str, daily_market_percentage = 0.2) -> pd.DataFrame:
        #Return a dataframe with the arbitrage percentages. 
        try:
            self.coin_to_buy = coin_to_buy
            self.coin_to_sell = coin_to_sell
            coin_to_buy_usd = fc.get_current_data(coin_to_buy)
            coin_to_sell_usd = fc.get_current_data(coin_to_sell)
            coin_price_dict = {coin_to_buy:coin_to_buy_usd, coin_to_sell:coin_to_sell_usd}
            self.arbitrage_table = fc.get_arbitrage_from_2_currencies(coin_to_buy, coin_to_sell, self.active_trades, self.filled_trades,
            coin_price_dict, self.defining_attributes, self.days, market_percentage=daily_market_percentage)
            if self.arbitrage_table.empty:
                print('The final table is empty. Check the coins used or the market_percentage.')
                sys.exit()
            return self.arbitrage_table
        except AttributeError:
            print('Please get both the active trades and the filled trades dataframes before attempting to get the arbitrage table.\n')
            sys.exit()
    def execute_trades(self, percentage_above = 20, price_reduction = 0.005, number_of_cards=0, cards_each_time=10) -> None:
        #Buys and sells the cards that you want to given the parameters. 
        try:
            fc.execute_trades(self.arbitrage_table, self.coin_to_buy, self.coin_to_sell, 
        number_of_total_cards=number_of_cards, cards_each_time=cards_each_time, percentage_above=percentage_above,
        price_reduction=price_reduction)
        except AttributeError:
            print('Please get the arbitrage table first by executing the function "determine_arbitrage".')
            sys.exit()


    





        
    
            
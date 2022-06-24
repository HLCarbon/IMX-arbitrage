import datetime as dt
import requests
import pandas as pd
from Naked.toolshed.shell import execute_js
import urllib3 
import time
import warnings
import sys
warnings.filterwarnings("ignore")
http = urllib3.PoolManager()
pd.set_option('display.max_colwidth', None)



#These are the keys that are associated with each token (coin)
dct_token = {'0xacb3c6a43d15b907e8433077b6d38ae40936fe2c':'NOP',
'0xccc8cb5229b0ac8069c51fd58367fd1e622afd97':'GODS',
 '0x9ab7bb7fdc60f4357ecfef43986818a2a3569c62': 'GOG',
  '0xf57e7e7c23978c3caec3c3548e3d615c346e79ff': 'IMX',
  '0xed35af169af46a02ee13b9d79eb57d6d68c1749e':'OMI',
 '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48':'USDC',
 '0x4d224452801aced8b2f0aebe155379bb5d594381':'APE'}


def get_current_data(from_sym='BTC', to_sym='USD', exchange='') -> int:
    #Goes to the website API and gets the price in dollars of the currency x
    url = 'https://min-api.cryptocompare.com/data/price'    
    
    parameters = {'fsym': from_sym,
                  'tsyms': to_sym }
    
    if exchange:
        parameters['e'] = exchange
        
    # response comes as json
    response = requests.get(url, params=parameters)   
    data = response.json()

    return data['USD']

def get_dict(json: list, defining_attributes: list):
    """
    get_dict Transforms the json data into a list of dictionaries

    :param json: data from website
    """    ''''''
    result = json['result']
    #print(sh)
    lst = []
    if len(result)>0:
        for i in result:
            dct = {}
            dct['order_id'] = i['order_id']
            dct['token_id'] = i['sell']['data']['token_id']
            if defining_attributes == ['name_hro']:
                dct['name_hro'] = ' '.join(i['sell']['data']['properties']['name'].split(' ')[2:])
            else:
                for j in defining_attributes:
                    dct[j] = i['sell']['data']['properties'][j]
            if i['buy']['type'] == 'ETH':
                dct['coin'] = i['buy']['type']
            else:
                try:
                    dct['coin'] = dct_token[i['buy']['data']['token_address']]
                except KeyError:
                    print(f"The coin address {i['buy']['data']['token_address']} isn't in the coin_token dictionary. Please manually add it in the file 'functions_for_class.'")
                    dct['coin'] = 'Undefined'
            if dct['coin'] == 'USDC':
                dct['amount_sold'] = int(i['buy']['data']['quantity'])/(10**6)
            else:
                dct['amount_sold'] = int(i['buy']['data']['quantity'])/(10**18)
            dct['updated_timestamp'] = i['updated_timestamp']
            lst.append(dct)
            
    return lst

def go_to_site(order_by='', site_type = 'orders', status = '',updated_min_timestamp='',
 cursor = '', sell_token_address = '', user = '', page_size = '200',
 sell_metadata = '', querystring = ''):
    """
    go_to_site This is how you ask the API for information

    """ 
    url = "https://api.x.immutable.com/v1/" + site_type
    querystring = {'page_size':page_size}
    if status:
        querystring['status'] = status
    if order_by:
        querystring['order_by'] = order_by[0]
        querystring['direction'] = order_by[1]
    if sell_token_address:
        querystring['sell_token_address'] = sell_token_address
    if cursor:
        querystring['cursor'] = cursor
    if sell_metadata:
        querystring['sell_metadata'] = sell_metadata
    if updated_min_timestamp:
        querystring['updated_min_timestamp'] = updated_min_timestamp
    if user:
        querystring['user'] = user


    headers = {"Accept": "application/json"}
    response_data = ''
    while not response_data:
        try:
            response = requests.request('GET',url, headers=headers, params = querystring)
            response_data = response.json()
        except:
            time.sleep(2)
            print('There was a problem loading the website:')
            print(f'URL:\n{url}')
            pass
    return response_data

def get_all_orders(defining_attributes: list, token_address = '0xacb3c6a43d15b907e8433077b6d38ae40936fe2c'):
    #dictionary_with_all_selling_cards = pd.read_csv('data_active_trades_for_sale.csv', sep = ';', encoding='cp1252', low_memory=False)
    #dictionary_with_all_selling_cards = dictionary_with_all_selling_cards.sort_values('updated_timestamp', ascending = False)
    #first_time = correct_time_stamp(dictionary_with_all_selling_cards.iloc[0]['timestamp'], second = 1)
    first_page = go_to_site(status = 'active', page_size = '200', cursor = '',
     sell_token_address = token_address)
    remaining = first_page['remaining']
    cursor = first_page['cursor']
    first_dict = get_dict(first_page, defining_attributes)
    first_df = pd.DataFrame(first_dict)
    whole_lst = [first_df]
    #print(whole_lst)
    while cursor and remaining >0: 
        next_page = go_to_site(status = 'active', page_size = '200', cursor  = cursor,
         sell_token_address = token_address)
        if next_page != {'message': 'Endpoint request timed out'} and next_page != {'code': 'internal_server_error', 'message': 'The server encountered an internal error and was unable to process your request'}:               
            cursor = next_page['cursor']
            next_dict = get_dict(next_page,defining_attributes)
            next_df = pd.DataFrame(next_dict)
            whole_lst += [next_df]
            #print(len(whole_lst))
            if len(whole_lst[-1])>0:
                print(whole_lst[-1]['updated_timestamp'].iloc[0])
            else:
                pass
    
    
    whole_df = pd.concat(whole_lst, ignore_index = True)
    whole_df = whole_df.drop_duplicates(ignore_index = True, subset = 'order_id')
    whole_df.sort_values('updated_timestamp', ascending = False,  inplace = True, ignore_index = True)
    whole_df['token_id'] = whole_df['token_id'].astype(str)
    whole_df.to_csv(f'csvs/active_trades_for_sale_{token_address}.csv', sep = ';', index = False, encoding = 'utf-8-sig')
    
    #df_updated = df_updated.drop('Unnamed: 0', axis = 1)

    return whole_df


def get_filled_trades_from_start_day(days_prior, defining_attributes , token_address = '0xacb3c6a43d15b907e8433077b6d38ae40936fe2c', ):
    """
    get_filled_trades_from_start_day Returns all the trades that were done in the marketplace days_prior days before now

    _extended_summary_

    :param days_prior: days prior to today
    :param token_address: game address that you want to analyze
    :return: Dataframe containing all the trades
    """    


    time_start = dt.datetime.strftime(dt.datetime.now()-dt.timedelta(days = days_prior),"%Y-%m-%dT%H:%M:%S.%fZ")

    next_page = go_to_site(order_by=['updated_at','asc'],status = 'filled', page_size = '200', cursor = '',
        sell_token_address = token_address,updated_min_timestamp = time_start)


    first_dict = get_dict(next_page, defining_attributes)
    #print(next_page)
    first_df = pd.DataFrame(first_dict)
    whole_lst = [first_df]
    cursor = next_page['cursor']

    while cursor and next_page: 
        if next_page != {'message': 'Endpoint request timed out'} and next_page != {'code': 'internal_server_error',
            'message': 'The server encountered an internal error and was unable to process your request'}:
            next_page = go_to_site(order_by=['updated_at','asc'],status = 'filled', page_size = '200', 
                cursor  = cursor, sell_token_address = token_address, 
                updated_min_timestamp = time_start)
            print(whole_lst[-1].iloc[-1]['updated_timestamp'])
            try:
                next_dict = get_dict(next_page, defining_attributes)
                next_df = pd.DataFrame(next_dict)
                whole_lst += [next_df]
                cursor = next_page['cursor']
            except:
                next_dict =[]
                cursor = ''
        else:
            print('Something happened with the API')
    whole_df = pd.concat(whole_lst, ignore_index = True)
    whole_df['token_id'] = whole_df['token_id'].astype(str)
    whole_df.to_csv(f'csvs/some_filled_trades_{token_address}.csv', index = False, sep = ';', encoding = 'utf-8-sig')
    return whole_df


def number_of_cards(x):
    print(x)
    if x.name == x.shift_name and x.quality == x.shift_quality:
        number = x.shift(-1)['positive']-1
    else:
        number = x.average_sold
    return number

def number_of_cards_sold_last_x_days(df_with_filled_trades ,df_with_minimum_price,defining_attributes, coin: str, days:int = 7):
    #gets the df by the coin x
    df = df_with_filled_trades[df_with_filled_trades['coin']==coin]
    df = df[defining_attributes + ['updated_timestamp']]
    #The timestamps are not all in the same format, so I'm gonna correct that
    df.updated_timestamp = df.updated_timestamp.apply(lambda x: x[:-1] + ".000Z" if x[-4] == ':' else x)
    #transform timestamps into datetime
    df.updated_timestamp = df.updated_timestamp.apply(lambda x: dt.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ") )
    #looks at the most recent timestamp
    last_sold_time = df.iloc[-1]['updated_timestamp']
    #get's only the trades that happened at most, x days before the last trade
    last_x_days = last_sold_time-dt.timedelta(days = days)
    last_x_days_df = df[df.updated_timestamp > last_x_days]
    #Get's the average number of trades per day over the last 7 days for each card
    counter_df = last_x_days_df.groupby(defining_attributes).updated_timestamp.count()/days
    counter_df = counter_df.reset_index()
    counter_df.rename(columns = {'updated_timestamp':'average_sold'}, inplace = True)
    df_with_minimum_price = pd.merge(df_with_minimum_price, counter_df, on = defining_attributes, how = 'inner')
    return df_with_minimum_price


def get_arbitrage_from_2_currencies(currency_one:str,currency_two:str,dc_with_every_trade, 
filled_trades , currency_to_usd: dict, defining_attributes: list, days_average:int = 7,
market_percentage:int  = 0.2):
    #For each card, it compares the lowest price for each currency and calculates the difference in dollars.
    df1 = dc_with_every_trade.copy()
    #print(df1)
    #print(df1.coin.unique())
    #gets only the active trades that are selling for the coin 1
    df_currency_one = df1[df1['coin']==currency_one]
    #gets only the active trades that are selling for the coin 2
    df_currency_two = df1[df1['coin']==currency_two]
    #gets the minimum price in dollars for each card
    #print(df_currency_one)
    #print(df_currency_two)
    try:
        dfmin_currency_two = df_currency_two.groupby(defining_attributes).amount_sold.min().reset_index()
    except KeyError:
        print('Please download the data with the corrected defining_attributes.')
        sys.exit()
    #print(dfmin_currency_two)
    #print(df_currency_one.head())
    df_currency_one[currency_one + '_USD'] = df_currency_one['amount_sold']*currency_to_usd[currency_one]
    dfmin_currency_two[currency_two + '_USD'] = dfmin_currency_two['amount_sold']*currency_to_usd[currency_two]
    #print(dfmin_currency_two)
    #for the coin that I'm going to sell the cards in, selects only those that have been selling for an average of x for y days
    dfmin_currency_two = number_of_cards_sold_last_x_days(filled_trades,dfmin_currency_two,defining_attributes, currency_two, days_average)
    #print(dfmin_currency_two)
    #merges the buying df with the sell df
    #final_df = pd.merge(dfmin_currency_two[['order_id_'+currency_two,'token_id_' +currency_two,'name','rarity','quality','set',currency_two + '_USD',
     #'amount_sold']],dfmin_currency_one[['order_id_' + currency_one,'token_id_' + currency_one,'name','rarity','quality','set',
     #currency_one + '_USD', 'amount_sold']], on = ['name','rarity','quality','set'],how ='inner', suffixes=('_' + currency_two, '_' + currency_one))
    final_df = pd.merge(df_currency_one,dfmin_currency_two, on = defining_attributes,how ='inner')
    #print(final_df)
    #print(final_df)
    final_df.sort_values(defining_attributes + [currency_one + '_USD'], ascending= True)
    for i in defining_attributes:
        final_df[f'shift_{i}'] = final_df[i].shift(1,  fill_value = 0)
    #print(final_df.head(20))

    for i in range (len(final_df)):
        number = 0
        for j in defining_attributes:
            if final_df.loc[i, j] == final_df.loc[i, f'shift_{j}']:
                number +=1
        if number == len(defining_attributes):
            final_df.loc[i, 'positive']= final_df.loc[i-1,'positive']-1
        else:
            final_df.loc[i, 'positive'] = final_df.loc[i, 'average_sold']*market_percentage
        number = 0
    try:
        final_df = final_df[final_df['positive'] >= 1]
    except KeyError:
        print('Please change the defining_attributes to the correct ones.')

    #print(final_df)
    final_df['percentage'] = round(final_df[currency_two + '_USD']/final_df[currency_one + '_USD']*100 -100,2)
    final_df = final_df.sort_values(by = 'percentage', ascending = False)    

    return final_df
        

def add_strings_for_node(string):
    #To the cards that I'm going to sell it adds this so the node.js file can then use it to execute the trade.
    string = "const lst = " + string + "\n\nmodule.exports.lst = lst"
    return string

def export_to_buy_and_sell(df,percentage_lower:int, coin_to_buy = 'ETH', coin_to_sell = 'GODS', ) -> None:
    #Exports a dataframe to in the necessary format to the nde.js file
    #number of cards that I want to send to the file
    #gets the cards id that I want to buy for coin X, the price that I'm going to buy them for and the order id
    df_to_export_to_buy = df[['order_id','amount_sold_x', 'token_id']]
    #The value has to go times 10**18 and in a string form. If the coin is USDC, the value has to go as 10**6:
    df_to_export_to_buy['amount_sold_x'] = df_to_export_to_buy['amount_sold_x']*10**6
    df_to_export_to_buy['amount_sold_x'] = df_to_export_to_buy['amount_sold_x'].astype('int64')
    df_to_export_to_buy['amount_sold_x'] = df_to_export_to_buy['amount_sold_x'].astype('str')
    if coin_to_buy != 'USDC':
        df_to_export_to_buy['amount_sold_x'] = df_to_export_to_buy['amount_sold_x'] + '000000000000'
    #The token id and order id also has to go in str form
    df_to_export_to_buy['order_id'] = df_to_export_to_buy['order_id'].astype('str')
    df_to_export_to_buy['token_id'] = df_to_export_to_buy['token_id'].astype('str')
    lst_to_export_to_buy = df_to_export_to_buy.values.tolist()
    with open('react_js/nft_to_buy.js', 'w',newline='') as data_file:
        data_file.write(add_strings_for_node(str(lst_to_export_to_buy)))
    with open('react_js/coin_to_buy.txt', 'w',newline='') as data_file:
        data_file.write(coin_to_buy)


    #same thing as above but now I'm selling the cards bought above with coin Y
    

    df['amount_sold_y'] = df['amount_sold_y']*(1-percentage_lower)

    df_to_export_to_sell_divided = df[['token_id','amount_sold_y']]
    df_to_export_to_sell=df_to_export_to_sell_divided
    #I'm going to sell the card for 0.5% cheaper above the 8 percent fees
    df_to_export_to_sell['amount_sold_y'] = df_to_export_to_sell['amount_sold_y']*10**6
    df_to_export_to_sell['amount_sold_y'] = df_to_export_to_sell['amount_sold_y'].astype('uint64')
    df_to_export_to_sell['amount_sold_y'] = df_to_export_to_sell['amount_sold_y'].astype('str')
    if coin_to_sell != 'USDC':
        df_to_export_to_sell['amount_sold_y'] = df_to_export_to_sell['amount_sold_y'] + '000000000000'
    df_to_export_to_sell['token_id'] = df_to_export_to_sell['token_id'].astype('str')
    lst_to_export_to_sell =df_to_export_to_sell.values.tolist()
    with open('react_js/nft_to_sell.js', 'w',newline='') as data_file:
        data_file.write(add_strings_for_node(str(lst_to_export_to_sell)))
    with open('react_js/coin_to_sell.txt', 'w',newline='') as data_file:
        data_file.write(coin_to_sell)

    
    
    
def execute_trades(df, coin_to_buy: str = 'ETH', coin_to_sell: str = 'GODS', number_of_total_cards: int = 0, 
cards_each_time:int = 10, percentage_above:int = 20, price_reduction = 0.005) ->None :
    #Selects cards that are with a margin of 20% and only the top 100 cards (in case there are a lot of them and I don't have money).
    df = df[df['percentage']>percentage_above]
    if number_of_total_cards >0:
        df = df.iloc[:number_of_total_cards]
    #Sells the cards 10 at a time because the marketplace API only allows me to make 10 trades per second.
    lst = []
    for i in range(int(len(df)/cards_each_time)+1):
        if i<len(df)/cards_each_time:
            new_df = df.iloc[cards_each_time*(i):(cards_each_time*(i+1))]
        else:
            new_df = df.iloc[cards_each_time*(i):]
        export_to_buy_and_sell(new_df, coin_to_buy = coin_to_buy,coin_to_sell = coin_to_sell, percentage_lower=price_reduction)
        p1 = execute_js('react_js/buy.js')
        if p1 == False:
            print("Something went wrong and we weren't able to buy and sell any of the cards")
            sys.exit()
        p2 = execute_js('react_js/sell.js')
        lst +=[p1,p2]
    if all(lst):
        print(f"Everything worked fine, we bought and put in the market {len(df)} NFT's!")
    else:
        print("Something went wrong and we weren't able to buy and sell the cards")
            


       
    
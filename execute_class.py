from class_for_IMX import game

hro = game('0x9e0d99b864e1ac12565125c5a82b59adea5a09cd')
print(hro.name)
#hro.change_defining_attributes(['type'])
print(hro.get_nft_properties())
hro.download_filled_trades(3)
hro.download_active_trades()
print(hro.filled_trades.coin.value_counts())
'''meh = hro.determine_arbitrage('GODS','ETH', daily_market_percentage=1)
print(meh)
hro.execute_trades(40, 0.005, 0, 10)'''

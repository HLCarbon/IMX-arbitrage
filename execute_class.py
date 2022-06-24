from class_for_IMX import game

hro = game('0x4fb656d9c7ad031e4eaad15e92ff10af75d8d621')
print(hro.name)
#hro.change_defining_attributes(['type'])
print(hro.get_nft_properties())
hro.download_filled_trades(10)
hro.download_active_trades()
print(hro.filled_trades.coin.value_counts())
meh = hro.determine_arbitrage('GODS','ETH', daily_market_percentage=1)
print(meh)
hro.execute_trades(40, 0.005, 0, 10)

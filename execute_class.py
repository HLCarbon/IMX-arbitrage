from class_for_IMX import game
import pandas as pd

hro = game('0xee972ad3b8ac062de2e4d5e6ea4a37e36c849a11')
print(hro.name)
#hro.change_defining_attributes(['name_hro'])
#print(hro.get_metadata_schema())
hro.download_filled_trades(10)
hro.download_active_trades()
print(hro.filled_trades.type2.value_counts())
meh = hro.determine_arbitrage('GODS','ETH', daily_market_percentage=20)
print(meh)
meh.to_csv('lol.csv', encoding = 'utf-8-sig', sep = ';', index = False)
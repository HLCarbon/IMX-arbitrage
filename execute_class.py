from class_for_IMX import game
import pandas as pd

hro = game('Hro')
print(hro.name)
hro.change_defining_attributes(['name_hro'])
#print(hro.get_metadata_schema())
hro.download_filled_trades(10)
hro.download_active_trades()
hro.determine_arbitrage('ETH','USDC', daily_market_percentage=0.2).to_csv('lol.csv', encoding = 'utf-8-sig', sep = ';')
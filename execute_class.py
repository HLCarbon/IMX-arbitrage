from class_for_IMX import game

hro = game('Hro')
print(hro.name)
hro.change_defining_attributes(['name_hro'])
#print(hro.get_metadata_schema())
hro.download_filled_trades(2)
hro.download_active_trades()
print(hro.determine_arbitrage('ETH','GOG', daily_market_percentage=1))
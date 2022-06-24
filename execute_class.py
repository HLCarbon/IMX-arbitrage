from class_for_IMX import game

hro = game('0xee972ad3b8ac062de2e4d5e6ea4a37e36c849a11')
print(hro.name)
#print(hro.get_metadata_schema())
hro.download_filled_trades(10)
hro.download_active_trades()
print(hro.filled_trades.coin.value_counts())
meh = hro.determine_arbitrage('ETH','USDC', daily_market_percentage=1)
print(meh)
hro.execute_trades(40, 0.005, 0, 10)

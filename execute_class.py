from class_for_IMX import game

gogh = game('0xee972ad3b8ac062de2e4d5e6ea4a37e36c849a11')
print(gogh.name)

gogh.load_filled_trades(9)
gogh.load_active_trades()
print(gogh.determine_arbitrage('ETH','GOG', daily_market_percentage=100)[['image','percentage']])
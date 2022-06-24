from class_for_IMX import game

hro = game('0x8cb332602d2f614b570c7631202e5bf4bb93f3f6')
print(hro.name)
hro.change_defining_attributes(['name_hro'])
print(hro.get_nft_properties())
hro.download_filled_trades(3)
hro.download_active_trades()
hro.get_value_counts
meh = hro.determine_arbitrage('ETH','USDC', daily_market_percentage=0.1)
print(meh[['name_hro', 'percentage']])
hro.execute_trades(40, 0.135, 0, 10)
#Since I didn't add the react.js file, this will always end in an error. The last phrase should be :'Something went wrong and we weren't able to buy and sell any of the cards'.
 
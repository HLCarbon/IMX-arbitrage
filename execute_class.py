from class_for_IMX import game

gogh = game('0xee972ad3b8ac062de2e4d5e6ea4a37e36c849a11')
print(gogh.name)

#gogh.download_filled_trades(2)

gogh.get_filled_trades(4)
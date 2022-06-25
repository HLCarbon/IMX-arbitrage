# IMX-arbitrage
Using Python to buy and sell cards to earn a profit

### Welcome to my arbitrage program!
[IMX](https://market.immutable.com/) is an L2 NTF market that hosts plenty of games. Some of these games have NTF's that are exactly the same apart of their ID:

**Eample**:
|Case 1 | Case 2|
|---|---|
| ![image](https://user-images.githubusercontent.com/97365179/175778369-257db92f-01fc-4286-b06f-a394f22d3502.png)   |  ![image](https://user-images.githubusercontent.com/97365179/175778369-257db92f-01fc-4286-b06f-a394f22d3502.png) |
|ID: 2022   |ID: 1000   |
|Price : 3.5 GODS (1.75$)    |Price: 0.0017 ETH (2.00$)   |
                      
What this program does is finding the same type of NFT's (in this example, playing cards of the game [Gods Unchained](https://godsunchained.com/)) where someone is selling one card for cheap (in USD terms) and where that same card is selling for a higher price in another currency. In the example above, the program would buy the first card for 3.5 GODS and then put a sell order on the market for 0.0017 ETH (or slightly lower, if you so choose). The program was bult with the intent of being run once a day, but the parameters can be easilally be changed so it is run multiple times a day or once a week, etc.

At this moment, the program will always end in an error. The last part is executing a node.js file to buy and sell the NFT's automatically. The file reads the coin that it needs to buy the NFT's for in the file [react_js/coin_to_buy.txt](https://github.com/HLCarbon/IMX-arbitrage/blob/main/react_js/coin_to_buy.txt) and the same thing for the selling coin. Since the react.js file contains sensible information, I will not add it to this project. This react.js file is a variation of the [ImmutableX-Sell-Orders](https://github.com/AkramDevelopment/ImmutableX-Sell-Orders) from the user [AkramDevelopment](https://github.com/AkramDevelopment).


#### How this works:

An example of a typical run would for the game **Guild of Guardians** would be:

gog.game('0xee972ad3b8ac062de2e4d5e6ea4a37e36c849a11')

>Instantiates the class game.

gog.download_filled_trades(10)

>This will download all the trades made on the IMX marketplace for the game Guild of Guardians over the last 10 days. 

gog.download_active_trades

>This will download all the active trades made on the IMX marketplace for the game Guild of Guardians.

gog.get_value_counts()

>This will go through the filled trades and determine which coins are being used to trade and sell NFT's. From here, you choose which coins you want to buy and sell the NFT's with.

gog.determine_arbitrage('GODS','ETH', daily_market_percentage=0.1)

>This is where most of the magic happens. First, it determines the price of BOTH of the coins in USD. Second, i creates two lists: one with the active trades for the coin GODS, and another with the active trades for the coin ETH. For the coin ETH, it groups every type of NFT (in the case above, it groups all the cards that have that image) and determines the lowest price that the card is selling for (in ETH). For the table with the GODS coin, it sorts every group of NFT and orders it by price in ascending order. For each type of NFT, it looks at the past 10 days, sums the number of times each type of NFT was sold and divides it by 10 (parameter on the `gog.download_filled_trades(10)`). It then multiplies that number by 0.1. The number of NFT's that the program will look at wil be average sold in the last 10 days \* 0.1. 
>
>An example should help: Imagine that we were looking at the game Gods Unchained and in the last 10 days the card **Echophon, Atlantean Hydra** was sold 305 times. We would like to ocuppy, at most, 10% of the market (the 0.1 in the function). Then, at most, the program will look at the cheapest 305/10 \* 0.1 = 3 (rounded to int) **Echophon, Atlantean Hydra** (selling for GODS). 
>
>It would then compare, all in USD, the price of the NFT's in GODS with the cheapest NFT for each type in ETH and calculate the difference. It sorts by the percentage difference in descending order.

gog.execute_trades(40, 0.005, 100, 10)
>Executes the buy and sell. It goes through the Dataframe created in the previous function and removes those that have an arbitrage percentage less than 40%. To the lowest price determined for the coin ETH (the one we want to sell the NFT's for) it lowers it by 0.5% (so our trade happears fisrt). After that it only selects the first 100 to buy/sell (we might not have enough money to execute all trades)(There are NFT's for 0.02$). The trades are executed 10 at a time. The IMX API only let's me do 10 trades per second at the time of writing.


How this is organized:
- [**functions folder**](https://github.com/HLCarbon/IMX-arbitrage/tree/main/functions) - Contains a python file with the functions used in this project.
- [**class_for_IMX.py**](https://github.com/HLCarbon/IMX-arbitrage/blob/main/class_for_IMX.py) - Contains the class used in this project. This is the base of the whole project. Everything is based on this class.
- [**execute_class.py**](https://github.com/HLCarbon/IMX-arbitrage/blob/main/execute_class.py) - This is the file used to work with the class. This is the file that each person should change to perform the desired actions.
- [**csvs**](https://github.com/HLCarbon/IMX-arbitrage/tree/main/csvs) - Folder to place the csvs downloaded/used by the class. There are two types of files:
   - Active trades
   - Filled trades
   
The file names are then suffixed with the address of the game that you want to analyze.

### Other functions
game.get_nft_properties
>Gives you the attributes that you can use to group the NFT's. At the time of writing, the only ones available are name and image.

game.change_defining_attributes
>In most NFT games you can just use the predifined one (image). However, if you want to change the defining attributes, you can do so with this function. It takes a list so you can add multiple deffining attributes.

**Note**

For the game Hro, the images change slightly since they have the different ID's and those are implemented in the image. So even though the type of cards are the same, the image url is different. The same happens with the name of the card. So I built an exception. If you change the defining attributes to ['name_hro'] the program will remove the first two rods of the name (which is the year it was minted and the ID), leaving only the real card name, permiting us to group them by card.

## Hope you enjoy

***

The goal is to eventually take this to AWS and once a day run the program to buy and sell NTF's in the games of my choosing.

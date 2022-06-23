# IMX-arbitrage
### Using Python to buy and sell cards to earn a profit ###

Welcome to my arbitrage program.
How this is organized:
- [**functions folder**](https://github.com/HLCarbon/IMX-arbitrage/tree/main/functions) - Contains a python file with the functions used in this project.
- [**class_for_IMX.py**](https://github.com/HLCarbon/IMX-arbitrage/blob/main/class_for_IMX.py) - Contains the class used in this project. This is the base of the whole project. Everything is based on this class.
- [**execute_class.py**](https://github.com/HLCarbon/IMX-arbitrage/blob/main/execute_class.py) - This is the file used to work with the class. This is the file that each person should change to perform the desired actions.
- [**csvs**](https://github.com/HLCarbon/IMX-arbitrage/tree/main/csvs) - Folder to place the csvs downloaded/used by the class. There are two types of files:
   - Active trades
   - Filled trades
The file names are then suffixed with the address of the game that you want to analyze.

The goal is to eventually take this to AWS and once a day run the program to buy and sell NTF's in the games of my choosing.

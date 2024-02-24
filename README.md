# Basic Copy Trade

This script allows to copy a one to one trade copying which means limited for only one account for coppiers. 
Multiple coppier version can be implemented also.

Exception Handling is not done.

## Table of Contents

- [Details](#Details)
- [Installation](#Installation)
- [Dependencies](#Dependencies)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Details

### Why ccxt ? 
Because ccxt allows to trade almost each well-known exchange, so leaders and coppiers exchange doesn't have to be the same. Default setted binance futures.
ccxt has fee discount for some exhanges and binance futures included. check for more indormation: 

*https://github.com/ccxt/ccxt#certified-cryptocurrency-exchanges*

### How to change usdt per order and leverage ?
At *main.py* you can change those variables before launch, those variables are not related with leaders positions, have to be setted before launching

### Should you use telegram for notifications ?
No it is additional feature, you can delete the telegram_msg_sender.send_message_to_developer() methods on long-short enter-exit methods there are 4 calling on main.

If you want to use it take your user id, on telegram you can use @userinfobot 

And bot can be handled with @botfather on telegram.

### How many assets are usable
All assets are usablle on binance futures so there is no limit, default there are 5 assets at symbols.txt file. please follow the given format. 

*BTCUSDT*
*SOLUSDT*
*DOGEUSDT*

Please do not forget to delete last empty line on txt file for avoid exceptions.

  
# Installation

Clone the repository with git:

*git clone https://github.com/denizyts/CopyTrader.git*

or just download the zip.


## Dependencies
Latest versions probably will be enough.

- *Python 3.11.8*
- *ccxt 4.0.80*


## Usage

*-python3 main.py*

For Ubuntu Droplet: 
 <span style="color: red;">*nohup python3 main.py*</span>

  this nohup command allows it to run at the back.






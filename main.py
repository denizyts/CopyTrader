import ccxt
from config import leader_api, leader_secret, copier_api, copier_secret
import symbolTextReader;
import telegram_msg_sender

class main:
 

 def __init__(self):  
  #create leader and copier exchange objects
  self.leader_exchange = ccxt.binance({
    'apiKey': leader_api,
    'secret': leader_secret,
    'options': {
        'defaultType': 'future'
    } ,
    'enableRateLimit': True
   });

  self.copier_exchange = ccxt.binance({
    'apiKey': copier_api,
    'secret': copier_secret,
    'options': {
        'defaultType': 'future'
    } ,
    'enableRateLimit': True
   });


  self.leader_positions = {};
  self.copier_positions = {};
  self.symbols = symbolTextReader.reader();
  self.in_position = {}; self.copier_position_side = {};
  self.usdt_per_order = 10;
  self.leverage = 5;

  for symbol in self.symbols:
   self.in_position[symbol] = False;   #initialize the in_position dictionary with False values for each symbol.
   self.copier_position_side[symbol] = None;  #initialize the copier_position_side dictionary with None values for each symbol.
  


 def fetch_leader_positions(self):
  self.leader_positions = self.leader_exchange.fetch_account_positions(symbols=self.symbols);

 def fetch_copier_positions(self):
  self.copier_positions = self.copier_exchange.fetch_account_positions(symbols=self.symbols);
  for position in self.copier_positions:
   if position["entryPrice"] != None:
    self.copier_position_side[position[0]["symbol"]] = position["side"];
    self.in_position[position[0]["symbol"]] = True;  
   else: 
    self.copier_position_side[position[0]["symbol"]] = None;
    self.in_position[position[0]["symbol"]] = False;
 

 def leader_new_position_check(self):            #checks if there is a new position opened by the leader.
  for position in self.leader_positions:
   if position[0]["entryPrice"] != 0 and self.in_position[position[0]["symbol"]] == False: 
    self.handle_new_position(position);
  
   if position["side"] != None and self.copier_position_side[position[0]["symbol"]] != None:
    if self.copier_position_side[position[0]["symbol"]] != position["side"]:
     self.handle_reverse_position(position);   #if a coppier position is opposite side of the leader position, this function will be called.
    else: #they are same side
     continue;

 def leader_closed_position_check(self): #checks if there is a position closed by the leader.
  for position in self.leader_positions:
   if position["entryPrice"] == None and self.in_position[position[0]["symbol"]] == True: #for each symbol, if there is no open position for the leader and there is an open position for the copier.
    self.handle_closed_position(position);
   else: #both are in position or both are not in position.
    continue;
   
 def check_copier_balance(self):
  free_balance = self.copier_exchange.fetch_free_balance()["USDT"];
  if free_balance < self.usdt_per_order:
   telegram_msg_sender.send_message_to_developer(f"Copier account does not have enough balance to open a new position with setted usdt_per_order value. Please check the copier account balance.");
   exit();
  else:
   return True;


 def leverage_setter(self):
  for symbol in self.symbols:
   self.copier_exchange.set_leverage(self.leverage , symbol);


 def handle_new_position(self , position): #this function will be called when a new position opened by the leader and there is no open position for the coppier.
  amount = (self.usdt_per_order*self.leverage / position[0]["entryPrice"]); #calculate the amount of the position.

  if position["side"] == "long":
   self.enter_long(position , amount);
  else:
   self.enter_short(position , amount);


#This function required because leader and copier might be opposite sides at same asset. 
 def handle_reverse_position(self , position):    #param position is position of the leader.
 
 #fetch position method accepts symbols parameter as array. So we need to create a list with the symbol.
 #here fetched only 1 symbols position
  coppier_position = self.copier_exchange.fetch_account_positions(symbols=[position[0]["symbol"]]); 
  amount = coppier_position[0]["contracts"]; #get the amount of the position.
 
  if coppier_position["side"] == "long": 
   self.exit_long(position , amount); #first exit the long position.
   required_amount = (self.usdt_per_order*self.leverage / position[0]["entryPrice"]); #calculate the amount of the new position.
   self.enter_short(position , required_amount); #enter the short position.
  else:
   self.exit_short(position , amount); #first exit the short position.
   required_amount = (self.usdt_per_order*self.leverage / position[0]["entryPrice"]); #calculate the amount of the new position.
   self.enter_long(position , required_amount); #enter the long position.


#again param position is position of the leader.
 def handle_closed_position(self , position): #this function will be called when a position closed by the leader and there is an open position for the coppier.
 
  coppier_position = self.copier_exchange.fetch_account_positions(symbols=[position[0]["symbol"]]); #get the amount of the position.
  amount = coppier_position[0]["contracts"]; #get the amount of the position.
 
  if coppier_position["side"] == "long":
   self.exit_long(position , amount);
  else:
   self.exit_short(position , amount);


 def enter_long(self , symbol , amount):  #just enters long.
  if self.check_copier_balance(): #if true
   self.copier_exchange.create_market_buy_order(symbol=symbol , amount=amount);
   telegram_msg_sender.send_message_to_developer(f"New long position opened by the leader for {symbol} with {self.usdt_per_order} USDT");

 def enter_short(self , symbol , amount): #enters short
  if self.check_copier_balance(): #if true
   self.copier_exchange.create_market_sell_order(symbol=symbol , amount=amount);
   telegram_msg_sender.send_message_to_developer(f"New short position opened by the leader for {symbol} with {self.usdt_per_order} USDT");

 def exit_long(self , symbol , amount): #exits long
  if(self.in_position[symbol] == True): #checks if there is an open position for the symbol.
   self.copier_exchange.create_market_sell_order(symbol=symbol , amount=amount);
   telegram_msg_sender.send_message_to_developer(f"Long position closed for {symbol} with {amount} contracts.");

 def exit_short(self , symbol , amount): #exits short
  if(self.in_position[symbol] == True): #checks if there is an open position for the symbol.
   self.copier_exchange.create_market_buy_order(symbol=symbol , amount=amount);
   telegram_msg_sender.send_message_to_developer(f"Short position closed for {symbol} with {amount} contracts.");


if __name__ == "__main__":
 main = main();
 main.leverage_setter();
 while True:
  main.fetch_leader_positions();
  main.fetch_copier_positions();
  main.leader_new_position_check();
  main.leader_closed_position_check();
   
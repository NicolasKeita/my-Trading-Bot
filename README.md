# :dollar: my-Trading-Bot
{tags : ongoing project, riddles.io, cryptocurrency, volume profile}

I created a bot able to buy / sell stocks.

How it works ?
<pre>
Input		: candlestick  
Input example   : "USDT_ETH,1516147200,1090.1676815,1022.16791604,1023.1,1029.99999994,1389783.7868468"
formatted as      pair,date,high,low,open,close,volume
</pre>
<pre>
Output		: "buy" or "sell" or "pass"
Output example  : "buy USDT_ETH 0.01"
</pre>


The engine sending inputs and receiving outputs is provided by riddles.io's platform
https://playground.riddles.io/competitions/crypto-trader

TEST THE BOT :

There is a gui program able to test the bot in the directory "ai-bot-workspace".
Change the program's settings to mine :
![Settings](https://ibb.co/k3YxPR6)

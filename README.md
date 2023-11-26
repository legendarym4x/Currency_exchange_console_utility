## Homework 04

In this task, we wrote a console utility that returns the EUR and USD exchange rates of PrivatBank for the past few days. 

We have set a limit so that the utility can find out the exchange rate no more than for the last 10 days. 

Aiohttp client was used to request the API. 

Added handling of possible errors during network requests.

An example of work (the argument after `"main.py"` indicates the output of the exchange rate for the required number of days starting from today):

`python main.py 2`

We save the result of the script to a file `rates.json`.

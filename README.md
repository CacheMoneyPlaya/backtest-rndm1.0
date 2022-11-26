
# Backtesting Fair Value Gap trading strategy

Backtesting of a fair value gap trading strategy on a rolling 300 data point input
Executable with M1-M30 timeframes, selectable exchanges and assets i.e.:
python3 main.py -a 'AVAX' -t '15m' -d '2021-11-03' -e 'binance'

## TODO:
- Move FVG shading anchor to start of detection date &#x2611;
- Filter out invalidated FVG zones at point of consumption &#x2611;
- Begin defining a set of entry strats depending on the last n-(10 to 20) candle movements &#x2611;
- Build in entry/exit position commands + fit to 1:1.5 or something &#x2611;
- Clean up a load of stuff for plug and play of strats, bit messy atm as i was just wanting to get soemthing working lol &#x2611;
- Introduce mutli-asset asyncio executions with complete PnL charting after
- Come up with some better research into FVG delta qualifications
- Introduce some proper risk/reward ratios


- Backtested with 10x leverage and numbers are shown in the above PnL chart, cant be true surely? Got to be some fuckery going on

![Backtest](https://github.com/CacheMoneyPlaya/backtest-rndm1.0/blob/main/Charts/Screenshot%202022-11-04%20at%2022.52.38.png?raw=true)
![FVG detection](https://github.com/CacheMoneyPlaya/backtest-rndm1.0/blob/main/Charts/Screenshot_2022-11-01_at_19.11.03.png?raw=true)
![The numbers Mason](https://tenor.com/view/what-do-they-mean-random-numbers-gif-10654449.gif)

## Backtests:
- ATOM - 10x Leverage - 1000USD -> 6521.90USD - M15 1 year (Trade EV, +EV: 324, -EV: 120)
  Config: -60 Rolling Window, 0.99/1.01, M15
- SUSHI - 10x Leverage - 1000USD -> 9044.50USD - M15 1 year (Trade EV, +EV: 373, -EV: 143)
  Config: -60 Rolling Window, 0.99/1.01, M15

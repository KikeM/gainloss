# gainloss
*FIFO PnL calculator for trading activity.*

Each trade consists of:
* time-like instant
* symbol 
* direction
* price
* quantity

## CLI

```bash
pnl --help
```
shows the CLI parametrization
```
Usage: pnl [OPTIONS]

Options:
  -p, --path TEXT         CSV file with trades.
  --print-trades BOOLEAN  Print trades matrix.  [default: False]
  --help                  Show this message and exit.
```
## Example

```bash
pnl -p trades.csv --print-trades
```
on the example `tests/trades.csv` file
```
TIME,SYMBOL,SIDE,PRICE,QUANTITY
2,AAPL,B,32.58,300
2,GOOG,S,1100.48,200
7,AAPL,S,40.07,3000
10,GOOG,S,1087.07,300
12,GOOG,B,1034.48,500
```
becomes
```
  OPEN_TIME    CLOSE_TIME  SYMBOL      QUANTITY    PNL  OPEN_SIDE    CLOSE_SIDE      OPEN_PRICE    CLOSE_PRICE
-----------  ------------  --------  ----------  -----  -----------  ------------  ------------  -------------
          2             7  AAPL             300   2247  B            S                    32.58          40.07
          2            12  GOOG             200  13200  S            B                  1100.48        1034.48
         10            12  GOOG             300  15777  S            B                  1087.07        1034.48

PnL = 31224.00
```

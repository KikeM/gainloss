HEADER_CLOSED = "Open,Close,Symbol,qty,PnL,PnL (fees),Adquisicion, Transmision, Side (E),Side (X),(E)ntry, e(X)it, Fees (E), Fees (X)"
HEADER_CLOSED = HEADER_CLOSED.split(",")


class TradeNames:

    TIME = "TIME"
    SYMBOL = "SYMBOL"
    SIDE = "SIDE"
    BUYING = "buying"
    PRICE = "PRICE"
    FEES = "transactionCost"
    QUANTITY = "QUANTITY"


class Direction:

    BUY = "B"
    SELL = "S"

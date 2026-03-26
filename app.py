from fastapi import FastAPI
from brain import generate_signal
from market import get_data

app = FastAPI()

@app.get("/signal/{symbol}")
def get_signal(symbol: str):
    df = get_data(symbol)

    signal = generate_signal(df)

    if signal:
        return {"status": "signal", "data": signal}

    return {"status": "no_trade"}

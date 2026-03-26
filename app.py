from fastapi import FastAPI
from brain import generate_signal
from market import get_multi_tf

app = FastAPI()

@app.get("/signal/{symbol}")
def get_signal(symbol: str):

    df_m5, df_h1 = get_multi_tf(symbol)

    signal = generate_signal(df_m5, df_h1)

    if signal:
        return {"status": "signal", "data": signal}

    return {"status": "no_trade"}

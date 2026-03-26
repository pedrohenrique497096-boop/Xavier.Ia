from fastapi import FastAPI
from brain import generate_signal
from market import get_multi_tf

app = FastAPI()

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/signal/{symbol}")
def get_signal(symbol: str):
    try:
        df_m5, df_h1 = get_multi_tf(symbol)

        if df_m5.empty or df_h1.empty:
            return {"status": "error", "msg": "dados vazios"}

        signal = generate_signal(df_m5, df_h1)

        if signal:
            return {"status": "signal", "data": signal}

        return {"status": "no_trade"}

    except Exception as e:
        return {"status": "error", "msg": str(e)}

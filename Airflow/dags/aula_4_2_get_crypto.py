from pathlib import Path
import yfinance
from airflow.decorators import dag, task
from airflow.macros import ds_add
import pendulum

TICKERS = [
     "BTC",
     "ETH",
     "DOGE",
     "AVAX"
]

#ds traz as datas via airflow
#None as faz serem opcionais
@task()
def get_history(ticker, ds=None, ds_nodash=None):
    file_path = f"/home/paulovictor/workspace/airflow-workspace/Airflow/dags/datalake/crypto/{ticker}/{ticker}_{ds_nodash}.csv"
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    yfinance.Ticker(ticker).history(
        period ="1d",
        interval = "1h",
        start = ds_add(ds, -1),
        end = ds,
        prepost = True
    ).to_csv(file_path)

@dag(
    schedule_interval = "0 0 * * 2-6",
    start_date = pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup = True
)
def aula_4_2_get_crypto_dag():
    for ticker in TICKERS:
        get_history.override(task_id = ticker, pool="small_pool")(ticker)

dag = aula_4_2_get_crypto_dag()
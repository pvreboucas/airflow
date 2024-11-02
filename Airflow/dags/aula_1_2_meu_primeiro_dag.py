from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

#instância do dag com os parâmetros de rotina
with DAG(
    'aula_1_2_meu_primeiro_dag',
    start_date=days_ago(2),
    schedule_interval='@daily'
) as dag:
    #instância das tarefas do meu_primeiro_dag
    tarefa_1 = EmptyOperator(task_id = 'tarefa_1')
    tarefa_2 = EmptyOperator(task_id = 'tarefa_2')
    tarefa_3 = EmptyOperator(task_id = 'tarefa_3')
    tarefa_4 = BashOperator(
        task_id = 'cria_pasta',
        bash_command = ' mkdir -p "/home/paulovictor/workspace/airflow-workspace/Airflow/pasta={{data_interval_end}}/" '
    )

    #ordem de execução das tarefas
    #as tarefas 2 e 3 serão executadas após a conclusão da tarefa 1
    tarefa_1 >> [tarefa_2, tarefa_3]
    #a tarefa 4 será executada após a conclusão da tarefa 3
    tarefa_3 >> tarefa_4
   
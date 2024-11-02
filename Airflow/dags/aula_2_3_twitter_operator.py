#import sys
#sys.path.append("Airflow")

from airflow.models import BaseOperator, DAG, TaskInstance
from aula_2_2_twitter_hook import TwitterHook
from datetime import datetime, timedelta
import json
from os.path import join
from pathlib import Path
from os import makedirs, path

class TwitterOperator(BaseOperator):

    template_fields = ["query", "file_path", "start_time", "end_time"]    

    def __init__(self, file_path, end_time, start_time, query, **kwargs):
        self.file_path = file_path
        self.end_time = end_time
        self.start_time = start_time
        self.query = query
        super().__init__(**kwargs)
    
    def create_parent_folder(self):
        #(Path(self.file_path).parent).mkdir(parents=True, exist_ok=True)
        makedirs(path.dirname(self.file_path), exist_ok=True)


    #método padrão de BaseOperator
    def execute(self, context):
        #local_time_zone = datetime.now().astimezone().tzname()
        #TIMESTAMP_FORMAT = f"%Y-%m-%dT%H:%M:%S.00{local_time_zone}:00"

        end_time = self.end_time
        start_time = self.start_time
        query = self.query

        self.create_parent_folder()

        with open(self.file_path, "w") as output_file:
            for pg in TwitterHook(end_time, start_time, query).run():
                json.dump(pg, output_file, ensure_ascii=False)
                output_file.write("\n")

#esse if garante que o que há dentro dele só será rodado se alguém executar este arquivo com o comando: python3 aula_2_twitter_hook.py
#mas não rodará se essa classe for importada em outro script
if __name__ == "__main__":
    local_time_zone = datetime.now().astimezone().tzname()
    TIMESTAMP_FORMAT = f"%Y-%m-%dT%H:%M:%S.00{local_time_zone}:00"
    end_time = datetime.now().strftime(TIMESTAMP_FORMAT)
    start_time = (datetime.now() + timedelta(-1)).date().strftime(TIMESTAMP_FORMAT)
    query = "datascience"
    file_path = join("../../datalake/twitter_datascience",
                f"extract_date={datetime.now().date()}",
                f"aula_2_3_datascience_{datetime.now().strftime('%Y%m%d')}.json")

    with DAG(dag_id = "aula_2_3_TwitterDag", start_date=datetime.now()) as dag:
        to = TwitterOperator(file_path =file_path, query=query, start_time=start_time, end_time=end_time, task_id="aula_2_3_test_twitter_run")
        ti = TaskInstance(task=to)
        to.execute(ti.task_id)
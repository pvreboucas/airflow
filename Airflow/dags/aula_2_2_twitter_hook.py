from airflow.providers.http.hooks.http import HttpHook
from datetime import datetime, timedelta
import requests, json

class TwitterHook(HttpHook):

    def __init__(self, end_time, start_time, query, conn_id=None):
        self.conn_id = conn_id or "twitter_default"
        self.end_time = end_time
        self.start_time = start_time
        self.query = query
        super().__init__(http_conn_id=self.conn_id)

    def create_url(self):
        local_time_zone = datetime.now().astimezone().tzname()
        TIMESTAMP_FORMAT = f"%Y-%m-%dT%H:%M:%S.00{local_time_zone}:00"

        end_time = self.end_time
        start_time = self.start_time
        query = self.query

        tweet_fields = "tweet.fields=author_id,conversation_id,created_at,id,in_reply_to_user_id,public_metrics,lang,text"
        user_fields = "expansions=author_id&user.fields=id,name,username,created_at"

        url_raw = f"{self.base_url}/2/tweets/search/recent?query={query}&{tweet_fields}&{user_fields}&start_time={start_time}&end_time={end_time}"
        return url_raw
    
    def connect_to_endpoint(self, url, session):
        request = requests.Request("GET", url)
        prep = session.prepare_request(request)
        self.log.info(f"URL:{url}")
        #run_and_check classe do httpHook
        return self.run_and_check(session, prep, {})
    
    def paginate(self, url_raw, session):
        lsita_json_response = []
        response = self.connect_to_endpoint(url_raw, session)
        json_response = response.json()
        lsita_json_response.append(json_response)
        limite_paginacao = 100
        contador = 1

        #paginação
        while "next_token" in json_response.get("meta",{}) and contador < limite_paginacao:
            next_token = json_response['meta']['next_token']
            url = f"{url_raw}&next_token={next_token}"
            response = self.connect_to_endpoint(url, session)
            json_response = response.json()
            lsita_json_response.append(json_response)
            contador += 1
        return lsita_json_response

    #função padrão de hoooks para execução
    def run(self):
        session = self.get_conn()
        url_raw = self.create_url()
        return self.paginate(url_raw, session)
    
#esse if garante que o que há dentro dele só será rodado se alguém executar este arquivo com o comando: python3 aula_2_twitter_hook.py
#mas não rodará se essa classe for importada em outro script
if __name__ == "__main__":
    local_time_zone = datetime.now().astimezone().tzname()
    TIMESTAMP_FORMAT = f"%Y-%m-%dT%H:%M:%S.00{local_time_zone}:00"
    end_time = datetime.now().strftime(TIMESTAMP_FORMAT)
    start_time = (datetime.now() + timedelta(-1)).date().strftime(TIMESTAMP_FORMAT)
    query = "datascience"

    for pg in TwitterHook(end_time, start_time, query).run():
        print(json.dumps(pg, indent=4, sort_keys=True))
    
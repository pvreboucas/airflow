from datetime import datetime, timedelta
import os, requests, json

#montando url
local_time_zone = datetime.now().astimezone().tzname()
TIMESTAMP_FORMAT = f"%Y-%m-%dT%H:%M:%S.00{local_time_zone}:00"
end_time = datetime.now().strftime(TIMESTAMP_FORMAT)
start_time = (datetime.now() + timedelta(-1)).date().strftime(TIMESTAMP_FORMAT)

query = "datascience"

tweet_fields = "tweet.fields=author_id,conversation_id,created_at,id,in_reply_to_user_id,public_metrics,lang,text"
user_fields = "expansions=author_id&user.fields=id,name,username,created_at"

url_raw = f"https://labdados.com/2/tweets/search/recent?query={query}&{tweet_fields}&{user_fields}&start_time={start_time}&end_time={end_time}"

#Montando headers
#recupera a token de uma ambiente de variável
bearer_token = os.environ.get("BEARER_TOKEN")
headers = {"Authorization":"Bearer{}".format(bearer_token)}
response = requests.request("GET", url_raw, headers=headers)

#imprime json
json_response = response.json()

print(json.dumps(json_response, indent=4, sort_keys=True))

#paginação
while "next_token" in json_response.get("meta",{}):
    next_token = json_response['meta']['next_token']
    url = f"{url_raw}&next_token={next_token}"
    response = requests.request("GET", url, headers=headers)
    print(json.dumps(json_response, indent=4, sort_keys=True))
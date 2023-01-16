import requests
from datetime import date
from flask import request,Flask
from twilio.twiml.messaging_response import MessagingResponse
app=Flask(__name__)
headers={
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "2e86c7171emsh0080f7daddd35aap1ace40jsn875245c19159"
    }

standings = requests.request("GET", "https://api-football-v1.p.rapidapi.com/v3/standings?league=39&season=2022", headers=headers)
standings=standings.json()
standings=standings["response"]

games = requests.request("GET", "https://api-football-v1.p.rapidapi.com/v3/fixtures?league=39&season=2022", headers=headers)
games=games.json()
games=games["response"]

  
        
@app.route("/",methods=['POST','GET'])
def response_sms():
    msg=request.values.get("Body","").lower().lstrip()
    resp=MessagingResponse()
    output=""
    if msg=="today":
        today=date.today()
        for game in games:
            if game["fixture"]["date"][-17]==today:
                output += f"{ game['teams']['home']['name']} vs {game['teams']['away']['name']} @ {game['fixture']['date'][10:][-9]} UTC\n"

    elif msg=="standings":
        i=0
        for team in standings[0]["standings"]:
            i+=1
            output += f"{team['team']['name']}, rank={i}\n"
            
    resp.message(output)
    return "hello"


if __name__=="__main__":
    app.run()
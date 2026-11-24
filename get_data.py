"""Download daily MLB box scores and derive player game batting observations."""
import argparse,csv,datetime as dt,json,time,urllib.request
BASE='https://statsapi.mlb.com/api/v1'
def fetch(path):
 with urllib.request.urlopen(BASE+path,timeout=30) as response: return json.load(response)
def extract(box,day):
 rows=[]
 for side in ('home','away'):
  for player in box['teams'][side]['players'].values():
   batting=player.get('stats',{}).get('batting',{}); at_bats=batting.get('atBats',0)
   if at_bats:
    rows.append({'player_id':str(player['person']['id']),'date':day,'performance':batting.get('hits',0)/at_bats,'at_bats':at_bats})
 return rows
p=argparse.ArgumentParser();p.add_argument('--start',required=True);p.add_argument('--end',required=True);p.add_argument('--out',default='observations.csv');a=p.parse_args()
start=dt.date.fromisoformat(a.start);end=dt.date.fromisoformat(a.end)
if end<start:p.error('end before start')
previous={}; rows=[]; day=start
while day<=end:
 date=str(day); schedule=fetch('/schedule?sportId=1&date='+date)
 for group in schedule.get('dates',[]):
  for game in group.get('games',[]):
   if game['status']['abstractGameState']!='Final':continue
   box=fetch('/game/'+str(game['gamePk'])+'/boxscore')
   for row in extract(box,date):
    prior=previous.get(row['player_id']); previous[row['player_id']]=day
    if prior is not None and (day-prior).days>0:
     row['rest_day']=int((day-prior).days>1);rows.append(row)
 print(date,len(rows),flush=True);day+=dt.timedelta(days=1)
with open(a.out,'w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['player_id','date','rest_day','performance','at_bats']);w.writeheader();w.writerows(rows)

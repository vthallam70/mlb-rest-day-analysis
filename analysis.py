import csv, datetime as dt, random, statistics, sys

def estimate(rows, seed=42, iterations=2000):
    treated=[r for r in rows if r['rest_day']=='1']; controls=[r for r in rows if r['rest_day']=='0']; pairs=[]
    for t in treated:
        candidates=[c for c in controls if c['player_id']==t['player_id'] and abs((dt.date.fromisoformat(c['date'])-dt.date.fromisoformat(t['date'])).days)<=30]
        if candidates:
            c=min(candidates,key=lambda x:abs((dt.date.fromisoformat(x['date'])-dt.date.fromisoformat(t['date'])).days))
            pairs.append(float(t['performance'])-float(c['performance']))
    if not pairs: raise ValueError('No matched observations')
    rng=random.Random(seed); boot=sorted(statistics.mean(rng.choices(pairs,k=len(pairs))) for _ in range(iterations))
    return {'matched_pairs':len(pairs),'unmatched_treated':len(treated)-len(pairs),'mean_difference':statistics.mean(pairs),'bootstrap_95_interval':[boot[int(.025*iterations)],boot[min(iterations-1,int(.975*iterations))]]}
if __name__=='__main__':
    with open(sys.argv[1],newline='') as f: print(estimate(list(csv.DictReader(f))))

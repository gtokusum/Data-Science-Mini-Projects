import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns

def getScore(year):
    url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    soup.findAll('tr',limit=2)
    headers = [th.getText() for th in soup.findAll('tr',limit=2)[0].findAll('th')]
    headers = headers[1:]
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
    stats = pd.DataFrame(player_stats,columns = headers)
    rowindex = ['Age','G','GS','MP','FG','FGA','FG%','3P','3PA','3P%','2P','2PA','2P%','eFG%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS']
    age, G, GS, MP, FG, FGA, FGper, s3P, s3PA, s3Pper, s2P, s2PA, s2Pper, eFGper, FT, FTA, FTper, ORB, DRB,TRB, AST, STL, BLK, TOV,PF,PTS = 'Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB','AST','STL','BLK','TOV','PF','PTS'
    for i in rowindex:
        stats[i] = stats[i].apply(pd.to_numeric)

    stats.fillna(value=0)    
    hollpts,hollfg,hollfga,hollfta,hollft,hollorb,holldrb,hollstl,hollast,hollblk,hollpf,holltov = [],[],[],[],[],[],[],[],[],[],[],[]
    GameScore = []
    for i in range(len(stats)):
        hollpts.append(stats['PTS'].iloc[i])
        hollfg.append(stats['FG'].iloc[i])
        hollfga.append(stats['FGA'].iloc[i])
        hollfta.append(stats['FTA'].iloc[i])
        hollft.append(stats['FT'].iloc[i])
        hollorb.append(stats['ORB'].iloc[i])
        holldrb.append(stats['DRB'].iloc[i])
        hollstl.append(stats['STL'].iloc[i])
        hollast.append(stats['AST'].iloc[i])
        hollblk.append(stats['BLK'].iloc[i])
        hollpf.append(stats['PF'].iloc[i])
        holltov.append(stats['TOV'].iloc[i])

    for i in range(len(stats)):
        GameScore.append(round(get_holl(hollpts[i],hollfg[i],hollfga[i],hollfta[i],hollft[i],hollorb[i],holldrb[i],hollstl[i],hollast[i],hollblk[i],hollpf[i],holltov[i]),5))

    stats['Game Score'] = GameScore
    stats.set_index('Player',inplace=True)
    droppedStats = stats.drop(['Age','Tm','G','GS','FG','FGA','3P','3PA','2P','2PA','2P%','FT','FTA'],axis=1)
    return droppedStats.nlargest(10,['Game Score'])


def get_holl(pts,fg,fga,fta,ft,orb,drb,stl,ast,blk,pf,tov):
    hollingerEQ = lambda PTS,FG,FGA,FTA,FT,ORB,DRB,STL,AST,BLK,PF,TOV: PTS + 0.4 * FG - 0.7 * FGA - 0.4*(FTA - FT) + 0.7 * ORB + 0.3 * DRB + STL + 0.7 * AST + 0.7 * BLK - 0.4 * PF - TOV
    return hollingerEQ(pts,fg,fga,fta,ft,orb,drb,stl,ast,blk,pf,tov)



if __name__ == '__main__':
    year = 2021
    score = getScore(year)
    print(score)

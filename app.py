from dotenv import load_dotenv
load_dotenv()

import pandas as pd

import os
import requests
import plotly

Name= os.environ.get('gameName')
Tag = os.environ.get('gameTag')
# api_key = os.environ.get('riot_api_key')
api_key = 'RGAPI-e809ce3a-6c4d-40e3-9668-9b7b4f854e59' 
# def write_to_gsheet(service_file_path, spreadsheet_id, sheet_name, data_df):
#     """
#     this function takes data_df and writes it under spreadsheet_id
#     and sheet_name using your credentials under service_file_path
#     """
#     gc = pygsheets.authorize(service_file=service_file_path)
#     sh = gc.open_by_key(spreadsheet_id)
#     try:
#         sh.add_worksheet(sheet_name)
#     except:
#         pass
#     wks_write = sh.worksheet_by_title(sheet_name)
#     wks_write.clear('A1',None,'*')
#     wks_write.set_dataframe(data_df, (1,1), encoding='utf-8', fit=True)
#     wks_write.frozen_rows = 1

def get_puuid(gameName=None, tagLine=None, api_key=None):
    

    link = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}'

    response = requests.get(link)
    
    return response.json()

def get_riotidbyPuuid(puuid=None, api_key=None):
    
    link = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={api_key}'

    response = requests.get(link)
    
    return f"{response.json()['gameName']}"

##{response.json()['tagLine']}

def get_puuid_by_summonerId(summonerId=None, api_key=None):
    link = f'https://europe.api.riotgames.com/lol/summoner/v4/summoners/{summonerId}?api_key={api_key}'
    
    response = requests.get(link)
    
    return response.json()['puuid']



def get_ladder(top=3000):
    
    root = 'https://europe.api.riotgames.com/'
    chall = 'lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5'
    gm = 'lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5'
    masters = 'lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5'


    chall_response = requests.get(root + chall + '?api_key=' + api_key )
    chall_df = pd.DataFrame(chall_response.json()['entries']).sort_values('leaguePoints', ascending=False).reset_index(drop=True)
    gm_df= pd.DataFrame()
    masters_df = pd.DataFrame()
    if (top > 300): 
        gm_response = requests.get(root + gm + '?api_key=' + api_key )
        gm_df = pd.DataFrame(gm_response.json()['entries']).sort_values('leaguePoints', ascending=False).reset_index(drop=True)
    if (top > 1000):
        masters_response = requests.get(root + masters + '?api_key=' + api_key )
        masters_df = pd.DataFrame(masters_response.json()['entries']).sort_values('leaguePoints', ascending=False).reset_index(drop=True)
    
    ladder = pd.concat([chall_df, gm_df, masters_df])[:top].reset_index(drop=True)
    ladder = ladder.drop(columns='rank').reset_index(drop=False).rename(columns={'index':'rank'})
    
    ladder['rank'] += 1
    
    return ladder

def get_match_history(puuid=None, start=0, count=20):
    root = 'https://europe.api.riotgames.com/'
    endpoint = f'lol/match/v5/matches/by-puuid/{puuid}/ids?type=tourney&start={start}&count={count}'

    response = requests.get(root + endpoint + '&api_key=' + api_key)
    
    return response.json()


def get_match_data_from_id(matchId=None):
    root = 'https://europe.api.riotgames.com/'
    endpoint = f'lol/match/v5/matches/{matchId}'

    response = requests.get(root + endpoint + '?api_key=' + api_key)
    
    return response.json()

def get_match_data_from_id_at15(matchId=None):
    root = 'https://europe.api.riotgames.com/'
    endpoint = f'lol/match/v5/matches/{matchId}/timeline'

    response = requests.get(root + endpoint + '?api_key=' + api_key)
    
    return response.json()


def process_match_json(match_json, puuid):
    ##Architecture
    metadata = match_json['metadata']

    match_id = metadata['matchId']
    participants = metadata['participants']
    info = match_json['info']
    players = info['participants']
    teams = info['teams']
    player = players[participants.index(puuid)]
    perks = player['perks']
    stats = perks['statPerks']
    styles = perks['styles']
        
    primary = styles[0]
    secondary = styles[1]

    defense = stats['defense']
    flex = stats['flex']
    offense = stats['offense']

    game_creation = info['gameCreation']
    game_duration = info['gameDuration']
    game_start_timestamp = info['gameStartTimestamp']
    game_end_timestamp = info['gameEndTimestamp']
    patch = info['gameVersion']

    kills = player['kills']
    deaths = player['deaths']
    assists = player['assists']
    first_blood = player['firstBloodKill']

    champ_level = player['champLevel']
    champion_id = player['championId']
    champion_transform = player['championTransform']
    champion_name = player['championName']
    gold_earned = player['goldEarned']
    cs = player['neutralMinionsKilled']
    item0 = player['item0']
    item1 = player['item1']
    item2 = player['item2']
    item3 = player['item3']
    item4 = player['item4']
    item5 = player['item5']
    objectives_stolen = player['objectivesStolen']
    objectives_stolen_assist = player['objectivesStolenAssists']
    participant_id = player['participantId']
    player_puuid = player['puuid']
    riot_name = player['riotIdGameName']
    riot_tag = player['riotIdTagline']
    summoner1Id = player['summoner1Id']
    summoner2Id = player['summoner2Id']
    summonerId = player['summonerId']
    summonerName = player['summonerName']
    total_damage_dealt_to_champions = player['totalDamageDealtToChampions']
    total_damage_shielded_on_teammates = player['totalDamageShieldedOnTeammates']
    total_damage_taken = player['totalDamageTaken']
    total_heals_on_teammates = player['totalHealsOnTeammates']
    total_minions_killed = player['totalMinionsKilled']
    total_time_cc_dealt = player['totalTimeCCDealt']
    wards_placed = player['wardsPlaced']
    wards_killed = player['wardsKilled']
    vision_score = player['visionScore']
    win = player['win']


    vision_wards_bought_in_game = player['visionWardsBoughtInGame']
    role = player['role']
    lane = player['lane']




    primary_style = primary['style']
    secondary_style = secondary['style']

    primary_keystone = primary['selections'][0]['perk']
    primary_perk_1 = primary['selections'][1]['perk']
    primary_perk_2 = primary['selections'][2]['perk']
    primary_perk_3 = primary['selections'][3]['perk']


    secondary_perk_1 = secondary['selections'][0]['perk']
    secondary_perk_2 = secondary['selections'][1]['perk']
    # secondary_perk_3 = secondary['selections'][2]['perk']
    for team in teams:
        # bans = team['bans']
        if team['teamId'] == player['teamId']:
        
            obj = team['objectives']
            baron = obj['baron']
            dragon = obj['dragon']
            grubs = obj['horde']
            riftHerald = obj['riftHerald']
            tower = obj['tower']
            inhibitor = obj['inhibitor']
        
        # for obj in [baron, dragon, grubs, riftHerald, tower, inhibitor]:
        #     first = obj['first']
        #     obj_kills = obj['kills']

    match_df = pd.DataFrame({
        'match_id': [match_id],
        'participants': [participants],
        'defense': [defense],
        'flex': [flex],
        'offense': [offense],
        'info' : [info],
        'game_creation': [game_creation],
        'game_duration': [game_duration],
        'game_start_timestamp': [game_start_timestamp],
        'game_end_timestamp': [game_end_timestamp],
        'patch': [patch],
        'kills': [kills],
        'deaths': [deaths],
        'assists': [assists],
        'first_blood': [first_blood],
        'champ_level': [champ_level],
        'champion_id': [champion_id],
        'champion_transform': [champion_transform],
        'champion_name' : [champion_name],
        'gold_earned': [gold_earned],
        'cs': [cs],
        'item0': [item0],
        'item1': [item1],
        'item2': [item2],
        'item3': [item3],
        'item4': [item4],
        'item5': [item5],
        'objectives_stolen': [objectives_stolen],
        'objectives_stolen_assist': [objectives_stolen_assist],
        'participant_id': [participant_id],
        'player_puuid': [player_puuid],
        'riot_name': [riot_name],
        'riot_tag': [riot_tag],
        'summoner1Id': [summoner1Id],
        'summoner2Id': [summoner2Id],
        'summonerId': [summonerId],
        'summonerName': [summonerName],
        'total_damage_dealt_to_champions': [total_damage_dealt_to_champions],
        'total_damage_shielded_on_teammates': [total_damage_shielded_on_teammates],
        'total_damage_taken': [total_damage_taken],
        'total_heals_on_teammates': [total_heals_on_teammates],
        'total_minions_killed': [total_minions_killed],
        'total_time_cc_dealt': [total_time_cc_dealt],
        'wards_placed': [wards_placed],
        'wards_killed': [wards_killed],
        'vision_score': [vision_score],
        'win': [win],
        'vision_wards_bought_in_game': [vision_wards_bought_in_game],
        'role': [role],
        'primary_style': [primary_style],
        'secondary_style': [secondary_style],
        'primary_keystone': [primary_keystone],
        'primary_perk_1': [primary_perk_1],
        'primary_perk_2': [primary_perk_2],
        'primary_perk_3': [primary_perk_3],
        'secondary_perk_1': [secondary_perk_1],
        'secondary_perk_2': [secondary_perk_2],
        'lane':[lane],
        
        
        #IMPORTANT
        'players':[players]
        
        
        
        # 'baron': [baron],
        # 'dragon': [dragon],
        # 'grubs': [grubs],
        # 'riftHerald': [riftHerald],
        # 'tower': [tower],
        # 'inhibitor': [inhibitor]
    })
    return match_df

def get_direct_opponent(match_id= None, match_json = None, participantId= 0, puuid= None):
    players = process_match_json(match_json=match_json, puuid=puuid)['players']
    if participantId <= 5:
        return players[0][participantId+4]
    return players[0][participantId-6]

        
def json_extract(obj, key):
    
    
    
    
    arr = []
    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k,v in obj.items(): #k = key and v = value
                if k==key:
                    arr.append(v)
                elif isinstance(v, (dict, list)):
                    extract(v, arr, key)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
                
        return arr
    
    values = extract(obj, arr, key)
    return values


get_puuid(gameName="UK Paradize", tagLine="TOP", api_key=api_key)
puuid_paradize = get_puuid(gameName="UK Paradize", tagLine="TOP", api_key=api_key)['puuid']


matchs = get_match_history(puuid=puuid_paradize, count=5)
# match_data = get_match_data_from_id(matchs[0])
# match_df = process_match_json(match_data, puuid=puuid_paradize)
# df = pd.DataFrame()
#EUW1_7188408808
# df = pd.concat([df, match_df])


df = pd.DataFrame()

for i in matchs:
    match_data = get_match_data_from_id(i)
    match_df = process_match_json(match_data, puuid=puuid_paradize)
    df = pd.concat([df, match_df])

gold_diff_15 = []
for i in matchs :
    match_at15 = get_match_data_from_id_at15(i)
    gold_para_15 =match_at15['info']['frames'][15]['participantFrames']['1']['totalGold']
    gold_adversaire_15 = match_at15['info']['frames'][15]['participantFrames']['6']['totalGold']
    gd15= gold_para_15 - gold_adversaire_15
    gold_diff_15.append(gd15)


df['GD15'] = gold_diff_15

opponent = []
for i in matchs:
    match_data = get_match_data_from_id(i)
    for j in df['participant_id']:
        opp = get_direct_opponent(match_id=i, match_json=match_data, participantId=j, puuid=puuid_paradize)
    opponent.append(opp)


champ_adverse = []
for i in opponent:
    
    champ_adverse.append(i['championName'])

df['champion_adverse'] = champ_adverse


perk = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json'
perk_styles = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/perkstyles.json'
items = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/items.json'

perk_json = requests.get(perk).json()
perk_styles_json = requests.get(perk_styles).json()
items_json = requests.get(items).json()


perk_ids = json_extract(perk_json, 'id')
perk_names = json_extract(perk_json, 'name')

perk_dict = dict(map(lambda i, j : (int(i),j), perk_ids, perk_names))


perk_styles_dict = {8400: 'Resolve',
 8000: 'Precision',
 8100: 'Domination',
 8200: 'Sorcery',
 8300: 'Inspiration'}

items_ids = json_extract(items_json, 'id')
items_names = json_extract(items_json, 'name') 

items_dict = dict(map(lambda i,j : (int(i), j), items_ids, items_names))

df = df.replace(perk_dict).replace(perk_styles_dict).replace(items_dict)

df['uuid'] = df['match_id'] + '_' + df['player_puuid']
df = df.set_index('uuid')


df = df.reindex(['win', 'champion_name', 'champion_adverse', 'kills', 'deaths', 'assists', 'total_damage_dealt_to_champions', 'vision_score', 'GD15'], axis = 1)




# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.




from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd

app = Dash(__name__)
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options



app.layout = html.Div(children=[
    html.H1(children='Hello ..'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",  #tri,
        style_table={'marginBottom': '20px'},


        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_cell={
            'fontFamily' : "Roboto, sans-serif"
        },
        style_data={'border': '1px solid #ddd'},
        tooltip_data=[
            {
                column: {'value': str(value), 'type': 'markdown'}
                for column, value in row.items()
            } for row in df.to_dict('records')
        ],
        tooltip_duration=None  # Tooltips persist until you move the mouse
    )

])

if __name__ == '__main__':
    app.run(debug=True)

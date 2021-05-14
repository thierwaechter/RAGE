import pandas as pd
from datetime import date
from datamanagement import source

heute = date.today()
heute_datum = heute.strftime("%Y-%m-%d")

def combine_race_drivers():
    all_info_df = pd.DataFrame()
    race_df = source.race_data_to_df()
    drivers_df = source.driver_data_to_df()
    all_info_df = pd.merge(race_df, drivers_df, how="left", on=['iRacingName'])
    return all_info_df

def get_drivers_races(name):
    race_driver_df = combine_race_drivers()
    driver_races_df = race_driver_df[race_driver_df['Name'] == name]
    if driver_races_df.empty:
        print("Keine Rennen zu " + name + " gefunden.")
    else:    
        driver_races_df['Team'] = driver_races_df.apply(lambda row: row[row['Seriename'] + '.Team'], axis=1)
        driver_races_df = driver_races_df[['iRacingNr', 'iRacingName', 'Name', 'Seriename', 'Team', 'Date', 'Track', 'Pos', 'Starts', 'Inc', 'Points']]
        driver_races_df = driver_races_df.sort_values(
            by=['Date'],
            ascending=[True])
        driver_races_df['iRacingNr'] = driver_races_df['iRacingNr'].astype(int)
        driver_races_df['Pos'] = driver_races_df['Pos'].astype(int)
        driver_races_df['Starts'] = driver_races_df['Starts'].astype(int)
        driver_races_df['Inc'] = driver_races_df['Inc'].astype(int)
        driver_races_df['Points'] = driver_races_df['Points'].astype(int)
        driver_races_df['Name'] = driver_races_df['Name'].str.upper() 
        driver_races_df['Team'] = driver_races_df['Team'].str.upper() 
        driver_races_df.columns = map(str.upper, driver_races_df.columns)
 #       print(driver_races_df)
        return [driver_races_df, heute_datum, name]


#Achtung! Keine Fahrer ausschliessen wegen "out" oder "", da sie in früheren Rennen ev. mitgefahren sind
def get_track_race(track, serie):
    pos_prev = 0
    starts_prev = 0
    inc_prev = 0
    points_prev = 0
    race_driver_df = combine_race_drivers()
    driver_races_df = race_driver_df[(race_driver_df['Track'] == track) & (race_driver_df['Seriename'] == serie)]
    try:
        date = driver_races_df['Date'].values[0]
        driver_races_df.loc[:,'Team'] = driver_races_df.apply(lambda row: row[row['Seriename'] + '.Team'], axis=1)
        driver_races_df.loc[:,'Name'] = driver_races_df['Name'].str.upper() 
        driver_races_df.loc[:,'Team'] = driver_races_df['Team'].str.upper() 
        driver_races_df = driver_races_df.sort_values(
            by=['Pos'],
            ascending=[True])
#        driver_races_df['iRacingNr'] = driver_races_df['iRacingNr'].astype(int)
        driver_races_df['Pos'] = driver_races_df['Pos'].astype(int)
        driver_races_df['Starts'] = driver_races_df['Starts'].astype(int)
        driver_races_df['Inc'] = driver_races_df['Inc'].astype(int)
        driver_races_df['Points'] = driver_races_df['Points'].astype(int)
        driver_races_df = driver_races_df[['Pos', 'Name', 'Team', 'Starts', 'Inc', 'Points']]
        for index, row in driver_races_df.iterrows():
            if row['Starts'] == starts_prev and row['Inc'] == inc_prev and row['Points'] == points_prev:
                driver_races_df.loc[index, 'Pos'] = pos_prev
            pos_prev = row['Pos']
            starts_prev = row['Starts']
            inc_prev = row['Inc']
            points_prev = row['Points']
        driver_races_df.columns = map(str.upper, driver_races_df.columns)
        return [driver_races_df, date, track]
    except IndexError: print("Kein Datensatz zur Serie " + serie + " vorhanden!")


#Achtung! Keine Fahrer ausschliessen wegen "out" oder "", da sie in früheren Rennen ev. mitgefahren sind
def get_date_race(date, serie):
    pos_prev = 0
    starts_prev = 0
    inc_prev = 0
    points_prev = 0
    race_driver_df = combine_race_drivers()
    driver_races_df = race_driver_df[(race_driver_df['Date'] == date) & (race_driver_df['Seriename'] == serie)]
    try:
        track = driver_races_df['Track'].values[0]
        driver_races_df.loc[:,'Team'] = driver_races_df.apply(lambda row: row[row['Seriename'] + '.Team'], axis=1)
        driver_races_df.loc[:,'Name'] = driver_races_df['Name'].str.upper() 
        driver_races_df.loc[:,'Team'] = driver_races_df['Team'].str.upper() 
        driver_races_df = driver_races_df.sort_values(
            by=['Pos'],
            ascending=[True])
        driver_races_df['Pos'] = driver_races_df['Pos'].astype(int)
        driver_races_df['Starts'] = driver_races_df['Starts'].astype(int)
        driver_races_df['Inc'] = driver_races_df['Inc'].astype(int)
        driver_races_df['Points'] = driver_races_df['Points'].astype(int)
        driver_races_df = driver_races_df[['Pos', 'Name', 'Team', 'Starts', 'Inc', 'Points']]
        for index, row in driver_races_df.iterrows():
            if row['Starts'] == starts_prev and row['Inc'] == inc_prev and row['Points'] == points_prev:
                driver_races_df.loc[index, 'Pos'] = pos_prev
            pos_prev = row['Pos']
            starts_prev = row['Starts']
            inc_prev = row['Inc']
            points_prev = row['Points']
        driver_races_df.columns = map(str.upper, driver_races_df.columns)
        print(driver_races_df)
        return [driver_races_df, date, track]
    except IndexError: print("Kein Datensatz zur Serie " + serie + " vorhanden!")


def get_all_racer_info():
    drivers_df = source.driver_data_to_df()
    drivers_df = drivers_df.sort_values(
        by=['Name'],
    ascending=[True])
    drivers_df['iRacingNr'] = drivers_df['iRacingNr'].astype(int) 
    drivers_df.columns = map(str.upper, drivers_df.columns)
    print(drivers_df)
    return [drivers_df, heute_datum, "FLANC Fahrerdatenbank"]


def get_all_track_races(serie):
    race_driver_df = combine_race_drivers()
    serie_df = race_driver_df[race_driver_df['Seriename'] == serie]
    serie_df['Team'] = serie_df.apply(lambda row: row[serie + '.Team'], axis=1)    
    del serie_df['iRacingNr']
    del serie_df['iRacingName']
    serie_df = serie_df[['Track', 'Date', 'Pos', 'Name', 'Team', 'Starts', 'Inc', 'Points']]
    serie_df = serie_df.sort_values(
        by=['Track', 'Pos'],
        ascending=[True, True])
    serie_df['Pos'] = serie_df['Pos'].astype(int)
    serie_df['Starts'] = serie_df['Starts'].astype(int)
    serie_df['Inc'] = serie_df['Inc'].astype(int)
    serie_df['Points'] = serie_df['Points'].astype(int)
    serie_df.loc[:,'Name'] = serie_df['Name'].str.upper() 
    serie_df.loc[:,'Team'] = serie_df['Team'].str.upper() 
    serie_df.columns = map(str.upper, serie_df.columns)
    print(serie_df)
    return [serie_df, heute_datum, serie]



def get_saison_races(serie):
    pos_prev = 0
    starts_prev = 0
    inc_prev = 0
    points_prev = 0
    race_driver_df = combine_race_drivers()
    saison_races_df = race_driver_df[race_driver_df['Seriename'] == serie]
    saison_races_df = saison_races_df[saison_races_df[serie + '.Status'] == 'aktiv']
    saison_races_df['Team'] = saison_races_df.apply(lambda row: row[row['Seriename'] + '.Team'], axis=1)  
    saison_races_df['Pos'] = 0
    saison_races_df = saison_races_df.groupby(['Pos', 'Name', 'Team'], as_index=False).sum()
    saison_races_df.loc[:,'Name'] = saison_races_df['Name'].str.upper() 
    saison_races_df.loc[:,'Team'] = saison_races_df['Team'].str.upper() 
    saison_races_df = saison_races_df.sort_values(by=['Points', 'Starts', 'Inc'], ascending=[False, False, True])
    start_pos = 1
    saison_races_df['Pos'] = range(start_pos, len(saison_races_df) + start_pos)
    saison_races_df = saison_races_df[['Pos', 'Name', 'Team', 'Starts', 'Inc', 'Points']]
    saison_races_df['Pos'] = saison_races_df['Pos'].astype(int)
    saison_races_df['Starts'] = saison_races_df['Starts'].astype(int)
    saison_races_df['Inc'] = saison_races_df['Inc'].astype(int)
    saison_races_df['Points'] = saison_races_df['Points'].astype(int)
    for index, row in saison_races_df.iterrows():
        if row['Starts'] == starts_prev and row['Inc'] == inc_prev and row['Points'] == points_prev:
            saison_races_df.loc[index, 'Pos'] = pos_prev
        pos_prev = row['Pos']
        starts_prev = row['Starts']
        inc_prev = row['Inc']
        points_prev = row['Points']
    saison_races_df.columns = map(str.upper, saison_races_df.columns)
    print(saison_races_df)
    return [saison_races_df, heute_datum, serie]

# WICHTIG: Auch Fahrer, die "out" sind, werden für die Saisonrangliste
# berücksichtigt, da ihre Punkte stehen bleiben
# Enthält ein Team nur Fahrer mit Status "out", wird das Team nicht angezeigt.
def get_team_races_and_korr(saison):
    race_driver_df = combine_race_drivers()
    drivers_df = source.driver_data_to_df()
    saison_df = race_driver_df[race_driver_df['Seriename'] == saison]
    saison_df['Team'] = saison_df.apply(lambda row: row[saison + '.Team'], axis=1)
    saison_df['Status'] = saison_df.apply(lambda row: row[saison + '.Status'], axis=1)
    saison_team_df = saison_df[['Team', 'Status', 'Starts', 'Inc', 'Points']]
    saison_team_df = saison_team_df.groupby(['Team', 'Status'], as_index=False).sum() 
    drivers_df['Team'] = drivers_df.apply(lambda row: row[saison + '.Team'], axis=1)
    drivers_df['Status'] = drivers_df.apply(lambda row: row[saison + '.Status'], axis=1)
    drivers_df['TeamStKorr'] = drivers_df.apply(lambda row: row[saison + '.TeamStKorr'], axis=1)
    drivers_df['TeamIncKorr'] = drivers_df.apply(lambda row: row[saison + '.TeamIncKorr'], axis=1)
    drivers_df['TeamPktKorr'] = drivers_df.apply(lambda row: row[saison + '.TeamPktKorr'], axis=1)                
    saison_teamKorr_df = drivers_df[['Team', 'Status', 'TeamStKorr', 'TeamIncKorr', 'TeamPktKorr']]
    saison_teamKorr_df = saison_teamKorr_df.groupby(['Team', 'Status'], as_index=False).sum()
    saison_team_with_korr_df = pd.merge(saison_team_df, saison_teamKorr_df, how="left", on=['Team', 'Status'])
    saison_team_with_korr_df['Team'] = saison_team_df['Team'].str.upper()
    saison_team_with_korr_df = saison_team_with_korr_df.sort_values(by=['Team'], ascending=[True])
#    print(saison_team_with_korr_df)
    return saison_team_with_korr_df

def get_team_races_incl_korr(serie):
    pos_prev = 0
    starts_prev = 0
    inc_prev = 0
    points_prev = 0
    saison_team_incl_korr_df = get_team_races_and_korr(serie)
    saison_team_incl_korr_df['Starts'] = saison_team_incl_korr_df['Starts'] + saison_team_incl_korr_df['TeamStKorr']
    saison_team_incl_korr_df['Inc'] = saison_team_incl_korr_df['Inc'] + saison_team_incl_korr_df['TeamIncKorr']
    saison_team_incl_korr_df['Points'] = saison_team_incl_korr_df['Points'] + saison_team_incl_korr_df['TeamPktKorr']
    saison_team_incl_korr_df.loc[:,'Team'] = saison_team_incl_korr_df['Team'].str.upper()
    saison_team_incl_korr_df = saison_team_incl_korr_df[['Team', 'Starts', 'Inc', 'Points', 'Status']]
    saison_team_incl_korr_known_df = saison_team_incl_korr_df[saison_team_incl_korr_df['Status'] != ""]
    saison_team_incl_korr_aktiv_df = saison_team_incl_korr_known_df.groupby('Team').filter(lambda x: (x['Status'] != "out").any())
    saison_team_incl_korr_aktiv_df = saison_team_incl_korr_aktiv_df[['Team', 'Starts', 'Inc', 'Points']]
    saison_team_incl_korr_aktiv_df = saison_team_incl_korr_aktiv_df.groupby(['Team'], as_index=False).sum()
    saison_team_incl_korr_aktiv_df = saison_team_incl_korr_aktiv_df.sort_values(by=['Points', 'Starts', 'Inc'], ascending=[False, False, True])
    saison_team_incl_korr_aktiv_df['Pos'] = 0
    start_pos = 1
    saison_team_incl_korr_aktiv_df['Pos'] = range(start_pos, len(saison_team_incl_korr_aktiv_df) +start_pos)
    saison_team_incl_korr_aktiv_df = saison_team_incl_korr_aktiv_df[['Pos', 'Team', 'Starts', 'Inc', 'Points']]
    saison_team_incl_korr_aktiv_df['Pos'] = saison_team_incl_korr_aktiv_df['Pos'].astype(int)
    saison_team_incl_korr_aktiv_df['Starts'] = saison_team_incl_korr_aktiv_df['Starts'].astype(int)
    saison_team_incl_korr_aktiv_df['Inc'] = saison_team_incl_korr_aktiv_df['Inc'].astype(int)
    saison_team_incl_korr_aktiv_df['Points'] = saison_team_incl_korr_aktiv_df['Points'].astype(int)
    for index, row in  saison_team_incl_korr_aktiv_df.iterrows():
        if row['Starts'] == starts_prev and row['Inc'] == inc_prev and row['Points'] == points_prev:
             saison_team_incl_korr_aktiv_df.loc[index, 'Pos'] = pos_prev
        pos_prev = row['Pos']
        starts_prev = row['Starts']
        inc_prev = row['Inc']
        points_prev = row['Points']
    saison_team_incl_korr_aktiv_df.columns = map(str.upper, saison_team_incl_korr_aktiv_df.columns)
    print(saison_team_incl_korr_aktiv_df)
    return [saison_team_incl_korr_aktiv_df, heute_datum, serie]
    

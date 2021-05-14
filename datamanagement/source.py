import os
from datetime import date
from shutil import copyfile
import json
import pandas as pd

# Das Verzeichnis unter Data gibt den Seriename für
# die eingelesenen Seriennamen vor!
iracing_data_path = "./data/"
driver_json = 'fahrer.json'
heute = date.today()
heute_datum = heute.strftime("%Y-%m-%d")

def json_open_and_load(file_name):
    with open(file_name, encoding='UTF-8') as json_file:
        json_data = json.load(json_file)
        return json_data


def json_save(df):
    with open(driver_json, 'w') as json_file:
        df['iRacingNr'] = df['iRacingNr'].astype('int64')
        df.to_json(json_file, orient='records')

def json_backup():
    copyfile(driver_json, "./fahrer DB Backup/" + str(heute) + "-"+ driver_json)

def race_data_to_df():
    races_df = pd.DataFrame()
    for serie in os.listdir(iracing_data_path):
        for file in os.listdir(iracing_data_path + serie):
            if file == "":
                pass
            else:
                filepath = iracing_data_path + serie + '/' + file
                race_data = json_open_and_load(filepath)
                serie_name = serie
                race_start_time = race_data['start_time'].split('T')[0]
                race_track_name = race_data['track']['track_name']
                race_results = race_data['session_results'][0]['results']
                for result in race_results:
                    display_name = result['display_name']
                    # Wer am Rennen teilgenommen hat, bekommt eine "1"
                    start = 1
                    incidents = result['incidents']
                    finish_position = result['finish_position'] + 1
                    aggregate_champ_points = result['aggregate_champ_points']
                    series = pd.Series([
                        serie_name,
                        race_start_time,
                        race_track_name,
                        finish_position,
                        display_name,
                        start,
                        incidents,
                        aggregate_champ_points], index=[
                                'Seriename',
                                'Date',
                                'Track',
                                'Pos',
                                'iRacingName',
                                'Starts',
                                'Inc',
                                'Points'])
                    races_df = races_df.append(series, ignore_index=True)
    return races_df


def driver_data_to_df():
    drivers_df = pd.DataFrame()
    drivers_data = json_open_and_load(driver_json)
    drivers_df = pd.json_normalize(drivers_data)
    return drivers_df

def del_driver(name):
    drivers_df = driver_data_to_df()
    del_driver = drivers_df[drivers_df['Name'] == name].index
    drivers_df.drop(del_driver, inplace=True)
    json_save(drivers_df)

def add_new_serie(serie):
    drivers_df = driver_data_to_df()
    if serie + '.Status' in drivers_df.columns:
        return "alreadythere"
    else:
        drivers_df[serie + '.Status'] = ""
        drivers_df[serie + '.Team'] = ""
        drivers_df[serie + '.TeamStKorr'] = 0
        drivers_df[serie + '.TeamIncKorr'] = 0
        drivers_df[serie + '.TeamPktKorr'] = 0
        drivers_df[serie + '.TeamKorrDatum'] = ""
        drivers_df[serie + '.TeamKorrGrund'] = ""
        json_save(drivers_df)
        return "Ok"

def edit_serie_name(seriename, new_seriename):
    drivers_df = driver_data_to_df()
    drivers_df = drivers_df.rename({seriename + ".Status" : new_seriename + ".Status"}, axis=1)
    drivers_df = drivers_df.rename({seriename + ".Team" : new_seriename + ".Team"}, axis=1)
    drivers_df = drivers_df.rename({seriename + ".TeamStKorr" : new_seriename + ".TeamStKorr"}, axis=1)
    drivers_df = drivers_df.rename({seriename + ".TeamIncKorr" : new_seriename + ".TeamIncKorr"}, axis=1)
    drivers_df = drivers_df.rename({seriename + ".TeamPktKorr" : new_seriename + ".TeamPktKorr"}, axis=1)
    drivers_df = drivers_df.rename({seriename + ".TeamKorrDatum" : new_seriename + ".TeamKorrDatum"}, axis=1)
    drivers_df = drivers_df.rename({seriename + ".TeamKorrGrund" : new_seriename + ".TeamKorrGrund"}, axis=1)
    json_save(drivers_df)

def del_serie(seriename):
    drivers_df = driver_data_to_df()
    del drivers_df[seriename + ".Status"]
    del drivers_df[seriename + ".Team"]
    del drivers_df[seriename + ".TeamStKorr"]
    del drivers_df[seriename + ".TeamIncKorr"]
    del drivers_df[seriename + ".TeamPktKorr"]
    del drivers_df[seriename + ".TeamKorrDatum"]
    del drivers_df[seriename + ".TeamKorrGrund"]
    json_save(drivers_df)
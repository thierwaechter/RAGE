from datamanagement import output, source
from excel import writeexport


#payload = output.combine_race_drivers()
#payload = source.driver_data_to_df()

#payload = source.race_data_to_df()
#print(payload)

payload = output.get_track_race("Okayama International Circuit", "F3 2020-21")
#payload = output.get_track_race("Watkins Glen International", "F3 2020-21")

#payload = output.get_date_race("2021-03-25", "GT3 2021")

#payload = output.get_saison_races("Club 2021")
#payload = output.get_saison_races("GT3 2021")
#writeexport.format_race_export(payload)

#payload = output.get_team_races_and_korr("F3 2020-21")
#payload = output.get_team_races_incl_korr("F3 2020-21")
#payload = output.get_team_races_incl_korr("GT3 2021")
#writeexport.format_team_export(payload)

#payload = output.get_all_track_races("F3 2020-21")
# payload = output.get_all_track_races("GT3 2021")

#writeexport.format_all_race_export(payload)

#payload = output.get_drivers_races("Tanner Nico")
#writeexport.format_driver_export(payload)

#payload = output.get_all_racer_info()
#writeexport.format_all_drivers_export(payload)

print(payload)



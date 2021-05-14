import sys
from datamanagement import output, source
from excel import writeexport
from ui.Ui_FLANC_RAGE import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTabWidget, QMessageBox


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        QtCore.QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class DlgMain(QTabWidget, Ui_TabWidget):
    def __init__(self):
        super(DlgMain, self).__init__()
        self.setupUi(self)

    ### GUI-Designer Korrektur
        self.iracingnr_edit.setValidator(QtGui.QIntValidator(0, 99999999))

    ###Register Ranglisten
        self.serie_btn.clicked.connect(self.evt_serie_btn_clicked)
        self.name_btn.clicked.connect(self.evt_name_btn_clicked)
        self.name_cbb.activated.connect(self.evt_selected_name)
        self.all_drivers_btn.clicked.connect(self.evt_all_drivers_btn_clicked)
        self.all_drivers_btn.setEnabled(True)
        self.serie_cbb.activated.connect(self.evt_selected_serie)
        self.teams_btn.clicked.connect(self.evt_teams_btn_clicked)
        self.teams_btn.setEnabled(False)
        self.track_btn.clicked.connect(self.evt_track_btn_clicked)
        self.track_btn.setEnabled(False)
        self.track_cbb.activated.connect(self.evt_selected_track)
        self.datum_btn.clicked.connect(self.evt_date_btn_clicked)
        self.datum_btn.setEnabled(False)
        self.datum_cbb.activated.connect(self.evt_selected_date)
        self.all_races_btn.clicked.connect(self.evt_all_races_btn_clicked)
        self.all_races_btn.setEnabled(False)
        self.export_btn.clicked.connect(self.evt_selected_export)

    ### Register Management
        self.mgmt_name_btn.clicked.connect(self.evt_mgmt_name_btn_clicked)
        self.mgmt_name_cbb.activated.connect(self.evt_mgmt_selected_name)
        self.mgmt_serie_btn.clicked.connect(self.evt_mgmt_serie_btn_clicked)
        self.mgmt_serie_cbb.activated.connect(self.evt_mgmt_selected_serie)
        self.fahrerundteam_speichern_btn.clicked.connect(self.evt_mgmt_fahrerundteam_speichern_btn_clicked)
        self.fahrer_loeschen_btn.clicked.connect(self.evt_fahrer_loeschen_btn_clicked)
        self.db_backup_btn.clicked.connect(self.evt_db_backup_btn_clicked)
        self.neue_serie_erstellen_btn.clicked.connect(self.evt_neue_serie_erstellen_btn_clicked)
        self.serie_name_aendern_btn.clicked.connect(self.evt_serie_aendern_btn_clicked)
        self.serie_loeschen_btn.clicked.connect(self.evt_serie_loeschen_btn_clicked)

### Funktionen für die Ranglisten
    def evt_serie_btn_clicked(self):
        serie_list = []
        drivers_df = source.driver_data_to_df()
        for col in drivers_df.columns:
            if ".Status" in col:
                serie_list.append(col.split(".")[0])
        self.serie_cbb.clear()
        self.serie_cbb.addItems(serie_list)


    def evt_selected_serie(self):
        self.serie = self.serie_cbb.currentText()
        try:
            serie_table = output.get_saison_races(self.serie)
            dataframe = serie_table[0]
            self.model = TableModel(dataframe)
            self.table.setModel(self.model)
            self.table.setColumnWidth(0, 50)
            self.table.setColumnWidth(1, 150)
            self.table.setColumnWidth(2, 220)
            self.table.setColumnWidth(3, 70)
            self.table.setColumnWidth(4, 70)
            self.table.setColumnWidth(5, 70)
            self.track_btn.setEnabled(True)
            self.datum_btn.setEnabled(True)
            self.teams_btn.setEnabled(True)
            self.all_races_btn.setEnabled(True)
            self.export_payload = serie_table
            self.export_format = "race_export"
            self.track_cbb.clear()
        except:
            QMessageBox.information(self, "Keine Daten gefunden", "Zu " + self.serie + 
                " wurden keine Daten gefunden. Es ev. fehlt das Verzeichnis und / oder Resultate aus iRacing.")
            self.track_btn.setEnabled(False)
            self.datum_btn.setEnabled(False)
            self.teams_btn.setEnabled(False)
            self.all_races_btn.setEnabled(False)

    def evt_name_btn_clicked(self):
        self.name_cbb.clear()
        drivers_df = source.driver_data_to_df()
        self.driverlist = drivers_df['Name'].sort_values(ascending=True)
        self.name_cbb.addItems(self.driverlist)
        self.track_btn.setEnabled(False)
        self.datum_btn.setEnabled(False)
        self.teams_btn.setEnabled(False)
        self.all_drivers_btn.setEnabled(True)
        self.all_races_btn.setEnabled(False)
        self.track_cbb.clear()


    def evt_selected_name(self):
        self.name = self.name_cbb.currentText()
        try:
            name_table = output.get_drivers_races(self.name)
            dataframe = name_table[0]
            self.model = TableModel(dataframe)
            self.table.setModel(self.model)
            self.table.setColumnWidth(0, 70)
            self.table.setColumnWidth(1, 150)
            self.table.setColumnWidth(2, 150)
            self.table.setColumnWidth(3, 90)
            self.table.setColumnWidth(4, 220)
            self.table.setColumnWidth(5, 80)
            self.table.setColumnWidth(6, 250)
            self.table.setColumnWidth(7, 60)
            self.table.setColumnWidth(8, 60)
            self.table.setColumnWidth(9, 60)
            self.table.setColumnWidth(10, 60)
            self.export_payload = name_table
            self.export_format = "driver_export"
        except:
            QMessageBox.information(self, "Keine Daten gefunden", "Zu " + self.name + " wurden keine Daten gefunden.")

    def evt_track_btn_clicked(self):
        all_info_df = output.combine_race_drivers()
        self.serie = self.serie_cbb.currentText()
        all_tracks_df = all_info_df[all_info_df['Seriename'] == self.serie]
        self.tracklist = all_tracks_df.groupby(['Track'], as_index=False).sum()['Track']
        self.datum_cbb.clear()        
        self.track_cbb.clear()
        self.track_cbb.addItems(self.tracklist)

    def evt_selected_track(self):
        del self.model
        self.serie = self.serie_cbb.currentText()
        self.track = self.track_cbb.currentText()
        track_table = output.get_track_race(self.track, self.serie)
        dataframe = track_table[0]
        self.model = TableModel(dataframe)
        self.table.setModel(self.model)
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 220)
        self.table.setColumnWidth(3, 60)
        self.table.setColumnWidth(4, 60)
        self.table.setColumnWidth(5, 60)
        self.export_payload = track_table
        self.export_format = "race_export"

    def evt_date_btn_clicked(self):
        all_info_df = output.combine_race_drivers()
        self.serie = self.serie_cbb.currentText()
        all_tracks_df = all_info_df[all_info_df['Seriename'] == self.serie]
        self.datelist = all_tracks_df.groupby(['Date'], as_index=False).sum()['Date']
        self.track_cbb.clear()
        self.datum_cbb.clear()
        self.datum_cbb.addItems(self.datelist)        
    
    def evt_selected_date(self):
        del self.model
        self.serie = self.serie_cbb.currentText()
        self.date = self.datum_cbb.currentText()
        track_table = output.get_date_race(self.date, self.serie)
        dataframe = track_table[0]
        self.model = TableModel(dataframe)
        self.table.setModel(self.model)
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 250)
        self.table.setColumnWidth(3, 60)
        self.table.setColumnWidth(4, 60)
        self.table.setColumnWidth(5, 60)
        self.export_payload = track_table
        self.export_format = "race_export"

    def evt_teams_btn_clicked(self):
        self.serie = self.serie_cbb.currentText()
        teams_table = output.get_team_races_incl_korr(self.serie)
        dataframe = teams_table[0]
        self.model = TableModel(dataframe)
        self.table.setModel(self.model)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 70)
        self.table.setColumnWidth(3, 70)
        self.table.setColumnWidth(4, 70)
        self.export_payload = teams_table
        self.export_format = "team_export"
        self.track_cbb.clear()

    def evt_all_drivers_btn_clicked(self):
        all_drivers_table = output.get_all_racer_info()
        dataframe = all_drivers_table[0]
        self.model = TableModel(dataframe)
        self.table.setModel(self.model)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.export_payload = all_drivers_table
        self.export_format = "all_drivers_export"

    def evt_all_races_btn_clicked(self):
        self.serie = self.serie_cbb.currentText()
        self.track_cbb.clear()
        self.datum_cbb.clear()
        all_races_table = output.get_all_track_races(self.serie)
        dataframe = all_races_table[0]
        self.model = TableModel(dataframe)
        self.table.setModel(self.model)
        self.table.setColumnWidth(0, 220)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 60)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 250)
        self.table.setColumnWidth(5, 60)
        self.table.setColumnWidth(6, 60)
        self.table.setColumnWidth(7, 60)
        self.export_payload = all_races_table
        self.export_format = "all_races_export"

    def evt_selected_export(self):
        if self.export_format == "race_export":
            writeexport.format_race_export(self.export_payload)
        elif self.export_format == "driver_export":
            writeexport.format_driver_export(self.export_payload)
        elif self.export_format == "team_export":
            writeexport.format_team_export(self.export_payload)
        elif self.export_format == "all_drivers_export":
            writeexport.format_all_drivers_export(self.export_payload)
        elif self.export_format == "all_races_export":
            writeexport.format_all_race_export(self.export_payload)
        else:
            print("Kann" + self.export_payload[2] + " nicht exportieren :-P")
        QMessageBox.information(self, "Erledigt", "Liste wurde exportiert")
        


### Funktionen für das Fahrer und Serienmanagement
    # Funktion, um die Widgets in der Serieschleife zu löschen, bevor diese neu eingelesen werden.
    def del_items_in_detail_layout(self):
        def deleteItems(layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        deleteItems(item.layout())
        deleteItems(self.layout_v_details_container)

    def evt_rdchbox_enable(self, checkbox_sender):
#        print("enable " + checkbox_sender.serie)
        for layouts in self.layout_v_details_container.findChildren(QtWidgets.QHBoxLayout):
            radiobutton_aktiv = layouts.itemAt(2)
            if radiobutton_aktiv.widget().serie == checkbox_sender.serie:
                radiobutton_aktiv.widget().setEnabled(True)
                radiobutton_aktiv.widget().setChecked(True)
            radiobutton_out = layouts.itemAt(3)
            if radiobutton_out.widget().serie == checkbox_sender.serie:
                radiobutton_out.widget().setEnabled(True)
            pushbutton = layouts.itemAt(4)
            if pushbutton.widget().serie == checkbox_sender.serie:
                pushbutton.widget().setEnabled(True)
    
    def evt_rdchbox_disable(self, checkbox_sender):
#        print("desable " + checkbox_sender.serie)
        for layouts in self.layout_v_details_container.findChildren(QtWidgets.QHBoxLayout):
            radiobutton_aktiv = layouts.itemAt(2)
            if radiobutton_aktiv.widget().serie == checkbox_sender.serie:
                radiobutton_aktiv.widget().setEnabled(False)
            radiobutton_out = layouts.itemAt(3)
            if radiobutton_out.widget().serie == checkbox_sender.serie:
                    radiobutton_out.widget().setEnabled(False)
            pushbutton = layouts.itemAt(4)
            if pushbutton.widget().serie == checkbox_sender.serie:
                pushbutton.widget().setEnabled(False)

    def evt_team_details_btn_clicked(self):
        button_sender = self.sender()
        serie = button_sender.serie
        self.team_details_lbl.setText(serie)
        teamname = self.driver[button_sender.serie + ".Team"].item()
        self.teamname_edit.setText(teamname)
        self.teamname_edit.setEnabled(True)
        starts = self.driver[button_sender.serie + ".TeamStKorr"].item()
        self.starts_edit.setText(str(starts))
        self.starts_edit.setEnabled(True)
        self.starts_edit.setValidator(QtGui.QIntValidator(-999, 999))
        incs = self.driver[button_sender.serie + ".TeamIncKorr"].item()
        self.incs_edit.setText(str(incs))
        self.incs_edit.setEnabled(True)
        self.incs_edit.setValidator(QtGui.QIntValidator(-999, 999))
        points = self.driver[button_sender.serie + ".TeamPktKorr"].item()
        self.points_edit.setText(str(points))
        self.points_edit.setEnabled(True)
        self.points_edit.setValidator(QtGui.QIntValidator(-999, 999))
        korrekturper = self.driver[button_sender.serie + ".TeamKorrDatum"].item()
        self.korrekturper_edit.setText(korrekturper)
        self.korrekturper_edit.setEnabled(True)
        korrekturgrund = self.driver[button_sender.serie + ".TeamKorrGrund"].item()
        self.korrekturgrund_edit.setText(korrekturgrund)
        self.korrekturgrund_edit.setEnabled(True)
#        print(f'button sender: {button_sender.serie}')

    def evt_select_serie_active_chkbx_toggeld(self):
        checkbox_sender = self.sender()
#        print("checkbox")
        if checkbox_sender.isChecked():
            self.evt_rdchbox_enable(checkbox_sender)

        else:
            self.evt_rdchbox_disable(checkbox_sender) 

    def evt_mgmt_name_btn_clicked(self):
        self.mgmt_name_cbb.clear()
        drivers_df = source.driver_data_to_df()
        self.driverlist = drivers_df['Name'].sort_values(ascending=True)
        self.mgmt_name_cbb.addItems(self.driverlist)


    def evt_mgmt_fahrerundteam_speichern_btn_clicked(self):
        new_entry = {}
        name = self.mgmt_name_cbb.currentText()
        new_name = self.name_edit.text()
        new_mail = self.mail_edit.text()
        new_iracingnr_str = self.iracingnr_edit.text()
        if new_iracingnr_str == "":
            new_iracingnr_str = "0"
        new_iracingnr = int(new_iracingnr_str)
        new_iracingname = self.iracingname_edit.text()
        new_entry.update([('iRacingNr', new_iracingnr), ('Name', new_name), ('iRacingName', new_iracingname), ('Mail', new_mail)])
        for layouts in self.layout_v_details_container.findChildren(QtWidgets.QHBoxLayout):
            if layouts.count() > 0:
                checkbox = layouts.itemAt(0)
                if checkbox.widget().isChecked():
                    radiobutton_aktiv = layouts.itemAt(2)
                    radiobutton_out = layouts.itemAt(3)
                    if radiobutton_aktiv.widget().isChecked():
                        status_serie = radiobutton_aktiv.widget().serie
                        new_serie_status = "aktiv"
                    else:
                        status_serie = radiobutton_out.widget().serie
                        new_serie_status = "out"
                else:
                    status_serie = checkbox.widget().serie
                    new_serie_status = ""
                new_entry.update([(status_serie + '.Status', new_serie_status)])

                if name == '1 neuer Eintrag':
                    new_entry.update([(status_serie + '.Team', ""), 
                                    (status_serie + '.TeamKorrDatum', ""),
                                    (status_serie + '.TeamKorrGrund', ""), 
                                    (status_serie + '.TeamStKorr', 0), 
                                    (status_serie + '.TeamIncKorr', 0), 
                                    (status_serie + '.TeamPktKorr', 0)])

                else:
                    pass
                
                if self.team_details_lbl.text() == "Team Details":
                    pass

                else:
                    korr_serie = self.team_details_lbl.text()
                    new_teamname = self.teamname_edit.text()
                    new_korrekturper = self.korrekturper_edit.text()
                    new_korrekturgrund = self.korrekturgrund_edit.text()
                    new_starts_str = self.starts_edit.text()
                    if new_starts_str == "":
                        new_starts_str = "0"
                    new_starts = int(new_starts_str)
                    new_incs_str = self.incs_edit.text()
                    if new_incs_str == "":
                        new_incs_str = "0"
                    new_incs = int(new_incs_str)
                    new_points_str = self.points_edit.text()
                    if new_points_str == "":
                        new_points_str = "0"
                    new_points = int(new_points_str)
                    new_entry.update([(korr_serie + '.Team', new_teamname), 
                                        (korr_serie + '.TeamKorrDatum', new_korrekturper), 
                                        (korr_serie + '.TeamKorrGrund', new_korrekturgrund), 
                                        (korr_serie + '.TeamStKorr', new_starts),
                                        (korr_serie + '.TeamIncKorr', new_incs),
                                        (korr_serie + '.TeamPktKorr', new_points)])
        
        driver_exists = self.drivers_df.loc[self.drivers_df['Name'] == new_entry['Name']]

        if name == '1 neuer Eintrag' and driver_exists['Name'].count() == 0:
            self.drivers_df = self.drivers_df.append(new_entry, ignore_index=True)
            source.json_save(self.drivers_df)
            QMessageBox.information(self, "Erledigt", "Neue Daten wurden angelegt.")

        elif name == '1 neuer Eintrag' and driver_exists['Name'].count() > 0:
            QMessageBox.warning(self, "Fehler", new_entry['Name'] + 
                " ist bereits vorhanden und kann nicht doppelt erfasst werden. Es wurde nichts gespeichert.")
        else:
            for key, value in new_entry.items():
                self.drivers_df.loc[self.drivers_df['Name'] == name, [key]] = [value]
            source.json_save(self.drivers_df)
            QMessageBox.information(self, "Erledigt", "Daten wurden überschrieben")
        
       
    def evt_db_backup_btn_clicked(self):
        source.json_backup()
        QMessageBox.information(self, "Erledigt", "fahrer.json wurde ins Backup Verzeichnis kopiert.")

    def evt_fahrer_loeschen_btn_clicked(self):
        del_warn_msg = QMessageBox.question(self, "Löschen?", "Bist du sicher, dass du " + self.name + " löschen willst?")
        if del_warn_msg == QMessageBox.Yes:
            source.del_driver(self.name)
            QMessageBox.information(self, "Gelöscht", 
            self.name + " wurde gelöscht")
        else:
            pass

    def evt_mgmt_selected_name(self):
        self.name = self.mgmt_name_cbb.currentText()
        if self.layout_v_details_container.findChild(QtWidgets.QHBoxLayout, "layout_h_serie_details"):
            self.del_items_in_detail_layout()      
        else:
            pass

        self.drivers_df = source.driver_data_to_df()
        self.driver = self.drivers_df.loc[self.drivers_df['Name'] == self.name]
        self.name = self.driver['Name'].item()
        self.mail = self.driver['Mail'].item()
        self.iracingnr = self.driver['iRacingNr'].item()
        self.iracingname = self.driver['iRacingName'].item()
        if self.name == '1 neuer Eintrag':
            self.name_edit.setText("")
            self.iracingnr_edit.setText("")
            self.mail_edit.setText("")     
            self.iracingname_edit.setText("")
        else:
            self.name_edit.setText(self.name)
            self.iracingnr_edit.setText(str(self.iracingnr))
            self.mail_edit.setText(self.mail)     
            self.iracingname_edit.setText(self.iracingname)
        for col in self.driver.columns:
            if ".Status" in col:
                self.serie = (col.split(".")[0])
                self.status = self.driver[self.serie + ".Status"]
                self.layout_h_serie_details = QtWidgets.QHBoxLayout()
                self.layout_h_serie_details.setObjectName("layout_h_serie_details")
                self.serie_active_chbox = QtWidgets.QCheckBox(self.mgmt_fahrer_groupBox)
                self.serie_active_chbox.setObjectName("serie_active_chbox")
                self.serie_active_chbox.setText(self.serie)
                self.serie_active_chbox.serie = self.serie
                self.serie_active_chbox.toggled.connect(self.evt_select_serie_active_chkbx_toggeld)
                self.layout_h_serie_details.addWidget(self.serie_active_chbox)
                spacerItem_links = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                self.layout_h_serie_details.addItem(spacerItem_links)
                self.serie_active_aktiv_chbox = QtWidgets.QRadioButton(self.mgmt_fahrer_groupBox)
                self.serie_active_aktiv_chbox.setObjectName("serie_active_aktiv_chbox")
                self.serie_active_aktiv_chbox.setText("aktiv")
                self.serie_active_aktiv_chbox.serie = self.serie
                self.serie_detail_buttonGroup = QtWidgets.QButtonGroup(self.layout_h_serie_details)
                self.serie_detail_buttonGroup.setObjectName("serie_detail_buttonGroup")
                self.serie_detail_buttonGroup.addButton(self.serie_active_aktiv_chbox)
                self.layout_h_serie_details.addWidget(self.serie_active_aktiv_chbox)
                self.serie_active_out_chbox = QtWidgets.QRadioButton(self.mgmt_fahrer_groupBox)
                self.serie_active_out_chbox.setObjectName("serie_active_out_chbox")
                self.serie_active_out_chbox.setText("out")
                self.serie_active_out_chbox.serie = self.serie
                self.serie_detail_buttonGroup.addButton(self.serie_active_out_chbox)
                self.layout_h_serie_details.addWidget(self.serie_active_out_chbox)
                self.team_details_btn = QtWidgets.QPushButton(self.mgmt_fahrer_groupBox)
                self.team_details_btn.setObjectName("team_details_btn")
                self.team_details_btn.setText("Team Details")
                self.team_details_btn.serie = self.serie
                self.team_details_btn.clicked.connect(self.evt_team_details_btn_clicked)
                self.layout_h_serie_details.addWidget(self.team_details_btn)
                spacerItem_rechts = QtWidgets.QSpacerItem(600, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
                self.layout_h_serie_details.addItem(spacerItem_rechts)
                self.layout_v_details_container.addLayout(self.layout_h_serie_details)
                
                if self.status.item() == "aktiv" or self.status.item() == "out":
                        self.serie_active_chbox.setChecked(True)
                        if self.status.item() == "aktiv":
                            self.serie_active_aktiv_chbox.setChecked(True)
                        else:
                            self.serie_active_aktiv_chbox.setChecked(False)
                        if self.status.item() == "out":
                            self.serie_active_out_chbox.setChecked(True)
                        else:
                            self.serie_active_out_chbox.setChecked(False)
                else:
                    self.serie_active_chbox.setChecked(False)
                    self.serie_active_aktiv_chbox.setEnabled(False)
                    self.serie_active_out_chbox.setEnabled(False)
                    self.team_details_btn.setEnabled(False)

        self.name_edit.setEnabled(True)
        self.mail_edit.setEnabled(True)
        self.iracingnr_edit.setEnabled(True)
        self.iracingname_edit.setEnabled(True)

        self.team_details_lbl.setText("Team Details")
        self.teamname_edit.setText("")
        self.korrekturper_edit.setText("")
        self.korrekturgrund_edit.setText("")
        self.starts_edit.setText("")
        self.incs_edit.setText("")
        self.points_edit.setText("")

    def evt_mgmt_serie_btn_clicked(self):
        self.mgmt_serie_cbb.clear()
        serie_list = []
        drivers_df = source.driver_data_to_df()
        for col in drivers_df.columns:
            if ".Status" in col:
                serie_list.append(col.split(".")[0])
        self.mgmt_serie_cbb.addItems(serie_list)
        
    def evt_mgmt_selected_serie(self):
        serie = self.mgmt_serie_cbb.currentText()
        self.serie_name_aendern_edit.setText(serie)
        self.serie_loeschen_edit.setText(serie)
        self.serie_loeschen_edit.setReadOnly(True)
    
    def evt_neue_serie_erstellen_btn_clicked(self):
        seriename = self.neue_serie_erstellen_edit.text()
        result = source.add_new_serie(seriename)
        if result == "Ok":
            QMessageBox.information(self, "Erstellt", seriename + 
                                    " wurde erstellt. Vergiss nicht ebenfalls ein Verzeichnis für die Serie zu erstellen")
        elif result == "alreadythere":
            QMessageBox.warning(self, "Fehler", seriename + " ist bereits vorhanden und kann nicht doppelt erstellt werden.")
        else:
            QMessageBox.warning(self, "Fehler", seriename + " konnte nicht erstellt werden.")

    def evt_serie_aendern_btn_clicked(self):
        seriename = self.mgmt_serie_cbb.currentText()
        new_seriename = self.serie_name_aendern_edit.text()
        edit_warn_msg = QMessageBox.question(self, "Ändern?", "Bist du sicher, dass du " + seriename + " umbenennen willst?")
        if edit_warn_msg == QMessageBox.Yes:
            source.edit_serie_name(seriename, new_seriename)
            QMessageBox.information(self, "Erledigt", 
            seriename + " wurde in " + new_seriename + " umbenannt. Falls nötig bitte Verzeichnis ebenfalls anpassen!")
        else:
            pass

    def evt_serie_loeschen_btn_clicked(self):
        seriename = self.mgmt_serie_cbb.currentText()
        del_warn_msg = QMessageBox.question(self, "Löschen?", "Bist du sicher, dass du " + seriename + " löschen willst?")
        if del_warn_msg == QMessageBox.Yes:
            source.del_serie(seriename)
            QMessageBox.information(self, "Gelöscht", 
            seriename + " wurde gelöscht")
        else:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlgMain = DlgMain()
    dlgMain.show()
    app.exec()


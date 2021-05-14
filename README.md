# RAGE - RAnglistenGEnerator für die FLANC (www.flanc.ch)
RAGE ist in Python 3.6 gechrieben und benötigt folgende Module.

Pandas
Die eingelesenen JSON Daten werden in ein Pandas Dataframe eingelsen. Deshalb startet alles jeweils mit einem "xxx laden" Button. Danach kann mit weiteren Buttons den Datenbestand gefilter und als Liste ausgegeben werden. Dies Lösung ist nicht die Beste, funktioniert aber soweit ganz gut. Vorallem können so Daten leicht ins Excel exportiert werden.
Die Funktionen, welche die Daten aufbereiten sind im Modul (Verzeichnis) "aufbereitung" und sind in input.py, output.py und work.py eingeteilt. 

openypxl
Um die Excel Exporte wunschgemäss formatieren zu können, wird openpyxl verwendet. Die Formatierung ist im Modul (Verzeichnis) "excel". Die formatexport.py formatiert die einzelnen Listen. Die writeexport.py schreibt diese dann effektiv ins Excel. Hier werden nur noch die Spaltenbreiten mitgegeben. Da dies teilweise noch statisch hinterlegt ist, dann es sein, dass hier später Anpassungen nötig werden.

PyQt5 und Qt
Um ein einigesmassen ansprechendes GUI zu erstellen wurde PyQt5 verwendet. Die Dateien befinden sich im Modul (Verzeichnis) "ui". Die FLANC_RAGE.ui wurde mit dem Qt Designer generiert und als Ui_FLANC_RAGE.py kompiliert. Ebenfalls vorhanden und kompiliert ist die Qt_GUI.qrc als Qt_GUI_rc.py. Damit werden Ressourden wie Bilder zur Verfügung gestellt. Das Layout wird in der app.py als Modul implementiert und kann daher problemlos immer wieder neu kompiliert werden, falls Änderungen im GUI nötig sind. Einzig muss in der Ui_FLANC_RAGE.py in der untersten Zeile der Eintrag:
import Qt_GUI_rc.py in
from ui import Qt_GUI_rc.py geändert werden.
Ebenfalls im "ui" Verzeichnis müssen sich alles Grafiken befinden.

pyinstaller
Das Programm wird mit pyinstaller. Die Parameter dazu befinden sich in der Datei wichtig.txt

Versionsverlauf
Version 1.0 - "Janeway": Bugfixes, stabile Version
Version 0.9 - "Crusher": Serienmanagement und Backup
Version 0.8 - "Troi": Fahrer*innen Management
Version 0.7 - "Yar": Nur Ranglisten generieren

Lizenzierung siehe separate Datei.

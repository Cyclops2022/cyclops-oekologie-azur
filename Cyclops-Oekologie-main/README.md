# Cyclops-Oekologie: Repository zum Dashboard für die ökologische Bewertung

## Prinzip des Dashboards
Welche Emissionen sind mit einem Recyclingprozess verbunden und wie setzen sie sich zusammen?    
Dieses Dashboard ermöglicht die Konstruktion eines individuellen Recyclingprozesses durch die Auswahl der verwendeten Maschinen.

Basierend auf zusammengetragenen Emissionswerten für Recyclingmaschinen wurde eine Webanwendung programmiert, in der User einen Recyclingprozess über die Auswahl der verwendeten Maschinen zusammenstellen können. Die getätigten Angaben werden verarbeitet und eine Übersicht über die anfallenden Emissionen pro kg Rezyklat ausgegeben.

## Umsetzung
Das Dashboard ist mit dem Python-Framework Dash entwickelt worden und wird auf Heroku gehostet: https://cyclops-oekologie.herokuapp.com/

Bei der Erstellung eines individuellen Recyclingprozesses im Auswahlbereich des Dashboards können sowohl Maschinen, für die Daten zu Durchsatz und Leistung recherchiert und in der Tabelle gesammelt wurden, über ein Dropdown-Menü ausgewählt werden, als auch Werte für Durchsatz und Leistung manuell eingetragen werden. Nachdem eine Maschine im Dropdown-Menü ausgewählt wurde, werden Leistung, Durchsatz und spezifische Emissionen mithilfe der Tabelle ermittelt und in den entsprechenden Feldern im Dashboard eingetragen. Die Berechnung der Emissionen erfolgt dabei über den Emissionsfaktor des deutschen Strommixes auf Grundlage des Stromverbrauchs und des Durchsatzes der Anlagen. Für einige Maschinen stehen die Daten zu Leistungsaufnahme und Durchsatz aus unserer Datentabelle zur Verfügung.

Über einen Button kann die Auswahl gespeichert werden, sodass die Maschine in den Recyclingprozess und damit in die Emissionsberechnung integriert wird. Im Dashboard werden sowohl die spezifischen Emissionen einer Maschine als auch die bisherigen Gesamtemissionen angezeigt, sodass der User mitbekommt, dass die Daten übernommen wurden. Gespeicherte Daten sind persistent, d.h., bei erneuter Auswahl des Prozessschrittes werden die bereits getätigten Angaben angezeigt. Über einen weiteren Button können gespeicherte Angaben zu einem Prozessschritt wieder gelöscht werden. 

Die Daten geben dabei nur eine Übersicht über die Emissionen, die aus dem Stromverbrauch der Anlagen entstehen. Andere Emissionen werden vernachlässigt. Das können z.B. Emissionen für die Bereitstellung von Betriebsmitteln wie Waschwasser sein, Emissionen für Transport und Logistik von und zu Ihrem Unternehmen aber auch innerhalb Ihres Prozesses, oder Emissionen die durch die Bereitstellung der Infrastruktur und Anlagen entstehen. Um eine vollständige Übersicht über all diese Emissionen zu erhalten, empfehlen wir Ihnen, sich mit unseren Kollegen vom SKZ in Verbindung zu setzen.

## Impressum:
Kontakt: Phillip Bendix, Wuppertal Institut - phillip.bendix@wupperinst.org     
Umsetzung: Jonathan Kirchhoff, Maike Jansen, Phillip Bendix

Das Dashboard entstand im Rahmen des CYCLOPS Projektes, gefördert durch das Bundesministerium für Bildung und Forschung.

## Lizenz
Die Inhalte des Repositories stehen unter der Creative Commmons Namensnennung 3.0 Deutschland (CC BY 3.0 DE) Lizenz. Sie können geteilt und weiterverarbeitet werden, wenn dabei auf die Urheber und die Lizenz verwiesen wird und eventuelle Änderungen kenntlich gemacht werden.
Die vollständige Lizenz kann unter folgendem Link eingesehen werden: https://creativecommons.org/licenses/by/3.0/de/

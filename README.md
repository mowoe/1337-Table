# Forked from a GitHub Account that has been deleted :warning:
# 1337 Table
## Der Tisch der Warpzone

### Der 1337, was ist das?
Der 1337 Table bzw. 1337 Tisch ist der Tisch der Warpzone, dem Hackerspace in Münster. Dies ist allerdings kein normaler Tisch, dieser Tisch ist zum einen komplett selber aus Beton gegossen. Zum Anderen sind in diesem Tisch ziemlich viele Leuchtdioden verbaut. In dem 150cm x 80cm großen Tisch verstecken sich 700 Leuchtdioden als Matrix angeordnet und an den seiten befindet sich jeweils einmal das Wort "Warpzone", welches ebenfalls beleuchtet werden kann.
### Was macht der Code in diesem Repo?
Der Code in diesem Repo ist bisher ausschließlich für die ansteuerung der im Tisch enthaltenen Matrix. Mit dem vorhanden Code ist ein Framework gestellt, für das man mit geringem Aufwand Apps für den Tisch schreiben kann. (Wie man dies macht wird weiter unten erklärt.) 
### Das Framework
Das Framework sorgt dafür, dass Eingaben vom Nutzer gelesen werden, diese an Apps weitergeleitet werden und die Apps wiederum irgendetwas auf der Matrix anzeigen können. Das Framework teilt Apps bisher in zwei Kategorien ein, zum einen "Games" und zum anderen "Ambients". Games sind Spiele, bzw. generell Applikationen die mit dem Nutzer interagieren. Ambients sind Animationen, bzw. andere anzeigen die keine Interaktion vom Nutzer erfordern. Diese unterteilung gibt es, damit das Framework Ambients starten kann, wenn es erkennt, dass der Nutzer im Moment inaktiv ist.
### Selber Apps schreiben
Um für das Framework Apps zu schreiben braucht es nicht viel. Man benötigt dieses Repo, einen python2.7 Interpreter und ein paar Abhängigkeiten von diesem Repo (siehe unten).
Der Aufbau einer App ist bei einem Game und einem Ambient der Selbe. Hier ist einfach mal ein Stück beispiel Code:
```python
#!/usr/bin/env python2.7
from Framework.apps.ambient import Ambient  # Als Elternklasse für die App
from Framework.font import render_text  # Um Text zu rendern
from Framework.theme import theme  # Um auf Themes zuzugreifen
from Framework.defaults import get_data_directory  # Um auf Datein zuzugreifen

class Example(Ambient):
    def __init__(self, matrix, parent):
        super(Example, self).__init__(matrix, parent)

    def loop(self):
    
    	# Zugriff auf Frame:
        self.frame[y, x] = (r, g, b)
        
        # Frame leeren:
        self.clear()
        
        # Text rendern
        # fr, fg, fb -> Vordergrundfarbe, br, bg, bb -> Hintergrundfarbe
        render_text(self.frame, (fr, fg, fb), (br, bg, bb), text, x, y)
        
        # Zugriff auf das aktuelle Theme
        r, g, b = theme["property"]
        
        # Zugriff auf Dateien
        # Der Parameter ist der Name der App, zurückgegeben wird ein
       	# Pfad in den die App am besten Dateienablegen soll.
        path = get_data_directory("Example") 
        
    	# Tastenabfragen:
        # Tasten: "A", "B", "X", "Y", "START", "SELECT", "UP", "DOWN", "LEFT", "RIGHT"
        if self.is_key_down("B"): pass  # Beim drücken der Taste
        if self.is_key_pressed("B"): pass  # Bei anhaltendem Tastendruck
        if self.is_key_up("B"): pass  # Beim lösen der Taste
        
        # Zum Menu zurückkehren:
        if self.is_key_up("B"):
        	self.parent.back()

```
##### Noch ein bisschen Erklärung zum Code:
```self.frame``` ist ein Numpy array der größe 35x20x3 bzw des Shapes (20, 35, 3).\
Um den Code auf ein Game umzubauen musst du deine Klasse bloß anstatt von Ambient von Game erben lassen und die eingebundenen Module ggf. abändern.

### Die App einbinden:
Um die neu geschriebene App in das Framework einzubinden muss man das Python File mit der Klasse in den richtigen Ordner legen. Dieser ist für Games ```Framework/apps/games/``` und für Ambients ```Framework/apps/ambients``` im zweiten schritt muss man in der ```conf.py``` im selben Verzeichnis noch das Dictionary ```apps``` mit seiner App erweitern. Hierzu erweitert man es mit dem Namen seiner App als key (ACHTUNG: Max 8 Zeichen) und als Value gibt man seine Klasse an, dazu muss sie natürlich vorher eingebunden werden. Dies wird nach dem Schema ```from Framework.apps.ambient.GameOfLife import GameOfLife``` gemacht. Bei Ambients ist in der ```conf.py``` noch eine List mit "Standby Apps" definiert, hier kann man seine Klasse angeben, damit das Framework diese bei Inaktivität des Nutzers startet. Tut man das nicht, wird sie auch nicht gestartet.

### Wie bekomme ich meine App jetzt auf den Tisch in der Warpzone?
Wende dich dazu am besten an mich, oder mache ein Pull Request auf dieses Repo, da ich allerdings ein n00b bin und keine Ahnung von Pull Requests habe wäre ist mir Momentan lieber wenn du dich an mich direkt wendest.

### Was sind nun die Abhängigkeiten, damit ich die Software auch bei mir selber laufen lassen kann?
Du braucht um die Software auf deinem Rechner laufen zu lassen folgende Python Pakete: ```pygame``` und ```numpy```, dies sind die mindestanforderungen. Apps können natürlich mehr Pakete benötigen, deswegen wird die Software im Zweifelsfall crashen, wenn du eine App startest für die Abhängigkeiten fehlen.


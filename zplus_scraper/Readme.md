# ZPlusScraper

Ein Python-Script basierend auf Scrapy um frei verfügbare Artikel auf zeit.de abzugreifen bevor sie im Z+ Bezahlabonnement verschwinden.

## Hintergrund
Beim regelmäßigen Lesen von zeit.de ist mir aufgefallen dass beliebte frei verfügbare Artikel nach kurzer Zeit im Bezahlabonnement verschwinden.

## Aufbau
Diese Programm nutzt Scrapy um in Regelmäßigen Abständen, wie in der main.py definiert, über die einzelnen Hauptseiten von zeit.de die Artikel abzugreifen.
Dabei werden keine Schutzmaßnahmen von zeit.de umgangen. ZPlusScraper lädt nur normal verfügbare Artikel herunter. Somit sind Artikel die direkt im Bezahlabonnement landen nicht herunterladbar.
Die Ergebnisse werden in eine mySql-Datenbank gespeichert aus der sich der Artikel-Text abrufen lässt.
Es ist möglich scrapy manuell über 'scrapy crawl zplus_spider' zu starten oder die main.py aufzurufen die das gleiche in einer Endlosschleife ausführt.

## Hinweise
Bitte geht damit respektvoll um, es ist nicht ansatzweise nötig ZPlusScraper häufiger als alle paar Minuten laufen zu lassen.

Dieses Projekt war einerseits etwas Frust von mir geschuldet und anderseits eine Übung für meine ausbaufähigen python Kenntnisse.
Um Feedback und Kritik bin ich dankbar.


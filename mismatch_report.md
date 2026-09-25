# Intent Schema Mismatch Report

This report highlights test cases where the model correctly followed the prompt's granular schema, but failed against the `.xlsx` expected labels.

| ID | Utterance | Golden Expected Intent | Prompt Output (Granular) |
|----|-----------|------------------------|--------------------------|
| 2 | Gehe zu 20:15 Uhr. | TV__NAVIGATE | TV__NAVIGATE_TO_DATETIME |
| 8 | Öffne die Sprachsteuerung | TV__OPEN_MENU | TV__NAVIGATE_MENU |
| 9 | Zeige mir das Programm. | TV__OPEN_MENU | TV__NAVIGATE_MENU |
| 10 | Okay. | TV__OK | N/A |
| 12 | Spule um fünf Minuten zurück. | TV__NAVIGATE | TV__SEEK_OR_REWIND |
| 13 | Wo läuft gerade ein Actionfilm? | TV__SEARCH, TV__PROGRAM_WHEN_WHERE | TV__PROGRAM_FOR_SPECIFIC_CONTENT |
| 15 | Was kommt gerade auf Kanal 12? | TV__PROGRAM | TV__PROGRAM_CHANNEL_OR_TIME_ONLY |
| 17 | Was läuft jetzt auf Kanal 25? | TV__PROGRAM | TV__PROGRAM_CHANNEL_OR_TIME_ONLY |
| 18 | vier Stunden später | TV__NAVIGATE | TV__NAVIGATE_TO_DATETIME |
| 21 | Zeig mir das Programm für morgen. | TV__PROGRAM | TV__PROGRAM_CHANNEL_OR_TIME_ONLY |
| 22 | Wann kommt Sturm der Liebe? | TV__SEARCH, TV__PROGRAM_WHEN_WHERE | TV__PROGRAM_FOR_SPECIFIC_CONTENT |
| 23 | Wann kommt ein Friller? | TV__SEARCH, TV__PROGRAM_WHEN_WHERE | TV__PROGRAM_FOR_SPECIFIC_CONTENT |

# Speech-to-SQL

The goal of this project was to use a natural language processing toolkit to pass the SQL exam from my university. 

I am using Google Cloud speech-to-text for <b> POLISH </b> language with a boost for specific phrases. It makes conversion from text to SQL query easier.
Then I use PLY lex to process words in natural language to SQL keywords, tables and column names (currently only hardcoded). Software is capable of handling logic, numbers and invented names. For advanced uses, it can also handle nested subqueries and joins. An output SQL query is in the correct syntax to copy-paste to  MySQL.

With this project, I was able to pass an example exam, given for training purposes from my university classes, with only my voice.

Examples
Input | Output
--- | ---
zaznacz suma koszt<br>z tabeli wizyty gdzie pacjent jest równy<br>stwórz podzapytanie zaznacz id pacjenta<br>z tabeli pacjenci gdzie<br>nazwisko jest równe nazwa własna gumowska<br>oraz imie jest równe nazwa własna anna<br>zakończ podzapytanie<br>|SELECT SUM(koszt)<br>FROM wizyty<br>WHERE pacjent = (<br> SELECT id_pacjenta<br>FROM pacjenci<br>WHERE nazwisko = 'gumowska' AND imie = 'anna');
wybierz nazwisko z tabeli pacjenci<br>połącz lewostronnie wizyty na pacjenci<br>kropka id pacjenta jest równe wizyty<br>kropka pacjent gdzie wizyty<br>kropka pacjent jest bez wartości|SELECT nazwisko<br>FROM pacjenci<br>LEFT JOIN wizyty ON pacjenci.id_pacjenta = wizyty.pacjent<br>WHERE wizyty.pacjent IS NULL;
zaznacz unikalne lekarze kropka nazwisko<br>lekarze kropka specjalnosc<br>z tabeli lekarze połącz  wizyty<br>na lekarze kropka id lekarza równe wizyty kropka lekarz<br>złącz pacjenci na pacjenci kropka<br>id pacjenta równe wizyty kropka pacjent<br>gdzie pacjent kropka nazwisko równe nazwa własna witkowski|SELECT DISTINCT lekarz.nazwisko, lekarz.specjalnosc<br>FROM lekarz<br>JOIN wizyty ON lekarz.id_lekarza = wizyty.lekarz<br>JOIN pacjenci ON pacjenci.id_pacjenta = wizyty.pacjent<br>WHERE pacjent.nazwisko = 'witkowski';
zaznacz nazwisko specjalnosc z tabeli lekarze<br>gdzie specjalnosc jest równa rozpocznij podzapytanie<br>wybierz specjalnosc z tabeli lekarze gdzie nazwisko<br>jest równe nazwa własna stefanowicz zakończ podzapytanie<br>oraz nazwisko jest różne od  nazwa własna stefanowicz|SELECT nazwisko specjalnosc<br>FROM lekarz<br>WHERE specjalnosc =(<br>SELECT specjalnosc<br>FROM lekarz<br>WHERE nazwisko = 'stefanowicz')<br>AND nazwisko != 'stefanowicz';

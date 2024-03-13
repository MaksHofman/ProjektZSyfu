Projekt z systemów cyfrowych.
Zadanie: wysyłamy 64 bity(wiadomosci) i podczas tranzytu 8 bitów jest obruconych(w "burstach"). Trzeba wyslać wiadomość tak żeby cała przeszła i nie trzeba było ponownie wysyłac.
Wykonanie: Użyłem kodu Hamminga warjantu SECDED. Przetasowałem bity przed wysłaniem tak żeby w segmentach 8 bitowych nie było 2 bitów z jednej paczki(rozbijamy 64bity na 8 paczek po 8 bitów).

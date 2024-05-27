# "Program do rejestrowania pacjentów na wizyty u lekarza"

### Założenia projektu
Program musi:
- umożliwić wprowadzenie danych pacjenta (imię, nazwisko, PESEL) oraz przypisanie mu terminu wizyty
- dla danego pacjenta udostępniać listę wszystkich wizyt, natomiast dla wybranego dnia – wyświetlać listę wszystkich zajętych terminów
- zapis/odczyt danych używanych przez program odbywa się do/z pliku tekstowego (można użyć standardowego formatu, np. CSV/TSV lub JSON)
***

### Struktura projektu

Punktem wejściowym aplikacji jest plik 'main.py', który można uruchomić zarówno w terminalu jak i wykorzystując IDE.
Po uruchomieniu pliku 'main.py' w konsoli pojawia się  czytelny dla użytkownika interfejs aplikacji.

Program nie wymaga instalowania pakietów dodatkowych spoza biblioteki standardowej.

Do trwałego przechowywania danych pacjentów i wizyt wykorzystano format JSON, a konkretnie 2 pliki: 'patients.json' i 'appointments.json'. Nie należy samemu edytować tych plików. W wyjątkowym przypadku, gdyby użytkownik chciał szybko usunąć wszyskie dane w tych plikach, należy zastąpić ich zawartość wyrażeniem '[]'.

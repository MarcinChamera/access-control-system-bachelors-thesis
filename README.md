W pliku requirements.txt znajdują się wszystkie niezbędne biblioteki do uruchomienia programu. Do pobierania bibliotek i wirtualnego środowiska
wykorzystano język Python w wersji 3.7. Taka też wersja jest wymagana, aby pomyślnie wykonać skrypty. Przed uruchomieniem programu za pomocą
skryptu run_app wymagana jest jednorazowa instalacja zależności za pomocą skryptu install_prerequirements.

1. Aby zainstalować wirtualne środowisko i niezbędne biblioteki przy pomocy skryptu:
* Dla systemu Windows należy uruchomić plik install_prerequirements.bat z folderu WINDOWS
* Dla systemu Linux należy uruchomić plik install_prerequirements.sh z folderu LINUX, wpisując w terminalu komendę bash install_prerequirements.sh.
  Aby móc uruchomić skrypt, należy nadać prawa do uruchamiania tego pliku za pomocą komendy: chmod +x install_prerequirements.sh

2. Aby uruchomić program:
* Dla systemu Windows należy uruchomić plik run_app.bat z folderu WINDOWS
* Dla systemu Linux należy uruchomić plik run_app.sh z folderu LINUX, wpisując w terminalu komendę bash run_app.sh
  Aby móc uruchomić skrypt, należy nadać prawa do uruchamiania tego pliku za pomocą komendy: chmod +x run_app.sh

W wypadku, gdy instalacja za pomocą skryptów nie przeszłaby pomyślnie, biblioteki należy pobrać ręcznie. W następnej kolejności należy uruchomić
plik face_biometry_access.system.py 
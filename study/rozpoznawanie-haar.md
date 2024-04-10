# Rozpoznawanie obiektów przy pomocy *Cascade Calssifiers*

Notatki na podstawie materiałów:
* [*Training a Cascade Classifier - OpenCV Object Detection in Games #8*](https://www.youtube.com/watch?v=XrCAvs9AePM&ab_channel=LearnCodeByGaming).
* [*Dokumentacja OpenCV - trenowanie klasyfikatora*](https://docs.opencv.org/4.2.0/dc/d88/tutorial_traincascade.html)
* [*Dokumentacja OpenCV - używanie klasyfikatora*](https://docs.opencv.org/4.2.0/db/d28/tutorial_cascade_classifier.html)
* [*OpenCV Python Tutorial #8 - Face and Eye Detectio*](https://www.youtube.com/watch?v=mPCZLOVTEc4&ab_channel=TechWithTim)
* [*Recommended values for OpenCV detectMultiScale() parameters*](https://stackoverflow.com/questions/20801015/recommended-values-for-opencv-detectmultiscale-parameters)

## Typy *Cascade Calssifiers*
* **Haar** - dokładniejszy
* **LBP** - szybszy w trenowaniu

## Trening
Do poprawnego rozpoznawania obiektów niezbędne jest przetrenowanie klasyfikatora na jak największym i zawierającej dobrej jakości elementy zbiorze danych (w tym wypadku zbiorze obrazów). Każdy klasyfikator powinien przy tym specjalizować się w wykrywaniu jednego typu obiektów (np. tylko twarzy, albo tylko oczy itd).

### Grupy danych
* **Positive images** - obrazy pokazujące obiekt, który klasyfikator ma wykryć. Najlepiej, aby pokazywały ten obiekt w dowolnie wielu różych kontekstach, pozycjach i warunkach.
* **Negative images** - obrazy nie przedstawiające obiektu, który klasyfikator ma wykryć.

### Jak duzo danych powinniśmy mieć?
Setki jak nie tysiące obrazów dla zarówno positive jak i negative images.

### Oprogramowanie treningu

#### Przygotowanie danych negatywnych
Należy stworzyć plik `txt` zawierający listę ścieżek do danych negatywnych. Każda ściezka powinna być w osobnej linii.

#### Przygotowanie danych pozytywnych
Dla danych pozytywnych również nalezy utworzyć plik `txt`. Jego struktura jest jednak dużo bardziej skomplikowana niż w przypadku danych negatywnych, gdyż musi on zawierać dodatkowe adnotacje. Z tego względu do jego wytworzenia należy wykorzystać program `opencv_annotation.exe`, zawarty w skompilowanej wersji *OpenCV* dostepnej na [*SourceForge*](https://sourceforge.net/projects/opencvlibrary/files/). Program znajduje się w folderze `build\x64\vc16\bin`. Należy go uruchomić z poziomu konsoli przy pomocy polecenia:

```bash
opencv_annotation.exe --annotations=output-file.txt --images=positive-images-directory
```
* `--annotations` - ścieżka do pliku wyjściowego
* `--images` - ścieżka do katalogu, w którym znajdują się obrazy pozytywne

Po uruchomieniu program będzie wyświetlał kolejne obrazy z zadanego w `--images` folderu. Należy na nich wyrysować prostokąy zawierające obiekt, który ma zostać wykryty i zatwierdzić każdy z nich klawiszem `C` (w przeciwnym wypadku prostokąt zostanie usunięty przy rysowaniu kolejnego prostokąta). Ostatni zatwierdzony prostokąt można usunąć klawiszem `D`. Przejść do kolejnego obrazu można klawiszem `N`.

> UWAGA! Program `opencv_annotations.exe` generuje niepoprawne ścieżki do plików z obrazami wstawiając w nich znaki `\`. Należy je wszystkie zamienić na znaki `/`. 

Po wygenerowaniu pliku `txt` nalezy wygenerować plik `vec` z próbkami dla klasyfikatora. Wystarczy posłużyć się w tym celu kolejnym programem ze skompilowanej *OpenCV* o nazwie `opencv_createsamples.exe`. Należy uruchomić go poleceniem:

```bash
opencv_createsamples.exe -info path-to-txt-file -w window-width -h window-height -num x -vec path-to-output-file
```
* `-info` - ścieżka do pliku `txt` z danymi
* `-w`, `-h` - wymiary okna detekcji w pikselach. Determinuje ono wymairy największego, możliwego do wykrycia obiektu. Im mniejsze okno, tym większa dokładność i dłuższy czas treningu. Zwykle przyjmuje się wymiary `(24, 24)` lub `(20, 20)`.
* `-num` - maksymalna liczba próbek, jaka ma zostać wygenerowana z pliku `-info`. Powinna być ona większa niz licza wyrysowanych na obrazach prostokątów.
* `-vec` - ścieżka do wyjściowego pliku `vec`.

#### Generowanie plików treningowych
Do generowania treningowych plików `xml` używa się kolejnego programu ze skompilowanej wersji *OpenCV* nazywającego się `opencv_traincascade.exe`. Uruchamia się go następującą komendą:

```bash
opencv_traincascade.exe -data output-directory -vec positive-data -bg negative-data -w window-width -h window-height -numPos p -numNeg n -numStages x -maxFalseAlarmRate mfa -minHitRate mhr
```
* `-data` - ścieżka do katalogu, gdzie zapisane mają zostać dane wyjściowe
* `-vec` - ścieżka do pliku `vec` z próbkami pozytywnymi.
* `-bg` - ścieżka do pliku `txt` z danymi negatywnymi
* `-w`, `-h` - wymiary okna detekcji. Muszą być identyczne z tymi, które posłużyły do generowania pliku `vec`.
* `-numPos` - maksymalna liczba próbek pozytywnych. Powinna być ona mniejsza niż liczba wektorów z pliku `-vec`.
* `-numNeg` - maksymalna liczba próbek negatywnych. Z zasady ustawia się ją na 2 razy mniejszą niż `-numPos`.
* `-numStages` - liczba iteracji treningu.
* `-maxFalseAlarmRate` - maksymalna, dopuszczalna wartość `FA`. Trener będzie zwiększał liczbę warst modelu aż to osiągnięcia wartości dopuszczalnej.
* `-minHitRate` - minimalna, dopuszczalna wartość `HR`. Trener będzie zwiększał liczbę warts modelu aż do osiągnięcia wartości dopuszczalnej.

W czasie działania program `opencv_traincascade.exe` będzie wyświetał w konsoli informacje o każdej iteracji w formie tabeli składającej się z kolumn:
* `HR` - *hit rate*, jak częśto dane pozytywne były poprawnie rozpoznane
* `FA` - *false alarm*, jaka często dane negatywne były pomylone z pozytywnymi
* `N` - numer warstwy

Najlepiej aby warstwa o największym `N` miała jak najmniejszą wartość `FA` przy jednoczesnym uniknięciu przetrenowania. To czy nastąpiło przetrenowanie można rozpoznać po wartości `NEG count : acceptanceRatio` znajdującej się nad tabelą. Jeżeli jej pierwsza cyfra znacząca pojawi się dopiero na 5 lub dalszym miejscu po przecinku, to wskazuje to na przetrenowanie.

#### Trenowanie modelu
Aby przetrenować model używany w apliakcji należy wgrać do niego plik `xml` z danymi treningowymi przy pomocy konstruktora klasy `cv.CascadeClassifier`.

```py
haar = cv.CascadeClassifier(file)
```
* `file` - ścieżka do pliku z danymi treningowymi

## Użycie modelu wykrywającego

W pierwszej kolejności należy stworzyć instancję klasy `cv.CascadeClassifier` wskazując przy tym odpowiedni plik `xml` z danymi treningowymi. Wykrywanie obiektów wykonać można przy pomocy metody `detectMultiScale()` tej instancji.

```py
classifier = cv.CascadeClassifier('model.xml')
```
```py
classifier.detectMultiScale(
    image=image,
    scaleFactor=1.05,
    minNeighbors=3
    minSize=[30, 30],
    maxSize=[200, 200]
)
```
* `scaleFactor` - obraz zadany do klasyfikatora może mieć dowolny wymiar. Obrazy treningowe mogły nie być tego samego rozmiaru i stąd niezbędne będzie krokowe skalowanie w dół obrazu, na którym mamy coś wykryć. Parametr `scaleFactor` określa jak bardzo mamy zmniejszać obraz `image` w po każdej iteracji. Przykładowo zalecana wartość `1.05` będzie zmniejszała obraz o 5% po każdej iteracji. Im mniejsza wartość tym lepsza dokładność, ale też dłuższy czas przetwarzania.
* `minNeighbors` - jak dokładny ma być algorytm? Im wyższa wartośc tym wyższa dokładność, ale też dłuższy czas ptrzetwarzania. Zalecana jest wartość `3-6`. Parametr opcjonalny.
* `minSize` - najmniejszy, dopusczalny rozmiar wykrywanego obiektu w pikselach. Zalecane jest 30x30 pikseli.
* `maxSize` - największy, dopuszczalny rozmair wykrywanego obiektu w pikselach. Parametr opcjonalny.

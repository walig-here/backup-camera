# Nauka _OpenCV_ - sesja 4

## Progowanie (eng. _thresholding_)

### Na co pozwala progowanie?
Progowanie pozwala na zbinaryzowanie obrazów, czyli np. przejścia z wielobarwnego obrazu do obrazu złożonego wyłącznie z pikseli białych (`'1'`) oraz czarnych (`'0'`).

### Proste progowanie (eng. _simple tresholding_)
Rodzaj progowania, który przechodzi przez każdy piksel obrazu i zamalowuje go jedną z 2 barw na podstawie prostego porównania **jego intensywności** do **instensywności progowej**. Proste progowanie można wykonać przy pomocy funkcji `treshold()`. Zwraca ona krotkę `(ret, image)`, gdzie `image` to zbinaryzowany obraz.

```py
thresholded_image = cv.threshold(image, threshold, color, mode)
```
* `image` - obraz w skali szarości, który chcemy sprogować.
* `treshold` - progowa intensywnośc piksela.
* `color` - intensywność odpowiadająca wartości logicznej `'1'`.
* `mode` - typ progowania.

### Typy progowania
* `cv.THRESH_BINARY` - piksel jest uznawany za logiczną `'1'` jeżeli jest powyżej intensywności progowej.
* `cv.THRESH_BINARY_INV` - piskel jest uznawany za logiczną `'1'` jeżeli jest poniżej intensywności progowej.

### Progowanie adaptywne (eng. _simple thresholding_)
Wartość **intensywności progowej** jest jest dobierana automatycznie przez algorytm progujący na podstawie sąsiedztwa piksela. Progowanie adaptacyjn można wykonać przy pomocy funkcji `adaptiveThreshold()`, także zwracającej krotkę `(ret, image)`.

```py
image = cv.adaptiveThreshold(image, color, threshold_alg, mode, kernel, constant)
```
* `image` - obraz w skali szarości, który chcemy sprogować.
* `color` - intensywność odpowiadająca wartości logicznej `'1'`.
* `threshold_alg` - algorytm progujący na podstawie sąsiedztwa.
* `mode` - typ progowania.
* `kernel` - długość boku okna sąsiedztwa w pikselach.
* `constant` - stała odniżająca intensywność progową.

#### Algorytmy progujące
* `cv.ADAPTIVE_MEAN_C` - intensywność progująca jest średnią intensywności pikseli z sąsiedztwa pomniejszoną o stałą `constant`.
* `cv.ADAPTIVE_GAUSSIAN_C` - intensywnośc progująca jest średnią intensywności rozkładu normalnego pikseli z sąsiedztwa pomniejszoną o stałą `constant`.

## Wykrywanie krawędzi

### Metoda Laplace'a
Metoda wykrywania krawędzi, której efekt może być przyrównany do **rozmazanego obrazka namalowanego kredą na czanrnej tablicy**. Jest to raczej rzadzko używana metoda. Można jej użyć wywołując funckję `Laplacian()` i obrabiając nieco jej wynik. Obróbka jest konieczna, gdyż zwraca ona **gradienty**, które mogą przyjąć wartości ujemne, a więc niedozwolone w obrazach. Do obróbki używa się pakietu _numpy_.

```py
laplacian_edges = cv.Laplacian(image, cv.CV_64F)
laplacian_edges = np.uint8(np.absolute(laplacian_edges))
```
* `image` - obrazek w odcieniach szarości.

### Metoda Sobel'a
Metoda obliczająca **gradienty** względem osi X bądź osi Y. Zatem, aby otrzymać krawędzie obrazka należy **wykonać logiczną sumę na obrazkach z wykrytymi krawędziami w osi X oraz Y**. Jest to nieco bardziej popularna metoda od metody Laplace'a. Krawędzie w niej są zaznaczane na czarno, a tło na biało. Skorzystać z niej można wywołując funckję `Sobel()`.

```py
sobelx = cv.Sobel(image, cv.CV_64F, 1, 0)
sobely = cv.Sobel(image, cv.CV_64F, 0, 1)
sobel_combine = cv.bitwise_or(sobel_x, sobel_y)
```
* `image` - obrazek w odcieniach szarości.

## Detekcja obiektów

### Haar Cascades
Typ klasyfikatora obiektów na obrazach, a więc mechanizmu, który sprawdza czy obraz zawiera obiekt lub obiekty danego typu. Niestety jest dosyć podatny na szumy na obrazach, co może wpłynąć na jego poprawność. Przetrenowane do rozpoznawania obiektów danego typu klasyfikatory _Haar Cascade_ są przechowywane w specjalnych plikach `.xml`.

#### Wczytanie klasyfikatora
Wczytanie klasyfikatora odbywa się przy pomocy funkcji `CascadeClassifier()`.

```py
haar = cv.CascadeClassifier(file)
```
* `file` - nazwa pliku z klasyfikatorem

#### Użycie klasyfikatora
Użycie klasyfikatora sprowadza się do wywołania funkcji `detectMultiscale()`. Zwraca ona prostokąt, w którym znajduje się wykryty obiekt. Jest to bardzo wygodne, gdyż taki prostokąt można następnie łątwo wyrysować na obrazku.

```py
rectangle = cv.detectMultiscale(image, scaleFactor=1.1, minNeighbors=3)
```
* `image` - obrazek, na którym mamy wykryć obiekt
* `scaleFactor` - parametr 1.
* `minNeighbors` - parametr będący odwrotnie proporcjonalny do czułości detektora.

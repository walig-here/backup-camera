# Nauka _OpenCV_ - sesja 1

## Spis treści
* [Dodatkowe elementy](#dodatkowe-elementy)
    * [Biblioteka _caer_](#biblioteka-caer)
* [Wczytywanie](#wczytywanie)
    * [Wczytywanie obrazów](#wczytywanie-obrazów)
        * [Stworzenie pustego obrazu](#stworzenie-pustego-obrazu)
    * [Wczytywanie wideo](#wczytywanie-wideo)
        * [Zwalnianie wideo](#zwalnianie-wideo)
* [Wyświetlanie](#wyświetlanie)
    * [Wyświetlanie obrazów](#wyświetlanie-obazu)
        * [Autoskalowanie obrazów](#autoskalowanie-obrazów)
    * [Wyświetlanie wideo](#wyświetlanie-wideo)
        * [Zakończenie wyświetlania](#zakończenie-wyświetlania)
* [Skalowanie](#skalowanie)
    * [Pobranie wymiarów obrazu](#pobranie-wymiarów-obrazu)
    * [Zmiana wymiarów (uniwersalna)](#zmiana-wymiarów-uniwersalna)
        * [Rodzaje interpolacji](#rodzaje-interpolacji)
    * [Zmiana wymiarów (wideo czasu rzeczywistego)](#zmiana-wymiarów-wideo-czasu-rzeczywistego)
* [Rysowanie na obrazach](#rysowanie-na-obrazach)
    * [Wypełnianie obrazu kolorem](#wypełnianie-obrazu-kolorem)
        * [Wypełnienie obszaru kolorem](#wypełnienie-obszaru-kolorem)
    * [Rysowanie prostokątów](#rysowanie-prostokątów)
    * [Rysowanie okręgów i kół](#rysowanie-okręgów-i-kół)
    * [Rysowanie linii](#rysowanie-linii)
    * [Rysowanie tekstu](#rysowanie-tekstu)
* [Podstawowe operacje na obrazach](#podstawowe-operacje-na-obrazach)
    * [Konwersja na skalę szarości](#konwersja-na-skalę-szarości)
    * [Blurowanie obrazów](#blurowanie-obrazów)
    * [Wyróżnianie krawędzi](#wyróżnianie-krawędzi)
        * [Optymalizacja wyróżniania krawędzi](#optymalizacja-wyróżniania-krawędzi)
    * [Efekt dilation (narastanie krawędzi)](#efekt-dilation-narastanie-krawędzi)
    * [Efekt erosion (erozja krawędzi)](#efekt-erosion-erozja-krawędzi)
    * [Przycinanie obrazów](#przycinanie-obrazów)


## Dodatkowe elementy
### Biblioteka _caer_
Biblioteka usprawniająca pracę z przetwarzaniem obrazów. Tyczy się to zwłaszcza tych jego części związanych z **sieciami neuronowymi**. Dostępna pod następującym [linkiem](https://pypi.org/project/caer/).

## Wczytywanie

### Wczytywanie obrazów
Wczytywanie obrazu wykonać można przy pomocy funkcji `imread()`. Wczytany obraz staje się obiektem typu `MatLike` (matryca). Jest to de facto tablica z biblioteki _numpy_, której elementami są piksele obrazu.

```py
import cv2 as cv

cv.imread(path)
```
* `path` - ścieżka do obrazu.

#### Stworzenie pustego obrazu
Można stworzyć pusty, czarny obraz typu `MatLike` przy pomocy biblioteki _numpy_. Wystarczy zadeklarować wypełnioną zerami macierz 8-bitowych liczb całkowitych.

```python
import numpy as np

empty_image = np.zeros(dimensions, dtype='uint8')
```
* `dimensions` - krotka o formie `(width, height, channels)`. Gdzie `width` i `height` są wymiarami obrazu w pikselach a `channels` mówi nam o ilości składowych opisujących barwę pikseli (np. 3 dla RGB).

### Wczytywanie wideo
Wczytanie wideo odbywa się poprzez utworzenie specjalnego obiektu `VideoCapture`, w którego konstruktorze podaje się źródło wideo. De facto jest to zbiór klatek, które reprezentowane są jako obrazy `MatLike`.

```python
import cv2 as cv

video = VideoCapture(source)
```
* `source` - źródło wczytywanego wideo. Może być to `int` jeżeli chcemy, aby wideo było przechwytywane w czasie rzeczywistym z urządzenia peryferyjnego (np. `0` to pierwsza dostępna kamera). W przypadku podania `string` wczytane zostanie gotowe wideo z zawartej w nim ścieżki.

#### Zwalnianie wideo
Każde wczytane wideo należy w pewnym momencie zwolnić przy pomocy metody `release()`.

```py
video.release()
```

## Wyświetlanie

### Wyświetlanie obazów
Wyświetlanie obrazu odbywa się przy pomocy funkcji `imshow()`.

```py
import cv2 as cv

cv.imshow(name, image)
```
* `name` - nazwa okna, w którym wyświetlony zostanie obraz.
* `obraz` - obiekt typu `MatLike` zawierający obraz do wyświetlenia.

#### Autoskalowanie obrazów
_OpenCV_ **nie dopasowuje rozmiaru wyświetlanego obrazu do rozdzielczości monitora**. Rozmiar okna w skali 1:1 odpowiada rozmiarowi obrazu. Zatem jeżeli obraz będzie za duży dla naszego monitora, to po prostu wyjdzie poza ekran. Dodatkowo biblioteka **nie umożliwia automatycznego dodawania scrollbarów** do okien z obrazem.

### Wyświetlanie wideo
Wideo odtwarzane jest przy pomocy pętli `for` iterującej się przez kolejne klatki. Każda klatka traktowana jest jak obraz `MatLike`. Aby odczytywać kolejne klatki wideo należy skorzystać z metody `read()`. Zwraca ona krotkę `(bool, MatLike)`.

```py
while True:
    isTrue, frame = video.read()
    cv.imshow("Wideo", frame)
```

#### Zakończenie wyświetlania
Jeżeli przeiterujemy się przez wszyskie klatki i wyołamy po raz kolejny `read()`, to wywołany zostanie wyjątek `-215`. Oznacza on błąd ocztu obrazu bądź klatki.

## Skalowanie

### Pobranie wymiarów obrazu
Dane na temat wymiarów obrazu zapisane są w jego atrybucie `shape`. Jest on tablicą, na następujących indeksach zawiera:
* `[0]` - wysokość obrazu w pikselach
* `[1]` - szerokość obrazu w pikselach

```py
height = image.shape[0]
widht = image.shape[1]
```

### Zmiana wymiarów (uniwersalna)
Przy pomocy funkcji `resize()` można zmienić wymairy:
* obrazów
* klatki gotowego wideo
* klatki wideo otrzymywanego w czasie rzeczywitym

Obraz/klatkę o zmienionych wymiarach otrzymuje się na wyjściu tejże funkcji.

```py
import cv2 as cv

resized_image = cv.resize(image, new_dimensions, interpolation)
```
* `image` - obraz/klatka, której wymiary mają zostać zmienione.
* `new_dimensions` - nowe wymiaru obrazu w formie krotki `(width, height)`.
* `interpolation` - stała wskazująca rodzaj interpolacji, jaka ma zostać zastosowana przy zmianie wymairów. Przykładowo może być to interpolacja `cv.INTER_AREA`.

#### Rodzaje interpolacji
W _OpenCV_ mamy do dyspozycji kilka rodzajów interpolacji.
* `cv.INTER_AREA` - domyślna interpolacja, sprawdzająca się najlepiej przy **pomniejszaniu** obrazu.
* `cv.INTER_LINEAR` - używana przy **powiększaniu** obrazu.
* `cv.INTER_CUBIC` - używana przy **powiększaniu** obrazu. Wolna, ale dająca najlepsze efekty.

### Zmiana wymiarów (wideo czasu rzeczywistego)
Przy pomocy metody `set()` obiektu `VideoCapture` można sterować atrybutami wideo. Jednym z tych atrybutów są wymiary tegoż wideo. Co ważne mogą być one ustawione tylko jeżeli obiekt **wczytuje wideo czasu rzeczywistego**.

```py
video.set(attribute_id, value)
```
* `attribute_id` - identyfikator atrybutu, który jest modyfikowany. W wypadku **szerokości** jest to `3`. W wypadku **wysokości** jest to `4`.
* `value` - nowa wartość atrybutu. W wypadku szerokości i wysokości jest to ich rozmiar w pikselach.

## Rysowanie na obrazach

### Wypełnianie obrazu kolorem
Wypełnienie obrazu kolorem korzysta z faktu, że `MatLike` jest de facto macierzą biblioteki _numpy_. Dzięki temu można łatwo przypisać jeden kolor wszystkim pikselom takiej macierzy przy pomocy operatora `[:]`.

```py
image[:] = 255, 0, 0    # Wypełnienie czerwienią
```

#### Wypełnienie obszaru kolorem
Analogicznie można wypełniać jednolistym kolorem poszczegolne obszary obrazu.

```py
# Wypelnienie zielenią obszaru rozciągającego się:
# * od 200 do 350 piksela obrazu w poziomie
# * od 300 do 400 piksela obrazu w pionie
image[200:350, 300:400] = 0, 255, 0 
```

### Rysowanie prostokątów
Można narysować prostokąt na obrazie przy pomocy funkcji `rectangle()`.

```py
cv.rectangle(image, position, dimensions, color, thickness)
```
* `image` - obraz, na którym obędzie się rysowanie.
* `pozycja` - pozycja `(x,y)` lewego górnego rogu prostokąta.
* `dimensions` - wysokość i szerokość prostokąta w postaci `(w, h)`.
* `color` - kolor konturu/wypełnienia w formacie `(r, g, b)`.
* `thickness` - grubość krawędzi lub stała `cv.FILLED` jeżeli prostokąt ma być wypełniony.

### Rysowanie okręgów i kół
Można rysować okręgi i koła na obrazie przy pomocy funkcji `circle()`.

```py
cv.circle(image, position, radius, color, thickness)
```
* `image` - obraz, na którym obędzie się rysowanie.
* `position` - pozycja `(x,y)` środka.
* `radius` - promień.
* `color` - kolor konturu/wypełnienia w formacie `(r, g, b)`.
* `thickness` - grubość krawędzi lub stała `cv.FILLED` jeżeli okręg ma być wypełniony.

### Rysowanie linii
Można rysować linie na obrazie przy pomocy funkcji `line()`.

```py
cv.line(image, start_position, end_position, color, thickness)
```
* `image` - obraz, na którym obędzie się rysowanie.
* `start_position` - pozycja `(x,y)` początku linii.
* `end_position` - pozycja `(x,y)` końca linii.
* `color` - kolor linii w formacie `(r, g, b)`.
* `thickness` - grubość linii.

### Rysowanie tekstu
Można rysować tekst na obrazie przy pomocy funkcji `putText()`.

```py
cv.putText(image, text, position, font, scale, color, thickness)
```
* `image` - obraz, na którym obędzie się rysowanie.
* `text` - treść wyświetlanego tekstu.
* `position` - pozycja `(x,y)` lewego, górnego krańca tekstu.
* `font` - identyfikator czcionki (np. `cv.FONT_HERSEY_TRIPLEX`).
* `scale` - powiększenie liter względem wielkości domyślnej w % przedstawionych jako ułamki dziesiętne.
* `color` - kolor tekstu w formacie `(r, g, b)`.
* `thickness` - grubość liter.

## Podstawowe operacje na obrazach

### Konwersja na skalę szarości
Przekonwertować obraz na jego czarno-białą wersję można przy pomocy funkcji `cvtColor()` z odpowiednim parametrem.

```py
gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY).
```
* `image` - obraz do przekonwertowania.

### Blurowanie obrazów
Zablurować obraz można chociażby funkcją `GaussianBlur()`.

```py
blured_image = cv.GaussianBlur(image, intensity, cv.BORDER_DEFAULT)
```
* `image` - obraz do zablurowania
* `intensity` - natężenie zablurowania w formie krotki `(i, j)`, gdzie `i` oraz `j` są liczbami nieparzystymi.

### Wyróżnianie krawędzi
Wyrożnić krawędzie na obrazie można chociażby metodą _canny_ przy pomocy funkcji `Canny()`.

```py
image_edges = cv.Canny(image, lower_bound, upper_bound)
```
* `image` - obraz, na którym krawędzie chcemy wyróżnić
* `upper_bound`, `lower_bound` - parametry sterujące efektem

#### Optymalizacja wyróżniania krawędzi
Wyróżnianie krawędzi możne być bardzo wymagające obliczeniowo. Można jednak zmniejszyć ilość wymaganych obliczeń zablurowując wcześniej obraz (redukując liczbę krawędzi i zbędnych szczegółów).

### Efekt dilation (narastanie krawędzi)
Pogrubić krawędzie na obrazie (efekt dilation) możemy poprzez wykorzystanie funkcji `dilate()`.

```py
dilated_image = cv.dilate(image, intensity, iterations=1)
```
* `image` - obraz, na który ma zostać nałożony efekt.
* `intensity` - natężenie efektu sterowane przez podanie krotki `(i, j)`, gdzie `i` oraz `j` to liczby nieparzyste.
* `iterations` - liczba powtórzeń nałożenia efektu.

### Efekt erosion (erozja krawędzi)
Można erodować krawędzie na obrazie poprzez wykorzystanie funkcji `erode()`.

```py
eroded_image = erode(image, intensity, iterations=1)
```
* `image` - obraz, na który ma zostać nałożony efekt.
* `intensity` - natężenie efektu sterowane przez podanie krotki `(i, j)`, gdzie `i` oraz `j` to liczby nieparzyste.
* `iterations` - liczba powtórzeń nałożenia efektu.

### Przycinanie obrazów
Przycinanie obrazów korzysta w możliwości indeksowania macierzy _numpy_.

```py
# Wycięcie obrau tak aby zawierał tylko fragment między:
# * 300 a 500 pikselem w poziomie
# * 200 a 300 pikselem w pionie
image = image[300:500, 200:300]
```

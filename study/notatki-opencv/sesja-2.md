# Nauka _OpenCV_ - sesja 2

## Transformacje obrazów

### Translacja
Wykonanie translacji wymaga utworzenia odpowiedniej **macierzy transformacji**, która przesunie obraz w pożądane miejsce. Niezbędne do tego będzie wykorzystanie _numpy_.

```py
import numpy as np

transformation_matrix = np.float32(
    [[1, 0, x],
     [0, 1, y]]
)
```
* `x` - składowa pozioma wektora translacji. Wartość **dodatnia** przesuwa obraz w **prawo**. **Ujemna** przesuwa obraz w **lewo**.
* `y` - składowa pionowa wektora translacji. Wartośc **dodatnia** przesuwa obraz w **dół**. **Ujemna** przesuwa obraz w **górę**.

Tak utworzoną macierz należy następnie użyć do wykonania transformacji funkcją `warpAffine()`.

```py
translated_image = cv.warpAffine(image, transformation_matrix, dimensions)
```
* `image` - obrazek, który poddajemy translacji.
* `transformation_matrix` - macierz transformacji.
* `dimensions` - wymiary obrazka poddawanego translacji.

### Rotacja
Wykonanie rotacji wymaga utworzenia odpowiedniej **macierzy transformacji**, która obróci obraz w odpowiedni sposób. Taką macierz można uzyskać przy pomocy funkcji `getRotationMatrix2D()`.

```py
transformation_matrix = cv.getRotationMatrix2D(rotation_point, angle, scale)
```
* `rotation_point` - punkt obrotu w formie krotki `(x, y)`.
* `angle` - kąt obrotu w stopniach (przeciwnie do ruchu wskazówek zegara).
* `scale` - skala powiększenia obrazu po obrocie.

Tak utworzoną macierz należy następnie użyć do wykonania transformacji funkcją `warpAffine()`.

```py
rotated_image = cv.warpAffine(image, transformation_matrix, dimensions)
```
* `image` - obrazek, który poddajemy rotacji.
* `transformation_matrix` - macierz transformacji.
* `dimensions` - wymiary obrazka poddawanego rotacji.

#### Dodatkowe skutki rotacji
W wyniku rotacji te części obrazu, które nie zmieszczą się w oknie go prezentującym są bezpowrotnie **ucinane**.

### Odwrócenie w pionie/poziomie
Odwrócenie obrazka wymaga użycia funkcji `flip()`.

```py
flipped_image = cv.flip(image, flic_code)
```
* `image` - obrazek do odwrócenia.
* `flip_code` - identyfikator typu odwrócenia. Identyfikator równy `0` do odwrócenie **w pionie**. Identyfikator równy `1` to odwrócenie **w poziomie**. Identyfikator równy `-1` to odwrócenie zwrówno **w pionie jak i w poziomie**.

## Wykrywanie konturów

### Binaryzacja obrazu
Binaryzacja obrazu polega na sprowadzeniu obrazu do formy, w której zawiera on wyłącznie piksele o 2 kolorach. W _OpenCV_ binaryzację przeprowadzić można przy pomocy funkcji `threshold()`, która zwraca krotkę `(ret, image)`. Obiekt `image` to zbinaryzowany obraz.

```py
ret, image = cv.threshold(image, treshold, color, cv.THRESH_BINARY)
```
* `image` - obraz, który ma zostać zbinaryzowany
* `threshold` - minimalny poziom natężenia piksela (w skali od 0 do 255), który sprawi, że nie zostanie on zaczerniony.
* `color` - natężenie (w skali od 0 do 255), które przyjmą wszystkie niezaczernione piksele.

### Wykrywanie konturów
Wykryć kontury na obrazie można przy pomocy funkcji `findContours()`, która zwraca krotkę `(contours, hierarchies)`. Obiekt `contours` jest listą punktów składających się na wykryte na obrazie kontury. Obiekt `hierarchies` opisuje hierarchię znalezionych konturów.

```py
contours, hierarchies = cv.findContours(image, mode, approximation)
```
* `image` - obraz, na którym wykrywane są kontury.
* `mode` - przyjęty sposób wykrywania i definiowania konturów.
* `approximation` - przyjęty sposób aproksymacji konturów.

#### Sposoby wykrywania i definiowania konturów
* `cv.RETR_LIST` - zwracane są wszystkie konury możliwe do znalezienia na obrazie.
* `cv.RETR_EXTERNAL` - zwracane są wyłącznie kontury zewnętrzne.
* `cv.RETR_TREE` - zwracane są wszystkie kontury należące do hierarchii konturów.

#### Sposoby aproksymacji konturów
* `cv.CHAIN_APPROX_NONE` - zwracane są wszystkie punkty składające się na kontury. Nie ma żadnych kompresji.
* `cv.CHAIN_APPROX_SIMPLE` - jeżeli w konturach znajdą się linie proste to są one kompresowane do 2 punktów: początkowego i końcowego.

### Sekwencje wykrywania konturów

#### Poprzez wykrywanie krawędzi (zalecane)
1. Wczytaj obrazek.
2. [Opcjonalnie] zabluruj obrazek dla lepszej optymalizacji.
3. Wykryj krawędzie na obrazku metodą _Canny_.
4. Wykryj kontury.

#### Poprzez binaryzację obrazka
1. Wczytaj obrazek.
2. Wykonaj binaryzację obrazka.
4. Wykryj kontury.

### Nanoszenie konturów na obrazek
Można nanieść znalezione kontury na obrazek przy pomocy funkcji `drawContours()`.

```py
cv.drawContours(image, contours, count, colour, thickness)
```
* `image` - obrazek, na który naniesione mają zostać kontury
* `contours` - lista konturów do naniesienia
* `count` - ilość konturów do naniesienia. Przy podaniu `-1` naniesione zostaną wszystkie kontury.
* `color` - kolor naniesionych konturów w postaci krotki o formace `(b, g, r)`.
* `thickness` - grubość naniesionych konturów.

## Modele kolorów

### Dostępne modele kolorów
* `BGR` - domyślny model kolorów w _OpenCV_. Jest to model `RGB` o odwróconej kolejności.
* `Skala szarości (GRAY)` - model kolorów operujący jedynie na odcieniach szarości. Idealny do ukazania intensywaności pikseli na obrazie.
* `HSV` - model od dużej saturacji barw.
* `LAB` - model generujący bardziej wyprane barwy.
* `RGB` - najpowszechniej używany model barw. W przypadku _OpenCV_ spowoduje to zamianę miejscami kolorów niebiekiego z czerwonym podczas wyświetlania.

### Konwersja między modelami
Konwersja między modelami kolorów jest możliwa dzięki funkcji `cvtColor()`. Pozwala ona jednak jedynie na konwersję modelu `BGR` na dowolny inny oraz odwrotnie. Nie mozna przykładowo zamienić modelu `HSV` na `LAB`. Wymagana jest w takim wypadku pośrednia konwersja na `BGR`.

```py
image = cv.cvtColor(image, convertion_type)
```
* `image` - obraz do konwresji.
* `convertion_type` - typ konwersji w formie stałej o składni `cv.COLOR_BGR2<model>` lub `cv.COLOR_<model>2BGR`.

## Kanały kolorów

### Kanał koloru
Kanał koloru to po prostu składowa aktualnie używanego na obrazie modelu koloru. Na przykład model `BGR` składa się z 3 kanałów `B`, `G` oraz `R`.

### Odczytanie liczby kanałów
Liczba kanałów zapisana jest w atrybucie `shape` obrazu i znajduje się pod indeksem `[2]`.

```py
number_of_channels = image.shape[2]
```

Modele o jednym kanale nie posiadają elementu pod indeksem `[2]` w swoim atrybucie `shape`.

### Rozdzielenie kanałów
Można rozdzielić kanały z obrazka przy pomocy funkcji `split()`. Zwraca ona krotkę zawierającą obrazki z tylko jednym kanałem, a zatem obrazki w odcieniach szarości (im bliżej białego, tym większe natężenie koloru odpowiadającego kanałowi).

```
b, g, r = cv.split(image)
```
* `image` - obrazek, z którego będą wydzielane kanały.

### Łączenie kanałów
Można połączyć kanały w jeden, wielokanałowy obrazek przy pomocy funkcji `merge()`. Zwraca ona obrazek o połączonych kanałach.

```py
image = cv.merge([b, g, r])
```
* `[b, g, r]` - lista z kanałami do połączenia.

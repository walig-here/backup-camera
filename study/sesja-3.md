# Nauka _OpenCV_ - sesja 3

## Blurowanie

### Kernel
Rozmiar okna blurowania, czyli krotka `(i, j)`, gdzie `i` oznacza szerokość okna w pikselach a `j` wysokoś okna w pikselach. Okno blurowania używane jest do obliczenia rozmycia piksela znajdującego się w jego centrum (stąd `i` oraz `j` muszą być niepatrzyste). Określa ono, które piksele z sąsiedztwa biorą udział w oblcizeniach. 

Generalnie można przyjąć, że im większy rozmiar okna tym większy blur.

### Blurowanie _average_
Rodzaj blurowania, w którym intensywność piksela jest określana na podstawie **średniej arytmetycznej intensywnosci pikseliw w oknie blurowania**. Blurowanie _average_ można zaaplikować przy pomocy funkcji `blur()`.

```py
blured_image = cv.blue(image, kernel)
```
* `image` - obrazek, który ma zostać zablurowany
* `kernel` - krotka `(i, j)`, która określa rozmiar okna blurowania.

### Blurowanie _Gaussian_
Rodzaj blurowania, w którym intensywność piksela jest określana na podstawie wartości **średniej z rozkładu normalnego intensywności pikseli w oknie blurowania**. Blurowanie _Gaussian_ można zaaplikować przy pomocy funkcji `GaussianBlur`.

```py
blured_image = cv.GaussainBlur(image, kernel, 0)
```
* `image` - obrazek, który ma zostać zablurowany
* `kernel` - krotka `(i, j)`, która określa rozmiar okna blurowania.

Blurowanie _Gaussian_ jest mniej intenstywne niż blurowanie _average_.

### Blurowanie _median_
Rodzaj blurowania, w którym intensywność piksela jest określana na podstawie **meidany intensywnosci pikseli w oknie blurowania**. Blurowanie _median_ można zaaplikować przy pomocy funkcji `medianBlur()`.

```py
blured_image = cv.medianBlur(image, kernel_size)
```
* `image` - obrazek, który ma zostać zablurowany
* `kernel_size` - wymiar okna blurowania w postaci pojedynczego `int`.

Jest bardziej efektywne w usuwaniu szumów z obrazka niż metody _average_ i _Gaussian_. Aplikuje przy tym mniejsze rozmycie na obrazek.

### Blurowanie _biliteral_
Rodzj blurowania, które **zachowuje krawędzie na obrazku w stanie nienaruszonym**. Nie jest ono sterowane rozmiarem okna blurowania, a **średnicą okręgu** definiującego sąsiedztwo piksela. Blurowanie _bilateral_ można zaaplikować przy pomocy funkcji `bilateralFilter()`.

```py
blured_image = cv.bilateralFilter(image, diameter, sigma_color, sigma_space)
```
* `image` - obrazek, który ma zostać zablurowany
* `diameter` - średnica okręgu sąsiedztwa.
* `sigma_color` - maksymalna ilość kolorów, które będą brane pod uwagę przy obliczaniu bluru.
* `sigma_space` - zwiększa dodatkowo rozmiar obszaru, z którego brane są piksele do określenia bluru.

Ten rodzaj blurowania jest zdecydowanie najbardziej subtelny.

## Operatory bitowe

### Piksele jako liczby binarne
Piksele można potraktować jako liczby binarne, gdzie:
* `'0'` - piksel zgaszony
* `'1'` - piksel zapalony

W związku z tym na obrazach można wykonywać operacje bitowie takie jak `AND`, `OR` czy `XOR`.

### Operator `AND`
Piksel zostaje zapalony wtedy i tylko wtedy, gdy 2 piksele wejściowe są zapalone. Mozna to potraktować jako **wyznaczenie części wspólnej** obrazków. Operator `AND` można użyć poprze funkcję `bitwise_and()`.

```py
and_image = cv.bitwise_and(image_1, image_2)
```
* `image_1`, `image_2` - obrazki, których piksele posłużą jako werścia operatora.

### Operator `OR`
Piksel zostaje zapalony, gdy co najmniej 1 piksel wejściowy jest zapalony. Można to potraktować jako **wykonanie nałożenia** obrazków. Operator `OR` można użyć poprze funkcję `bitwise_or()`.

```py
and_image = cv.bitwise_or(image_1, image_2)
```
* `image_1`, `image_2` - obrazki, których piksele posłużą jako werścia operatora.

### Operator `XOR`
Piksel zostaje zapalony, gdy wyłącznie 1 z pikseli wejściowych jest zapalony. Mozna to potraktować jako **nałozenie obrazków, a następnie usunięcie ich części wspólnej**. Operator `XOR` można użyć poprze funkcję `bitwise_and()`.

```py
and_image = cv.bitwise_xor(image_1, image_2)
```
* `image_1`, `image_2` - obrazki, których piksele posłużą jako werścia operatora.

### Operator `NOT`
Gasi zapalone piksele i zapala zgaszone piksele. Operatora `NOT` można użyć poprzez funkcję `bitwise_not()`.

```py
and_image = cv.bitwise_not(image)
```
* `image` - obrazek, którego piksele posłużą jako werścia operatora.

## Maskowanie

### Efekt maskowania
Maskowanie pozwala na wydzielnie z obrazka dowolnego obszaru o dowolnym kształcie.

### Sekwencja maskowania
1. Stwórz pusty obraz o czarnym tle i przy pomocy funkcji rysujących oraz operatorów bitowych stwórz na nim dowolny kształt o kolorze białym. Ten kształt stanie się maską.
2. Wykonaj właściwe maskowania aplikując operator `AND` na dowolnym obrazie wskazując wcześniej stworzoną maskę.

```py
masked_image = cv.bitwise_and(image, image, mask=my_mask)
```
* `image` - obrazek, który maskujemy
* `my_mask` - maska nakładana na obrazek

### Rozmiar maski
Rozmiar maski musi być **identyczny** jak obrazk obrazka, do którego maskowania zostanie ona użyta.

## Histogramy

### Histogramy w _OpenCV_
Histogramy pozwalają na graficzną prezentację rozkładu intensywności pikseli na danym obrazku. Ich zaprezentowanie wymaga jednak importu biblioteki _matplotlib_.

### Histogram obrazka czarno-białego
Histogram obrazka czarno białego składa się z jednej serii danych obrazujących intensywnośc jedynego kanału takiego obrazka. W celu jego wyrysowania należy.
1. Wczytać obrazek w odcieniach czarno-białym
2. Wyliczyć histogram przy pomocy funkcji `calcHist()`.
3. Zaprezentować histogram przy pomocy _matplotplib_.

#### Wyliczanie histogramu
```py
histogram = cv.calcHist(images, channel_indicies, mask, histSize, ranges)
```
* `images` - lista obrazków, dla których wyliczony ma zostać histogram.
* `channel_indicies` - lista indeksów kanałów kolorów, których intensywności chemy uwzględnić na histogramie. W przypadku obrazków czarno-białych jest to wartość `0`.
* `maska` - maska binarna, która ma ograniczyć obszar obrazków uwzględniany przy wyliczeniach. Nalezy wprowadzić `None`, gdy nie chcemy uwzględniać maski.
* `histSize` - lista z liczami możliwych do wyróżnienia poziomów intensywności. Przykładowo dla `BGR` może być to `256` poziomów.
* `ranges` - lista zawierająca zakres możliwych do przyjęcia przez  piksele poziomów intensywności. Przykładowo dla `BGR` może być to `[0, 256]`.

#### Prezentacja histogramu
```py
import matplotlib.pyplot as ply

plt.figure()
plt.title('Histogram')
plt.xlabel('intensywność')
plt.ylabel('liczba pikseli')
plt.plot(histogram)
plt.xlim([0, 256])
plt.show()
```

### Histogram obrazka kolorego
Histogram obrazka kolorowego składa się z jednej serii danych obrazujących intensywnośc jedynego kanału takiego obrazka. W celu jego wyrysowania należy.
1. Wczytać obrazek
2. Wyliczyć histogramy wszystkich kanałów przy pomocy funkcji `calcHist()`.
3. Zaprezentować histogramy wszystkich przy pomocy _matplotplib_.

#### Wyliczanie histogramu
```py
for mask, color in enumerate('b', 'g', 'r'):
    histogram = cv.calcHist(images, channel_indicies, mask, histSize, ranges)
```
* `images` - lista obrazków, dla których wyliczony ma zostać histogram.
* `channel_indicies` - lista indeksów kanałów kolorów, których intensywności chemy uwzględnić na histogramie. W przypadku gdy chcemy uzyskać historgram dla zieleni jest to wartość `[1]`.
* `maska` - maska binarna, która ma ograniczyć obszar obrazków uwzględniany przy wyliczeniach. Nalezy wprowadzić `None`, gdy nie chcemy uwzględniać maski.
* `histSize` - lista z liczami możliwych do wyróżnienia poziomów intensywności. Przykładowo dla `BGR` może być to `256` poziomów.
* `ranges` - lista zawierająca zakres możliwych do przyjęcia przez  piksele poziomów intensywności. Przykładowo dla `BGR` może być to `[0, 256]`.

#### Prezentacja histogramu
```py
import matplotlib.pyplot as ply

plt.figure()
plt.title('Histogram')
plt.xlabel('intensywność')
plt.ylabel('liczba pikseli')
for mask, color in enumerate('b', 'g', 'r'):
    histogram = cv.calcHist(images, channel_indicies, mask, histSize, ranges)
    plt.plot(histogram, color=mask)
    plt.xlim([0, 256])
    plt.show()
```

ymaps.ready(init);

function init() {
    // Подключаем поисковые подсказки к полю ввода.
    var suggestView = new ymaps.SuggestView('suggest');

    var myMap = new ymaps.Map('map', {
        center: [55.753994, 37.622093],
        zoom: 9
    }, {
        searchControlProvider: 'yandex#search'
    });

    var myPlacemark;

    // Слушаем клик на карте.
    myMap.events.add('click', function (e) {
        var coords = e.get('coords');

        // Если метка уже создана – просто передвигаем ее.
        if (myPlacemark) {
            myPlacemark.geometry.setCoordinates(coords);
        }
        // Если нет – создаем.
        else {
            myPlacemark = createPlacemark(coords);
            myMap.geoObjects.add(myPlacemark);
            // Слушаем событие окончания перетаскивания на метке.
            myPlacemark.events.add('dragend', function () {
                getAddress(myPlacemark.geometry.getCoordinates());
            });
        }
        getAddress(coords);
        $('#suggest').val(myPlacemark.properties.get('iconCaption'));
    });

    // Создание метки.
    function createPlacemark(coords) {
        return new ymaps.Placemark(coords, {
            iconCaption: 'поиск...'
        }, {
            preset: 'islands#violetDotIconWithCaption',
            draggable: true
        });
    }

    // Определяем адрес по координатам (обратное геокодирование).
    function getAddress(coords) {
        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);
            var address = [
                firstGeoObject.getLocalities().length ? firstGeoObject.getLocalities() : firstGeoObject.getAdministrativeAreas(),
                firstGeoObject.getThoroughfare(),
                firstGeoObject.getPremiseNumber()
            ].filter(Boolean).join(', ');

            myPlacemark.properties
                .set({
                    iconCaption: address, // Устанавливаем полный адрес в подпись метки
                    balloonContent: firstGeoObject.getAddressLine()
                });

            $('#suggest').val(address); // Записываем полный адрес в поле ввода
        });
    }

    // Обработка ввода адреса в поле
    $('#suggest').bind('change', function () {
        geocode();
    });

    function geocode() {
        // Забираем запрос из поля ввода.
        var request = $('#suggest').val();
        // Геокодируем введённые данные.
        ymaps.geocode(request).then(function (res) {
            var obj = res.geoObjects.get(0),
                error, hint;

            if (obj) {
                switch (obj.properties.get('metaDataProperty.GeocoderMetaData.kind')) {
                    case 'house':
                        // Об оценке точности ответа геокодера можно прочитать тут: https://tech.yandex.ru/maps/doc/geocoder/desc/reference/precision-docpage/
                        switch (obj.properties.get('metaDataProperty.GeocoderMetaData.precision')) {
                            case 'exact':
                                break;
                            case 'number':
                                error = 'Неточный адрес, требуется уточнение';
                                hint = 'Уточните номер дома';
                                break;
                            case 'near':
                                error = 'Неточный адрес, требуется уточнение';
                                hint = 'Уточните номер дома';
                                break;
                            case 'range':
                                error = 'Неточный адрес, требуется уточнение';
                                hint = 'Уточните номер дома';
                                break;
                            case 'street':
                                error = 'Неполный адрес, требуется уточнение';
                                hint = 'Уточните номер дома';
                                break;
                            case 'other':
                            default:
                                error = 'Неточный адрес, требуется уточнение';
                                hint = 'Уточните адрес';
                        }
                        break;
                    default:
                        error = 'Неполный адрес';
                        hint = 'Уточните номер дома';
                        break;
                }
            } else {
                error = 'Адрес не найден';
                hint = 'Уточните адрес';
            }

            // Если геокодер возвращает пустой массив или неточный результат, то показываем ошибку.
            if (error) {
                showError(error);
                showMessage(hint);
            } else {
                showResult(obj);
            }
        }, function (e) {
            console.log(e)
        })
    }

    function showResult(obj) {
        // Удаляем сообщение об ошибке, если найденный адрес совпадает с поисковым запросом.
        $('#suggest').removeClass('input_error');
        $('#notice').css('display', 'none');

        var mapContainer = $('#map'),
            bounds = obj.properties.get('boundedBy'),
            // Рассчитываем видимую область для текущего положения пользователя.
            mapState = ymaps.util.bounds.getCenterAndZoom(
                bounds,
                [mapContainer.width(), mapContainer.height()]
            ),
            // Сохраняем полный адрес для сообщения под картой.
            address = [obj.getCountry(), obj.getAddressLine()].join(', '),
            // Сохраняем укороченный адрес для подписи метки.
            shortAddress = [
                obj.getThoroughfare(),
                obj.getPremiseNumber(), // Добавляем номер дома
                obj.getPremise()
            ].filter(Boolean).join(' ');

        // Убираем контролы с карты.
        mapState.controls = [];

        // Если метка уже создана – просто передвигаем ее.
        if (myPlacemark) {
            myPlacemark.geometry.setCoordinates(mapState.center);
        }
        // Если нет – создаем.
        else {
            myPlacemark = createPlacemark(mapState.center);
            myMap.geoObjects.add(myPlacemark);
            // Слушаем событие окончания перетаскивания на метке.
            myPlacemark.events.add('dragend', function () {
                getAddress(myPlacemark.geometry.getCoordinates());
                $('#suggest').val(myPlacemark.properties.get('iconCaption'));
            });
        }

        // Устанавливаем новый центр карты и меняем данные и позицию метки.
        myMap.setCenter(mapState.center, mapState.zoom);
        myPlacemark.properties.set({
            iconCaption: shortAddress,
            balloonContent: address
        });
    }

    function showError(message) {
        $('#notice').text(message);
        $('#suggest').addClass('input_error');
        $('#notice').css('display', 'block');
        // Удаляем карту.
        if (myPlacemark) {
            myMap.geoObjects.remove(myPlacemark);
            myPlacemark = null;
        }
    }

    function showMessage(message) {
        $('#messageHeader').text('Данные получены:');
        $('#message').text(message);
    }
}
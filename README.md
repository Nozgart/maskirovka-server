# Maskirovka

FastAPI-приложение — API для каталога юнитов BattleTech с поддержкой фильтрации, сортировки и пагинации.

## Описание

**Maskirovka** — это асинхронное REST API для работы с каталогом боевых машин (юнитов) вселенной BattleTech. Приложение предоставляет удобный интерфейс для получения информации об эрах, фракциях и юнитах с возможностью сложной фильтрации и сортировки.

## ⚠️ Дисклеймер

**BattleTech** — зарегистрированная торговая марка [Catalyst Game Labs](https://www.catalystgamelabs.com/) / Topps.  
Все данные юнитов, названия и игровые механики являются собственностью соответствующих правообладателей.

Этот проект является **неофициальной фанатской разработкой**, созданной исключительно в образовательных целях.  
Проект не аффилирован с Catalyst Game Labs, не одобрен и не спонсируется ею.

Исходный код приложения распространяется под лицензией MIT (см. [LICENSE](LICENSE)).

## Функциональность

- 📚 **Справочники**: получение списков эр, фракций, ролей и типов юнитов
- 🔍 **Фильтрация юнитов** по множеству параметров:
  - Эра и фракции
  - Тип и название юнита
  - Характеристики (PV, размер, броня, структура и др.)
  - Оружейные показатели (short, medium, long, extreme)
  - Особые способности (specials)
- 📊 **Сортировка** по различным полям (название, PV, роль, характеристики)
- 📄 **Пагинация** результатов
- 🔗 **Получение юнита по ID** — один юнит по `unit_id`
- ⚡ **Кэширование** справочных данных (5 минут)

## Стек технологий

- **FastAPI** — современный асинхронный веб-фреймворк
- **Tortoise ORM** — асинхронная ORM для Python
- **SQLite** — легковесная база данных
- **Pydantic** — валидация данных и настроек
- **fastapi-pagination** — пагинация результатов
- **fastapi-cache2** — кэширование в памяти

## Установка и запуск

### Требования

- Python 3.9+
- Установленные зависимости из `requirements.txt`

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Запуск приложения

```bash
uvicorn main:app --reload
```

Приложение будет доступно по адресу: `http://localhost:8000`

### Документация API

После запуска доступна интерактивная документация:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Эндпоинты

### Справочники (кэшируются 5 минут)

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/eras` | Список эр |
| GET | `/factions` | Список фракций |
| GET | `/roles` | Уникальные роли юнитов |
| GET | `/types` | Уникальные типы юнитов |

### Юниты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/units` | Список юнитов с фильтрацией и сортировкой |
| GET | `/units/{unit_id}` | Один юнит по идентификатору |

#### Параметры фильтрации `/units`

| Параметр | Тип | Описание |
|----------|-----|----------|
| `era_id` | int | Фильтр по эре |
| `faction_id` | list[int] | Фильтр по фракциям (можно несколько) |
| `unit_type` | str | Фильтр по типу юнита (icontains) |
| `title` | str | Фильтр по названию (icontains) |
| `role` | str | Фильтр по роли (icontains) |
| `specials` | str | Фильтр по способностям (через запятую) |
| `pv`, `sz`, `armor`, `struc` и др. | int | Числовые фильтры |

#### Заголовки режимов фильтрации

| Заголовок | По умолчанию | Варианты |
|-----------|--------------|----------|
| `X-Specials-Mode` | `or` | `or`, `and` |
| `X-Pv-Mode` и др. | `eq` | `eq`, `gt`, `gte`, `lt`, `lte` |

#### Параметры сортировки

| Параметр | Значения | Описание |
|----------|----------|----------|
| `sort_by` | `title`, `pv`, `role`, `short`, `medium`, `long`, `armor`, `struc`, `mv` | Поле сортировки |
| `sort_order` | `asc`, `desc` | Порядок (по умолчанию `asc`) |

## Примеры запросов

### Получение одного юнита по ID
```bash
curl "http://localhost:8000/units/280"
```

### Фильтр по эре и фракции
```bash
curl "http://localhost:8000/units?era_id=1&faction_id=1&faction_id=2"
```

### Поиск по названию
```bash
curl "http://localhost:8000/units?title=Atlas"
```

### Фильтр по PV >= 50
```bash
curl "http://localhost:8000/units?pv=50" -H "X-Pv-Mode: gte"
```

### Фильтр по способностям (все должны присутствовать)
```bash
curl "http://localhost:8000/units?specials=ENE,SRCH" -H "X-Specials-Mode: and"
```

### Сортировка по PV по убыванию
```bash
curl "http://localhost:8000/units?sort_by=pv&sort_order=desc"
```

### Комбинированный запрос
```bash
curl "http://localhost:8000/units?era_id=1&title=Warrior&sort_by=pv&sort_order=desc"
```

## Структура проекта

```
Maskirovka_server/
├── main.py              # Точка входа FastAPI
├── settings.py          # Конфигурация (Pydantic Settings)
├── requirements.txt     # Зависимости
├── .env                 # Переменные окружения
├── LICENSE              # Лицензия MIT
├── models/              # ORM модели (Tortoise)
│   ├── __init__.py
│   ├── era.py           # EraModel, EraFactionItem
│   ├── faction.py       # FactionModel
│   └── unit.py          # UnitModel
├── schemas/             # Pydantic схемы
│   ├── __init__.py
│   ├── era.py           # EraItem
│   ├── faction.py       # FactionItem
│   └── unit.py          # UnitItem
├── routers/             # API эндпоинты
│   ├── __init__.py
│   ├── eras.py          # GET /eras
│   ├── factions.py      # GET /factions
│   ├── units.py         # GET /units, GET /units/{unit_id}
│   └── meta.py          # GET /roles, GET /types
└── services/
    ├── __init__.py
    └── unit_service.py  # Логика построения запросов
```

## Конфигурация

Создайте файл `.env` в корне проекта:

```env
DB_URL='sqlite://MY_DB.db'
```

## Лицензия

Исходный код проекта распространяется под лицензией [MIT](LICENSE).

---

*Создано с ❤️ для сообщества российской лиги BattleTech Alpha Strike*

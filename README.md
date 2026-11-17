# SpeakUp 3D — English Trainer

Тренажёр английского для тех, кто хочет **быстро начать говорить**. 1506 слов и фраз уровней A1–B1 по 30 темам. Для каждой карточки есть транскрипция, перевод, описание на английском, пояснение, где применяется, пример и его перевод.

**Демо:** https://sobchenyuk.github.io/English-Trainer-3d/

## Возможности

- **Учить:** 3D-карточки с интервальным повторением (1 → 3 → 7 → 14 → 30 дней). Кнопки «Не знаю / Сложно / Знаю».
- **Тест:** выбрать перевод слова.
- **Слушать:** выбрать перевод фразы на слух, есть медленный режим.
- **Говорить:** произнести фразу, распознавание речи отмечает слова, которые не распознались (Chrome / Edge). В других браузерах можно оценить себя самому.
- **Словарь:** поиск по всем словам и фильтр по темам.
- **Прогресс:** цель «100 ответов в день», серия дней, точность, график за неделю, путь к 3000 слов, прогресс по темам.
- **Настройки:** сколько новых слов в день, тема, скорость озвучки, экспорт и импорт прогресса.

Работает без сервера и сборки. Прогресс хранится в `localStorage` браузера.

## Запуск

```bash
python3 -m http.server 8000
# открыть http://localhost:8000
```

## Docker (свой сервер)

Контейнер на `nginx:alpine` раздаёт статику с gzip, в нём есть healthcheck `/healthz`, файловая система только для чтения.

**Вариант 1. Собрать на сервере:**
```bash
git clone https://github.com/sobchenyuk/English-Trainer-3d.git
cd English-Trainer-3d
cp .env.example .env      # необязательно: без .env используются значения по умолчанию
docker compose up -d --build
# http://<сервер>:38417
```

**Вариант 2. Готовый образ.** GitHub Actions собирает `ghcr.io/sobchenyuk/english-trainer-3d:latest` (amd64 + arm64) при каждом push в `main`:
```bash
docker compose pull && docker compose up -d
```
Если пакет в GHCR приватный, сделайте его публичным: GitHub → Packages → english-trainer-3d → Package settings → Change visibility. Второй способ — выполнить `docker login ghcr.io` на сервере.

**Домен.** Для распознавания речи нужен HTTPS (браузер не даёт микрофон по http). С Cloudflare Tunnel: Zero Trust → Networks → Tunnels → ваш туннель → Public Hostname → `english.ваш-домен` → Service `http://localhost:38417` (или ваш `HOST_PORT`). Если `cloudflared` запущен в Docker в общей сети, укажите `http://english-trainer-3d:80`, где `english-trainer-3d` — это `CONTAINER_NAME`. Когда трафик идёт только через туннель, поставьте `BIND_ADDRESS=127.0.0.1`: тогда порт не будет открыт наружу.

### Переменные окружения

Настройки лежат в файле `.env` в корне проекта. Шаблон — `.env.example`:

```bash
cp .env.example .env
nano .env
docker compose up -d        # применить изменения
```

Docker Compose читает `.env` автоматически и подставляет значения в `docker-compose.yml`. Тот же файл передаётся в контейнер через `env_file`. Все переменные необязательны: если `.env` нет или переменная не задана, берётся значение по умолчанию. Сам `.env` в git не попадает (он в `.gitignore`).

| Переменная | По умолчанию | Что делает |
|---|---|---|
| `HOST_PORT` | `38417` | Порт на сервере, по которому открывается тренажёр. Внутри контейнера nginx всегда слушает `80`. |
| `BIND_ADDRESS` | `0.0.0.0` | На каком адресе сервера открыть порт. `0.0.0.0` — доступен из сети, `127.0.0.1` — только с самого сервера (для Cloudflare Tunnel или reverse proxy). |
| `CONTAINER_NAME` | `english-trainer-3d` | Имя контейнера. Используется в `docker ps`, `docker logs` и как адрес в общей Docker-сети. |
| `IMAGE` | `ghcr.io/sobchenyuk/english-trainer-3d:latest` | Имя и тег образа. `docker compose pull` скачивает его, `docker compose up --build` собирает локально под этим именем. Можно закрепить версию: `...:<commit-sha>`. |
| `TZ` | `Europe/Kyiv` | Часовой пояс контейнера: время в логах nginx. |

Проверить, какие значения подставились:

```bash
docker compose config
```

**Обновление:** `git pull && docker compose up -d --build`. Прогресс пользователей хранится в их браузерах, поэтому при обновлении он не пропадает.

## Публикация на GitHub Pages

Settings → Pages → Source: **Deploy from a branch** → Branch: `main` / `/ (root)` → Save.

## Как добавить слова

1. Добавьте строки в любой файл из `data/` или создайте новый, например `data/12.txt`:
   ```
   @B2|Название темы
   word|перевод|short English definition|Где применяется|Example sentence.|Перевод примера.
   ```
2. Пересоберите словарь (транскрипция проставится автоматически):
   ```bash
   pip install eng_to_ipa
   python3 tools/build.py
   ```

## Структура

```
index.html      — приложение (HTML + CSS + JS, без зависимостей)
words.js        — собранный словарь
data/*.txt      — исходники слов по темам
tools/build.py  — сборка words.js с IPA-транскрипцией
```

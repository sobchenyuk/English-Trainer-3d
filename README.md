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
docker compose up -d --build
# http://<сервер>:8080
```

**Вариант 2. Готовый образ.** GitHub Actions собирает `ghcr.io/sobchenyuk/english-trainer-3d:latest` (amd64 + arm64) при каждом push в `main`:
```bash
docker compose pull && docker compose up -d
```
Если пакет в GHCR приватный, сделайте его публичным: GitHub → Packages → english-trainer-3d → Package settings → Change visibility. Второй способ — выполнить `docker login ghcr.io` на сервере.

**Домен.** Для распознавания речи нужен HTTPS (браузер не даёт микрофон по http). С Cloudflare Tunnel: Zero Trust → Networks → Tunnels → ваш туннель → Public Hostname → `english.ваш-домен` → Service `http://localhost:8080`. Если `cloudflared` запущен в Docker в общей сети, укажите `http://english-trainer-3d:80`.

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

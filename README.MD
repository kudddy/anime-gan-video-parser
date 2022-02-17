## anime-gan-video-parser
Сервис разбивает на кадры видео и отправляет фото в хранилище. Хранилище отдает идентификаторы файлов, сервис отправляет 
id в трансформер.

## Сборка проекта
сборка образа
```
docker build -t docker.io/kudddy/anime-gan-video-parser:release-01 .
```

загрузка образа
```
docker push docker.io/kudddy/anime-gan-video-parser:release-01
```


запуск redis
```
docker run -d --name some-redis -p 6379:6379 -d redis
```

```
docker run -d  --name some-postgres -p 5434:5432 -e POSTGRES_PASSWORD=pass -e POSTGRES_USER=user -e POSTGRES_DB=db postgres:9.6
```

тестовый file_id

```
file_id = "BAACAgIAAxkBAAEBESliAjYdRwoKtkM349RAzJnyVH5OPAACyBIAAqXeEUibNt2b1akicCME"
```
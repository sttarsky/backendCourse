
docker network create myNetwork

docker run --name booking_db \
    -p 5432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=123456 \
    -e POSTGRES_DB=booking \
    --network=myNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:14.8-alpine3.18

docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --network=myNetwork \
    --rm -p 80:80 nginx

docker run --name booking_cache \
    -p 7379:6379 \
    --network=myNetwork \
    -d redis:7.4

docker run --name booking_back \
    -p 7777:8000 \
    --network=myNetwork \
    booking_image


docker run --name booking_celery_worker \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO


docker run --name booking_celery_beat \
    --network=myNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B


docker build -t booking_image .
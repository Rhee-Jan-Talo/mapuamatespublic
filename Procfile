web: gunicorn mapuamates.asgi:application --preload --log-file - -w 5 -k uvicorn.workers.UvicornWorker --env UVICORN_LIFESPAN=off
heroku ps:scale web=1
heroku config:set DJANGO_SETTINGS_MODULE=mapuamates.settings


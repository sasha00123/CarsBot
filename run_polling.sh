export $(egrep -v '^#' .env | xargs)
python manage.py botpolling --username "$BOT_USERNAME"
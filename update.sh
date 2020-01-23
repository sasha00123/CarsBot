export SERVER=root@95.179.212.198
scp -r main/*.py $SERVER:~/cars/main
scp -r cars/*.py $SERVER:~/cars/cars
scp -r cars/settings/*.py $SERVER:~/cars/cars/settings
scp -r messages/* $SERVER:~/cars/messages
scp .env $SERVER:~/cars/.env
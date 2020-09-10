Решение тестового задания. 
В БД записал все в одну таблицу, чтобы упростить. По хорошему понимаю что необходимы отдельные справочники для цветов, производителей авто и т.д.
Инициализация схемы БД тоже сделал в скрипте питона, пока с докером не до конца разобрался.



Примеры запросов:

curl -XGET 'localhost:5000/api/cars/'

curl -XPOST -H 'Content-Type: application/json' -d '{"car_id":1, "colour":"white","year":2020, "manufacturer":"tesla"}' 'localhost:5000/api/cars/'

curl -XPOST -H 'Content-Type: application/json' -d '{"car_id":2, "colour":"blue","year":1998, "manufacturer":"audi"}' 'localhost:5000/api/cars/'

curl -XPOST -H 'Content-Type: application/json' -d '{"car_id":3, "colour":"green","year":2013, "manufacturer":"toyota"}' 'localhost:5000/api/cars/'


curl -XGET 'localhost:5000/api/cars/1/'



curl -XDELETE 'localhost:5000/api/cars/1/'

curl -XGET 'localhost:5000/api/cars/'


curl -XPATCH -H 'Content-Type: application/json' -d '{"colour":"black","year":1998, "manufacturer":"audi"}' 'localhost:5000/api/cars/2/'

curl -XGET 'localhost:5000/api/cars/'  

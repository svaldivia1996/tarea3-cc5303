# tarea3-cc5303


## Para ejecucion usando Dockerfile
Primero crear una network para los contenedores
`docker network create mynetwork`

Hacer la imagen de app.py
`docker build -t my-flask-app .`

Luego para crear los containers que son nuestros nodos pueden recibir dos parametros como enviroment 'IP' la ip de un nodo vecino al cual conecarse
'MYPORT' el puerto que tiene el contenedor mapeado en el docker run
Ejemplo de caso de uso para crear 4 nodos
#### Ejemplo de crear un nodo 1 (el primer nodo se conoce a si mismo)
    docker run -d -p 8080:8080 --name nodo1 --network=mynetwork my-flask-app
### Ahora uno puede revisar los nodos que conoce el nodo1 (si mismo)
    localhost:8080/nodes
    muestra solo
    http://172.19.0.2:8080/ que es la ip e si mismo dentro de mynetwork
#### Ejemplo de nodo 2 (el nodo2 se conectará con el nodo1 cuya ip es 172.19.0.2)
    `docker run -d -p 8081:8080 -e IP=172.19.0.2 -e MYPORT=8081 --name nodo2 --network=mynetwork my-flask-app`
#### Ahora al revisar:
    localhost:8080/nodes
    localhost:8081/nodes
    deberian aparecer listado las 2 ip's y los puertos de los 2 nodos
#### Ejemplo de nodo 3 (el nodo3 se conectará con el nodo2 cuya ip es 172.19.0.3)
    docker run -d -p 8082:8080 -e IP=172.19.0.3 -e MYPORT=8082 --name nodo3 --network=mynetwork my-flask-app

## Para uso

Luego para revisar los nodos vecinos por ejemplo del nodo 1, en un inicio solo se conocen a si mismos:
http://localhost:8080/nodes

En caso de crear un nodo y no conectarlo con otro se disponibilizo un POST request para conectar
Un ejemplo de peticion POST para conectar el nodo 1 cuya ip es  (172.193.0.2 con puerto 8080) al nodo 2 (con port 8081):
`curl -X POST -H "Content-Type: application/json" -d '{"node_address": "172.19.0.2", "node_port": "8080"}' http://localhost:8081/connect `

finalmente revisar en
    -http://localhost:8080/nodes
    -http://localhost:8081/nodes
para verificar si fueron conectados.

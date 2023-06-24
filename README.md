# tarea3-cc5303

## Explicación sobre implementación
Para la implementación sobre la iteración de esta tarea se decidió formatear los mensajes para ser representados con un JSON
que contiene un id el mensaje y el emisor. La razón de realizar esto es para resolver aquellos casos bordes en que se envian mensajes al mismo tiempo con misma
id, para estos casos lo que se realiza y comparar el emisor de cada mensaje con id repetido y ordenarlos desde menor ip a mayor y luego actualzar aquellos id's repetidos
Debido a esto el POST request fue modificado de solo mensaje a los 3 atributos descrito anteriormente. Para facilitar su uso se creo un interfaz simple de chat en html
para mandar estos mensajes de manera rapida y mas comoda (con la desventaja de no ser responsiva ya que es html puro con script pequeño dentro).


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
### Muestra solo
    http://172.19.0.2:8080/ que es la ip e si mismo dentro de mynetwork
#### Ejemplo de nodo 2 (el nodo2 se conectará con el nodo1 cuya ip es 172.19.0.2)
    `docker run -d -p 8081:8080 -e IP=172.19.0.2 -e MYPORT=8081 --name nodo2 --network=mynetwork my-flask-app`
#### Ahora al revisar:
    localhost:8080/nodes
    localhost:8081/nodes
    deberian aparecer listado las 2 ip's y los puertos de los 2 nodos
#### Ejemplo de nodo 3 (el nodo3 se conectará con el nodo2 cuya ip es 172.19.0.3)
    docker run -d -p 8082:8080 -e IP=172.19.0.3 -e MYPORT=8082 --name nodo3 --network=mynetwork my-flask-app

## Para uso de conección entre nodos (Tarea 2)

Luego para revisar los nodos vecinos por ejemplo del nodo 1, en un inicio solo se conocen a si mismos:
http://localhost:8080/nodes

En caso de crear un nodo y no conectarlo con otro se disponibilizo un POST request para conectar
Un ejemplo de peticion POST para conectar el nodo 1 cuya ip es  (172.193.0.2 con puerto 8080) al nodo 2 (con port 8081):
`curl -X POST -H "Content-Type: application/json" -d '{"node_address": "172.19.0.2", "node_port": "8080"}' http://localhost:8081/connect `

finalmente revisar en
    -http://localhost:8080/nodes
    -http://localhost:8081/nodes
para verificar si fueron conectados.

## Para uso de chat global (Tarea 3)

# Revisar todos los mensajes
    http://localhost:8080/messages
# Revisar last=XX mensajes
    http://localhost:8080/messages?last=XX
# Se habilitó una interfaz simple de chat en html(no se actualiza en tiempo real es solo para facilitar el envio de POST request)
    http://localhost:8080/chat

# Ejemplo de POST request
    curl -X POST -H "Content-Type: application/json" -d '{"id":2,"message":"saludos a todos desde el nodo 3", "sender":"172.18.0.4"}' http://localhost:8080/messages
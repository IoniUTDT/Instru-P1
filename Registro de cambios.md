Voy a limpiar y emprolijar el codigo que ya tenemos andando. 

La idea es crear un archivo AudioCotrol.py que tenga una recopilacion de las cosas utiles dentro no como clase (como veniamos haciendo) sino como funciones. 
En ese archivo deberia converger lo que haya util en p1.py, pruebainstru.py y en test.py

Por otro lado creo un archivo ipynb (un jupyter notebook) donde se deberian poder testaer y ejecutar todas las pruebas y experimentos que querramos realizar. 


Cosas tomadas/mudadas/corregidas desde pruebainstru (que es el archivo con mas desarrollo)

9/9/18:
16hs:

- Importamos todos los paquetes
- Eliminamos la estructura de clase y simplemente definimos funciones
- Definimos las constantes, bajamos ampMax a 0,5 porque creo que el rango total es 1, entonces con 1 se va a +-1 y satura. Al menos eso pasa en a compu de la casa de Ioni
- Copiamos crear onda, eliminamos las referencias a self porque no es mas una clase.
- Copiamos test, eliminamos las refrencias a self porque no es mas una clase. La testeamos y funciona. 
- crearRect no la incorporamos porque parece no ser funcional y/o util
- crearRamp idem
- crearCons idem
- la funcion serrucho la salteamos por el momento porque no parece tener funcionalidad
- la funcion sawtooth la salteamos porque no queda clara la utilidad por el momento.
- la funcion square la salteamos

- Copiamos la funcion playrec_onda haciendo las modificaciones porque ya no es mas parte de una clase.
- La testeamos y funciona!

- Salteamos la funcion playrec_sw porque la idea seria crear un playrec generico donde el imput sea un array de datos con la funcion
- Armamos la funcion playrec. Anda. Vamos a armar el input de los playrec preexistentes

- Agrego un long_d para tener una referencia de longitud predeterminada en todas las funciones. 
- Cambio los nombres sawtooth a rampa y triangulo respectivamente
- Ya no tiene sentido usar crarRampa y serrucho que estaban definidos en el archivo fuente. Queda pendiente ver como se genera una cuadrada
- Creada la cuadrada con la misma logica
- Queda obsoleto el playrec_square. Tesetado. 

- Anotamos para desarrollar la funcion slewrate
- Copiamos la funcion del calculo de potencia. La mejoramos un porquito y agregamos opcion de debug.
- Retocamos la funcion barrido en frecuencia
- Copiamos addCola
- Copiamos el add triguer.
- Copiamos el sync que esta a medio hacer.

19:13

Hasta aca ya revisamos todos los codigos de pruebaInstru. En test no hay nada que no sea redundante. Y lo mismo en p1.py

23/9/18

Ayer estuve desarrollando la version final del sync y parece funcionar.

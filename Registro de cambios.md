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

Estoy probando porque parece que no anda bien algo con el tema del filtro en frecuencias. Da una señal muy rara usando los cables que arme pero siempre la misma.

24/8/18 

Al final comprobe que era un problema del rango de frecuencias que es gigantesco, en el notebook Mediciones se puede ver que da identico con el cable bueno que con los armados.

Ahora estuve retocando algunos detalles del codigo, de coherencia y nombres mas que nada y simplificando cosas. La mas importante es que la funcion potencia asume que se usa el playrec_sync en lugar de recortar arbitrariamente. 
Acabo de hacer un test que se me habia ocurrido que era hacer un playrec_sync de una señal trigguer para ver si efectivamente recorta bien xq mandando una sinusoidal es dificil saber si no corta de mas y efectiovamente hay un error logico que es que recorta en el principio del trigguer del final y no en el final posta. SOLUCIONADO

PENDIENTE: habria que hacer algun tipo de codigo para calibrar la escala (con un divisor de tensiones fijo asociado al USB) y otro para ver que no este saturando la entrada/salida (se puede ver como da la convolucion de una señal contra si misma y ver si a travez de la medicion en el chanel del trigguer varia mucho la forma). 

Cambio el delay default para evitar que siempre se duplique el tiempo de medicion (en casa dio que el default era muy corto pero con el doble da mas o menos bien)

Para poder usar el playrec_sync con el barrido de frecuencia tuve que agregar la opcion de alternar los canales en el playrec_sync porque sino no se puede evaluar ambos canales. Tambien voy a hacer que sea opcional testear ambos canales. Lo hice, por alguna razon extraña ahora tarda casi el doble en ejecutarse. Como windows tiene en el control de audio un indicador de si el microfono esta midiendo o no, pude observar que a diferencia de antes que hacia un play rec e inmediatamente otro, ahora hay un tiempo apreciable muerto entre cada registro del microfono, puede deberse a tiempos de ejecucion del sync. Por ahora no parece grave, pero estaria bueno ver que onda.

Cambio que la escala del barrido en frecuencia sea log.

25/9/18

14:30
Me di cuenta que tarda mas xq hay como 0.8 segundos de "cola en las señales", no esta claroq ue haga falta que sea tan larga la inicial y tampoco que sea tan largo el largo en el barrido en frecuencias xq ahora recorta bien! Voy a cambiar parametros a ver si funciona bien siendo mas rapido. Parece funcionar bien, lo unico, si pongo que los triguers sean de frecuencias altas empiezo a tener problemas con el fs de aliasing. Hay que considerar si eso no es el problema que se ve en parte de la mala respuesta en frecuencia. QUE ONDA QUE EL FS SEA 48000 Y EL LIMITE DEL AUDIBLE SEA 20000? 
Despues de hacer varios cambios y ajustar, la señal medida mid 0.5 segundos, pero la iteracion mide 1.6 segundos. Evidentemente el tiempo es tiempo de procesamiento. 

Agregamos una opcion plot en el playrec_sync para que grafique el resultado ademas de devolver los datos.
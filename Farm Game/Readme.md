# Tarea 02: DCCampo 

## Consideraciones generales :octocat:

Esta tarea funciona en parte, pero me falto completar varias funcionalidades por temas de tiempo :c.
El mapa se crea como se pide, pero se me olvido sacarle los frames a los labels de los elementos. Se puede sembrar solo en las areas de cultivo predeterminadas, porque si bien uno puede arar con la azada, estas nuevas areas de cultivo no pueden ser sembradas :c. El personaje si respeta las colisiones, excepto cuando se trata de arboles, y tambien respeta los limites del mapa, excepto porque en el limite inferior y el derecho se pasa un poquito. Otra cosa respecto a las colisiones es que al chocar el personaje solo puede moverse en la direccion opuesta, porque sino se queda incrustado en la roca. Se me olvidó hacer que se muera al perder la energía, pero el juego si se acaba cuando compra el ticket. Finalmente la pausa igual funciona pero solo detiene el tiempo y el personaje, no los timers de los recursos.

### Cosas implementadas y no implementadas :white_check_mark: :x:

Solo escribiré los items que no implemente por completo.

 - **Ventanas:**
	
	- **Inventario:**
		- ***Las semillas se pueden arrastrar correctamente al mapa usando drag and drop.  Lo hace con un correcto uso de señales:*** Funcion bien solo que no se puede sembrar sobre tierra arada con la azada.
 - **Entidades:** 
	 - **Jugador:**
		 - ***El movimiento del jugador es fluido, continuo, animado y respeta colisiones.  Lo hace con un correcto uso de señales:*** Colisiona pero debe moverse hacia atras una vez para poder volver a mover su cuerpo. Se sale un poco del mapa.
		 - ***Se implementa correctamente la enegía del jugador:*** No muere cuando se le acaba la energía.
	 - **Recursos:**
		 - ***Los árboles y el oro aparecen de forma correcta en el mapa. Lo hace con un correcto uso de señales:*** El oro y los arboles pueden aparecer en sonas de cultivo.

 - **Funcionalidades Extra:** 
	 - **Pausa:**
		 - ***Está implementado el boton, al seleccionarlo se produce el efecto indicado:*** Los timers de los recursos no se pausan.

 - **Bonus:**
	 - No alcance a hacer ningun bonus :c

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Para no confundirte, estos son los otros archivos que cree que vienen en el repo:
1. ```DCCampo.png``` en ```sprites_propias```
2. ```Back_End.py``` en ```T02``` es el back end. 
3. ```formulas.py``` en ```T02```  para formulas que use.
4. ```front_end_2.py``` en ```T02``` para modularizar el front end. Este modulo tiene lo necesario para hacer el mapa.
5. ```FrontEnd.py``` en ```T02```  Tiene el modulo principal para hacer el mapa, la ventana de inicio, y la ventana de juego. 
6. ```parametros.py``` en ```T02``` Tiene los parametros que no venian en el syllabus y los diccionarios de sprites.
7. ```stats.py``` en ```T02``` Tiene la widget de las estadisticas del juego.
8. ```ventana_inv_tienda.py``` en ```T02``` Tiene la widget del inventario y la tienda.

## Librerías :books:
### Librerías externas utilizadas
Fuera de PyQt5, utilice las siguientes librerias.

1. ```random.uniform()```: ```evento_ocurre() / formulas.py```
2.  ```random.choice()```: ```arbol_o_oro() / FrontEnd.py```



## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1.  Supuse que como todas las cosas se veian de frente, el personaje colisionaría solo con sus pies y no su cabeza. por lo que hice un QRect en los pies que colisiona con el QRect de los elementos del mapa.


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<[Link](https://stackoverflow.com/questions/55636860/drag-and-drop-qlabels-with-pyqt5-pixmap-and-text)>: Permite que los QLabels apliquen Drag And Drop. Lo utilice para hacer la clase `DraggableLabel` del modulo `ventana_inv_tienda.py`  y `DropLabel` de `front_end_2.py`.

## MEME:
Hice casi toda la tarea el viernes en la noche y el sabado en el dia, y debo reconocer que si bien no me quedó buena, logré hacer más de lo que esperaba con el tiempo que tuve. Adjunto meme de como me sentí. [uwu](https://drive.google.com/file/d/11MZEbQy0Q8swy3aoHL95lUn75rum0caL/view?usp=sharing)





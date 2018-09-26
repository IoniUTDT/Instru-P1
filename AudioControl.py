'''
Este archivo contiene las funciones desarrolladas para usar las entradas y salidad de audio y con ellas realizar mediciones experimentales de respuestas de circuitos.
'''


# Importamos paquetes
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy import signal

# Definimos constantes
fs = 48000
ampMax = 0.5 # En valores arbitrarios float que es lo que recibe el paquetes sounddevice
long_d = 1 # En segundos
DEBUG = False
triguer_max = 1000
triguer_min = 400
triguer_test = 800
t_trig = 0.02 # Tiempo que dura la senal de trigger


# Definimos funciones utiles

def testOutput():
    sd.play(np.stack((Onda(440),Onda(440,amp=0)), axis=-1))
    sd.wait()
    sd.play(np.stack((Onda(440,amp=0),Onda(440)), axis=-1))
    sd.wait()
    print('Tendría que haber escuchado 1 segundo de audio en cada canal')
    
def slewrate ():
    print ('Falta implementar')
    # Hay que desarrollar esta funcion
    
def calculo_potencia(data,excluir=0.5):
    # Data tiene que ser un array de dimension 1
    if DEBUG:
        print ('Largo original: ' + str(len(data)))
        plt.plot(data,label='Original')
    data_recortada = np.array(data[int(len(data)*excluir/2):int(len(data)-len(data)*excluir/2)])
    if DEBUG:
        print ('Largo recortado: ' + str(len(data_recortada)))
        plt.plot(data_recortada,label='recortada')
        plt.legend()
    return np.sum(data_recortada**2)/(len(data_recortada))


# Definimos funciones de usuario

def playrec_onda(frec,amp=ampMax,long=long_d):
    # pone una función onda y la graba al mismo tiempo. La salida de esta función es: un gráfico que muestra la señal que mandó y la que midió y el array correspondiente a la medición.
    myrec=sd.playrec(Onda(frec,amp=amp,long=long),fs,channels=2)
    sd.wait()
    plt.plot(myrec)
    return myrec

def playrec (data,show=False):
    myrec=sd.playrec(data,fs,channels=2)
    sd.wait()
    if show:
        plt.figure()
        plt.plot(data, label = 'Input')
        plt.plot([data[0] for data in myrec], label = 'Ch1')
        plt.plot([data[1] for data in myrec], label = 'Ch2')
        plt.legend()
    return myrec

def rampa(frec, amp=ampMax, long=long_d):
    t = np.linspace(0,long,num=fs*long)
    return signal.sawtooth(2*np.pi*frec*t)*amp

def triangular(frec, amp=ampMax, long=long_d):
    t = np.linspace(0,long,num=fs*long)
    return signal.sawtooth(2*np.pi*frec*t,0.5)*amp

def square(frec, amp=ampMax, long=long_d):
    t = np.linspace(0,long,num=fs*long)
    return signal.square(2*np.pi*frec*t)*amp

def Onda(frec,amp=ampMax,long=long_d):
    t=np.arange(long*fs)
    return amp*np.sin(2*np.pi*frec*t/fs)

def barrido_frecuencia_sin(frec_min=10,frec_max=1000000,pasos=1000,amp=ampMax,long=long_d):
        "Genera un vector de frecuencias entre la mínima y la máxima, con los pasos especificados. Manda funcines senoidales de esa frencuencia y graba la respuesta. Devuelve (por ahora) el vector de frecuencias y un gráfico que muestra la amplitud máxima registrada (puede mejorarse como la obtiene) en función de la frecuencia.CALCULAR LÍMITE TEORICO"
        if DEBUG:
            print ('Iniciando barrido en frecuencias')
        frecs=np.logspace(np.log10(frec_min),np.log10(frec_max),num=pasos)
        if DEBUG:
            print ('frecuencias a testear')
            print (frecs)
        pot_in_ch1 = []
        pot_in_ch2 = []
        pot_out_ch1 = []
        pot_out_ch2 = []
        for frec in frecs:
            if DEBUG:
                print (frec)
            signal = Onda(frec)
            rec = playrec(signal)
            sd.wait()
            pot_in_ch1 += [calculo_potencia(signal)]
            pot_in_ch2 += [calculo_potencia(signal)]
            pot_out_ch1 += [calculo_potencia(rec[:,0])]
            pot_out_ch2 += [calculo_potencia(rec[:,1])]
            print ('Evaluando frecuencia: ' + str(frec)) # Mejorar esta linea
            
        plt.plot(frecs,pot_in_ch1,label='In_Ch1')
        plt.plot(frecs,pot_in_ch2,label='In_Ch2')
        plt.plot(frecs,pot_out_ch1,label='Out_Ch1')
        plt.plot(frecs,pot_out_ch2,label='Out_ch2')
        plt.legend()
        return frecs, [pot_in_ch1,pot_in_ch2],[pot_out_ch1,pot_out_ch2]
    
def add_cola(signal, long=0.2):
    ret=np.concatenate((np.zeros(int(np.round(long*fs))),signal,np.zeros(int(np.round(long*fs)))))
    return ret

def gen_trigger(senal):
    samples_triguer = t_trig * fs
    N=len(senal)
    if N>=samples_triguer * 2: # Pedimos que haya una senal lo suficientemente larga
        c1=Onda(triguer_min,long=t_trig)
        c2=np.zeros(int(np.round(N-samples_triguer*2)))
        c3=Onda(triguer_max,long=t_trig)
        trig=np.concatenate((c1,c2,c3))
        return trig
    else:
        return print('La cantidad de muestras de la señal no cumple el criterio de ser 10 veces mayor al tamaño de los triggers')
    
def sync(signal):
    print ('Funcion en desarrollo')
    print ('Esta funcion asume que el Ch1 conecta directamente la salida de audio con la entrada de microfono, y que el Ch2 conecta la salida de audio con la entrada del dispositivo a caracterizar, cuya respuesta llega al Ch2 del microfono.')
    rec=self.playrec(np.stack((add_cola(gen_trigger(senal)),add_cola(senal)),axis=-1))
    sd.wait()
    plt.figure(2),plt.plot(rec)
    return rec

def sync_test(signal):
    ratio_umbral=3
    import numpy
    print ('Funcion en desarrollo. Queremos probar implementar el sync salteando la medicion')
    trig = gen_trigger(signal)
    trig = add_cola(add_cola(trig))
    plt.figure(1)
    plt.plot(signal)
    plt.plot(trig)
    #trig = trig[0:int(len(trig)/2)]
    t = numpy.fft.fft(trig)
    plt.figure(2)
    plt.plot(numpy.abs(t))
    frec_min_esperada = triguer_min * len(trig)/fs
    frec_max_esperada = triguer_max * len(trig)/fs
    frec_test_esperada = triguer_test * len(trig)/fs
    delta = int((frec_max_esperada-frec_min_esperada)/20)
    if delta < 10:
        print ('Error: la distancia entre los picos esperados en el triguer es muy cercana a cero.')
        return
    if frec_min_esperada < delta:
        print ('Error: el ancho del pico minimo abarca al cero')
        return
    if frec_max_esperada > len(t) + delta:
        print ('Error: el ancho del pico maximo abarca al borde')
        
    print ('Pico 1 esperado en: ' + str(frec_min_esperada))
    print ('Pico 2 esperado en: ' + str(frec_max_esperada))
    print ('Pico no esperado en: ' + str(frec_test_esperada))
    print (delta)
    valor_pico_min = np.mean(np.abs(t[int(frec_min_esperada-delta):int(frec_min_esperada+delta)]))
    valor_pico_max = np.mean(np.abs(t[int(frec_max_esperada-delta):int(frec_max_esperada+delta)]))
    valor_pico_test = np.mean(np.abs(t[int(frec_test_esperada-delta):int(frec_test_esperada+delta)]))
    print (valor_pico_min)
    print (valor_pico_max)
    print (valor_pico_test)
    detectados = 0 
    if valor_pico_min/valor_pico_test > ratio_umbral:
        detectados += 1
        print ('Primer pico detectado')
    if valor_pico_max/valor_pico_test > ratio_umbral:
        detectados += 1
        print ('Segundo pico detectado')
    if detectados == 2:
        print ('Principio y fin de la señal detectadas')
    else:
        print ('Error, no se ha detectado el principio o fin de la señal en el Ch1.')
        return 
    frecuencia_arbitraria = 440
    a_convolucionar = gen_trigger(Onda(frecuencia_arbitraria,long=t_trig*2))
    a_convolucionar = a_convolucionar[0:int(len(a_convolucionar)/2)]
    a_convolucionar = Onda(triguer_min,long=t_trig)
    plt.figure(3)
    plt.plot(a_convolucionar)
    plt.plot(trig,'*')
    convolucion = np.convolve(np.flip(a_convolucionar),trig,'valid')  # Revisar porque funciona con un flip
    plt.figure(4)
    plt.plot(convolucion)
    pos_max = np.argmax(convolucion)
    print ('pos max: ' + str(pos_max/fs))
    
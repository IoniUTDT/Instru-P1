'''
Este archivo contiene las funciones desarrolladas para usar las entradas y salidad de audio y con ellas realizar mediciones experimentales de respuestas de circuitos.
'''


# Importamos paquetes
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy import signal

# Definimos constantes
fs = 48000
ampMax = 0.5 # En valores arbitrarios float que es lo que recibe el paquetes sounddevice
long_d = 1 # En segundos defalut para mediciones
long_frec = 0.1 #Segundos. Tiempo que duira la señal para hacer barrido en frecuencias. Es mas corto para evitar que el barrido tarde mucho al recorree muchas frecuencias. 
DEBUG = False
triguer_max = 1000
triguer_min = 400
triguer_test = 800
t_trig = 0.02 # Tiempo que dura la senal de trigger
delay_soft_default = 0.1 # Segundos. Es el tiempo estimado que se asume que tarda 
extra_delay = 0.2 # Segundo. Tiempo extra que agrega si no ve medicion. 

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
    # return np.sum(data_recortada**2)/(len(data_recortada))
    # Como ahora tenemos una funcion sync que mide exactamente la señal enviada podemos hacer la potencia de toda la señal.
    return np.sum(np.array(data)**2)/len(data)

# Definimos funciones de usuario

def playrec (data,show=False):
    myrec=sd.playrec(data,fs,channels=2)
    sd.wait()
    if show:
        plt.figure()
        if type (data[0]) == list:
            plt.plot([dat[0] for dat in data], label = 'In1')
            plt.plot([dat[1] for dat in data], label = 'In2')
        else:
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

def RtaFrecuencia(frec_min=1,frec_max=1000000,pasos=1000,amp=ampMax,long=long_frec,stereo=False):
    "Genera un vector de frecuencias entre la mínima y la máxima, con los pasos especificados. \
    Manda funcines senoidales de esa frencuencia y graba la respuesta. \
    Devuelve (por ahora) el vector de frecuencias y un gráfico que muestra la amplitud máxima registrada \
    (puede mejorarse como la obtiene) en función de la frecuencia.CALCULAR LÍMITE TEORICO"
    if DEBUG:
        print ('Iniciando barrido en frecuencias')
    frecs=np.logspace(np.log10(frec_min),np.log10(frec_max),num=pasos)
    if DEBUG:
        print ('frecuencias a testear')
        print (frecs)
    pot_in_ch1 = []
    if stereo:
        pot_in_ch2 = []
    pot_out_ch1 = []
    if stereo:
        pot_out_ch2 = []
    for count in tqdm(range(len(frecs))):
        frec=frecs[count]
        signal = Onda(frec)
        rta = playrec_sync(signal)
        sd.wait()
        pot_in_ch1 += [calculo_potencia(signal)]
        pot_out_ch1 += [calculo_potencia(rta)]
        if stereo:
            rta = playrec_sync(signal,alternar=True)
            sd.wait()
            pot_in_ch2 += [calculo_potencia(signal)]
            pot_out_ch2 += [calculo_potencia(rta)]
        
    plt.semilogx(frecs,pot_in_ch1,label='In_Ch1')
    plt.semilogx(frecs,pot_out_ch1,label='Out_Ch1')
    if stereo:
        plt.semilogx(frecs,pot_in_ch2,label='In_Ch2')
        plt.semilogx(frecs,pot_out_ch2,label='Out_ch2')
    plt.legend()
    out = [frecs, pot_in_ch1, pot_out_ch1]
    if stereo:
        out = [frecs, pot_in_ch1, pot_out_ch1, pot_in_ch2, pot_out_ch2]
    return out

def add_cola(signal, prelong=delay_soft_default, postlong = delay_soft_default):
    ret=np.concatenate((np.zeros(int(np.round(prelong*fs))),signal,np.zeros(int(np.round(postlong*fs)))))
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
    
def playrec_sync(signal,show=False,alternar=False,plot=False):
    ratio_umbral=3
    import numpy
    # Generamos la señal triguer a partir de la señal deseada.
    trig = gen_trigger(signal)
    # Aqui empezamos un loop previendo que haya un delay mas largo del esperado en el soft. 
    trigguer_detected = False
    delay = delay_soft_default
    while not trigguer_detected:
        delay = delay + extra_delay
        signal_toplay = add_cola(signal,delay_soft_default,delay)
        trig_toplay = add_cola(trig,delay_soft_default,delay)
        if not alternar:
            toplay = np.stack((signal_toplay,trig_toplay), axis=-1)
        else: 
            toplay = np.stack((trig_toplay,signal_toplay), axis=-1)
        rec = playrec(toplay,show=show)
        if not alternar:
            rta = [data[0] for data in rec]
            trigRta = [data[1] for data in rec]
        else:
            rta = [data[1] for data in rec]
            trigRta = [data[0] for data in rec]
        if show:
                    plt.figure()
                    plt.plot(rta,label='Rta')
                    plt.plot(trigRta,label='Trig')
                    plt.legend()
        t = numpy.fft.fft(trigRta)
        if show:
                    plt.figure()
                    plt.plot(numpy.abs(t))
        frec_min_esperada = triguer_min * len(trigRta)/fs
        frec_max_esperada = triguer_max * len(trigRta)/fs
        frec_test_esperada = triguer_test * len(trigRta)/fs
        delta = int((frec_max_esperada-frec_min_esperada)/20)
        if delta < 10:
            print ('Error: la distancia entre los picos esperados en el triguer es muy cercana a cero.')
            return
        if frec_min_esperada < delta:
            print ('Error: el ancho del pico minimo abarca al cero')
            return
        if frec_max_esperada > len(t) + delta:
            print ('Error: el ancho del pico maximo abarca al borde')
        if DEBUG:
                    print ('Pico 1 esperado en: ' + str(frec_min_esperada))
                    print ('Pico 2 esperado en: ' + str(frec_max_esperada))
                    print ('Pico no esperado en: ' + str(frec_test_esperada))
        valor_pico_min = np.mean(np.abs(t[int(frec_min_esperada-delta):int(frec_min_esperada+delta)]))
        valor_pico_max = np.mean(np.abs(t[int(frec_max_esperada-delta):int(frec_max_esperada+delta)]))
        valor_pico_test = np.mean(np.abs(t[int(frec_test_esperada-delta):int(frec_test_esperada+delta)]))
        if DEBUG:
                    print (valor_pico_min)
                    print (valor_pico_max)
                    print (valor_pico_test)
        detectados = 0 
        if valor_pico_min/valor_pico_test > ratio_umbral:
            detectados += 1
            if DEBUG:
                print ('Primer pico detectado')
        if valor_pico_max/valor_pico_test > ratio_umbral:
            detectados += 1
            if DEBUG:
                        print ('Segundo pico detectado')
        if detectados == 2:
            if DEBUG:
                        print ('Principio y fin de la señal detectadas')
            trigguer_detected = True
        else:
            if DEBUG:
                        print ('Error, no se ha detectado el principio o fin de la señal en el Ch1.')
            delay += extra_delay
            if delay > 5 * extra_delay:
                print ('Ha ocurrido un error, no se logra detectar bien el trigguer pese a esperar cinco veces lo predeterminado')
                return
            if DEBUG:
                        print ('Cambiando tiempo de espera a: ' + str(delay))

    # Detectamos ambos extremos y recortamos.
    a_convolucionar = Onda(triguer_min,long=t_trig)
    convolucion = np.convolve(np.flip(a_convolucionar),trigRta,'valid')  # Revisar porque funciona con un flip
    if show:
        plt.figure()
        plt.plot(convolucion)
    pos_max_ini = np.argmax(convolucion)
    if DEBUG:
        print ('Se ha detectado el inicio de la señal a los ' + str(pos_max_ini/fs) + ' segundos o en el frame: ' + str(pos_max_ini))
    
    a_convolucionar = Onda(triguer_max,long=t_trig)
    convolucion = np.convolve(np.flip(a_convolucionar),trigRta,'valid')  # Revisar porque funciona con un flip
    if show:
        plt.figure()
        plt.plot(convolucion)
    pos_max_final = np.argmax(convolucion)
    pos_max_final += int (t_trig*fs) # agregamos el tiempo que dura el triguer para no recortar cuando empieza.
    if DEBUG:
        print ('Se ha detectado el fin de la señal a los ' + str(pos_max_final/fs) + ' segundos o en el frame: ' + str(pos_max_final))
    rta = rta[pos_max_ini:pos_max_final]
    if show or plot:
        plt.figure()
        plt.plot(rta)
    return rta
    
    
    
    

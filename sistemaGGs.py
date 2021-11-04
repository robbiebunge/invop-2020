import numpy as np 
import matplotlib.pyplot as plt

# Definir la semilla 
np.random.seed(0)

# Definir parametros del sistema
landa = 4.5
mu = 5

# Definir funciones auxiliares
# def generarEventoDiscreto(probOutcomes):
#     x = np.random.uniform()
#     intervalosDeProb = np.cumsum(probOutcomes[:,1])
#     filaOutcome = np.digitize(x, intervalosDeProb)
#     outcome = probOutcomes[filaOutcome, 0]
#     return outcome

def agregarPersonaACola(nCola, cabeceraCola, nPersonasArribadas):
    nCola = nCola + 1
    if nCola == 1:
        cabeceraCola = nPersonasArribadas

    return nCola, cabeceraCola

def sacarPersonaACola(nCola, cabeceraCola):
    nCola = nCola - 1
    if nCola == 1:
        cabeceraCola = cabeceraCola + 1

    return nCola, cabeceraCola

def asignarPersonaASever(serversOcupados, tServicioServers, ti):
    jServersDesocupados = np.argwhere(serversOcupados == 0) # encontrar los indices de servers desocupados (recordad que los indices arrancan a contar desde 0!)
    nServersDesocupados = np.sum(serversOcupados == 0)      # computar el numero de servers desocupados
    serverAOcupar = np.random.randint(nServersDesocupados)  # elegir el indice de uno de los servers desocupados de manera aleatoria
    serverAOcupar = jServersDesocupados[serverAOcupar]      # elegir el indice de uno de los servers desocupados de manera aleatoria (continued)
    serversOcupados[serverAOcupar] = 1  # marcar el server como ocupado
    tServicioServers[serverAOcupar] = ti + generarTiempoServicio()  # generar aleatoriamente el tiempo en que el server recien ocupado completara el servicio

    return serversOcupados, tServicioServers

def generarTiempoArribo():
    #Tarribo = generarEventoDiscreto(probArribos)
    Tarribo = np.random.exponential(1/landa)
    return Tarribo

def generarTiempoServicio():
    #Tservicio = generarEventoDiscreto(probServicios)
    # Tservicio = np.random.uniform(2,5)
    Tservicio = np.random.exponential(1/mu)
    return Tservicio

def sim(s):
    # Definir parametros de la simulacion
    T = 5*60
    nSim = 2000
    
    # Crear variables necesarias
    tTicks = np.zeros(nSim)
    nPersonas = np.zeros(nSim)
    serversOcupados = np.zeros(s)
    tServicioServers = np.zeros(s)
    
    # Inicializar sistema
    nPersonasInicial = 0
    nPersonas[0] = nPersonasInicial
    cabeceraCola = 0
    nCola = max(nPersonasInicial - s, 0)
    proximoEvento = 'arribo'
    tProximoEvento = generarTiempoArribo()
    nPersonasArribadas = 0
    tServicioServers[:] = np.inf
    serverCompletaServicio = 0
    nServersOcupados = min(nPersonasInicial, s)
    for i in range(int(nServersOcupados)):
        asignarPersonaASever(serversOcupados, tServicioServers, 0)
    
    # Correr la simulacion
    for i in range(1, nSim):
    
        evento = proximoEvento
        tTicks[i] = tProximoEvento 
    
        # Procesar evento
        if evento == 'arribo':
            # Incrementar el numero de personas en el sistema y el numero de personas arribadas al sistema
            nPersonas[i] = nPersonas[i-1] + 1
            nPersonasArribadas = nPersonasArribadas + 1
    
            if np.sum(serversOcupados) <  s: # no hay nadie en la cola y hay por lo menos un server desocpuado ==> arribado va a un server
                serversOcupados, tServiciosServers = asignarPersonaASever(serversOcupados, tServicioServers, tTicks[i])
                
            else : # arribado va a la cola
                nCola, cabeceraCola = agregarPersonaACola(nCola, cabeceraCola, nPersonasArribadas)
         
            # generar aleatoriamente el tiempo del proximo arribo
            tProximoArribo = tTicks[i] + generarTiempoArribo()
    
        elif evento == 'servicio':
            # Decrementar numero de personas en el sistema
            nPersonas[i] = nPersonas[i-1] - 1
            
            # Desocupar el server donde ocurrio el servicio
            serversOcupados[serverCompletaServicio] = 0
            tServicioServers[serverCompletaServicio] = np.inf
    
            if nCola >= 1: # hay personas en la cola ==> head va a un server y sacamos una persona de la cola
                serversOcupados, tServicioServers = asignarPersonaASever(serversOcupados, tServicioServers, tTicks[i])
                nCola, cabeceraCola = sacarPersonaACola(nCola, cabeceraCola)
        
        # Determinar cual sera el proximo evento
        tProximoServicio = np.min(tServicioServers)
        if tProximoArribo <= tProximoServicio:
            proximoEvento = 'arribo'
            tProximoEvento = tProximoArribo
        else:
            proximoEvento = 'servicio'
            tProximoEvento = tProximoServicio
            serverCompletaServicio = np.argmin(tServicioServers)
    
        # Terminar la simuulacion si llegamos al tiempo T
        if tTicks[i] > T:
            nSim = i
            nPersonas = nPersonas[0:nSim]
            tTicks = tTicks[0:nSim]
            break
    
    # Calcular el numero promedio de personas en el sistema y en la cola
    nPersonasCola = np.maximum(nPersonas - s, 0)
    L  = (1/T) * np.sum(nPersonas[:-1] * np.diff(tTicks))
    Lq = (1/T) * np.sum(nPersonasCola[:-1] * np.diff(tTicks))
    
    # print('L = ' + str(L))
    # print('Lq = ' + str(Lq))
    # print('')

    # Graficar canLtidad de personas en el sitema vs. tiempo
    plt.figure()
    plt.bar(tTicks,nPersonas)
    plt.xlabel('Tiempo')
    plt.ylabel('Numero de personas')
    plt.show()
    
    return L, Lq
    
def monteCarlo(N, s):
    L_sim = np.zeros(N)
    Lq_sim = np.zeros(N)
    for j in range(N):
        L_sim[j], Lq_sim[j] = sim(s)
    
    # print(L_sim)
    # print(Lq_sim)
    # print('')
    
    L_mc = np.mean(L_sim)
    Lq_mc = np.mean(Lq_sim)
    
    print(L_mc)
    print(Lq_mc)
    
    return L_mc, Lq_mc

L_mc, Lq_mc = monteCarlo(N = 100, s = 1)


    







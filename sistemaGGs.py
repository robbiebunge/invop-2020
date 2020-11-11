import numpy as np 
import matplotlib.pyplot as plt

# Definir la semilla 
np.random.seed(0)

# Definir funcion auxiliar para generar eventos discretos
def generarEventoDiscreto(probOutcomes):
    x = np.random.uniform()
    intervalosDeProb = np.cumsum(probOutcomes[:,1])
    filaOutcome = np.digitize(x, intervalosDeProb)
    outcome = probOutcomes[filaOutcome, 0]
    return outcome


# Definir parametros del sistema
s = 2
probArribos =  np.array([[1, 0.2],
                [2, 0.3],
                [3, 0.35],
                [4, 0.15]])

probServicios =  np.array([[1, 0.35],
              [2, 0.40], 
              [3, 0.25]])

def generarTiempoArribo():
	Tarribo = generarEventoDiscreto(probArribos)
	return Tarribo

def generarTiempoServicio():
	Tservicio = generarEventoDiscreto(probServicios)
	return Tservicio

# Definir parametros de la simulacion
T = 400
nSim = 200

# Crear variables necesarias
tTicks = np.zeros(nSim)
nPersonas = np.zeros(nSim)
serversOcupados = np.zeros(s)

# Inicializar sistema
nPersonas[0] = 0
cabeceraCola = 0
nCola = 0
proximoEvento = 'arribo'
tProximoEvento = generarEventoDiscreto(probArribos)
nPersonasArribadas = 0
serverServicio = 0
tServicioServers = np.zeros(s)
tServicioServers[:] = np.inf

# Definir funciones auxiliares
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
    jServersDesocupados = np.argwhere(serversOcupados == 0)
    nServersDesocupados = np.sum(serversOcupados == 0)
    serverAOcupar = np.random.randint(nServersDesocupados)
    serverAOcupar = jServersDesocupados[serverAOcupar]
    serversOcupados[serverAOcupar] = 1
    tServicioServers[serverAOcupar] = ti + generarTiempoServicio()

    return serversOcupados, tServicioServers

# Correr la simulacion
for i in range(1, nSim):

    evento = proximoEvento
    tTicks[i] = tProximoEvento 

    # Procesar evento
    if evento == 'arribo':
        # Incrementar el numero de personas en el sistema y numero de personas arribadas
        nPersonas[i] = nPersonas[i-1] + 1
        nPersonasArribadas = nPersonasArribadas + 1

        if np.sum(serversOcupados) <  s: # no hay nadie en la cola y hay por lo menos un server desocpuado ==> arribado va a un server
            serversOcupados, tServiciosServers = asignarPersonaASever(serversOcupados, tServicioServers, tTicks[i])
            
        else : # arribado va a la cola
            nCola, cabeceraCola = agregarPersonaACola(nCola, cabeceraCola, nPersonasArribadas)
     
        # generar el tiempo del proximo arribo
        tProximoArribo = tTicks[i] + generarTiempoArribo()

    elif evento == 'servicio':
        # Decrementar numero de personas en el sistema
        nPersonas[i] = nPersonas[i-1] - 1
        
        # Desocupar el server donde ocurrio el servicio
        serversOcupados[serverCompletaServicio] = 0
        tServiciosServers[serverCompletaServicio] = np.inf

        if nCola >= 1: # hay personas en la cola ==> head va a un server y sacamos una persona de la cola
            serversOcupados, tServiciosServers = asignarPersonaASever(serversOcupados, tServicioServers, tTicks[i])
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
L  = (1/T) * np.sum(nPersonas[0:-1] * np.diff(tTicks))
Lq = (1/T) * np.sum(nPersonasCola[0:-1] * np.diff(tTicks))

print('L = ' + str(L))
print('Lq = ' + str(Lq))

plt.figure()
plt.bar(tTicks,nPersonas)
plt.xlabel('Tiempo (min)')
plt.ylabel('Numero de personas')
plt.show()
    







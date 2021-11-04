import numpy as np 
import matplotlib.pyplot as plt
import math

# 1. Definir parametros del sistema
landa = 5
mu = 40

# 2. Definir parametros de la simulación
T = 1
dt = 0.01/60
nSim = int(T/dt)

# 3. Crear arrays de la simulación
nPersonas = np.zeros(nSim) 
eventoArribo = [False] * nSim
eventoServicio = [False] * nSim
t = np.arange(0, T, dt)

# 4. Definir el estado inicial del sistema
nPersonasInicial = 0
nPersonas[0] = nPersonasInicial

# 5. Simular la evolucion del sistema
for i in range(nSim-1):

	#5.a Generar eventos aleatorios
	# Eventos de arribo con probabilidad exponencial
	probArrival = 1 - math.exp(-landa*dt)
	x = np.random.uniform()
	if x <= probArrival:
		eventoArribo[i] = True
	else:
		eventoArribo[i] = False

	# Eventos de servicio con probabilidad exponencial
	if 0 < nPersonas[i]: 
		probServicio = 1 - math.exp(-mu*dt) 
		x = np.random.uniform()
		if x <= probServicio:
			eventoServicio[i] = True
		else:
			eventoServicio[i] = False

	#5.b Computar el estado en el tick siguiente, en base al estado actual y los eventos
	nPersonas[i+1] = nPersonas[i] + 1*eventoArribo[i] - 1*eventoServicio[i]

	#5.c Chequear si hay que terminar la simulación 
	# No hay condición de terminación en esta simulación

#6. Computar variables de interes derivadas del estado
serverOcupado = nPersonas > 0
nPersonasCola = np.maximum(nPersonas - 1,0)
promedioPersonas = np.mean(nPersonas)
promedioPersonasCola = np.mean(nPersonasCola)
faccionTiempoServerOcupado = np.sum(serverOcupado*dt)/T
print('Promedio de personas en el sistema = ' + str(promedioPersonas))
print('Promedio de personas en la cola = ' + str(promedioPersonasCola))
print('Fracción de tiempo server ccupado = ' + str(faccionTiempoServerOcupado))

#7. Graficar resultados 
# Graficar evolucion del sistema y eventos
plt.figure()
f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
ax1.plot(t*60, nPersonas, label = '# personas en el sistema')
ax1.plot(t*60, nPersonasCola, label = '# personas en la cola')
ax1.set_title('Numero de Personas en el Sistema')
ax1.legend()

ax2.plot(t*60, eventoArribo, 'o-', label = 'Arribo')
ax2.plot(t*60, eventoServicio, 'o-', label = 'Servicio')
ax2.set_yticks([0, 1])
ax2.set_title('Eventos de Arribo y Servicio')
ax2.legend()

ax3.plot(t*60, serverOcupado, label = 'Server Ocupado')
ax3.set_yticks([0, 1])
ax3.set_xlabel('Tiempo (min)')
ax3.legend()
ax3.set_title('Server Ocupado?')
plt.show()




















	
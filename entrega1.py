from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

from simpleai.search.viewers import WebViewer, BaseViewer

from simpleai.search.traditional import astar


#CAMIONES = []
#PAQUETES = []
COMBUSTIBLE = ['rafaela', 'santa_fe']


CONECTADAS = {
    'sunchales': [('lehmann', 32)],
    'lehmann': [('rafaela', 8), ('sunchales', 32)],
    'rafaela': [('susana', 10), ('esperanza', 70), ('lehmann', 8)],
    'susana': [('angelica', 25), ('rafaela', 10)],
    'esperanza': [('recreo', 20), ('rafaela', 70)],
    'recreo': [('santa_fe', 10), ('esperanza', 20)],
    'santa_fe': [('santo_tome', 5), ('recreo', 10)],
    'santo_tome': [('angelica', 85), ('sauce_viejo', 15), ('santa_fe', 5)],
    'sauce_viejo': [('santo_tome', 15)],
    'san_vicente': [('angelica', 18)],
    'sc_de_saguier': [('angelica', 60)],
    'angelica': [('san_vicente', 18), ('sc_de_saguier', 60), ('susana', 25), ('santo_tome', 85)],
}


class tp_iaProblem(SearchProblem):
    
    def cost(self,state1,action,state2):
        camiones1, paquetes1 = state1
        camiones1 = []
        if isinstance(state1[0][0], str):
            camiones1.append(state1[0])
        else:
            for camon in state1[0]:
                camiones1.append(camon)

        costo = 0

        for index, camion in enumerate(camiones1):
            if index == action[0]:
                for ciudad in CONECTADAS[camion[0]]:
                    if ciudad[0] == action[1]:
                        costo = camion[1] - round((ciudad[1]/100),2)
        
        return costo
    
    def is_goal(self,state):
        camiones_estado, paquetes_estado = state
        lista = []
        if len(paquetes_estado) != 0:
            return False

        for cam in camiones_estado:
            lista.append(cam)

        for camion in lista:
            if camion[0] not in COMBUSTIBLE or len(camion[2]) != 0:
                return False

        return True
    
    def actions(self,state):
        acciones_posibles = []
        camiones = []
        paquetes = []
        if isinstance(state[0][0], str):
            camiones.append(state[0])
        else:
            for camon in state[0]:
                camiones.append(camon)

        paquetes.append(state[1])
        lista_ciudades = []
        for index,  camion in enumerate(camiones):
            lista_ciudades = CONECTADAS[camion[0]]
            for ciudad in lista_ciudades:
                nafta = round((ciudad[1]/100),2)
                if (camion[1] >= nafta):
                    acciones_posibles.append((index, ciudad[0]))
        return acciones_posibles    
            
    
    def result(self, state, action):
        camiones_estado, paquetes_estado = state
        camiones_estado = []
        paquetes_estado = list(paquetes_estado)
        if isinstance(state[0][0], str):
            camiones_estado.append(state[0])
        else:
            for camon in state[0]:
                camiones_estado.append(camon)
        nafta = 0
        ciudad_destino = action[1]
        camion_estado = list(camiones_estado[action[0]])
        caracteristicas_camion = CAMIONES[action[0]]
        if camion_estado[0] == 'rafaela' or camion_estado[0] == 'santa_fe':
            camion_estado[1] = caracteristicas_camion[2]
        else:
            for destino in CONECTADAS[camion_estado[0]]:
                if destino[0] == ciudad_destino:
                    nafta = round((destino[1]/100),2)
        
        
        for index_paq, paq in enumerate(PAQUETES):
            for paquete in paquetes_estado:
                if paquete == index_paq and camion_estado[0] == paq[1]:
                    camion_estado[2] = list(camion_estado[2])
                    camion_estado[2].append(paquete)
                    camion_estado[2] = tuple(camion_estado[2])

        for paq in camion_estado[2]:
            for paq2 in paquetes_estado:
                if paq == paq2:
                    paquetes_estado.remove(paq)

        if len(camion_estado[2]) != 0:
            for paquete in camion_estado[2]:
                for index_paq, paq in enumerate(PAQUETES):
                    if index_paq == paquete:
                        camion_estado[2] = list(camion_estado[2])
                        camion_estado[2].remove(index_paq)
                        camion_estado[2] = tuple(camion_estado[2])
        camion_estado[1] -= nafta
        camion_estado[0] = ciudad_destino
        camiones_estado[action[0]] = tuple(camion_estado)
        state = (tuple(camiones_estado), tuple(paquetes_estado))
        print(state)
        return state


    def heuristic (self, state):
        camiones, paquetes = state
        return len(paquetes)
        #return 0.1
    

def planear_camiones (metodo, camiones, paquetes):
    lista = []
    for camion in camiones:
        lista.extend(((camion[1], camion[2]), ())) 

    lista2 = []
    for index, paquete in enumerate(paquetes):
        lista2.append(index)

    INITIAL_STATE = (tuple(lista), tuple(lista2))

    global CAMIONES
    CAMIONES =  list(camiones)
    global PAQUETES 
    PAQUETES = list(paquetes)

    problem = tp_iaProblem(INITIAL_STATE)


    METODOS = {
        'breadth_first': breadth_first,
        'depth_first': depth_first,
        'iterative_limited_depth_first': iterative_limited_depth_first,
        'uniform_cost': uniform_cost,
        'astar': astar,
    }

    result = METODOS[metodo](problem)

    itinerario = []
    nasta = 0

    for action, state in result.path():
        camiones_estado, paquetes_estado = state
        index_camion_action, ciudad_destino = action
        lista_paquetes = []
        
        ciudad = camiones_estado[index_camion_action][0]
        camion = camiones[index_camion_action][0]
        lista_paquetes = camiones_estado[index_camion_action][2]
        for index, camon in enumerate(camiones_estado):
            if index == action[0]:
                for ciudad in CONECTADAS[camon[0]]:
                    if ciudad[0] == action[1]:
                        nasta = camon[1] - round((ciudad[1]/100),2)

        itinerario.append((camion, ciudad, nasta, list(lista_paquetes)))

    return itinerario

'''
if __name__ == '__main__':
    
    
    camiones=[
        # id, ciudad de origen, y capacidad de combustible máxima (litros)
        ('c1', 'rafaela', 1.5),
        ('c2', 'rafaela', 2),
        ('c3', 'santa_fe', 2),
    ]

    paquetes=[
        # id, ciudad de origen, y ciudad de destino
        ('p1', 'rafaela', 'angelica'),
        ('p2', 'rafaela', 'santa_fe'),
        ('p3', 'esperanza', 'susana'),
        ('p4', 'recreo', 'san_vicente'),
    ]

    itinerario = planear_camiones(
        # método de búsqueda a utilizar. Puede ser: astar, breadth_first, depth_first, uniform_cost o greedy
        breadth_first,camiones,paquetes
    )

    print(itinerario)
'''




    


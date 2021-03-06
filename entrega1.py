from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

from simpleai.search.viewers import WebViewer, BaseViewer

from simpleai.search.traditional import astar

import time



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
        
        return action[2]
    
    def is_goal(self,state):
        camiones_estado, paquetes_estado = state
        lista = []
        if len(paquetes_estado) != 0:
            return False

        for cam in camiones_estado:
            lista.append(cam)

        for camion in lista:
            if camion[0] not in COMBUSTIBLE or len(camion[2]) != 0:
                if camion[0] in COMBUSTIBLE:
                    for paquete_camion in camion[2]:
                        if PAQUETES[paquete_camion][2] != camion[0]: 
                            return False
                else:
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
                nafta_camion = round(camion[1], 2)
                if (nafta_camion >= nafta):
                    acciones_posibles.append((index, ciudad[0], nafta))
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

        nafta_camion = round(camion_estado[1])
        if nafta_camion >= nafta: 
            nafta = action[2]
        
        
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
                    if index_paq == paquete and paq[2] == camion_estado[0]:
                        camion_estado[2] = list(camion_estado[2])
                        camion_estado[2].remove(index_paq)
                        camion_estado[2] = tuple(camion_estado[2])
        camion_estado[1] = round((camion_estado[1] - nafta), 2)
        camion_estado[0] = ciudad_destino
        #print(camion_estado[1])
        camiones_estado[action[0]] = tuple(camion_estado)
        state = (tuple(camiones_estado), tuple(paquetes_estado))
        return state


    def heuristic (self, state):
        camiones, paquetes = state
        lista_paquetes = []
        heuristica = 0
        if len(paquetes) != 0:
            for index, paquete in enumerate(PAQUETES):
                for paq in paquetes:
                    if paq == index:
                        lista_paquetes.append(paquete[2])
        for camion in camiones:
            if len(camion[2]) != 0:
                for index, paquete in enumerate(PAQUETES):
                    for paq in camion[2]:
                        if paq == index:
                            lista_paquetes.append(paquete[2])
        lista_paquetes = set(lista_paquetes)
        heuristica = round((len(lista_paquetes)/12.5), 2)

        return heuristica



def planear_camiones (metodo, camiones, paquetes):
    lista = []
    for camion in camiones:
        lista.append((camion[1], camion[2], ())) 

    lista2 = []
    for index, paquete in enumerate(paquetes):
        lista2.append(index)

    INITIAL_STATE = (tuple(lista), tuple(lista2))
    print(INITIAL_STATE)
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
    

    for action, state in result.path():
        nasta = 0
        if action is not None:
            camiones_estado, paquetes_estado = state
            index_camion_action, ciudad_destino, nafta = action
            
            lista_paquetes = []
            c = camiones_estado[index_camion_action][1]
            ciudad = camiones_estado[index_camion_action][0]
            camion = camiones[index_camion_action][0]
            for indep, paq in enumerate(PAQUETES):
                for paquete in camiones_estado[index_camion_action][2]:
                    if indep == paquete:
                        lista_paquetes.append(paq[0])
            camiones_estado = list(camiones_estado)
            itinerario.append((camion, ciudad, round(nafta, 2), list(lista_paquetes)))
    return itinerario


if __name__ == '__main__':
    #start_time = time.time()
    '''
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

    '''

    camiones=[
        # id, ciudad de origen, y capacidad de combustible máxima (litros)
        ('c1', 'rafaela', 1.5),
    ]

    paquetes=[
        # id, ciudad de origen, y ciudad de destino
        ('p1', 'rafaela', 'lehmann'),
        ('p2', 'lehmann', 'rafaela'),
        ('p3', 'esperanza', 'susana'),
       #('p4', 'recreo', 'san_vicente'),
        #('p5', 'esperanza', 'santa_fe'),
        #('p4', 'santa_fe', 'san_vicente'),
    ]
    
    itinerario = planear_camiones(
        # método de búsqueda a utilizar. Puede ser: astar, breadth_first, depth_first, uniform_cost o greedy
        'astar',camiones,paquetes
    )

    print(itinerario)




    


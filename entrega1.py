from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    iterative_limited_depth_first,
    uniform_cost,
)

from simpleai.search.viewers import WebViewer, BaseViewer

CAMIONES = [
    ('c1', 'rafaela', 1.5),
    ('c2', 'rafaela', 2),
    ('c3', 'santa_fe', 2),
    ]
PAQUETES = [
    ('p1', 'rafaela', 'angelica'),
    ('p2', 'rafaela', 'santa_fe'),
    ('p3', 'esperanza', 'susana'),
    ('p4', 'recreo', 'san_vicente'),
]

INITIAL_STATE = ((('sunchales',1.5,()), ('sunchales',2,()), ('rafaela',2, ())), ('p1', 'p2', 'p3', 'p4'))

CONECTADAS = {
    'sunchales': [('lehmann', 32)],
    'lehmann': [('rafaela', 8), ('sunchales', 32)],
    'rafaela': [('susana', 10), ('esperanza', 70), ('lehmann', 8)],
    'susana': [('angelica', 25), ('rafaela', 10)],
    'angelica': [('san_vicente', 18), ('sc_de_saguier', 60), ('susana', 25)],
    'esperanza': [('recreo', 20), ('rafaela', 70)],
    'recreo': [('santa_fe', 10), ('esperanza', 20)],
    'santa_fe': [('santo_tome', 5), ('recreo', 10)],
    'santo_tome': [('angelica', 85), ('sauce_viejo', 15), ('santa_fe', 5)],
    'sauce_viejo': [('santo_tome', 15)],
    'san_vicente': [('angelica', 18)],
    'sc_de_saguier': [('angelica', 60)],
    'angelica': [('san_vicente', 18), ('sc_de_saguier', 60), ('susana', 25), ('santo_tome', 85)],
}

def planear_camiones (metodo, camiones, paquetes):
    lista = []
    for camion in camiones:
        lista.append((camion[1], camion[2]), ()) 

    lista2 = []
    for index, paquete in enumerate(paquetes):
        lista2.append(index)

    INITIAL_STATE = (tuple(lista), tuple(lista2))

    CAMIONES = camiones
    PAQUETES = paquetes


class tp_iaProblem(SearchProblem):
    
    def cost(self,state1,action,state2):
        camiones1, paquetes1 = state1
        camiones2, paquetes2 = state2
        costo = 0
        nafta_origen = 0
        nafta_destino = 0

        for index_2, camion2 in enumerate(camiones2):
            if camiones2[index_2] == action[0]:
                nafta_destino = camion2[2]
                for index_1, camion1 in enumerate(camiones1):
                    if index_1 == index_2:
                        nafta_origen = camion1[2]
        
        costo = nafta_origen - nafta_destino
        return costo
    
    def is_goal(self,state):
        camiones, paquetes = state
        camiones = list(camiones)
        paquetes = list(paquetes)
        return (set(camiones[0]) == ('rafaela', 'santa_fe') or set(camiones[0]) == ('santa_fe', 'rafaela')) and len(paquetes) == 0
    
    def actions(self,state):
        acciones_posibles = []
        camiones, paquetes = state

        for index,  camion in enumerate(camiones):
            for ciudad in CONECTADAS[camion[0]]:
                nafta = ciudad[1]/100
                if (camion[1] >= nafta):
                    acciones_posibles.append((index, ciudad[0]))
        return acciones_posibles    
            
    
    def result(self, state, action):
        camiones_estado, paquetes_estado = state
        camiones_estado = list(camiones_estado)
        paquetes_estado = list(paquetes_estado)
        nafta = 0
        
        for index, camion in enumerate(CAMIONES):
            if index == action[0]:
                camion_estado = list(camiones_estado[index])
                if action[1] == 'rafaela' or action[1] == 'santa_fe':
                    camiones_estado[index][1] = camiones[index][2]
                else:
                    for destino in CONECTADAS[camion_estado[0]]:
                        if destino[0] == action[1]:
                            nafta = destino[1]/100
                    camion_estado[1] -= nafta
                for paquete in paquetes_estado:
                    for index_paq, paq in enumerate(PAQUETES):
                        if paquete == index_paq and camion_estado[0] in paq[1]:
                            paquetes_estado.remove(paq)
                            camion_estado[2] = list(camion_estado[2])
                            camion_estado[2].append(paquete)
                            camion_estado[2] = tuple(camion_estado[2])

                        if paquete == index_paq and camion_estado[0] in paq[2]:
                            camion_estado[2] = list(camion_estado[2])
                            camion_estado[2].remove(paquete)
                            camion_estado[2] = tuple(camion_estado[2])
                camiones_estado[index] = tuple(camion_estado)
        state = (tuple(camiones_estado), tuple(paquetes_estado))

        return tuple(state)

    def heuristic (self, state):
        camiones, paquetes = state
        return len(paquetes)
    
    
    
metodos = (
    #breadth_first,
    #depth_first,
    #iterative_limited_depth_first,
    uniform_cost,
)    
        
for metodo_busqueda in metodos:
    print()
    print('=' * 50)
    print("corriendo:", metodo_busqueda)
    visor = BaseViewer()
    problem = tp_iaProblem(INITIAL_STATE)
    result = metodo_busqueda(problem, graph_search = True, viewer = visor)
    print ('estado final:')
    print(result.state)

    print('-' * 50)

    print('estadísticas:')
    print('cantidad de acciones hasta la meta:', len(result.path()))
    print(visor.stats)

    for action,state in result.path():
        print('accion:', action)
        print('estado resultante:', state)

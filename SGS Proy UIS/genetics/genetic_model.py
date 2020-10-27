
# Indice exito


# La selección -> La regla a definir

    resources = Resources(10,10,5)

    activities.append(Activity(1,  0,  0, [0],           Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(2,  0,  0, [1],           Resources(5,0,0),     False, False, False, 0))
    activities.append(Activity(3,  0,  0, [1],           Resources(0,0,5),     False, False, False, 0))
    activities.append(Activity(4,  4,  0, [1],           Resources(2,0,5),     False, False, False, 0))
    activities.append(Activity(5,  6,  0, [2,3,4],       Resources(8,0,0),     False, False, False, 0))
    activities.append(Activity(6,  7,  0, [5],           Resources(5,0,0),     False, False, False, 0))
    activities.append(Activity(7,  0,  0, [1],           Resources(4,0,0),     False, False, False, 0))
    activities.append(Activity(8,  8,  0, [6,7],         Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(9,  10, 0, [8],           Resources(0,0,0),     False, False, False, 0))
    activities.append(Activity(10, 28, 0, [9],           Resources(0,10,0),    False, False, False, 0))
    activities.append(Activity(11, 30, 0, [9],           Resources(0,10,0),    False, False, False, 0))

    # 1) w3 + 0 = y

    # 1. Inicia la actividad 1
    # 2. Se identifican las actividades a programar -> 2,3,4,7
    # 2.1. Evaular los recursos con sus combinaciones.
    # Caso 1 -> Se escoge la 2, sí tiene recursos suficientes. (En caso práctico se escogen aleatoriamente) -> Se puede algo más eficiente
    #  - Según los recursos ambas se pueden programar.
    #  - Fitness


    # La función de selección debe retornar un valor entre 1 y el número de actividades disponibles (n), 1.

# La mutación -> 0% - 1% (LFT)
# La repoducción -> Se escojen muestras del modelo de selección. (Perceptrones)
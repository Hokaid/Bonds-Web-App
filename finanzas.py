def calbonos(parametros):
    resultado = []
    resultado.append(2)
    resultado.append(5)
    resultado.append(5)
    resultado.append(6)
    resultado.append(4)
    resultado.append(1000)
    resultado.append(500)
    resultado.append(700)
    resultado.append(400)
    resultado.append(60)
    resultado.append(2000)
    resultado.append(600)
    resultado.append(320)
    resultado.append(560)
    resultado.append(430)
    flujo = []
    for i in range(5):
        renta = []
        renta.append(i+1)
        renta.append('2020-01-01')
        renta.append(30)
        renta.append(0.05)
        renta.append(0)
        renta.append(1000)
        renta.append(-1000)
        renta.append(-2000)
        renta.append(-500)
        renta.append(0)
        renta.append(12.5)
        renta.append(-50.5)
        renta.append(-50.5)
        renta.append(50.5)
        flujo.append(renta)
    resultado.append(flujo)
    return resultado


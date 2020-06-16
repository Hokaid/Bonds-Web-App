from datetime import timedelta
from datetime import datetime
import numpy_financial as npf
from scipy import optimize

def xnpv(rate, cashflows):
  return sum([cf/(1+rate)**((t-cashflows[0][0]).days/365.0) for (t,cf) in cashflows])
 
def xirr(cashflows, guess=0.1):
  try:
    return optimize.newton(lambda r: xnpv(r,cashflows),guess)
  except:
    print("Wrong Calc")

def calbonos(mcalculo,vnominal,vcomercial,nanos,fpago,dxano,ttasa,capi,tinteres,tdesc,irenta,femision,prima,estruc,coloc,flota,cavali):
  fcupon = 360
  if fpago == "Diaria": fcupon = 1
  if fpago == "Quincenal": fcupon = 15
  if fpago == "Mensual": fcupon = 30
  if fpago == "Bimestral": fcupon = 60
  if fpago == "Trimestral": fcupon = 90
  if fpago == "Cuatrimestral": fcupon = 120
  if fpago == "Semestral": fcupon = 180
  if fpago == "Anual": fcupon = 360
  dcapi = 360
  if capi == "Diaria": dcapi = 1
  if capi == "Quincenal": dcapi = 15
  if capi == "Mensual": dcapi = 30
  if capi == "Bimestral": dcapi = 60
  if capi == "Trimestral": dcapi = 90
  if capi == "Cuatrimestral": dcapi = 120
  if capi == "Semestral": dcapi = 180
  if capi == "Anual": dcapi = 360
  npano = 360/fcupon
  ntp = int(npano*nanos)
  tea =  tinteres
  if ttasa == "Nominal": tea = ((1+(tinteres/(dxano/dcapi)))**(dxano/dcapi))-1
  tep = ((1+tea)**(fcupon/dxano))-1
  cok = ((1+tdesc)**(fcupon/dxano))-1
  ciemisor = vcomercial*(estruc+coloc+flota+cavali)
  cibonista = vcomercial*(flota+cavali)
  flujo = [["" for i in range(14)] for i in range(ntp+1)]
  fechaemi = datetime.strptime(femision, '%d/%m/%Y')
  for i in range(ntp+1):
    flujo[i][0] = i #Numero
    fechrent = fechaemi + timedelta(days=fcupon*i)
    flujo[i][1] = fechrent.strftime('%d/%m/%Y') #Fecha
    if (i > 0):
      flujo[i][2] = 0 #Inflación anual
      flujo[i][3] = 0 #Inflación periodo
      flujo[i][4] = 'S' #Plazo de gracia
      if mcalculo == "Americano":
        flujo[i][5] = vnominal #Bono
        flujo[i][6] = -1*tep*flujo[i][5] #Cupon
        if (i == ntp):flujo[i][8] = -1*vnominal #Amoritización
        else: flujo[i][8] = 0
        flujo[i][7] = flujo[i][8] + flujo[i][6] #Cuota
      elif mcalculo == "Aleman":
        flujo[i][8] = vnominal/ntp
        flujo[i][5] = vnominal - (flujo[i][8]*(i-1))
        flujo[i][6] = -1*tep*flujo[i][5] #Cupon
        flujo[i][7] = (-1*flujo[i][8]) + flujo[i][6] #Cuota
      elif mcalculo == "Frances":
        if i == 1: flujo[i][5] = vnominal
        else: flujo[i][5] = flujo[i-1][5] + flujo[i-1][8]
        flujo[i][6] = -1*tep*flujo[i][5] #Cupon
        flujo[i][7] = -1*(vnominal*((tep*((1+tep)**ntp))/(((1+tep)**ntp)-1))) #Cuota
        flujo[i][8] = flujo[i][7] - flujo[i][6]
      if (i == ntp):flujo[i][9] = -1*vnominal*prima #Prima
      else: flujo[i][9] = 0
      flujo[i][10] = -1*irenta*flujo[i][6] #Escudo
      if (i == ntp): flujo[i][11] = (-1*flujo[i][5])+flujo[i][6]+flujo[i][9] #Flujo Emisor
      else: flujo[i][11] = flujo[i][7] #Flujo Emisor
      flujo[i][12] = flujo[i][10]+flujo[i][11] #Flujo Emisor c/ Escudo
      flujo[i][13] = flujo[i][11]*-1 #Flujo Bonista
    if (i == 0):
      flujo[i][11] = vcomercial - ciemisor
      flujo[i][12] = flujo[i][11]
      flujo[i][13] = (-1*vcomercial) - cibonista
  fluemi = []
  fluemice = []
  fluboni = []
  xfluemi = []
  xfluemice = []
  xfluboni = []
  for i in range(ntp+1):
    fluemi.append(flujo[i][11])
    fluemice.append(flujo[i][12])
    fluboni.append(flujo[i][13])
    xfluemi.append((datetime.strptime(flujo[i][1], '%d/%m/%Y'),flujo[i][11]))
    xfluemice.append((datetime.strptime(flujo[i][1], '%d/%m/%Y'),flujo[i][12]))
    xfluboni.append((datetime.strptime(flujo[i][1], '%d/%m/%Y'),flujo[i][13]))
  pactual = npf.npv(cok,fluboni) - flujo[0][13] 
  vna = npf.npv(cok,fluboni)
  tceaemi = ((npf.irr(fluemi)+1)**(dxano/fcupon))-1
  tceaemice = ((npf.irr(fluemice)+1)**(dxano/fcupon))-1
  treaboni = ((npf.irr(fluboni)+1)**(dxano/fcupon))-1
  tirremi = xirr(xfluemi)
  tirremice = xirr(xfluemice)
  tirrboni = xirr(xfluboni)
  return round(npano),round(ntp),round(tea*100,4),round(tep*100,3),round(cok*100,3),round(ciemisor,2),round(cibonista,2),round(tirremi*100,5),round(tirrboni*100,5),round(tirremice*100,5),round(pactual,2),round(vna,2),round(tceaemi*100,5),round(tceaemice*100,5),round(treaboni*100,5),flujo           

from datetime import timedelta
from datetime import datetime
import numpy as npf
from scipy import optimize

def xnpv(rate, cashflows):
  return sum([cf/(1+rate)**((t-cashflows[0][0]).days/365.0) for (t,cf) in cashflows])
 
def xirr(cashflows, guess=0.1):
  try:
    return optimize.newton(lambda r: xnpv(r,cashflows),guess)
  except:
    print("Wrong Calc")

def calbonos(mcalculo,infla,ianual,vnominal,vcomercial,nanos,fpago,dxano,ttasa,capi,pgracia,tinteres,tdesc,irenta,femision,prima,estruc,coloc,flota,cavali):
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
  flujo = [["" for i in range(15)] for i in range(ntp+1)]
  fechaemi = datetime.strptime(femision, '%d/%m/%Y')
  plazosg = pgracia.split(sep=',')
  for i in range(1, len(plazosg)+1):
    flujo[i][4] = plazosg[i-1] #Plazo de gracia
  for i in range(ntp+1):
    flujo[i][0] = i #Numero
    fechrent = fechaemi + timedelta(days=fcupon*i)
    flujo[i][1] = fechrent.strftime('%d/%m/%Y') #Fecha
    if (i > 0):
      if (infla == True): flujo[i][2] = ianual*100 #Inflación anual
      elif (infla == False): flujo[i][2] = 0 #Inflación anual
      flujo[i][3] = (((1+(flujo[i][2]/100))**(fcupon/dxano))-1)*100 #Inflación periodo
      if (flujo[i][4] != 'T' and flujo[i][4] != 'P'): flujo[i][4] = 'S' #Plazo de gracia
      if i == 1: flujo[i][5] = vnominal #Bono
      elif (flujo[i-1][4] == 'P' or flujo[i-1][4] == 'S'): flujo[i][5] = flujo[i-1][6] + flujo[i-1][9] #Bono
      elif (flujo[i-1][4] == 'T'): flujo[i][5] = flujo[i-1][6] - flujo[i-1][7]
      flujo[i][6] = flujo[i][5]*(1+(flujo[i][3]/100)) #Bono indexado
      flujo[i][7] = -1*tep*flujo[i][6] #Cupon
      if flujo[i][4] == 'S':
        if mcalculo == "Americano":
          if (i == ntp): flujo[i][9] = -1*flujo[i][6] #Amoritización
          else: flujo[i][9] = 0
          flujo[i][8] = flujo[i][9] + flujo[i][7] #Cuota
        elif mcalculo == "Aleman":
          flujo[i][9] = -1*flujo[i][6]/(ntp-i+1) #Amoritización
          flujo[i][8] = flujo[i][9] + flujo[i][7] #Cuota
        elif mcalculo == "Frances":
          flujo[i][8] = -1*(flujo[i][6]*((tep*((1+tep)**(ntp-i+1)))/(((1+tep)**(ntp-i+1))-1))) #Cuota
          flujo[i][9] = flujo[i][8] - flujo[i][7] #Amoritización
      elif flujo[i][4] == 'P':
        flujo[i][8] = flujo[i][7] #Cuota
        flujo[i][9] = 0 #Amoritización
      elif flujo[i][4] == 'T':
        flujo[i][8] = 0 #Cuota
        flujo[i][9] = 0 #Amoritización
      if (i == ntp): flujo[i][10] = -1*vnominal*prima #Prima
      else: flujo[i][10] = 0
      flujo[i][11] = -1*irenta*flujo[i][7] #Escudo
      if (i == ntp): flujo[i][12] = (-1*flujo[i][6])+flujo[i][7]+flujo[i][10] #Flujo Emisor
      else: flujo[i][12] = flujo[i][8] #Flujo Emisor
      flujo[i][13] = flujo[i][11]+flujo[i][12] #Flujo Emisor c/ Escudo
      flujo[i][14] = flujo[i][12]*-1 #Flujo Bonista
    if (i == 0):
      flujo[i][12] = vcomercial - ciemisor
      flujo[i][13] = flujo[i][12]
      flujo[i][14] = (-1*vcomercial) - cibonista
  fluemi = []
  fluemice = []
  fluboni = []
  xfluemi = []
  xfluemice = []
  xfluboni = []
  for i in range(ntp+1):
    fluemi.append(flujo[i][12])
    fluemice.append(flujo[i][13])
    fluboni.append(flujo[i][14])
    xfluemi.append((datetime.strptime(flujo[i][1], '%d/%m/%Y'),flujo[i][12]))
    xfluemice.append((datetime.strptime(flujo[i][1], '%d/%m/%Y'),flujo[i][13]))
    xfluboni.append((datetime.strptime(flujo[i][1], '%d/%m/%Y'),flujo[i][14]))
  pactual = npf.npv(cok,fluboni) - flujo[0][14] 
  vna = npf.npv(cok,fluboni)
  tceaemi = ((npf.irr(fluemi)+1)**(dxano/fcupon))-1
  tceaemice = ((npf.irr(fluemice)+1)**(dxano/fcupon))-1
  treaboni = ((npf.irr(fluboni)+1)**(dxano/fcupon))-1
  tirremi = npf.irr(fluemi) if (xirr(xfluemi) is None) else xirr(xfluemi)
  tirremice = npf.irr(fluemice) if (xirr(xfluemice) is None) else xirr(xfluemice)
  tirrboni = npf.irr(fluboni) if (xirr(xfluboni) is None) else xirr(xfluboni)
  return round(npano),round(ntp),round(tea*100,4),round(tep*100,3),round(cok*100,3),round(ciemisor,2),round(cibonista,2),round(tirremi*100,5),round(tirrboni*100,5),round(tirremice*100,5),round(pactual,2),round(vna,2),round(tceaemi*100,5),round(tceaemice*100,5),round(treaboni*100,5),flujo           

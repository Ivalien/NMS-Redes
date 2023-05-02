#!/usr/bin/python3.9
#
# Equipo 3

import os
import re
import csv
import time
import hashlib
import getpass
import argparse
from fpdf import FPDF
from datetime import date
from datetime import datetime
from netmiko import ConnectHandler

RED = "\033[0;31m"
BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
MAGENTA = '\033[38;5;127m'

banner = f"""{MAGENTA}

 ███▄    █ ▓█████▄▄▄█████▓▓█████  ▄████▄   ██░ ██ 
 ██ ▀█   █ ▓█   ▀▓  ██▒ ▓▒▓█   ▀ ▒██▀ ▀█  ▓██░ ██▒
▓██  ▀█ ██▒▒███  ▒ ▓██░ ▒░▒███   ▒▓█    ▄ ▒██▀▀██░
▓██▒  ▐▌██▒▒▓█  ▄░ ▓██▓ ░ ▒▓█  ▄ ▒▓▓▄ ▄██▒░▓█ ░██ 
▒██░   ▓██░░▒████▒ ▒██▒ ░ ░▒████▒▒ ▓███▀ ░░▓█▒░██▓
░ ▒░   ▒ ▒ ░░ ▒░ ░ ▒ ░░   ░░ ▒░ ░░ ░▒ ▒  ░ ▒ ░░▒░▒
░ ░░   ░ ▒░ ░ ░  ░   ░     ░ ░  ░  ░  ▒    ▒ ░▒░ ░
   ░   ░ ░    ░    ░         ░   ░         ░  ░░ ░
         ░    ░  ░           ░  ░░ ░       ░  ░  ░
                                 ░                

                Equipo 3: Advanced NMS

"""

################# Seccion de funciones ##############################################
####################### IPAM ##########################
def csvExporter(IPList1,IPList2, IPList3, IPList4, IPList5):
    IPList1.insert(0, 'Router 1:')
    IPList2.insert(0,'Router 2:')
    IPList3.insert(0, 'Router 3:')
    IPList4.insert(0, 'Router 4:')
    IPList5.insert(0, 'Router 5:')

    columnas = ['Dispositivo', 'Direcciones IP encontradas']

    with open("./ArchivosIPAM/DireccionesIPAM.csv", mode='w') as archivo:
        escritor_archivo = csv.writer(archivo, delimiter=',')
        escritor_archivo.writerow(columnas)
        escritor_archivo.writerow(IPList1)
        escritor_archivo.writerow(IPList2)
        escritor_archivo.writerow(IPList3)
        escritor_archivo.writerow(IPList4)
        escritor_archivo.writerow(IPList5)

    print("\n[*] Informacion exportada a csv con exito!")

def pdfExporter(router1, router2, router3, router4, router5):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 10, txt = "Direcciones IP encontradas", ln = 1, align = 'C')

    matriz = [ router1, router2, router3, router4, router5]

    for i in range(5):
        pdf.cell(0,20, txt = "Router " + str(i + 1) + ":", ln = 1)
        for x in matriz[i]:
            pdf.cell(200,5, txt = "    " + x, ln = 1)

    pdf.output("./ArchivosIPAM/ReporteIPAM.pdf")
    print("\n[*] Informacion exportada a PDF con exito!")

def ipValidator(lista):
    temp = []
    for i in range(len(lista)):
        temp_checker = lista[i].split('.')
        if('255' in temp_checker):
            continue
        elif('0.0' in lista[i]):
            continue
        else:
            temp.append(lista[i])
            print("  " + lista[i])

    return temp

def IPAM(router1, router2, router3, router4, router5):
    print("###################### Imprimiendo direcciones IP ########################\n")
    ## Aqui entramos al modo enable
    ######## Router 1 #########
    router1.enable()
    configRouter1 = router1.send_command('show run') 
    direccionesRouter1 = re.findall("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", configRouter1)
    print("Router 1: ")
    clean1 = ipValidator(direccionesRouter1)
    ######## Router 2 #########
    router2.enable()
    configRouter2 = router2.send_command('show run')
    direccionesRouter2 = re.findall("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", configRouter2)
    print("Router 2: ")
    clean2 = ipValidator(direccionesRouter2)
    ####### Router 3 ##########
    router3.enable()
    configRouter3 = router3.send_command('show run')
    direccionesRouter3 = re.findall("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", configRouter3)
    print("Router 3: ")
    clean3 = ipValidator(direccionesRouter3)
    ####### Router 4 ##########
    router4.enable()
    configRouter4 = router4.send_command('show run')
    direccionesRouter4 = re.findall("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", configRouter4)
    print("Router 4: ")
    clean4 = ipValidator(direccionesRouter4)
    ###### Router 5 ##########
    router5.enable()
    configRouter5 = router5.send_command('show run')
    direccionesRouter5 = re.findall("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", configRouter5)
    print("Router 5: ")
    clean5 = ipValidator(direccionesRouter5)

    ## Verificamos la ruta del directorio de archivos exportados del sistema IPAM
    if(os.path.exists('./ArchivosIPAM') == True):
        bait = 1
    elif(os.path.exists('./ArchivosIPAM') == False):
        os.system('mkdir ArchivosIPAM')
    menu_exportaciones = """
Metodos de exportacion:
1.- CSV
2.- PDF
3.- Ninguno
    """
    print(menu_exportaciones)
    opcion = int(input("\n[*] Digita la opcion para el metodo de exportacion a utilizar: "))
    if(opcion == 1):
        csvExporter(clean1, clean2, clean3, clean4, clean5)
    elif(opcion == 2):
        pdfExporter(clean1, clean2, clean3, clean4, clean5)
        return 0
    elif(opcion == 3):
        return 0
    
    return 0


########################### Configuration Manager #############################
def configurationManager(router1, router2, router3, router4, router5):
    ## Entramos al modo enable en todos los routers
    print("\n[*] Exportando las configuraciones a sus respectivas carpetas...")
    router1.enable()
    router2.enable()
    router3.enable()
    router4.enable()
    router5.enable()
    config1 = router1.send_command("show run")
    config2 = router2.send_command("show run")
    config3 = router3.send_command("show run")
    config4 = router4.send_command("show run")
    config5 = router5.send_command("show run")
    ## Verificacion y creacion de directorios por router
    for i in range(5):
        ruta = "Router" + str(i + 1)
        if(os.path.exists("./" + ruta) == True):
            bait = 1
        elif(os.path.exists("./" + ruta) == False):
            os.system("mkdir " + ruta)

    ## Matriz de configuraciones para iterar sobre las variables y ahorrar lineas de codigo
    configs = [ config1, config2, config3, config4, config5]

    ## Creacion y guardado de archivos
    for a in range(5):
        tiempo = datetime.now()
        archivo = "Router" + str(a + 1) + "-" + str(date.today()) + "-" + str(tiempo.strftime("%H:%M:%S")) + ".txt"
        f = open("./Router" + str(a + 1) + "/" + archivo, "w")
        f.write(configs[i])
        f.close()

    print("\n[*] Archivos exportados con exito!")

################################ Change Management ##################################
def lectorComandos():
    control = 0
    flag = 0
    print(menu_change3)
    while(flag == 0):
        opcion = int(input("\n[*] Digita la opcion que quieres utilizar: "))
        if(opcion == 1):
            ## Uno solo
            comando = str(input("\n[*] Digita el comando a ejecutar: "))
            control = 1
            return control,comando
            flag += 1
        elif(opcion == 2):
            ## Varios
            a = 0
            while(a == 0):
                archivo = str(input("\n[*] Digita la ruta del archivo en el que estan todos los comandos a ejecutar separados por un salto de linea: "))
                if(os.path.isfile(archivo) == True):
                    ## Abrimos y retornamos lista
                    comandos = [line.rstrip('\n') for line in open(archivo, "r")]
                    control = 2
                    return control,comandos
                    a += 1
                elif(os.path.isfile(archivo) == False):
                    print("\n[*] El archivo no existe, por favor revisa que la ruta sea correcta.")
                    continue
            flag += 1
        else:
            print("\n[*] Opcion invalida, por favor escoge una opcion correcta.")
            continue

def commandSender(router, comando):
    output = router.send_command(comando)
    if('Invalid' in output):
        print(RED + "\n[*] Comando " + str(comando) + " invalido, revisa la sintaxis" + BLUE)
    elif('Ambiguous' in output):
        print(RED + "\n[*] Comando " + str(comando) + " invalido, revisa la sintaxis" + BLUE)
    else:
        print(output + "\n")
        return 0

    return 0

def changeManagement(router1, router2, router3, router4, router5):
    flag = 0
    flag2 = 0
    while(flag == 0):
        print(menu_change1)
        while(flag2 == 0):
            opcion1 = int(input("\n[*] Digita la opcion que quieres utilizar: "))
            if(opcion1 == 1):
                ## Router especifico
                ## Retornar dos variables, una que diga si fueron varios o un comando nada mas y otra que tenga el o los comandos
                control,comando = lectorComandos()
                print(menu_change2)
                a = 0
                while(a == 0):
                    eleccion_router = int(input("\n[*] Elige a que router quieres mandar el comando: "))
                    if(eleccion_router <= 5 and eleccion_router > 0 and control == 1):
                        ## Mandamos comando
                        match eleccion_router:
                            case 1:
                                print("\nRouter 1: ")
                                commandSender(router1, comando)
                            case 2:
                                print("\nRouter 2: ")
                                commandSender(router2, comando)
                            case 3:
                                print("\nRouter 3: ")
                                commandSender(router3, comando)
                            case 4:
                                print("\nRouter 4: ")
                                commandSender(router4, comando)
                            case 5:
                                print("\nRouter 5: ")
                                commandSender(router5, comando)
                        a += 1
                    ## Mandamos varios comandos
                    elif(eleccion_router <= 5 and eleccion_router > 0 and control == 2):
                        match eleccion_router:
                            case 1:
                                print("\nRouter 1:")
                                for c in comando:
                                    commandSender(router1, c)
                            case 2:
                                print("\nRouter 2:")
                                for c in comando:
                                    commandSender(router2, c)
                            case 3:
                                print("\nRouter 3:")
                                for c in comando:
                                    commandSender(router3, c)
                            case 4:
                                print("\nRouter 4:")
                                for c in comando:
                                    commandSender(router4, c)
                            case 5:
                                print("\nRouter 5:")
                                for c in comando:
                                    commandSender(router5, c)
                        a += 1
                    else:
                        print("\n[*] Opcion invalida")
                        continue
                flag2 += 1
            elif(opcion1 == 2):
                control,comandos = lectorComandos()
                matriz = [ router1, router2, router3, router4, router5]
                ## Broadcast de routers
                if(control == 1):
                    print("\nRouter 1: ")
                    commandSender(router1, comandos)
                    print("\nRouter 2: ")
                    commandSender(router2, comandos)
                    print("\nRouter 3: ")
                    commandSender(router3, comandos)
                    print("\nRouter 4: ")
                    commandSender(router4, comandos)
                    print("\nRouter 5: ")
                    commandSender(router5, comandos)
                elif(control == 2):
                    for z in range(5):
                        print("\nRouter " + str(z + 1) + ":")
                        for c in comandos:
                            commandSender(matriz[z], c)
                flag2 += 1
            elif(opcion2 == 3):
                return 0
            else:
                print("\n[*] Opcion invalida, por favor escoge una opcion correcta.")
                continue
        opcion_retorno = int(input("\n\n[*] Quieres seguir mandando comandos o salir? (1:Continuar, 2:Salir): "))
        if(opcion_retorno == 1):
            flag2 = 0
            continue
        elif(opcion_retorno == 2):
            return 0
            flag = 1

    return 0

################################ Syslog #####################################
def logExporter(logs1, logs2, logs3, logs4, logs5):

    ## Creamos directorio para output del archivo csv y verificamos si existe
    if(os.path.exists('./SyslogExport') == True):
        bait = 1
    elif(os.path.exists('./SyslogExport') == False):
        os.system('mkdir SyslogExport')

    ## Regex que agarre los logs y que los separe en una lista solito
    listaLogs1 = re.findall('\*.+', logs1)
    listaLogs2 = re.findall('\*.+', logs2)
    listaLogs3 = re.findall('\*.+', logs3)
    listaLogs4 = re.findall('\*.+', logs4)
    listaLogs5 = re.findall('\*.+', logs5)
    ## Insertamos el nombre de los routers al principio de cada lista
    matriz_logger = [listaLogs1, listaLogs2, listaLogs3, listaLogs4, listaLogs5]
    for i in range(5):
        matriz_logger[i].insert(0, 'Router ' + str(i + 1) + ":")

    ## Creacion de archivo e insercion
    columnas = ['Dispositivo', 'Ultimos 5 logs']

    with open("./SyslogExport/RouterLogs.csv", mode='w') as archivo:
        escritor_archivo = csv.writer(archivo, delimiter=',')
        escritor_archivo.writerow(columnas)
        for i in range(5):
            escritor_archivo.writerow(matriz_logger[i])

    print("\n[*] Informacion exportada a csv con exito!")

    return 0

## Detector de logs de severidad alta
def detect_priority_log(texto):
    frases = re.findall(r'%[^:]+:', texto)
    numeros = []
    for elemento in frases:
        coincidencias = re.findall(r'\d+', str(elemento))
        numeros.extend(coincidencias)
    lista_numeros = list(map(float, numeros))
    for element in lista_numeros:
        ## Cambiamos numero para mostrar que funciona
        if isinstance(element, (int, float)) and element <= 3:
            return True
        return False

def logTail(router):
    ## Habilitamos modo enable
    router.enable()
    router.send_command('terminal shell')
    ## Obtenemos los ultimos 5 logs del router y retornamos texto
    logs = router.send_command('show logging | tail 5')
    return logs


def syslog(router1, router2, router3, router4, router5):
    ## Creamos una matriz con los objetos de los routers para iterar en ellos
    matriz_routers = [ router1, router2, router3, router4, router5]
    matrizLogs = []
    for i in range(5):
        print("Router " + str(i + 1) + ":")
        logs = logTail(matriz_routers[i])
        matrizLogs.append(logs)
        print(logs)
        severity = detect_priority_log(logs)
        if(severity == True):
            print(RED + "\n[*] Se encontraron logs con severidad alta!" + BLUE)
        elif(severity == False):
            continue

    logExporter(matrizLogs[0], matrizLogs[1], matrizLogs[2], matrizLogs[3], matrizLogs[4])

    return 0

menu_change1 = f"""{BLUE}

1.- Mandar un comando a un router en especifico
2.- Mandar un comando a todos los routers
3.- Salir
"""

menu_change2 = f"""{BLUE}

1.- Router1
2.- Router2
3.- Router3
4.- Router4
5.- Router5

"""

menu_change3 = f"""{BLUE}

1.- Mandar un solo comando
2.- Mandar varios comandos desde un archivo de texto

"""

## Menu de opciones
menu = f"""{BLUE}

1.- IPAM
2.- Configuration Manager
3.- Change Management
4.- Log Analyzer
5.- Compliance/Security Management
6.- Salir

"""

# Funcion de retorno a menu para seguir usando la herramienta sin tener que detener la ejecucion
def retorno_menu():
    while True:
        opcion = int(input("\n[*] Deseas terminar el programa o volver al menu principal? (1:Terminar,2:Volver): "))
        if(opcion == 1):
            print("[*] Hasta luego!!!")
            log_salida = "Salida de programa: " + str(datetime.now()) + "\n"
            init_log.write(log_salida)
            init_log.close()
            desconexion()
            return 1
            break
        elif(opcion == 2):
            return 2
            break
        else:
            print("Opcion incorrecta!\n\n")
            continue

# Main del programa

def main():
    while True:
        os.system("clear")
        print(banner)
        print(menu)
        opcion = int(input("\n[*] Digita la opcion de la herramienta a utilizar: "))
        ## IPAM
        if(opcion == 1):
            IPAM(BorderRouter, router2, router3, router4, router5)
            opcion_2 = retorno_menu()
            if(opcion_2 == 1):
                quit()
            elif(opcion_2 == 2):
                continue
        elif(opcion == 2):
            configurationManager(BorderRouter, router2, router3, router4, router5)
            opcion_2 = retorno_menu()
            if(opcion_2 == 1):
                quit()
            elif(opcion_2 == 2):
                continue
        elif(opcion == 3):
            changeManagement(BorderRouter, router2, router3, router4, router5)
            opcion_2 = retorno_menu()
            if(opcion_2 == 1):
                quit()
            elif(opcion_2 == 2):
                continue
        elif(opcion == 4):
            syslog(BorderRouter, router2, router3, router4, router5)
            opcion_2 = retorno_menu()
            if(opcion_2 == 1):
                quit()
            elif(opcion_2 == 2):
                continue
        elif(opcion == 6):
            print("\n[*] Hasta luego! :)")
            log_salida = "Salida de programa: " + str(datetime.now()) + "\n"
            init_log.write(log_salida)
            init_log.close()
            quit()
        else:
            print("\n[*] Opcion incorrecta, por favor escriba una opcion valida.")
            print("[*] Reimprimiendo el menu principal...")
            time.sleep(1)
            continue


################ Sistema de login ######################

'''
admin:admin
root:password
user:test
vim:google
'''

######## CALCULADO CON SHA256 ########

usuarios = {
            "admin" : "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",
            "root" : "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
            "user" : "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
            "vim" : "bbdefa2950f49882f295b1285d4fa9dec45fc4144bfb07ee6acc68762d12c2e3"
            }

## Parser de argumentos donde vamos a pasar la direccion IP del router conectado a nuestro host
parser = argparse.ArgumentParser(description='NMS Avanzado')
parser.add_argument('-ip', type=str, help='Direccion IP del router', required=True)
args = parser.parse_args()
## Inicio del programa con creacion de directorios para logs
os.system("clear")
print(banner)
os.system("mkdir -p Logs")
os.system("touch ./Logs/init.log")
os.system("touch ./Logs/auth.log")
## Logs de inicio de programa
init_log = open("./Logs/init.log", "a")
initLog_completo = "Inicializacion del programa: " + str(datetime.now()) + "\n"
init_log.write(initLog_completo)
#### Apertura de log de inicios de sesion e intentos #######
auth_log = open("./Logs/auth.log", "a")
contador_intentos = 0

################ Zona de dispositivos para conexiones con netmiko #########################

def inicializador():
    ## Podemos hacer una barrita de carga para ver que se vayan cargando las conexiones
    ## Router 1
    print("\n\n[*] Iniciando conexiones a routers...")
    DHCPMain_border_router = {
        'device_type' : 'cisco_ios',
        'host' : args.ip,
        'username' : 'admin',
        'password' : 'password',
        'secret' : 'cisco123'
    }

    Router2 = {
        'device_type' : 'cisco_ios',
        'host' : '192.168.123.82',
        'username' : 'admin',
        'password' : 'password',
        'secret' : 'cisco123'
    }
    
    Router3 = {
        'device_type' : 'cisco_ios',
        'host' : '192.168.123.18',
        'username' : 'admin',
        'password' : 'password',
        'secret' : 'cisco123'
    }

    Router4 = {
        'device_type' : 'cisco_ios',
        'host' : '192.168.123.50',
        'username' : 'admin',
        'password' : 'password',
        'secret' : 'cisco123'
    }

    Router5 = {
        'device_type' : 'cisco_ios',
        'host' : '192.168.123.114',
        'username' : 'admin',
        'password' : 'password',
        'secret' : 'cisco123'
    }

    ## Activacion de conexiones a routers
    router1 = ConnectHandler(**DHCPMain_border_router)
    router2 = ConnectHandler(**Router2)
    router3 = ConnectHandler(**Router3)
    router4 = ConnectHandler(**Router4)
    router5 = ConnectHandler(**Router5)

    ## Hace un retorno multiple con todos los routers
    return router1,router2,router3,router4,router5


## Agregar el resto de routers
def desconexion():
    BorderRouter.disconnect()
    router2.disconnect()
    router3.disconnect()
    router4.disconnect()
    router5.disconnect()


############## Sistema y logger de inicios de sesion e inicializaciones y salidas del programa ###########################
while(contador_intentos < 3):
    print(RED + "\n[*] Intento numero: " + str(contador_intentos) + BLUE)
    usuario = str(input("[*] Digita tu nombre de usuario: "))
    password = getpass.getpass()
    ## Calculamos hash
    calculo_password = hashlib.sha256(password.encode())
    hex_password = calculo_password.hexdigest()
    if usuario in usuarios:
        if(usuarios[usuario] == hex_password):
            log_inicio_correcto = str(datetime.now()) + " LoginSystem: " + "Inicio de sesion exitoso con usuario: " + usuario + "\n"
            auth_log.write(log_inicio_correcto) 
            BorderRouter,router2,router3,router4,router5 = inicializador()
            main()
        elif(usuarios[usuario] != hex_password):
            if(contador_intentos != 2):
                log_intento_fallido = str(datetime.now()) + " LoginSystem: " + "Intento de inicio de sesion fallido para usuario: " + usuario + "\n"
                auth_log.write(log_intento_fallido)
                print(RED + "[*] Los datos introducidos no son correctos.")
                contador_intentos += 1
            elif(contador_intentos == 2):
                log_intento_bloqueado = str(datetime.now()) + " LoginSystem: " + "Intento de inicio de sesion bloqueado para usuario: " + usuario + "\n"
                auth_log.close()
                print(RED + "[*] NUMERO DE INTENTOS EXCEDIDOS, SALIENDO!")
                quit()
    elif usuario not in usuarios:
        if(contador_intentos != 2):
            log_mal_usuario = str(datetime.now()) + " LoginSystem: " + "Intento de inicio de sesion fallido con usuario inexistente, para: " + usuario + ". [POSIBLE ATAQUE DE FUERZA BRUTA DETECTADO]\n"
            auth_log.write(log_mal_usuario)
            print(RED + "[*] Los datos introducidos no son correctos.")
            contador_intentos += 1
        elif(contador_intentos == 2):
            log_posible_ataque = str(datetime.now()) + " LoginSystem: " + "Intento de inicio de sesion bloqueado por exceso de intentos, con usuario inexistente para: " + usuario + ". [POSIBLE ATAQUE DE FUERZA BRUTA DETECTADO]\n"
            auth_log.write(log_posible_ataque)
            auth_log.close()
            print(RED + "[*] NUMERO DE INTENTOS EXCEDIDOS, SALIENDO!")
            quit()

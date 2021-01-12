from spider import spider
from scrapper import scrapper
from alternator import alternator
from utilities import unix_time_millis
import data_extraction_tools as det
from request_handler import request_handler
import datetime
import sys

#Definimos la configuración ---------

API_KEY = sys.argv[1] #La api key se pasa como argumento
servers = ["EUW", "KR", "NA", "EUNE"] #Los servidores que vamos a utilizar.
#corea (KR) esta muy lejos por lo que a veces da error 504.
desired_matches = 30000 #Los datos de cuantas partidas queremos obtener.
#Fecha a partir de la cual queremos partidas
startime = int(unix_time_millis(datetime.datetime(2020, 12, 24)))

#Inicializamos valores ------------

rh = request_handler(API_KEY) #La api key queda almacenada en el objeto que
# se encarga de las requests

spider(rh, servers, desired_matches)
scrapper(rh)

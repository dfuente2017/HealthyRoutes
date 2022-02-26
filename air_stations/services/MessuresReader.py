import requests
from bs4 import BeautifulSoup
from ..models import AirStation, Town, MessuresQuality
from django.core.exceptions import ObjectDoesNotExist


class MessuresReaderInterface():
    def __init__(self, args):
        self.args = list()
        for arg in args:
            self.args.append(arg)
    
    def read_messures(self):
        pass

class MessuresReader1(MessuresReaderInterface): #args -> [0]:container, [1]: town, [2]: air_station, [3]: messure, [4]:hour, [5]:verified, [6]:town_id   used in: Madrid(79)
    def __init__(self, args):
        super().__init__(args)


    def read_messures(self):
        verified_list = ["v01","v02","v03","v04","v05","v06","v07","v08","v09","v10","v11","v12","v13","v14","v15","v16","v17","v18","v19","v20","v21","v22","v23","v24"]
        air_stations = dict()
        url = Town.objects.get(id = self.args[6]).url

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')

        data_container = soup.find_all(self.args[0])
        for data in data_container:

            town = data.find(self.args[1]).contents[0]
            air_station = data.find(self.args[2]).contents[0][:8]
            messure = data.find(self.args[3]).contents[0]

            value = 'N'
            for verified_string in verified_list:
                if(data.find(verified_string).contents[0] == 'V'):  #Tenemos que recorrer todos los valores ya que es posible que se intercalesn N con valores validos entre horas
                    value = float(data.find(verified_string.replace(self.args[5],self.args[4])).contents[0])

            if(not (air_station in air_stations)):
                air_stations[air_station] = list()

            if value != 'N':
                air_stations[air_station].append((messure,value))

        self.save_messures(air_stations)


    def save_messures(self, air_stations = dict()):
        keys = list(air_stations.keys())
        messure_id = 0

        for air_station in air_stations:
            messure_id += 1
            so2_messure = None
            co_messure = None
            no_messure = None
            no2_messure = None
            pm2_5_messure = None
            pm10_messure = None
            nox_messure = None
            o3_messure =  None
            tol_messure = None
            btx_messure = None
            ebe_messure = None
            mxy_messure = None
            pxy_messure = None
            oxy_messure = None
            tch_messure = None
            ch4_messure = None
            nmhc_messure = None

            for messure in air_stations[air_station]:
                if messure[0] == 'id':
                    messure_id = messure[1]
                if messure[0] == '1':
                    so2_messure = messure[1]
                if messure[0] == '6':
                    co_messure = messure[1]
                if messure[0] == '7':
                    no_messure = messure[1]
                if messure[0] == '8':
                    no2_messure = messure[1]
                if messure[0] == '9':
                    pm2_5_messure = messure[1]
                if messure[0] == '10':
                    pm10_messure = messure[1]
                if messure[0] == '12':
                    nox_messure = messure[1]
                if messure[0] == '14':
                    o3_messure = messure[1]
                if messure[0] == '20':
                    tol_messure = messure[1]
                if messure[0] == '30':
                    btx_messure = messure[1]
                if messure[0] == '35':
                    ebe_messure = messure[1]
                if messure[0] == '37':
                    mxy_messure = messure[1]
                if messure[0] == '38':
                    pxy_messure  = messure[1]
                if messure[0] == '39':
                    oxy_messure = messure[1]
                if messure[0] == '42':
                    tch_messure = messure[1]
                if messure[0] == '43':
                    ch4_messure = messure[1]
                if messure[0] == '44':
                    nmhc_messure = messure[1]

            messure_db = {'id':messure_id, 'so2_messure':so2_messure, 'co_messure':co_messure, 'no_messure':no_messure,'no2_messure':no2_messure, 'pm2_5_messure':pm2_5_messure,
            'pm10_messure':pm10_messure, 'nox_messure':nox_messure,'o3_messure':o3_messure, 'tol_messure':tol_messure,'btx_messure':btx_messure, 'ebe_messure':ebe_messure,
            'mxy_messure':mxy_messure, 'pxy_messure':pxy_messure, 'oxy_messure':oxy_messure, 'tch_messure':tch_messure, 'ch4_messure':ch4_messure, 'nmhc_messure':nmhc_messure}

            air_station_db = AirStation.objects.get(id = keys[0])
            air_station_db.messures = messure_db

            air_station_db.air_quality = self.getAirQuality(messure_db.copy())

            air_station_db.save()

            keys.remove(keys[0])

    
    def getAirQuality(self, messures):
        del messures['id']
        n_messures_analyzed = 0
        accumuled_messure_quality = 0

        for messure in messures:
            try:
                messure_quality = MessuresQuality.objects.get(messure_name = messure)
                
                if messures[messure] != None:
                    n_messures_analyzed += 1
                    if messures[messure] <= messure_quality.very_good:
                        accumuled_messure_quality = accumuled_messure_quality + 5
                    elif messures[messure] <= messure_quality.good:
                        accumuled_messure_quality = accumuled_messure_quality + 4
                    elif messures[messure] <= messure_quality.mediocre:
                        accumuled_messure_quality = accumuled_messure_quality + 3
                    elif messures[messure] <= messure_quality.bad:
                        accumuled_messure_quality = accumuled_messure_quality + 2
                    elif messures[messure] <= messure_quality.very_bad:
                        accumuled_messure_quality = accumuled_messure_quality + 1
            except:
                pass    #Captura el error de cuando no encuenra la messure en la base de datos
            
        if(n_messures_analyzed == 0):
            return None
        else:
            return int(round(accumuled_messure_quality/n_messures_analyzed, 0))
import requests
from bs4 import BeautifulSoup
from ..models import Messures, AirStation, Town


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
        #url = 'https://www.mambiente.madrid.es/opendata/horario.xml' # define XML location

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')

        data_container = soup.find_all(self.args[0])
        for data in data_container:

            town = data.find(self.args[1]).contents[0]
            air_station = data.find(self.args[2]).contents[0][:8]
            messure = data.find(self.args[3]).contents[0]

            value = 'N'
            for verified_string in verified_list:
                if(data.find(verified_string).contents[0] == 'N'):
                    break
                else:
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
            no2_messure = None
            so2_messure = None
            co_messure = None
            pm10_messure = None
            pm2_5_messure = None
            o3_messure =  None
            btx_messure = None

            for messure in air_stations[air_station]:
                if messure[0] == 'id':
                    messure_id = messure[1]
                if messure[0] == '1':
                    so2_messure = messure[1]
                if messure[0] == '6':
                    co_messure = messure[1]
                if messure[0] == '7':
                    no2_messure = messure[1]
                if messure[0] == '9':
                    pm2_5_messure = messure[1]
                if messure[0] == '10':
                    pm10_messure = messure[1]
                if messure[0] == '14':
                    o3_messure = messure[1]
                if messure[0] == '30':
                    btx_messure = messure[1]

            messure_db = {'id':messure_id, 'so2_messure':so2_messure, 'co_messure':co_messure, 'no2_messure':no2_messure, 
                            'pm2_5_messure':pm2_5_messure, 'pm10_messure':pm10_messure, 'o3_messure':o3_messure, 'btx_messure':btx_messure}   
            air_station_db = AirStation.objects.get(id = keys[0])
            air_station_db.messures = messure_db
            air_station_db.save()

            keys.remove(keys[0])
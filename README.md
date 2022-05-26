# HealthyRoutes
![Prueba](https://github.com/dfuente2017/HealthyRoutes/blob/develop/HealthyRoutes/static/img/header-logo.png)

**HealthyRoutes** is a web application for persons that practices sports on big cities. This app recommends the healthiest routes taking care for the air quality state. It has a client-server architecture that implements MVC pattern with Django framework and NoSQL database MongoDB. The routes are obtained from GraphHopper API and the air quality data is supported at the moment by the Madrid town hall open data.

---
# Installation Manual
This installation manual has been developed for **Windows 10** and **Firefox**, and it shows how to install the app and the steps required for upload and visualizing Madrid air quality data.


1. Install **Python 3.9.1** and **Pip**.

2. Install **MongoDB 4.4** on your local machine.

3. Execute the command `pip install -r requirements.txt` on .../HealthyRoutes/.

4. Create an **.env** file on .../HealthyRoutes/HealthyRoutes/ directory with the variables **SECRET_KEY** as the Django secret key and **GRAPHHOPPER_API_KEY** as the key for GraphHopper api. There is an example of how to do it on the **.env.example** on the same directory.

5. Execute the `python manage.py migrate` and `python manage.py makemigrations` commands.

6. Create a superuser with the command `python manage.py createsuperuser`.

7. Open the shell with the `python manage.py shell` command for creating the required objects on the database for showing Madrid air quality info.
~~~
from air_stations.models import Country, Province, Town, Arguments, Argument, MessuresQuality
Country.objects.create(id=0,name='Spain')
Province.objects.create(id=28, name='Madrid', country=0)
Town.objects.create(id=79, name='Madrid', url='https://www.mambiente.madrid.es/opendata/horario.xml', province=28)
Arguments.objects.create(id=0, town_id=79, argument_type='AMD', arguments=[{'id':0, 'argument':'dato_horario'},{'id':1, 'argument':'municipio'},{'id':2, 'argument':'punto_muestreo'},{'id':3, 'argument':'magnitud'},{'id':4, 'argument':'h'},{'id':5, 'argument':'v'}])
Arguments.objects.create(id=1, town_id=79, argument_type='ASD', arguments=[{'id':0, 'argument':'CODIGO'},{'id':1, 'argument':'ESTACION'},{'id':2, 'argument':'LONGITUD'},{'id':3, 'argument':'LATITUD'}])
MessuresQuality.objects.create(id=0, messure_name='pm2_5_messure', very_good=10, good=20, mediocre=25, bad=50, very_bad=800)
MessuresQuality.objects.create(id=1, messure_name='pm10_messure', very_good=20, good=35, mediocre=50, bad=100, very_bad=1200)
MessuresQuality.objects.create(id=2, messure_name='no2_messure', very_good=40, good=100, mediocre=200, bad=400, very_bad=1000)
MessuresQuality.objects.create(id=3, messure_name='o3_messure', very_good=80, good=120, mediocre=180, bad=240, very_bad=600)
Messupython resQuality.objects.create(id=4, messure_name='so2_messure', very_good=100, good=200, mediocre=350, bad=500, very_bad=1250)
exit()
~~~
8. For next step run the `python manage.py runserver` command, login as the superuser you created and access to the http://localhost:8000/upload-air-stations url on your browser. Select the country, province and town and upload the air-station-data.csv that is on .../HealthyRoutes/

9. Then, stop the server and execute `python manage.py update_air_stations_data 79` for uploading air quality data for Madrid air stations.

10. For running this command periodically, you can create a task on your OS running the `python manage.py update_air_stations_data ${id}` with the id of the city that you want to update (79 id is for Madrid).
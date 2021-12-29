const tilesProvider = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
var numMarkers = 0;

var mymap = L.map('mapid').setView([40.4166314,-3.7038148], 13);

L.tileLayer(tilesProvider,{
    maxZoom: 18
}).addTo(mymap);

//var marker = L.marker([40.4166314,-3.7038148]).addTo(mymap);

mymap.on('dblclick', e => {
    if(numMarkers<2){
        let latLng = mymap.mouseEventToLatLng(e.originalEvent);
        L.marker([latLng.lat,latLng.lng]).addTo(mymap);
        numMarkers++;
    }
})

/*
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'your.mapbox.access.token'
}).addTo(mymap);
*/
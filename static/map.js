const tilesProvider = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'

let map = L.map('myMap').setView([51.505,-0.09],13)

L.tileLayer(tilesProvider,{
    maxZoom: 18
}).addTo(map);
L.Control.geocoder().addTo(map);
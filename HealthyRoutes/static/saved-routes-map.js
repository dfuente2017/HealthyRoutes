function createMap(n){
    const tilesProvider = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';
    L.tileLayer(tilesProvider).addTo(L.map("mymap-"+n).setView([43.64701, -79.39425], 3));
}
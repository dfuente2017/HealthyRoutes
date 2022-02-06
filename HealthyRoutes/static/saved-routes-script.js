function createMap(n){
    const tilesProvider = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';

    var map = L.map("mymap-"+n,{
        /*minZoom: 13,
        maxZoom: 13*/
    }).setView([43.64701, -79.39425], 3);

    L.tileLayer(tilesProvider).addTo(map);

    nodes = JSON.parse(document.getElementById("nodes-"+n).innerHTML.replace(/'/g, '"').replace(/None/g, null).replace(/Decimal/g,"").replaceAll("(","").replaceAll(")",""))

    var latlngs = [];
    for(let i=0;i<nodes.length;i++){
        latlngs.push([nodes[i].latitude, nodes[i].longitude]);
    }

    polyline = L.polyline(latlngs, {color:'#3388ff', weight:5}).addTo(map);

    map.fitBounds(polyline.getBounds());

    
}

function orderBy(param){
    document.getElementById("operation").value = "order-by";
    switch(param){
        case "date-asc":
            document.getElementById("order-by").value = "date-asc";
            break;
        case "date-desc":
            document.getElementById("order-by").value = "date-desc";
            break;
        case "points":
            document.getElementById("order-by").value = "points";
            break;
        case "distance":
            document.getElementById("order-by").value = "distance";
            break;
        default:
            document.getElementById("order-by").value = "date";
    }
    document.forms["saved-routes-form"].submit();
}

function removeRoute(user,n){
    document.getElementById("operation").value = "delete";
    document.getElementById("user").value = user;
    document.getElementById("date-saved").value = document.getElementById("date-"+n).innerHTML;
    document.forms["saved-routes-form"].submit();
}
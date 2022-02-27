const tilesProvider = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
var airStations = new Array();
var airStationsMarkersOptions = {
    clickable: true,
    draggable: false
}

var lastRouteShown = null;
var initEndRouteMarkers = new Array();
var routeMarkers = new Array();
var polyline = null;

var airStationsLayer = new L.layerGroup();

var routeRanking = null;

getAirStations();

function getAirStations(){
    $.ajax({
        url:'api/air_stations',
        type: 'get',
        data: {
            //town_id: getTown()
        },
        success: function(response) {
            for(let key in response){
                jsonObject = response[key]
                putAirStationMarker(jsonObject.name, jsonObject.latitude, jsonObject.longitude, jsonObject.messures, jsonObject.air_quality)
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            alert(textStatus + ':' + errorThrown)
        }
    });
}
/*Implement a method to request the towns ids*/
function getTown(){
    
}
function putAirStationMarker(name, latitude, longitude, messures, air_quality){
    //var marker = new L.Marker([latitude, longitude], airStationsMarkersOptions).bindPopup('Estacion de ' + name + '</br>' + 'Estado del aire: ' + airQualityTraduction(air_quality));
    var circleColor = getCircleColor(air_quality)
    var circle = new L.circle([latitude,longitude],{
        color: circleColor,
        fillColor: circleColor, 
        fillOpacity: 0.3,
        radius: 1500
    }).bindPopup('Estacion de ' + name + '</br>' + 'Estado del aire: ' + airQualityTraduction(air_quality));;

    //airStationsLayer.addLayer(marker);
    airStationsLayer.addLayer(circle);
}
function airQualityTraduction(air_quality){
    switch(air_quality){
        case 5:
            return "Muy bueno"
        case 4:
            return "Bueno"
        case 3:
            return "Regular"
        case 2:
            return "Malo"
        case 1:
            return "Muy malo"
        default:
            return "Desconocido"
    }
}
function getCircleColor(air_quality){
    switch(air_quality){
        case 5:
            return "#00FFFB"
        case 4:
            return "#5AB507"
        case 3:
            return "#FFFF01"
        case 2:
            return "#FEA500"
        case 1:
            return "#BD0100"
        default:
            return "#C3C3C3"
    }
}

var map = L.map('map', {
    center: [40.417,-3.703],
    zoom: 13,
    layers: [airStationsLayer]
});

var overlayMaps = {
    "Estaciones de calidad del aire": airStationsLayer
}

L.control.layers(null, overlayMaps).addTo(map);

map.doubleClickZoom.disable();
L.tileLayer(tilesProvider, {
    maxZoom: 18
}).addTo(map);

var routeMarkersOptions = {
    clickable: true,
    draggable: true
}

var initEndRouteMarkersOptions = {
    clickable: true,
    draggable: false
}


map.on("dblclick", function(e){
    if(routeMarkers.length < 2){
        document.getElementById("remove-markers-button").disabled = false;  
        routeMarkers.push(new L.Marker([e.latlng.lat, e.latlng.lng], routeMarkersOptions).addTo(map));
        if(routeMarkers.length == 2){
            document.getElementById("search-route-button").disabled = false;
        }
    }
})

function removeMarkers(){
    routeMarkers.forEach(function(marker){
        map.removeLayer(marker);
    });

    routeMarkers = new Array();
    document.getElementById("remove-markers-button").disabled = true;
    document.getElementById("search-route-button").disabled = true;
}

function searchRoutes(){
    document.getElementById('initLatitude').value = routeMarkers[0].getLatLng().lat;
    document.getElementById('initLongitude').value = routeMarkers[0].getLatLng().lng;
    document.getElementById('endLatitude').value = routeMarkers[1].getLatLng().lat;
    document.getElementById('endLongitude').value = routeMarkers[1].getLatLng().lng;
    document.myform.submit();
}


function selectRoute(n){
    if(n != lastRouteShown){
        var nodesHTML = document.getElementById("route_nodes_"+n).innerText.replace(/'/g, '"').replace(/None/g, null);
        var nodesParsed = JSON.parse(nodesHTML);
    
        if(polyline != null){
            map.removeLayer(polyline);
        }
    
    
        moreInfo(n);
        document.getElementById("card_" + n).setAttribute("class", document.getElementById("card_"+n).attributes['class'].textContent.replace("bg-primary", "bg-secondary"));
        if(lastRouteShown == null){
            lastRouteShown = 0;
        }else{
            moreInfo(lastRouteShown);
            document.getElementById("card_" + lastRouteShown).setAttribute("class", document.getElementById("card_"+lastRouteShown).attributes['class'].textContent.replace("bg-secondary", "bg-primary"));
        }
        
    
        document.getElementById("instructions_" + lastRouteShown).hidden = true;
        lastRouteShown = n;
    
        document.getElementById("instructions_" + n).hidden = false;
    
        var latlngs = [];
    
        for(let i=0;i<nodesParsed.length;i++){
            latlngs.push([nodesParsed[i].latitude, nodesParsed[i].longitude]);
        }

        initEndRouteMarkers.push(new L.Marker([latlngs[0][0], latlngs[0][1]], initEndRouteMarkersOptions).addTo(map));
        initEndRouteMarkers.push(new L.Marker([latlngs[latlngs.length-1][0], latlngs[latlngs.length-1][1]], initEndRouteMarkersOptions).addTo(map));

        polyline = L.polyline(latlngs, {color:'#3388ff', weight:5}).addTo(map);
    
        map.fitBounds(polyline.getBounds());
    }
}


function moreInfo(n){
    if(document.getElementById("info_button_" + n).attributes[1].value == "glyphicon glyphicon-chevron-down"){
        document.getElementById("extended_info_" + n).hidden = false;
        document.getElementById("info_button_" + n).attributes[1].value = "glyphicon glyphicon-chevron-up";
    } else{
        document.getElementById("extended_info_" + n).hidden = true;
        document.getElementById("info_button_" + n).attributes[1].value = "glyphicon glyphicon-chevron-down";
    }
}


$(document).ready(function() {
    if(document.getElementById("route_nodes_0") != null){
        selectRoute(0);
    }
});


//document.getElementById("card_0").setAttribute("class", document.getElementById("card_0").attributes['class'].textContent.replace("bg-primary", "bg-2934d3"));

/*L.Control.geocoder({
    geocoder: L.Control.Geocoder.nominatim()
}).addTo(map);*/
function changeNick(){
	document.getElementById("user-nick").disabled = false;
	document.getElementById("change-nick").remove();
}

function changePassword(){
	document.getElementById("change-password").remove();
	document.getElementById("pwd1").hidden = false;
	document.getElementById("pwd1").required = true;
	document.getElementById("pwd2").hidden = false;
	document.getElementById("pwd2").required = true;
	document.getElementById("pwd1-show").hidden = false;
	document.getElementById("pwd2-show").hidden = false;
}

function like(n){
	if(document.getElementById("like-icon-" + n).attributes[1].value == "glyphicon glyphicon-heart-empty"){
		document.getElementById("like-icon-" + n).setAttribute("class","glyphicon glyphicon-heart");
		saveRoute(n);
	}else{
		document.getElementById("like-icon-" + n).setAttribute("class","glyphicon glyphicon-heart-empty");
		removeRoute(n);
	}
}

function disableSubmit(idButton){
	document.getElementById(idButton).disabled = true;
}

function checkPassword(idButton){
	var pwd1 = document.getElementById("pwd1").value;
	var pwd2 = document.getElementById("pwd2").value;

	var msg1 = document.getElementById("pass-dis");
	var msg2 = document.getElementById("pass-range");
	var msg3 = document.getElementById("pass-length");

	msg1.hidden = true;
	msg2.hidden = true;
	msg3.hidden = true;

	if(pwd1 != pwd2){
		msg1.hidden = false;
		disableSubmit(idButton);
		return false;
	}else if(!pwd1.match(/[A-Z]/g) || !pwd1.match(/[a-z]/g) || !pwd1.match(/[0-9]/g)){
		msg2.hidden = false;
		disableSubmit(idButton);
		return false;
	}else if(pwd1.length<10){
		msg3.hidden = false;
		disableSubmit(idButton);
		return false;
	}else{
		return true;
	}
}

function checkForm(idButton){
	if(checkPassword(idButton)){
		document.getElementById(idButton).disabled = false;
	}
}

function deleteImage(){
	document.getElementById("delete-img").value="true";
	document.getElementById("profile-img").src = "/static/img/user.png";
}

function showPassword(idInput){
	if(document.getElementById(idInput).type == "password"){
		document.getElementById(idInput).type = "text";
	}else{
		document.getElementById(idInput).type = "password";
	}
}

function showRouteVariation(){
	document.getElementById("routes_variation").hidden = !document.getElementById("routes_variation").hidden;
	if(document.getElementById("routes_variation_button").getAttribute("Class") == "glyphicon glyphicon-chevron-down"){
		document.getElementById("routes_variation_button").setAttribute("Class","glyphicon glyphicon-chevron-up");
	}else{
		document.getElementById("routes_variation_button").setAttribute("Class","glyphicon glyphicon-chevron-down");
	}
}

function saveRoute(n){
	$.ajax({
		url: 'api/route',
		type: 'POST',
		data: {
			csrfmiddlewaretoken: document.getElementById("csrfmiddlewaretoken").innerText,
			type: "POST",
			distance: document.getElementById("route-distance-"+n).innerText,
			time: document.getElementById("route-time-"+n).innerText,
			nodes: document.getElementById("route_nodes_"+n).innerText,
			veryGoodAirQualityNodes: document.getElementById("route-very-good-air-quality-nodes-"+n).innerText,
			goodAirQualityNodes: document.getElementById("route-good-air-quality-nodes-"+n).innerText,
			mediocreAirQualityNodes: document.getElementById("route-mediocre-air-quality-nodes-"+n).innerText,
			badAirQualityNodes: document.getElementById("route-bad-air-quality-nodes-"+n).innerText,
			veryBadAirQualityNodes: document.getElementById("route-very-bad-air-quality-nodes-"+n).innerText,
			unknownAirQualityNodes: document.getElementById("route-unknown-air-quality-nodes-"+n).innerText,
			rankingPuntuation: document.getElementById("route-ranking-puntuation-"+n).innerText
		},
		success: function(response){
			alert(response['message']);
			document.getElementById("route-date-saved-"+n).innerText = response['route_date_saved']
		},
		error: function(jqXHR, textStatus, errorThrown){
			document.getElementById("like-icon-" + n).setAttribute("class","glyphicon glyphicon-heart-empty");		
			if(errorThrown === "Unauthorized"){
				alert("Para poder guardar rutas necesitas iniciar sesion");
			}
			else if(errorThrown === "Bad Request"){
				alert("La ruta no pudo guardarse correctamente");
			}
			else{
				alert(textStatus + ':' + errorThrown);
			}
		}
	});
}

function removeRoute(n){
	$.ajax({
		url: 'api/route',
		type: 'POST',
		data: {
			csrfmiddlewaretoken: document.getElementById("csrfmiddlewaretoken").innerText,
			type: "DELETE",
			routeDateSaved: document.getElementById("route-date-saved-"+n).innerText
		},
		success: function(response){
			alert(response['message']);
		},
		error: function(jqXHR, textStatus, errorThrown){
			document.getElementById("like-icon-" + n).setAttribute("class","glyphicon glyphicon-heart");
			if(errorThrown === "Unauthorized"){
				alert("Para poder guardar rutas necesitas iniciar sesion");
			}
			else if(errorThrown === "Bad Request"){
				alert("La ruta no pudo eliminarse correctamente");
			}
			else{
				alert(textStatus + ':' + errorThrown);
			}
		}
	});
}
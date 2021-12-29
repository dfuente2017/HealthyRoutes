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

function moreInfo(){
	if(document.getElementById("info_button").attributes[1].value == "glyphicon glyphicon-chevron-down"){
		document.getElementById("basic_info").hidden = true;
		document.getElementById("extended_info").hidden = false;
		document.getElementById("info_button").attributes[1].value = "glyphicon glyphicon-chevron-up";
	} else{
		document.getElementById("basic_info").hidden = false;
		document.getElementById("extended_info").hidden = true;
		document.getElementById("info_button").attributes[1].value = "glyphicon glyphicon-chevron-down";
	}
}

function like(){
	if(document.getElementById("like-icon").attributes[1].value == "glyphicon glyphicon-heart-empty"){
		document.getElementById("like-icon").attributes[1].value = "glyphicon glyphicon-heart";
	}else{
		document.getElementById("like-icon").attributes[1].value = "glyphicon glyphicon-heart-empty";
	}
}

function disableSubmit(idButton){
	document.getElementById(idButton).disabled = true;
	//document.getElementById(idButton).styles = ?
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
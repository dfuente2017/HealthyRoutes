function changeTab(n){
	if(n==0){
		document.getElementById("login-tab").attributes[2].value = "col-sm-6 text-center pestañas-login-1";
		document.getElementById("register-tab").attributes[2].value = "col-sm-6 text-center pestañas-login-2 non-active";
		if(document.getElementById("pwd2") != null){
			document.getElementById("pwd2").remove();
			document.getElementById("nick").remove();
			document.getElementById("submit-button").textContent = "Iniciar Sesión";
		}
	}else{
		if(document.getElementById("pwd2") == null){
			document.getElementById("login-tab").attributes[2].value = "col-sm-6 text-center pestañas-login-1 non-active";
			document.getElementById("register-tab").attributes[2].value = "col-sm-6 text-center pestañas-login-2";
			addPwd2();
			addNick();
			document.getElementById("submit-button").textContent = "Registrarse";
		}
	}
}

function addPwd2(){
	var pwd2 = document.createElement("INPUT");
	pwd2.setAttribute("id", "pwd2");
	pwd2.setAttribute("name", "pwd2")
	pwd2.setAttribute("type", "password");
	pwd2.setAttribute("class", "form-control w-75 mx-auto mt-5");
	pwd2.setAttribute("placeholder", "Repita contraseña");
	document.getElementById("login").appendChild(pwd2);
}

function addNick(){
	var nick = document.createElement("INPUT");
	nick.setAttribute("id","nick");
	nick.setAttribute("name","nick")
	nick.setAttribute("type", "text");
	nick.setAttribute("class", "form-control w-75 mx-auto mt-5");
	nick.setAttribute("placeholder", "Nick");
	document.getElementById("login").appendChild(nick);
}

function changeNick(){
	document.getElementById("user-nick").disabled = false;
	document.getElementById("change-nick").remove();
}

function changePassword(){
	document.getElementById("change-password").remove();
	document.getElementById("user-password1").hidden = false;
	document.getElementById("user-password2").hidden = false;
}

function moreInfo(){
	if(document.getElementById("info_button").attributes[1].value == "glyphicon glyphicon-chevron-down"){
		document.getElementById("extended_info").hidden = false;
		document.getElementById("info_button").attributes[1].value = "glyphicon glyphicon-chevron-up";
	} else{
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

function checkPassword(){
	var pwd1 = document.getElementById("pwd1");
	var pwd2 = document.getElementById("pwd2");

	if(pwd1 != pwd2){
		return false;
	}
	if(pwd1 == ""){
		return false;
	}
	if(pwd1.length<15){
		return false;
	}
	if(!pwd1.match(/[A-Z]/g)){
		return false;
	}
	if(!pwd1.match(/[a-z]/g)){
		return false
	}
	if(!pwd1.match(/[0-9]/g)){
		return false
	}

	return true;
}

function checkForm(){
	if(checkPassword()){
		document.getElementById("profile-form").submit()
	}else{
		console.log("Contraseña no valida");
	}
}
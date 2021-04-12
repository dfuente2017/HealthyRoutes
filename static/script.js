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
	pwd2.setAttribute("type", "password");
	pwd2.setAttribute("class", "form-control w-75 mx-auto mt-5");
	pwd2.setAttribute("placeholder", "Repita contraseña");
	document.getElementById("login").appendChild(pwd2);
}

function addNick(){
	var nick = document.createElement("INPUT");
	nick.setAttribute("id","nick");
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
	document.getElementById("user-password1").disabled = false;
	document.getElementById("user-password1").value = "";
	document.getElementById("change-password").remove();
	document.getElementById("user-password2").hidden = false;
	//var password = document.getElementById("user-password");
	//password.attributte
	//document.getElementById("password-field").appendChild(password);
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
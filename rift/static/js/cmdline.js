console.log("cmdline.js loaded");

window.onload = function() {
	cmdInput = document.forms["cmdline"]["cmd"];
	prompt = document.getElementById("prompt");
	defaultPrompt = prompt.innerHTML;
	promptDir = document.getElementById("prompt-dir");
	prev_args = [];

	login_mode = false;
	register_mode = 0;
	username = null;
	email = null;
	password = null;
}

function executeCmd() {
	/* Store cmd */
	var cmd = cmdInput.value;
	var args = cmd.split(' ');
	/* clear cmdInput */
	cmdInput.value = "";

	if(login_mode) {
		password = cmd;
		login(username, password)
		return false
	}

	if(register_mode > 0) {
		switch (register_mode) {
			case 1:
				password = cmd;
				prompt.innerHTML = "Re Password: ";
				register_mode++;
				break;
			case 2:
				var repassword = cmd;
				if (repassword == password) {
					prompt.innerHTML = "Email: ";
					cmdInput.type = "text";
					register_mode++;
				} else {
					prompt.innerHTML = "Password: ";
					register_mode--;
				}
				break;
			case 3:
				email = cmd;
				register(username, email, password)

		}
		return false
	}

	if (args[0] == "su") {
		/* Store entered username for login request */
		username = args[1];
		/* Change process */
		login_mode = true;
		cmdInput.type = "password";
		prompt.innerHTML = "Password: ";
	}

	if (args[0] == "adduser") {
		/* Store entered username for login request */
		username = args[1];
		/* Change process */
		register_mode = 1;
		cmdInput.type = "password";
		prompt.innerHTML = "Password: "
	}
	
	if(args[0] == "logout") {
		cmdInput.placeholder = "logging out..."
		logout();
	}

	/*
	if(login_mode || register_mode) {
		cmdInput.type = "password";
		prompt.innerHTML = "Password: "
	} else {
		cmdInput.type = "text";
		prompt.innerHTML = defaultPrompt;
	}
	*/
	return false;
}

function registerProcess(step) {

}

function loginProcess(step) {
	if (step == 2) {
		cmdInput.type = "password";
		prompt.innerHTML = "Password: "
	}
}

function login(uname, pword) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			location.reload();
		}
	};
	xhttp.open("POST", "/login", true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send("type=login&"+"uname=" + uname + "&pword=" + pword);
}

function register(uname, email, pword) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			location.reload();
		}
	};
	xhttp.open("POST", "/login", true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send("type=register&"+"uname=" + uname + "&pword=" + pword + "&email=" + email);
}

function logout() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			location.reload();
		}
	};
	xhttp.open("GET", "/logout", true);
	xhttp.send();
}
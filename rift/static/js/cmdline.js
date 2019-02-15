console.log("cmdline.js loaded");

window.onload = function() {
    cmdInput = document.forms["cmdline"]["cmd"];
    prompt = document.getElementById("prompt");
    defaultPrompt = prompt.innerHTML;
    promptDir = document.getElementById("prompt-dir");
    prev_args = [];

    login_mode = false;
    login_username = "";
    login_password = "";
}

function executeCmd() {
    /* Store cmd */
    var cmd = cmdInput.value;
    var args = cmd.split(' ');
    /* clear cmdInput */
    cmdInput.value = "";

    if(login_mode) {
        cmdInput.placeholder = "logging in..."
        login_password = cmd;
        login(login_username,login_password);
    } else if (args[0] == "su") {
        /* Store entered username for login request */
        login_username = args[1];

        /* Change input to accept password */
        login_mode = true;

    } else if(args[0] == "logout") {
        cmdInput.placeholder = "logging out..."
        logout();
    }

    if(login_mode) {
        cmdInput.type = "password";
        prompt.innerHTML = "Password: "
    } else {
        cmdInput.type = "text";
        prompt.innerHTML = defaultPrompt;
    }

    prev_args = args;
	return false;
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

function register(uname, pword) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            location.reload();
        }
    };
    xhttp.open("POST", "/login", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("type=register&"+"uname=" + uname + "&pword=" + pword);
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
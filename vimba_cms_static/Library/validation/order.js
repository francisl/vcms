

function checkifcompleted( formname, elemlist, errmess ) {
	var form = formname;
	var len = elemlist.length;
	var taglist = elemlist;
	var errorcolor = "thin solid red";
	var err = 0;
	var errormess = "";
	var errormesslist = new Array();
	if (!errmess) {	// default value if not set
		errormesslist = ["Please fill all required fields!", "Please, enter a valid email address!", "Email address don't match!"];
	} else {
		errormesslist = errmess;
	}
	var defaultcolor = document.getElementById("default_input").style.border;
	
	// Pass through all field past in elemlist and check if not empty
	for (var i = 0; i < len; i++){

		var tag = document.getElementById(taglist[i]);
		//var label = document.getElementById(taglist[i]);
		tag.style.border = defaultcolor;
		if (tag.value == null || tag.value == "") {
			tag.style.border=errorcolor;
			err = 1;
			errormess = '- ' + errormesslist[0] + '\n';
		}
	}
	
	// Check email
	var email = document.getElementById("id_email");
	var email2 = document.getElementById("id_email2");
	email.style.border = email2.style.border = defaultcolor;
	//var label = document.getElementById("Email");
	//var label2 = document.getElementById("Email2");
	
	if (!validateEmail(email.value)){
		email.style.border=errorcolor;
		err = 1;
		errormess = errormess + '- ' + errormesslist[1] + '\n';
	}

	// check if both email are equal
	if (email.value != email2.value){
		email.style.border=errorcolor;
		email2.style.border=errorcolor;
		err = 1;
		errormess = errormess + '- ' + errormesslist[2] + '\n';
	}
	
	if (err < 1){
		try {
			document.getElementById("content_main").style.display = "none";
			document.getElementById("content_main_processing").style.display = "block";
		} catch (e){
			return true;
		}		
		return true;
	} else {
		alert(errormess);
		return false;
	}
	
}

// Check if email is valid form
function validateEmail(email){
	var re = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
	return re.test(email);
}



// Ajax resquest, not yet used
function goConfirmation(){
	document.getElementById("content").innerHTML = "<p>Processing your order!</p><br />";
	
	var xhr;
	try {
		xhr = new ActiveXObject("Msxml2.XMLHTTP");		
	} catch (e) {
		try{ 
			xhr = new ActiveXObject("Microsoft.XMLHTTP"); 
		} catch (e) {
			xhr = false;
		}
	}
	if (!xhr && typeof XMLHttpRequest != 'undefined' ){
		xhr = new XMLHttpRequest();
	}

	xhr.open("POST", "/order/confirmation?test=234");
	xhr.onreadystatechange = function () {
		if (xhr.readyState != 4) return;
		document.getElementById("content_main").innerHTML = xhr.responseText;
	}
	xhr.send(null);

}
	
	

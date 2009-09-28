

function checkmemberlogin(formlogin, user, passwd ) {
	var _form = formlogin;
	var _user = user;
	var _passwd = passwd;
	var errormess = "Invalid login!";

	try {
		_form.username.style.border="thin solid red";
		_form.passwd.style.border="thin solid red";
		return false;
	} catch (e){
		return false;
	}		
	
}
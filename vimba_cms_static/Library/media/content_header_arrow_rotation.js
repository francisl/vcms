var elements = {};
var CLOSED = "False";
var OPEN = "True";

function change_status(elementid){
	if (elements[elementid] === OPEN){
		elements[elementid] = CLOSED;
		$("#"+elementid+"_image").rotateAnimation(90);
	}else if (elements[elementid] === CLOSED){
		elements[elementid] = OPEN;
		$("#"+elementid+"_image").rotateAnimation(0);
	}
	return true;
}

function create_header_arrow(elementid, elementdisplay){
    if( typeof($('#'+elementid+"_image").get(0)) !== "undefined"){
	    elements[elementid] = elementdisplay;
	    $("#"+elementid+"_image").rotate(0);
    }
	return elementid;
}

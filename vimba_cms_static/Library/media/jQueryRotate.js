/*
 * THIS IS FREE SCRIPT BUT LEAVE THIS COMMENT IF
 * YOU WANT USE THIS CODE ON YOUR SITE
 * 
 * Made by Wilq32, wilq32@gmail.com, Wroclaw, Poland, 01.2009
 * 
 */
/*
Description:

This is an final product of a Wilq32.PhotoEffect Snippet. Actually you can
 use this simple and tiny script to get effect of rotated images directly 
 from client side (for ex. user generated content), and animate them using
 own functions. 


Notices:

Include script after including main jQuery. Whole plugin uses jQuery
namespace and should be compatible with older version (unchecked). 
If you want to get this work in Internet Explorer you will need to 
include ExCanvas also.

Usage:

jQuery(imgElement).rotate(angleValue)
jQuery(imgElement).rotate(parameters)
jQuery(imgElement).rotateAnimation(parameters)
jQuery(imgElement).rotateAnimation(parameters)



Returns:

jQueryRotateElement - !!! NOTICE !!! function return rotateElement
instance to help connect events with actually created 'rotation' element.

Parameters:

    ({angle:angleValue,
     [animateAngle:animateAngleValue],
     [maxAngle:maxAngleValue],
     [minAngle:minAngleValue],
     [callback:callbackFunction],
     [bind:[{event: function},{event:function} ] })
jQuery(imgElement).rotateAnimation

Where:

- angleValue - clockwise rotation given in degrees,
- [animateAngleValue] - optional parameter, animate rotating into this value,
- [maxAngleValue] - optional parameter, maximum angle possible for animation,
- [minAngleValue] - optional parameter, minimum angle possible for animation,
- [callbackFunction] - optional function to run after animation is done
- [bind: [ {event: function}...] -optional parameter, list of events binded
  to newly created rotateable object

Examples:

		$(document).ready(function()
		{
			$('#image').rotate(-25);			
		});

		$(document).ready(function()
		{
			$('#image2').rotate({angle:5});	
		});

		$(document).ready(function()
		{
			var rot=$('#image3').rotate({maxAngle:25,minAngle:-55,
			bind:
				[
					{"mouseover":function(){rot.rotateAnimation(85);}},
					{"mouseout":function(){rot.rotateAnimation(-35);}}
				]
			});
		});
*/


jQuery.fn.extend({
ImageRotate:function(parameters)
{	
	if (this.Wilq32&&this.Wilq32.PhotoEffect) return;
	return (new Wilq32.PhotoEffect(this,parameters))._temp;
},
rotate:function(parameters)
{
	if (typeof parameters=="undefined") return;
	if (typeof parameters=="number") parameters={angle:parameters};
	if (typeof this.get(0).Wilq32 == "undefined") 
		return $(this.ImageRotate(parameters));
	else 
	{
		this.get(0).Wilq32.PhotoEffect._rotate(parameters.angle);
	}
},

rotateAnimation:function(parameters)
{
	if (typeof parameters=="undefined") return;
	if (typeof parameters=="number") parameters={angle:parameters};
	if (typeof this.get(0).Wilq32 == "undefined") 
		return $(this.ImageRotate(parameters));	
	else 
	{
		this.get(0).Wilq32.PhotoEffect._parameters.animateAngle = parameters.angle;
		this.get(0).Wilq32.PhotoEffect._parameters.callback = parameters.callback ||
		function()
		{
		};
		this.get(0).Wilq32.PhotoEffect._animateStart();
	}
}

});

Wilq32={};

Wilq32.PhotoEffect=function(img,parameters)
{
			img = img.get(0);
			this._IEfix=img;
			this._parameters=parameters;
			this._parameters.className=img.className;
			this._parameters.id=img.getAttribute('id');
			
			if (!parameters) this._parameters={};
			this._angle=0;
			if (!parameters.angle) this._parameters.angle=0;
			this._temp=document.createElement('span');
			this._temp.Wilq32 = 
				{
					PhotoEffect: this
				};			
			var image=img.src;
			img.parentNode.insertBefore(this._temp,img);
			this._img= new Image();
			this._img.src=image;
			this._img._ref=this;
			jQuery(this._img).bind("load", function()
			{
				this._ref._Loader.call(this._ref);
			});
			if (jQuery.browser.msie) if (this._img.complete) this._Loader();
}

Wilq32.PhotoEffect.prototype._Loader=function ()
{
	this._IEfix.parentNode.removeChild(this._IEfix);
	this._temp.setAttribute('id',this._parameters.id);
	this._temp.className=this._parameters.className;
	var width=this._img.width;
	var height=this._img.height;
	
	this._img._widthMax=this._img._heightMax=Math.sqrt((height)*(height) + (width) * (width));

	this._canvas=document.createElement('canvas');
	this._canvas._ref=this;
	this._canvas.height=width;
	this._canvas.width=height;

	this._canvas.setAttribute('width',width);

	this._temp.appendChild(this._canvas);

	if (jQuery.browser.msie) 
		{	
			// ExCanvas to make it work in IE
			this._canvas.id="Wilq32.PhotoTemp";
			G_vmlCanvasManager.initElement(this._canvas);
			this._canvas=document.getElementById('Wilq32.PhotoTemp');
			this._canvas.id="";							
			this._canvas._ref=this;
		}
	var self = this;
	this._parameters.animateAngle=0;
	if (this._parameters.bind) 
	{
		for (var a in this._parameters.bind) if (this._parameters.bind.hasOwnProperty(a)) 
		for (var b in this._parameters.bind[a]) if (this._parameters.bind[a].hasOwnProperty(b)) 
		jQuery(this._canvas).bind(b,this._parameters.bind[a][b]);
	}
	this._cnv=this._canvas.getContext('2d');
	this._rotate(this._parameters.angle);
}

Wilq32.PhotoEffect.prototype._animateStart=function()
{	
	if (this._timer) clearTimeout(this._timer);
	this._animate();
}
Wilq32.PhotoEffect.prototype._animate=function()
{	
    var temp=this._angle;
	if (typeof this._parameters.animateAngle!="undefined") this._angle-=(this._angle-this._parameters.animateAngle)*0.1;
	if (typeof this._parameters.minAngle!="undefined") if (this._angle<this._parameters.minAngle) this._angle=this._parameters.minAngle;
	if (typeof this._parameters.maxAngle!="undefined") if (this._angle>this._parameters.maxAngle) this._angle=this._parameters.maxAngle; 

	if (Math.round(this._angle * 100 - temp * 100) == 0 && this._timer) 
		{
			clearTimeout(this._timer);
			if (this._parameters.callback) 
				this._parameters.callback();
		}
		else 
		{
			this._rotate(this._angle);
			var self = this;
			this._timer = setTimeout(function()
			{
				self._animate.call(self);
			}, 10);
		}
}

Wilq32.PhotoEffect.prototype._rotate = function(angle)

{

	if (!this._img.width) return;
	if (typeof angle!="number") return;
	angle=(angle%360)* Math.PI / 180;
	var width=this._img.width;
	var height=this._img.height;
	var widthAdd = this._img._widthMax - width;
	var heightAdd = this._img._heightMax - height;
	// clear canvas	
	this._canvas.width = width+widthAdd;
	this._canvas.height = height+heightAdd;

	//this._cnv.scale(0.8,0.8); // SCALE - if needed ;)
	
	// REMEMBER: all drawings are read from backwards.. so first function is translate, then rotate, then translate, translate..
	this._cnv.save();
	this._cnv.translate(widthAdd/2,heightAdd/2); // at least center image on screen
	this._cnv.translate(width/2,height/2);		  // we move image back to its orginal 
	this._cnv.rotate(angle);					  // rotate image
	this._cnv.translate(-width/2,-height/2);	  // move image to its center, so we can rotate around its center
	this._cnv.drawImage(this._img, 0, 0);		  // First - we draw image
	this._cnv.restore();
}


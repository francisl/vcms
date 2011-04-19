/* ------------------------------------------------------------------------
	s3Slider
	
	Developped By: Boban Karišik -> http://www.serie3.info/
        CSS Help: Mészáros Róbert -> http://www.perspectived.com/
	Version: 1.0
	
	Copyright: Feel free to redistribute the script/modify it, as
			   long as you leave my infos at the top.

    Modified : Francis Lavoie
------------------------------------------------------------------------- */


(function($){  

    $.fn.s3Slider = function(vars) {       
        
        var element     = this;
        var timeOut     = (vars.timeOut !== undefined) ? vars.timeOut : 6000;
        var effetTimeOut = (vars.effetTimeOut !== undefined) ? vars.timeOut : 500;
        var slideSwitchTimeOut = 0;
        var mOver       = false;
        var items       = $("#" + element[0].id + "Content ." + element[0].id + "Image");
        var itemsSpan   = $("#" + element[0].id + "Content ." + element[0].id + "Image span");
        var timeOutFun  = null;
        
        items.each(function(i) {
           $(items[i]).mouseover(function() {
               mOver = true;
            });
            $(items[i]).mouseout(function() {
                mOver   = false;
            });
        });
        
        var fadeElement = function(isSwitching, fn) {
            var thisTimeOut = (isSwitching) ? slideSwitchTimeOut : timeOut;
            timeOutFun = setTimeout(fn, thisTimeOut);
        };
        
        function currentPosition(current) {
            return (current >= items.length) ? 0 : current;
        }

        var hideIt = function(itemToHide){
            if(!mOver) {
                var nextFun = function (){ showIt(currentPosition(itemToHide+1)); };
                var switchSlide = function (){ fadeElement(true, nextFun); };
                var fadeOut = function() { $(items[itemToHide]).fadeOut(effetTimeOut, switchSlide); };
                if($(itemsSpan[itemToHide]).css('bottom') === 0) {
                    $(itemsSpan[itemToHide]).slideDown((effetTimeOut), fadeOut);
                } else {
                    $(itemsSpan[itemToHide]).slideUp((effetTimeOut), fadeOut);
                }
            } else {
                fadeElement(true, function (){ hideIt(itemToHide);});
            }
        };

        var showIt = function(itemToShow){
            var nextFun = function (){ hideIt(itemToShow); };
            if(!mOver) {
                $(items[itemToShow]).fadeIn(effetTimeOut, function() {
                    if($(itemsSpan[itemToShow]).html() !== "") {
                        if($(itemsSpan[itemToShow]).css('bottom') === 0) {
                            $(itemsSpan[itemToShow]).slideUp(effetTimeOut);
                        } else {
                            $(itemsSpan[itemToShow]).slideDown(effetTimeOut);
                        }
                    }
                });
            } 
            fadeElement(false, nextFun);
        }
        
        if(items.length > 0) {
            fadeElement(true, function() { showIt(0); });
        } else {
            console.log("Poof..");
        }

    };

})(jQuery); 
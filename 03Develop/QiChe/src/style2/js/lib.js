(function ($) {
    $.fn.jqueryzoom = function (options) {
        var settings = {
            xzoom: 200,
            yzoom: 200,
            offset: 10,
            position: "right",
            lens: 1,
            preload: 1
        };
        if (options) {
            $.extend(settings, options);
        }
        var noalt = '';
        $(this).hover(function () {
            var imageLeft = $(this).offset().left;
            var imageTop = $(this).offset().top;
            var imageWidth = $(this).children('img').get(0).offsetWidth;
            var imageHeight = $(this).children('img').get(0).offsetHeight;
            noalt = $(this).children("img").attr("alt");
            var bigimage = $(this).children("img").attr("jqimg");
            $(this).children("img").attr("alt", '');
            if ($("div.zoomdiv").get().length == 0) {
                $(this).after("<div class='zoomdiv'><img class='bigimg' src='" + bigimage + "'/></div>");
                $(this).append("<div class='jqZoomPup'>&nbsp;</div>");
            }
            if (settings.position == "right") {
                if (imageLeft + imageWidth + settings.offset + settings.xzoom > screen.width) {
                    leftpos = imageLeft - settings.offset - settings.xzoom;
                } else {
                    leftpos = imageLeft + imageWidth + settings.offset;
                }
            } else {
                leftpos = imageLeft - settings.xzoom - settings.offset;
                if (leftpos < 0) {
                    leftpos = imageLeft + imageWidth + settings.offset;
                }
            }
            $("div.zoomdiv").css({ top: imageTop, left: leftpos });
            $("div.zoomdiv").width(settings.xzoom);
            $("div.zoomdiv").height(settings.yzoom);
            $("div.zoomdiv").show();
            if (!settings.lens) {
                $(this).css('cursor', 'crosshair');
            }
            $(document.body).mousemove(function (e) {
                mouse = new MouseEvent(e);
                var bigwidth = $(".bigimg").get(0).offsetWidth;
                var bigheight = $(".bigimg").get(0).offsetHeight;
                var scaley = 'x';
                var scalex = 'y';
                if (isNaN(scalex) | isNaN(scaley)) {
                    var scalex = (bigwidth / imageWidth);
                    var scaley = (bigheight / imageHeight);
                    $("div.jqZoomPup").width((settings.xzoom) / (scalex * 1));
                    $("div.jqZoomPup").height((settings.yzoom) / (scaley * 1));
                    if (settings.lens) {
                        $("div.jqZoomPup").css('visibility', 'visible');
                    }
                }
                xpos = mouse.x - $("div.jqZoomPup").width() / 2 - imageLeft;
                ypos = mouse.y - $("div.jqZoomPup").height() / 2 - imageTop;
                if (settings.lens) {
                    xpos = (mouse.x - $("div.jqZoomPup").width() / 2 < imageLeft) ? 0 : (mouse.x + $("div.jqZoomPup").width() / 2 > imageWidth + imageLeft) ? (imageWidth - $("div.jqZoomPup").width() - 2) : xpos;
                    ypos = (mouse.y - $("div.jqZoomPup").height() / 2 < imageTop) ? 0 : (mouse.y + $("div.jqZoomPup").height() / 2 > imageHeight + imageTop) ? (imageHeight - $("div.jqZoomPup").height() - 2) : ypos;
                }
                if (settings.lens) {
                    $("div.jqZoomPup").css({ top: ypos, left: xpos });
                }
                scrolly = ypos;
                $("div.zoomdiv").get(0).scrollTop = scrolly * scaley;
                scrollx = xpos;
                $("div.zoomdiv").get(0).scrollLeft = (scrollx) * scalex;
            });
        }, function () {
            $(this).children("img").attr("alt", noalt);
            $(document.body).unbind("mousemove");
            if (settings.lens) {
                $("div.jqZoomPup").remove();
            }
            $("div.zoomdiv").remove();
        });
        count = 0;
        if (settings.preload) {
            $('body').append("<div style='display:none;' class='jqPreload" + count + "'>360buy</div>");
            $(this).each(function () {
                var imagetopreload = $(this).children("img").attr("jqimg");
                var content = jQuery('div.jqPreload' + count + '').html();
                jQuery('div.jqPreload' + count + '').html(content + '<img src=\"' + imagetopreload + '\">');
            });
        }
    }
})(jQuery);
function MouseEvent(e) {
    this.x = e.pageX;
    this.y = e.pageY;
}
/*jdMarquee*/
(function($){$.fn.jdMarquee=function(option,callback){if(typeof option=="function"){callback=option;option={};};var s=$.extend({deriction:"up",speed:10,auto:false,width:null,height:null,step:1,control:false,_front:null,_back:null,_stop:null,_continue:null,wrapstyle:"",stay:5000,delay:20,dom:"div>ul>li".split(">"),mainTimer:null,subTimer:null,tag:false,convert:false,btn:null,disabled:"disabled",pos:{ojbect:null,clone:null}},option||{});var object=this.find(s.dom[1]);var subObject=this.find(s.dom[2]);var clone;if(s.deriction=="up"||s.deriction=="down"){var height=object.eq(0).outerHeight();var step=s.step*subObject.eq(0).outerHeight();object.css({width:s.width+"px",overflow:"hidden"});};if(s.deriction=="left"||s.deriction=="right"){var width=subObject.length*subObject.eq(0).outerWidth();object.css({width:width+"px",overflow:"hidden"});var step=s.step*subObject.eq(0).outerWidth();};var init=function(){var wrap="<div style='position:relative;overflow:hidden;z-index:1;width:"+s.width+"px;height:"+s.height+"px;"+s.wrapstyle+"'></div>";object.css({position:"absolute",left:0,top:0}).wrap(wrap);s.pos.object=0;clone=object.clone();object.after(clone);switch(s.deriction){default:case "up":object.css({marginLeft:0,marginTop:0});clone.css({marginLeft:0,marginTop:height+"px"});s.pos.clone=height;break;case "down":object.css({marginLeft:0,marginTop:0});clone.css({marginLeft:0,marginTop:-height+"px"});s.pos.clone=-height;break;case "left":object.css({marginTop:0,marginLeft:0});clone.css({marginTop:0,marginLeft:width+"px"});s.pos.clone=width;break;case "right":object.css({marginTop:0,marginLeft:0});clone.css({marginTop:0,marginLeft:-width+"px"});s.pos.clone=-width;break;};if(s.auto){initMainTimer();object.hover(function(){clear(s.mainTimer);},function(){initMainTimer();});clone.hover(function(){clear(s.mainTimer);},function(){initMainTimer();});};if(callback){callback();};if(s.control){initControls();}};var initMainTimer=function(delay){clear(s.mainTimer);s.stay=delay?delay:s.stay;s.mainTimer=setInterval(function(){initSubTimer()},s.stay);};var initSubTimer=function(){clear(s.subTimer);s.subTimer=setInterval(function(){roll()},s.delay);};var clear=function(timer){if(timer!=null){clearInterval(timer);}};var disControl=function(A){if(A){$(s._front).unbind("click");$(s._back).unbind("click");$(s._stop).unbind("click");$(s._continue).unbind("click");}else{initControls();}};var initControls=function(){if(s._front!=null){$(s._front).click(function(){$(s._front).addClass(s.disabled);disControl(true);clear(s.mainTimer);s.convert=true;s.btn="front";if(!s.auto){s.tag=true;};convert();});};if(s._back!=null){$(s._back).click(function(){$(s._back).addClass(s.disabled);disControl(true);clear(s.mainTimer);s.convert=true;s.btn="back";if(!s.auto){s.tag=true;};convert();});};if(s._stop!=null){$(s._stop).click(function(){clear(s.mainTimer);});};if(s._continue!=null){$(s._continue).click(function(){initMainTimer();});}};var convert=function(){if(s.tag&&s.convert){s.convert=false;if(s.btn=="front"){if(s.deriction=="down"){s.deriction="up";};if(s.deriction=="right"){s.deriction="left";}};if(s.btn=="back"){if(s.deriction=="up"){s.deriction="down";};if(s.deriction=="left"){s.deriction="right";}};if(s.auto){initMainTimer();}else{initMainTimer(4*s.delay);}}};var setPos=function(y1,y2,x){if(x){clear(s.subTimer);s.pos.object=y1;s.pos.clone=y2;s.tag=true;}else{s.tag=false;};if(s.tag){if(s.convert){convert();}else{if(!s.auto){clear(s.mainTimer);}}};if(s.deriction=="up"||s.deriction=="down"){object.css({marginTop:y1+"px"});clone.css({marginTop:y2+"px"});};if(s.deriction=="left"||s.deriction=="right"){object.css({marginLeft:y1+"px"});clone.css({marginLeft:y2+"px"});}};var roll=function(){var y_object=(s.deriction=="up"||s.deriction=="down")?parseInt(object.get(0).style.marginTop):parseInt(object.get(0).style.marginLeft);var y_clone=(s.deriction=="up"||s.deriction=="down")?parseInt(clone.get(0).style.marginTop):parseInt(clone.get(0).style.marginLeft);var y_add=Math.max(Math.abs(y_object-s.pos.object),Math.abs(y_clone-s.pos.clone));var y_ceil=Math.ceil((step-y_add)/s.speed);switch(s.deriction){case "up":if(y_add==step){setPos(y_object,y_clone,true);$(s._front).removeClass(s.disabled);disControl(false);}else{if(y_object<=-height){y_object=y_clone+height;s.pos.object=y_object;};if(y_clone<=-height){y_clone=y_object+height;s.pos.clone=y_clone;};setPos((y_object-y_ceil),(y_clone-y_ceil));};break;case "down":if(y_add==step){setPos(y_object,y_clone,true);$(s._back).removeClass(s.disabled);disControl(false);}else{if(y_object>=height){y_object=y_clone-height;s.pos.object=y_object;};if(y_clone>=height){y_clone=y_object-height;s.pos.clone=y_clone;};setPos((y_object+y_ceil),(y_clone+y_ceil));};break;case "left":if(y_add==step){setPos(y_object,y_clone,true);$(s._front).removeClass(s.disabled);disControl(false);}else{if(y_object<=-width){y_object=y_clone+width;s.pos.object=y_object;};if(y_clone<=-width){y_clone=y_object+width;s.pos.clone=y_clone;};setPos((y_object-y_ceil),(y_clone-y_ceil));};break;case "right":if(y_add==step){setPos(y_object,y_clone,true);$(s._back).removeClass(s.disabled);disControl(false);}else{if(y_object>=width){y_object=y_clone-width;s.pos.object=y_object;};if(y_clone>=width){y_clone=y_object-width;s.pos.clone=y_clone;};setPos((y_object+y_ceil),(y_clone+y_ceil));};break;}};if(s.deriction=="up"||s.deriction=="down"){if(height>=s.height&&height>=s.step){init();}};if(s.deriction=="left"||s.deriction=="right"){if(width>=s.width&&width>=s.step){init();}}}})(jQuery);

;(function(global, document, $){
	var sliderList = [];
	//buildSlider
	ds.buildSlider = function(shell, ops, buildHandler){
		if(!(shell = $(shell)).length){ return; }

		ops = ops || {};
		var 
		triggers = shell.find('.triggers a'),
		_ops = {
			duration: 400,
			unitSize: 880,
			imgLoadFlag: null,
			imgLoadHandler: ds.noop,
			onplay: function(inx, prevInx){
				if(ops.imgLoadFlag && !ops.imgLoadFlag[inx]){
					ops.imgLoadHandler.call(this, inx, prevInx);
					ops.imgLoadFlag[inx] = true;
				}

				prevInx > -1 && triggers.eq(prevInx).removeClass('current');
				triggers.eq(inx).addClass('current');
			}
		};
		for(var k in _ops){
			if(typeof ops[k] === 'undefined'){
				ops[k] = _ops[k];
			}
		}
		if(!ops.shell){
			ops.shell = shell.find('ul').eq(0);
			if(typeof ops.length !== 'number'){
				ops.length = ops.shell.find('li').length;
			}
		}

		var timer, slider = new (buildHandler || Slider)(ops);
		shell.delegate('a.prev,a.next', 'click', function(e){
			e.preventDefault();

			clearTimeout(timer);
			slider[this.className.indexOf('next')>-1 ? 'next' : 'prev']();
		})
		.hover(function(){
			slider.mouseEnter = true;
			slider.stopAuto();
		}, function(){
			slider.mouseEnter = false;
			slider.autoPlay();
		});
		triggers.bind('click', function(e){
			e.preventDefault();
		})
		.hover(function(){
			clearTimeout(timer);
			var self = this;
			timer = setTimeout(function(){
				slider.play(triggers.index(self));
			}, 160);
		}, function(){
			clearTimeout(timer);
		});

		sliderList.push(slider);
		slider.shellWrap = shell;
		
		//Fix IE6 hover
		if(ds.isIE6){
			var prevAndNext = shell.find('a.prev,a.next');
			shell.hover(function(){
				prevAndNext.show();
			}, function(){
				prevAndNext.hide();
			});
		}
		return slider;
	};



	//scroll
	var 
	scrollTimer,
	view = $(global),
	checkScroll = function(){
		var 
		viewHeight = view.height(),
		scrollTop = view.scrollTop();
		//checkSlider in viewport
		$.each(sliderList, function(){
			var 
			offsetTop = this.shellWrap.offset().top,
			height = this.shellWrap.height();
			if( !this.mouseEnter && ( (offsetTop >= scrollTop && offsetTop <= scrollTop+viewHeight)
				|| (offsetTop+height >= scrollTop && offsetTop+height <= scrollTop+viewHeight) )
			){
				this.autoPlay();
			}
			else{
				this.stopAuto();
			}
		});

	},
	scrollHandler = function(){
		clearTimeout(scrollTimer);
		scrollTimer = setTimeout(checkScroll, 128);
	};
	view.bind('scroll resize', scrollHandler);
	scrollHandler();
})(window, document, jQuery);

//Banner
jQuery(function($){
    //var baseUrl = window.baseJSUrl || 'js/';
    //alert(baseJSUrl);
 
    ds.loadScript('/style2/js/jquery.FadeList.js', function () {
		var slider = ds.buildSlider('#home_banner', {
			delay: 3200,
			imgLoadFlag: [true],
			imgLoadHandler: function(inx){
				var panel = this.items.eq(inx), img = panel.find('img'), url = img.attr('longDesc');

				panel.css('backgroundImage', 'url('+ url +')');
				img.attr('src', url);
			}
		}, window.FadeList);
	});
});


 
 
 
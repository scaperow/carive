/**
 * myq add 2014-11-18，用于处理广告box内多个图片的切换问题
 * config.element,包含slider-box的外层元素
 * config.interval,图片自动切换的间隔,单位为秒
 * config.animation,图片之间切换的动画模式，预留，暂时只支持dispear模式
 */
haux.component.Switch = function(config){
	//0.提取config中的参数，初始化
	this._element = config.element;
	this._sleepTime = config.sleepTime || 5000;
	this._flashTime = config.flashTime || 1000;
	this._animation = config.animation || "dispear";
	this._switchCount = config.switchCount;
	this._iterator = 0;
	
	haux.dom.fixElement(this._element);
	this._forwardBtn = this._element.getElementsByClassName("next")[0];
	this._backBtn = this._element.getElementsByClassName("previous")[0];
	this._scrollDiv = this._element.getElementsByClassName("scroll-content")[0];
	
	this._navDiv = this._element.getElementsByClassName("nav-point")[0];

	var scrollLiElements = this._scrollDiv.getElementsByTagName("li");
	this._count = scrollLiElements.length;
	if(this._count <= this._switchCount){
		return;
	}
	
	//2.为slider-box中的前进、后退按钮添加切换事件相应函数
	var switchObj = this;
	this._forwardBtn.onclick = function(){
		switchObj.switchNext();
		switchObj.startAutoSwitch();
	}
	this._backBtn.onclick = function(){
		switchObj.switchPrevious();
		switchObj.startAutoSwitch();
	}
	
	//3.为box下方的 缩略图/圆点 设置事件响应函数
	if(this._navDiv){
		var liElements = this._navDiv.getElementsByTagName("li");
		for(var i = 0, len = liElements.length; i < len; i++){
			var liElement = liElements[i];
			liElement.setAttribute("switch-index", i);
			liElement.onclick = function(){
				var switchIndex = this.getAttribute("switch-index");
				switchObj.switchTo(switchIndex);
				switchObj.startAutoSwitch();
			}
		}
	}
}


haux.component.Switch.prototype.switchNext = function(){
	var index = this._iterator + 1;
	if(index >= Math.ceil(this._count / this._switchCount)){
		index = 0;
	}
	this.switchTo(index);
}

haux.component.Switch.prototype.switchPrevious = function(){
	var index = this._iterator - 1;
	if(index < 0){
		index = Math.ceil(this._count / this._switchCount) - 1;
	}
	this.switchTo(index);
}

haux.component.Switch.prototype.switchTo = function(targetIndex){
	if(this._iterator == targetIndex){
		return;
	}	
	var render = this.getRender();
	
	render.switchTo(this._iterator, parseInt(targetIndex), this._switchCount, 
		this._scrollDiv, this._navDiv, this._flashTime);	
	
	this._iterator = targetIndex;
}

haux.component.Switch.prototype.startAutoSwitch = function(){
	if(this._count <= 1){
		return;
	}
	
	if(this._interval){
		clearInterval(this._interval);
	}
	var switchObj = this;
	this._interval = setInterval(function(){
		switchObj.switchNext();
	}, this._sleepTime);
}

haux.component.Switch.prototype.getRender = function(){
	switch(this._animation){
		case "vertical":
			return haux.component.Switch.VerticalRender;
		case "horizontal":
			return haux.component.Switch.HorizontalRender;
		default:
			return haux.component.Switch.DispearRender;
	}
}

haux.component.Switch.DispearRender = function(){
	
}

haux.component.Switch.DispearRender._switchNav = function(navDiv, currentIndex, flashTime){
	var liElements = navDiv.getElementsByTagName("li");
	setTimeout(function(){
		for(var i = 0, len = liElements.length; i < len; i++){
			var liElement = liElements[i];
			liElement.className = (i == currentIndex) ? "current" : "";
		}
	}, flashTime);
}

haux.component.Switch.DispearRender.switchTo = function(currentIndex, targetIndex, switchCount, 
	scrollDiv, navDiv, flashTime){
	
	var liElements = scrollDiv.getElementsByTagName("li");
	var oldLiElements = [];
	for(var i = currentIndex * switchCount; i < liElements.length && i < currentIndex * switchCount + switchCount; i++){
		oldLiElements.push(liElements[i]);
	}
	
	var newLiElements = [];
	for(var i = targetIndex * switchCount; i < liElements.length && i < targetIndex * switchCount + switchCount; i++){
		newLiElements.push(liElements[i]);
	}
	
	//2.改变navDiv 中li元素的selected效果
	
	
	//1.把毫秒切成N个等分，相当于动画分解成N个贞，并确定每个动画贞需要偏移的距离
	var actions = [];
	var segCount = 50
	var segTime = Math.floor(flashTime / segCount);
	for(var i = 1; i < segCount; i++){
		actions.push({t : segTime * i, o : 1 - i / 50});
	}
	actions.push({t : flashTime, o : 0});
	
	//2.执行actions中的动画效果，不断改变scrollDiv.scrollLeft，以达到滑动视觉效果
	for(var i = 0; i < actions.length; i++){
		var action = actions[i];
		(function(interval, opacity){
			setTimeout(function(){
				for(var j = 0; j < oldLiElements.length; j++){
					oldLiElements[j].style.opacity = opacity;
				}
			}, interval);
			//console.log("setTimeout " + interval + ", " + scrollLeft);
		})(action.t, action.o);
	}
	setTimeout(function(){
		for(var j = 0; j < oldLiElements.length; j++){
			oldLiElements[j].style.display = "none";
			oldLiElements[j].style.opacity = "";
		}
		for(var j = 0; j < newLiElements.length; j++){
			newLiElements[j].style.display = "block";
		}
	}, flashTime);
}
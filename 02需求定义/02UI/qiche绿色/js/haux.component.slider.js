/**
 * myq add 2014-11-18，用于处理首页的滚动图片
 * config.element,包含slider-box的外层元素
 * config.interval,图片自动切换的间隔,单位为秒
 * config.animation,图片之间切换的动画模式，预留，暂时只支持垂直(vertical)和水平(horizontal )等其它模式
 */
haux.component.Slider = function(config){
	//0.提取config中的参数，初始化
	this._element = config.element;
	this._flashTime = config.flashTime || 2000;
	this._sleepTime = config.sleepTime || 5000;
	this._animation = config.animation || "horizontal";
	this._iterator = 0;
	
	haux.dom.fixElement(this._element);
	this._forwardBtn = this._element.getElementsByClassName("next")[0];
	this._backBtn = this._element.getElementsByClassName("previous")[0];
	this._scrollDiv = this._element.getElementsByClassName("scroll-content")[0];
	
	
	this._navDiv = this._element.getElementsByClassName("nav-point")[0] 
		|| this._element.getElementsByClassName("nav")[0];

	var scrollLiElements = this._scrollDiv.getElementsByTagName("li");
	this._count = scrollLiElements.length;
	if(this._count <= 1){
		this._forwardBtn.style.display = "none";
		this._backBtn.style.display = "none";
		return;
	}
	this._firstLiElement = scrollLiElements[0];
	this._lastLiElement = scrollLiElements[this._count - 1];
	
	//2.为slider-box中的前进、后退按钮添加切换事件相应函数
	var sliderObj = this;
	this._forwardBtn.onclick = function(){
		sliderObj.switchNext();
		sliderObj.startAutoSwitch();
	}
	this._backBtn.onclick = function(){
		sliderObj.switchPrevious();
		sliderObj.startAutoSwitch();
	}
	
	//3.为box下方的 缩略图/圆点 设置事件响应函数
	if(this._navDiv){
		var liElements = this._navDiv.getElementsByTagName("li");
		for(var i = 0, len = liElements.length; i < len; i++){
			var liElement = liElements[i];
			liElement.setAttribute("slider-index", i);
			liElement.onclick = function(){
				var sliderIndex = this.getAttribute("slider-index");
				sliderObj.switchTo(sliderIndex);
				sliderObj.startAutoSwitch();
			}
		}
	}

	
	//4.启动定时器，以便自动切换
	//this.startAutoSwitch();
}

haux.component.Slider.seriesIndex = 0;
haux.component.Slider.instances = {};

haux.component.Slider.prototype.switchNext = function(){
	var index = this._iterator + 1;
	if(index >= this._count){
		index = 0;
	}
	this.switchTo(index);
}

haux.component.Slider.prototype.switchPrevious = function(){
	var index = this._iterator - 1;
	if(index < 0){
		index = this._count - 1;
	}
	this.switchTo(index);
}

haux.component.Slider.prototype.switchTo = function(targetIndex){
	if(this._iterator == targetIndex){
		return;
	}
	
	var render = this.getRender();
	if(this._iterator == this._count - 1 && targetIndex == 0){
		//以最后一个图片为起始，伪装平滑切换到第一个图片，实际上是切换到后面的this._firstLiClone去
		render.switchFromLastToFirst(this._firstLiElement, this._lastLiElement, this._navDiv, this._flashTime);	
	}
	else if(this._iterator == 0 && targetIndex == this._count - 1){
		//以第一个图片为起始，伪装平滑切换到最后一个图片，实际上是切换到前面的this._lastLiClone去
		render.switchFromFirstToLast(this._firstLiElement, this._lastLiElement, this._navDiv, this._flashTime);	
	}
	else{
		render.switchTo(this._iterator, targetIndex, this._scrollDiv, this._navDiv, this._flashTime);	
	}
	
	
	this._iterator = parseInt(targetIndex);
}

haux.component.Slider.prototype.startAutoSwitch = function(){
	if(this._count <= 1){
		return;
	}
	
	if(this._interval){
		clearInterval(this._interval);
	}
	var sliderObj = this;
	this._interval = setInterval(function(){
		sliderObj.switchNext();
	}, this._sleepTime);
}

haux.component.Slider.prototype.getRender = function(){
	switch(this._animation){
		case "vertical":
			return haux.component.Slider.VerticalRender;
		case "horizontal":
			return haux.component.Slider.HorizontalRender;
		default:
			return haux.component.Slider.HorizontalRender;
	}
}

haux.component.Slider.HorizontalRender = function(){
	
}
haux.component.Slider.HorizontalRender.switchFromLastToFirst = function(firstLiElement, lastLiElement, navDiv, flashTime){
	//0.预处理
	var targetLiElement = null;
	if(!firstLiElement.getAttribute("slider-clone")){
		targetLiElement = firstLiElement.cloneNode(true);
		targetLiElement.className = "fist-li-clone";
		firstLiElement.parentNode.appendChild(targetLiElement);
		firstLiElement.setAttribute("slider-clone", "true");
	}
	else{
		targetLiElement = lastLiElement.nextSibling;
		while(targetLiElement.tagName != "LI"){
			targetLiElement = targetLiElement.nextSibling;
		}
	}
	
	//1.启动切换动画
	this._switchImg(lastLiElement, targetLiElement, flashTime);
	
	//2.改变navDiv 中li元素的selected效果
	this._switchNav(navDiv, 0, flashTime);
}

haux.component.Slider.HorizontalRender._switchNav = function(navDiv, currentIndex, flashTime){
	var liElements = navDiv.getElementsByTagName("li");
	setTimeout(function(){
		for(var i = 0, len = liElements.length; i < len; i++){
			var liElement = liElements[i];
			liElement.className = (i == currentIndex) ? "current" : "";
		}
	}, flashTime);
}

haux.component.Slider.HorizontalRender.switchFromFirstToLast = function(firstLiElement, lastLiElement, navDiv, flashTime){
	var targetLiElement = null;
	if(!lastLiElement.getAttribute("slider-clone")){
		targetLiElement = lastLiElement.cloneNode(true);
		targetLiElement.className = "last-li-clone";
		firstLiElement.parentNode.insertBefore(targetLiElement, firstLiElement);
		lastLiElement.setAttribute("slider-clone", "true");
	}
	else{
		targetLiElement = firstLiElement.previousSibling;
		while(targetLiElement.tagName != "LI"){
			targetLiElement = targetLiElement.previousSibling;
		}
	}
	
	//1.启动切换动画
	this._switchImg(firstLiElement, targetLiElement, flashTime);
	
	//2.改变navDiv 中li元素的selected效果
	this._switchNav(navDiv, navDiv.getElementsByTagName("li").length - 1, flashTime);
}

haux.component.Slider.HorizontalRender.switchTo = function(currentIndex, targetIndex, scrollDiv, navDiv, flashTime){
	var liElements = scrollDiv.getElementsByTagName("li");
	targetIndex = parseInt(targetIndex);
	if(liElements[0].className == 'last-li-clone'){
		this._switchImg(liElements[currentIndex + 1], liElements[targetIndex + 1], flashTime);
	}
	else{
		this._switchImg(liElements[currentIndex], liElements[targetIndex], flashTime);
	}
	
	//2.改变navDiv 中li元素的selected效果
	this._switchNav(navDiv, targetIndex, flashTime);
}

haux.component.Slider.HorizontalRender._switchImg = function(startLiElement, endLiElement, flashTime){
	//0.计算当前页面和目标页面之间的距离
	
	var startScrollLeft = startLiElement.offsetLeft;
	var endScrollLeft = endLiElement.offsetLeft;
	var offsetScrollLeft = endScrollLeft - startScrollLeft;
	
	//1.把毫秒切成N个等分，相当于动画分解成N个贞，并确定每个动画贞需要偏移的距离
	var actions = [];
	var segCount = 50
	var segTime = Math.floor(flashTime / segCount);
	var segWidth = Math.floor(offsetScrollLeft / segCount);
	for(var i = 1; i < segCount; i++){
		actions.push({t : segTime * i, s : startScrollLeft + segWidth * i});
	}
	actions.push({t : flashTime, s : endScrollLeft});
	
	//2.执行actions中的动画效果，不断改变scrollDiv.scrollLeft，以达到滑动视觉效果
	var scrollDiv = startLiElement.parentNode.parentNode;
	for(var i = 0; i < actions.length; i++){
		var action = actions[i];
		(function(interval, scrollLeft){
			setTimeout(function(){
				scrollDiv.scrollLeft = scrollLeft;
			}, interval);
			//console.log("setTimeout " + interval + ", " + scrollLeft);
		})(action.t, action.s);
	}
}

haux.component.Slider.VerticalRender = {};
for(var r in haux.component.Slider.HorizontalRender){
	haux.component.Slider.VerticalRender[r] = haux.component.Slider.HorizontalRender[r];
}

haux.component.Slider.VerticalRender._switchImg = function(startLiElement, endLiElement, flashTime){
	//0.计算当前页面和目标页面之间的距离
	
	var startScrollTop = startLiElement.offsetTop;
	var endScrollTop = endLiElement.offsetTop;
	var offsetScrollTop = endScrollTop - startScrollTop;
	
	//1.把毫秒切成N个等分，相当于动画分解成N个贞，并确定每个动画贞需要偏移的距离
	var actions = [];
	var segCount = 50
	var segTime = Math.floor(flashTime / segCount);
	var segWidth = Math.floor(offsetScrollTop / segCount);
	for(var i = 1; i < segCount; i++){
		actions.push({t : segTime * i, s : startScrollTop + segWidth * i});
	}
	actions.push({t : flashTime, s : endScrollTop});
	
	//2.执行actions中的动画效果，不断改变scrollDiv.scrollTop，以达到滑动视觉效果
	var scrollDiv = startLiElement.parentNode.parentNode;
	for(var i = 0; i < actions.length; i++){
		var action = actions[i];
		(function(interval, scrollTop){
			setTimeout(function(){
				scrollDiv.scrollTop = scrollTop;
			}, interval);
			//console.log("setTimeout " + interval + ", " + scrollTop)		
		})(action.t, action.s);
	}
}
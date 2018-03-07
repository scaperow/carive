/**
 * myq add 2014-12-23,联动显示组件，用于控制鼠click/进入 srcElement元素后，相关的联动显示逻辑
 * @param {Object} srcElement
 * @param {Object} targetElements
 */
haux.component.LinkageDisplay = function(source, follows, action){
	this._source = source;
	haux.dom.fixElement(source);
	this._follows = follows;
	this._action = action || "hover";
	var linkageObj = this;
	
	//1.根据触发条件，为发起元素设置对应的事件响应函数 
	if(this._action == "hover"){
		source.onmouseover = function(ev){
			linkageObj._show();
			//haux.component.LinkVisible._show(source, follows);
		}
	}
	else if(this._action == "click"){
		source.onclick = function(ev){
			if(this.containClass("hover")){//已显示，点击则需要关闭
				//haux.component.LinkVisible._hide(source, follows);
				linkageObj._hide();
			}	
			else{//未显示，打开		
				//haux.component.LinkVisible._show(source, follows);
				linkageObj._show();
			}
		}
	}
	
	//2.确保source元素能发起关闭
	source.onmouseout = function(ev){
		if(linkageObj._remainFocus(ev)){
			return;
		}
		linkageObj._hide();
	}
	//3.确保follow elements能够正常发起关闭操作
	for(var i = 0; i < follows.length; i++){
		var follow = follows[i];
		haux.dom.fixElement(follow);
	}
} 

haux.component.LinkageDisplay.prototype._show = function(){
	this._source.addClass("hover");
	var linkageObj = this;
	for(var i = 0; i < this._follows.length; i++){
		var follow = this._follows[i];
		follow.addClass("hover");
		follow.onmouseout = function(ev){
			if(linkageObj._remainFocus(ev)){
				return;
			}
			linkageObj._hide();
		}
	}
}
haux.component.LinkageDisplay.prototype._hide = function(){
	this._source.removeClass("hover");
	for(var i = 0; i < this._follows.length; i++){
		var follow = this._follows[i];
		follow.removeClass("hover");
		follow.onmouseout = null;
	}
}

haux.component.LinkageDisplay.prototype._remainFocus = function(ev){
	ev = ev || window.event;
	var toElement = ev.relatedTarget || ev.toElement;
	if(toElement == null){
		return true;//ie6-7 bug，鼠标滑动到<s>上，会无缘无故的产生一个onmouseout事件，且srcElement = <s>，toElement = null
	}
	if(this._source == toElement || this._source.hasChild(toElement)){
		return true;
	}
	//鼠标移动到了follow元素中，也不需要干什么
	for(var i = 0; i < this._follows.length; i++){
		var follow = this._follows[i];
		if(follow == toElement || follow.hasChild(toElement)){
			return true;
		}
	}
	return false;
}
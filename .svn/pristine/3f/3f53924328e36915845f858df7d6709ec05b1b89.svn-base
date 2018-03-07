haux.component.Tab = function(config){
	this._element = config.element;	
	this._action = config.action || "click";//支持 click、hover两种模式，默认click
	var dlElement = this._element.getElementsByTagName("dl")[0];
	
	var tabLabels = [];
	var tabContents = [];
	var childNode = dlElement.firstChild;
	
	while(childNode){
		haux.dom.fixElement(childNode);
		if(childNode.tagName == "DT" && childNode.containClass("tab-label")){
			tabLabels.push(childNode);
		}	
		else if(childNode.tagName == "DD" && childNode.containClass("tab-content")){
			tabContents.push(childNode);
		}
		childNode = childNode.nextSibling;
	}
	for(var i = 0; i < tabLabels.length; i++){
		var actionName = this._action == "click" ? "onclick" : "onmouseover";
		tabLabels[i][actionName] = function(){
			for(var j = 0; j < tabLabels.length; j++){
				var selected = tabLabels[j] == this;
				if(selected){
					tabLabels[j].addClass("selected");
					tabContents[j].addClass("selected");
				}
				else{
					tabLabels[j].removeClass("selected");
					tabContents[j].removeClass("selected");
				}
			}
		}
		
	}
}

haux.dom.addBodyLoadAction(function(){
	haux.dom.fixElement(document);
	var tabElements = document.getElementsByClassName("tab-box");
	for(var i = 0, len = tabElements.length; i < len; i++){
		var tabElement = tabElements[i];
		new haux.component.Tab({
			element:tabElement,
			action:tabElement.getAttribute("tabaction")
		});
	}
});

/**
	myq 2013-4-23 add，针对portal端，仅保留最基本的js扩展
	该文件主要作用如下：
		a.定义自定义js组建的名字空间 
		b.设置全局变量和函数
		c.完成通用的页面初始化工作
**/

/***********************************************************************************************
	Part 0 —— 定义huax js扩展库名字空间，创建通用的haux基础方法
***********************************************************************************************/
if(!window.haux){
	var haux = {};
	//0.1 基本的js语法补充代码，涉及对象、数组、字符串等，与浏览器无关
	haux.util = {};
	
	//0.2 window、nagigator、screen、histroy、lication等浏览器框架相关js代码
	haux.bom = {};
	
	//0.3 dom相关代码，主要是针对document内的元素进行操作的代码
	haux.dom = {};
	
	//0.4 定义系统自定义的前端组件，如itree、imenu等
	haux.component = {};
}

/***********************************************************************************************
	Part 1 —— 定义全局变量，将全部通用常量都保存在这里
***********************************************************************************************/
var GLOBAL = {};
//2.1浏览器相关常量属性
try{
	var ua = navigator.userAgent.toLowerCase();
	if (window.ActiveXObject || "ActiveXObject" in window){
		GLOBAL.isIE = true;
		/*GLOBAL.isIE6 = GLOBAL.isIE && !window.XMLHttpRequest;    
		GLOBAL.isIE7 = GLOBAL.isIE && !GLOBAL.isIE6 && !GLOBAL.isIE8;
		GLOBAL.isIE8 = GLOBAL.isIE && !!document.documentMode;   
		GLOBAL.isIE9 = document.documentMode && document.documentMode ===9;*/
	} 
	else if (document.getBoxObjectFor){
		GLOBAL.isFirefox = true;
	}
	else if (window.MessageEvent && !document.getBoxObjectFor){
		GLOBAL.isChrome = true;
	}
	else if (window.opera){
		GLOBAL.isOpera = true;
	}
	else if (window.openDatabase){
		GLOBAL.isSafari = true;
	}
}
catch(err){
	alert("haux.min.js failed:\n" + err);
}
       

/***********************************************************************************************
	Part 2 —— 创建全局haux基础方法，
***********************************************************************************************/

/*
	版本信息：myq 2013-5-8 add。
		
	函数说明：
		扩展document.createElement函数，解决ie6-ie8下element.type属性只读的bug，同时可快速设定各项attribute值
	
	编码背景：
		1.ie6-ie8下,input、button的type、name、id等属性是只读的，导致通过document.createElement创建元素后，无法继续设置上述属性值
			需要利用ie提供的非标准语法，创建跨浏览器通用的createElement方法，满足创建element时自定义type属性的需求
		2.同时，采用标准dom语法创建element时，如果element的自定义属性比较多的时候，还存在需要连续设置id、value、innerHTML等属性，
			比较复杂，宜采用一次性生成的方式；
	参数说明：
		tagName：element的tagName，如input、button、textarea等；
		attributeObj：element属性对象，记录element所需要设置的属性名和属性值（限文本类型），格式如下{name:"age", type:"text", value:"30", disabled:"true"}
*/
haux.dom.createElement = function(tagName, attributeObj){
	var targetElement;
	if(GLOBAL.isIE6 || GLOBAL.isIE7 || GLOBAL.isIE8){
		var elementHtml = "<" + tagName;
		if(attributeObj)
			for(property in attributeObj){
				var proValue = attributeObj[property];
				if(proValue == null || proValue == undefined)
					continue;
				if(property == "innerHTML" || property == "className")
					continue;//innerHTML需要创建
				else
					elementHtml += " " + property + "=\"" + proValue.replace(/\"/g, "&quot;") + "\"";
			}
		elementHtml += "></" + tagName + ">";
		//alert("生成：" + elementHtml);
		targetElement = document.createElement(elementHtml);
		//补充innerHTML等属性
		if(attributeObj.innerHTML){
			targetElement.innerHTML = attributeObj.innerHTML;
		}
		if(attributeObj.className){
			targetElement.className = attributeObj.className;
		}
	}
	else{
		var targetElement = document.createElement(tagName);
		if(attributeObj){
			for(property in attributeObj){
				var proValue = attributeObj[property];
				if(proValue == null || proValue == undefined)
					continue;
				if(property == "innerHTML")
					targetElement.innerHTML = proValue;
				else if(property == "className")
					targetElement.className = proValue;
				else
					targetElement.setAttribute(property, proValue);
			}
		}
	}
	return targetElement;
}

/*
	版本信息：myq 2013-5-8 add。
		
	函数说明：扩展dom二级事件处理程序，包括添加事件响应函数、删除事件响应函数等
	参数说明：element—目标element元素，eventName—事件名称(去掉开头的on),handlerFunc—事件响应函数
*/
haux.dom.addEventHandler = function(element, eventName, handlerFunc){
	if(element.addEventListener){
		//chrome/firefox
		element.addEventListener(eventName, handlerFunc, false);
	}
	else if(element.attachEvent){
		//ie6+，注意采用这种方法邦定的事件响应函数，函数执行时this=window，而非element对象
		//此时，需要在响应函数中，通过参数event的target属性，才能找回element对象
		element.attachEvent("on" + eventName, handlerFunc)
	}
	else{
		//ie5 or更古老的ie浏览器，基本不会出现此现象
		element["on" + eventName] = handlerFunc;
	}
}

haux.dom.removeEventHandler = function(element, eventName, handlerFunc){
	if(element.removeEventListener){
		//chrome/firefox
		element.removeEventListener(eventName, handlerFunc, false);
	}
	else if(element.detachEvent){
		//ie6+
		element.detachEvent("on" + eventName, handlerFunc)
	}
	else{
		//ie5 or更古老的ie浏览器，基本不会出现此现象
		element["on" + eventName]= null;
	}
}
//阻止event事件冒泡，使得event不再触发外层element的对应事件响应函数
haux.dom.stopPropagateEvent = function(ev){
	if(GLOBAL.isIE)
		ev.cancelBubble = true;
	else
		ev.stopPropagation();
}

//阻止event事件引发的浏览器默认行为
haux.dom.stopDefaultEvent = function(ev){
	if(GLOBAL.isIE){
		ev.returnValue = false;
	}
	else{
		ev.preventDefault();
	}
}

haux.dom.addCssFile = function(fileSrc){
	var linkElement = document.createElement('link');
	linkElement.setAttribute("rel", "stylesheet");
	linkElement.setAttribute("type", "text/css");
	linkElement.setAttribute("href", fileSrc);
	document.getElementsByTagName("head")[0].appendChild(linkElement);
}

haux.dom.addJsFile = function(fileSrc){
	var scriptElement= document.createElement("script"); 
    scriptElement.type = "text/javascript"; 
    scriptElement.src = fileSrc; 
	document.getElementsByTagName("head")[0].appendChild(scriptElement);
}


haux.util.getType = function(obj){
	if(obj === null)
		return "null";
	
	var type = typeof(obj);
	if ("object" == type) {
		if (Object.prototype.toString.call(obj) === '[object Array]')
			return "array";
		if (Object.prototype.toString.call(obj) === '[object RegExp]')
			return "regexp";
	}
	return type;
}

/*
	json对象-字符串转换功能
*/
haux.util.Json = {};

/*	版本信息：myq 2013-4-24 add。
		
	函数说明：
		将js数据类型转换为json字符串,支持object,array,string,function,number,boolean,regexp等
	
	算法说明：
		1.判断数据类型
		2.分类处理
		
	参数说明：jsonObj—目标js对象
*/
haux.util.Json.getString = function (jsonObj) {
	//0.预处理空值
	if(jsonObj === null)
		return null;
	//1.判断对象的数据类型	
	var type =  haux.util.getType(jsonObj);
	
	//2.处理不同的数据类型
	switch (type) {
	  case "undefined":
	  	return "undefined";
	  case "unknown":
		return;
	  case "function":
	  	return;
	  case "boolean":
	    return jsonObj ? "true" : "false";
	  case "regexp":
		return jsonObj.toString();
	  case "number":
		return isFinite(jsonObj) ? jsonObj.toString() : "null";
	  case "string":
		return "\"" + jsonObj.replace(/(\\|\")/g, "\\$1").replace(/\n|\r|\t/g, function () {
			var a = arguments[0];
			return (a == "\n") ? "\\n" : (a == "\r") ? "\\r" : (a == "\t") ? "\\t" : "";
		}) + "\"";
		break;
	  case "object":
		if (jsonObj === null) {
			return "null";
		}
		var results = [];
		for (var property in jsonObj) {
			
			var value = jsonObj[property];
			if(value === jsonObj)//防止属性指向自己，形成死循环
				continue;

			if (value !== undefined) {
				results.push(property + ":" + haux.util.Json.getString(value));
			}
		}
		return "{" + results.join(",") + "}";
		break;
	  case "array":
		var results = [];
		for (var i = 0; i < jsonObj.length; i++) {
			var value = haux.util.Json.getString(jsonObj[i]);
			if (value !== undefined) {
				results.push(value);
			}
		}
		return "[" + results.join(",") + "]";
		break;
	}
};

/*	版本信息：myq 2013-4-24 add。
		
	函数说明：
		将json字符串转换为js对象
	
	算法说明：
		1.使用eval方式将String转为对象
		2.对不正确的json数据格式，返回null
		
	参数说明：jsonObj—目标js对象
*/
haux.util.Json.getObject = function (jsonStr, defaultObj){
	if(!jsonStr)
		return defaultObj || null;
	
	try{
		return eval("(" + jsonStr + ")");
	}
	catch(err){
		
	}
	return defaultObj || null;
	
}

/***********************************************************************************************
	Part 4 —— 全局页面修正、框架调整、页面渲染等
*********************************************************************s**************************/
//4.公用js函数定义

function home() {
	var _home;
	var win = window;
	while (!_home && win) {
		_home = win._home || win.top._home;
		win = win.opener;_home="/htw";
	}
	return _home;
}


/***********************************************************************************************
	Part 5 —— 基本类型扩展
***********************************************************************************************/
String.prototype.trim= function(){  
    // 用正则表达式将前后空格  
    // 用空字符串替代。  
    return this.replace(/(^\s*)|(\s*$)/g, "");  
}
Array.prototype.indexOf = function(target){
	for(var i = 0; i < this.length; i++)
		if(this[i] === target)
			return i;
	return -1;
}
Array.prototype.remove = function(target){
	var index = this.indexOf(target)
	if(index >= 0)
  		this.splice(index, 1);
}
Array.prototype.contain = function(el){
	for (var i = 0; i < this.length; i++){
		if (this[i] === el){
			return true;
		}
	}
	return false;
};

haux.dom._elementExtFuncs = {
	containClass : function(className){
		if(!className || ! this.className)
			return false;
			
		return this.className == className 
			|| (new RegExp("^" + className + " | " + className + "$| " + className + " ")).test(this.className);
	},
	removeClass : function(className){
		if(this.containClass(className)){
			//this.className = nodeClassName.replace(new RegExp("^" + className + " | " + className + "$| " + className + " "), ""); 
			var classNames = this.className.split(" ");
			
			for(var i = 0; i < classNames.length; i++){
				if (classNames[i] == className){
					classNames.splice(i, 1);
					this.className = classNames.join(" ");
					return true;
				}
			}
		}
		return false;
	},
	replaceClass : function(oldClassName, newClassName){
		if(this.containClass(oldClassName)){
			//this.className = nodeClassName.replace(new RegExp("^" + className + " | " + className + "$| " + className + " "), ""); 
			var classNames = this.className.split(" ");
			for(var i = 0; i < classNames.length; i++){
				if (classNames[i] == oldClassName){
					classNames[i] = newClassName;
					this.className = classNames.join(" ");
					return true;
				}
			}
		}
		return false;
	},
	addClass : function(className){
		if(this.containClass(className))
			return false;
		
		this.className = !this.className ? className : this.className + " " + className;
		
		return true;
	},
	hasChild : function(targetElement){
		var parentNode = targetElement.parentNode;
		while(parentNode){
			if(this == parentNode)
				return true;
			parentNode = parentNode.parentNode;
		}
		return false;
	},
	containOrEqual : function(targetElement){
		return this == targetElement || this.contain(targetElement);
	},
	getElementsByClassName : function(className){
		var result = [];
		var elements = [this];
		//ie6-7浏览器不支持document.createNodeIterator，只能自己写 
		while(elements.length){
			var targetElement = elements.shift();
			if(targetElement.className && targetElement.className.split(" ").contain(className)){
				result.push(targetElement);
			}
			var childNode = targetElement.firstChild; 
			while(childNode){
				if(childNode.tagName){
					elements.push(childNode);
				}
				childNode = childNode.nextSibling;
			}
		}
		
		return result;
	}
}

if(window.Element){
	for(var funcName in haux.dom._elementExtFuncs){
		if(!Element.prototype[funcName]){
			Element.prototype[funcName] = haux.dom._elementExtFuncs[funcName];
		}
	}
}

//myq add 2014-11-18，针对ie6/ie7/ie8被过度保护的问题，手动扩展具体的element元素
haux.dom.fixElement = function(targetElement){
	for(var funcName in haux.dom._elementExtFuncs){
		if(!targetElement[funcName]){
			targetElement[funcName] = haux.dom._elementExtFuncs[funcName];
		}
	}
}

haux.dom.createOptions = function(selectElement, optionArray, valueName, textName, selectedValue){
	if(typeof optionArray == "string"){
		try{
			optionArray = eval("(" + optionArray + ")");
		}
		catch(e){
			optionArray = [];
		}
	}
		
	for(var i = 0; i < optionArray.length; i++){
		var optionObj = optionArray[i];
		var optionValue;
		var optionText;
		if(typeof optionObj == "string" || typeof optionObj == "number"){
			optionText = optionObj;
			optionValue = optionObj;
		}
		else{
			optionValue = optionObj[valueName];
			optionText = optionObj[textName];
		}
		var optionElement = document.createElement("option");
		optionElement.value = optionValue;
		optionElement.innerHTML = optionText;
		if(optionValue == selectedValue)
			optionElement.selected = "selected";
		
		selectElement.appendChild(optionElement);
	}
}

/**
 * myq add 2015-5-8，在页面body元素加载完成后，执行action函数对应的初始化页面逻辑
 * 传统的onload事件是在页面所有的图片、flash、音频加载完成后才执行的，导致复杂页面加载速度慢的时候，容易有很长时间不能进行操作
 */
haux.dom.addBodyLoadAction = function(action){
	//1.启动定时器，监听document.body是否创建成功（此时image,flash可能还没加载完毕）
	var interval = setInterval(function(){
		if(document.body){
			//2.body元素已被创建，不再等待image元素加载（onload有这个问题），而是立即执行
			clearInterval(interval);
			setTimeout(action, 1000);
			//action();//执行，好像马上执行偶尔还是会出问题，改成body完成构建后再等一秒，后续再等找找完美的解决方案
		}
	}, 100);
}

/**
 * myq add 2015-5-17，用于自动关联省市区的select组建
 * @param provinceSelect
 * @param citySelect
 * @param districtSelect
 * @param provinceId
 * @param cityId
 * @param districtId
 * @param allowNull
 */
function initAreaBox(provinceSelect, citySelect, districtSelect, 
		provinceId, cityId, districtId, allowNull){
	var srcPrefix = home() + "/common/area_functions.json?pid=";
	//alert(srcPrefix)
	//设置
	provinceSelect.onchange = function(){	
		$.ajax({url : srcPrefix + this.value,
			type:"post",
			dataType: "json",
			error: function(){
				alert("load city list error");
			}, 
			success:function(areas){
				citySelect.innerHTML = "";
				if(allowNull){
					areas.splice(0, 0, {id:"", text:"请选择市"});
				}
				if(cityId){
					haux.dom.createOptions(citySelect, areas, "id", "text", cityId);
					initCity = null;
				}
				else{
					haux.dom.createOptions(citySelect, areas, "id", "text");
				}
				citySelect.onchange();
			}
		});	
	}
	
	citySelect.onchange = function(){	
		$.ajax({url : srcPrefix + this.value,
			type:"post",
			dataType: "json",
			error: function(){
				alert("load county list error");
			}, 
			success:function(areas){
				districtSelect.innerHTML = "";
				if(allowNull){
					areas.splice(0, 0, {id:"", text:"请选择区/县"});
				}
				
				if(districtId){
					haux.dom.createOptions(districtSelect, areas, "id", "text", districtId);
					districtId = null;
				}
				else{
					haux.dom.createOptions(districtSelect, areas, "id", "text");	
				}
			}
		});	
	}
	
	//1.加载省级列表
	$.ajax({url : srcPrefix + "100",
		type:"post",
		dataType: "json",
		error: function(){
			alert("load province error");
		}, 
		success:function(areas){
			provinceSelect.innerHTML = "";
			if(allowNull){
				areas.splice(0, 0, {id:"", text:"请选择省"});
			}
			haux.dom.createOptions(provinceSelect, areas, "id", "text", provinceId);
			provinceSelect.onchange();
		}
	});	
}


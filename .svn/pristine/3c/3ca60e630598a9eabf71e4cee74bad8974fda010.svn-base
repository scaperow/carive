
haux.dom.addBodyLoadAction(function(){
	//1.顶部商品分类菜单 切换效果
	var dlElement = document.getElementById("category-box");
	new haux.component.LinkageDisplay(document.getElementById("category-label"),
		[dlElement]);
	
	//2.主菜单切换效果
	var childNode = dlElement.firstChild;
	var dtElement = null;
	var shadowElement = document.getElementById("catalog-shadow-mask");
	while(childNode){
		if(childNode.tagName == "DT"){
			dtElement = childNode;
		}
		else if(childNode.tagName == "DD" && childNode.className.indexOf("list-all") >= 0){
			new haux.component.LinkageDisplay(dtElement, [childNode, shadowElement]);
		}
		childNode = childNode.nextSibling;
	}

	//3.城市切换效果
	new haux.component.LinkageDisplay(document.getElementById("switch-city-list"), 
		[document.getElementById("city-list")]);
	
	//4.对登陆车主统计购物车
	// staticCart();
});

function staticCart(){
	$.ajax({url : home() + "/cart.do?op=getItemCount",
		type:"post",
		dataType: "json",
		error: function(){
		}, 
		success:function(data){
			var labelElement = document.getElementById("cart_count");
			labelElement.innerHTML = "<i></i>" + data.itemCount;
			labelElement.style.display = data.itemCount ? "block" : "none";
		}
	});	
}


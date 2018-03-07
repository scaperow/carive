/**
 * Created by KZK on 2014/11/9.
 */
//将商品放入购物车
function AddCart(userObj,pid,psid,PName,PPrice,PAmount,imgUrl,OPrice){
    if(parseInt(userObj) != 0) {
        $.get("/ajax/addCart", { pid: pid, quantity: PAmount,psid:psid}, function (data) {});
    }else{
        $.get("/ajax/addCart", { pid: pid, quantity: PAmount,psid:psid}, function (data) {});

         //var jsonStr = '[{"PId":"' + pid + '","PName":"' + PName + '","PPrice":"' + PPrice + '","PAmount":"' + PAmount + '","psid":"'+psid+'","imgUrl":"'+imgUrl+'","oprice":"'+OPrice+'"}]';
         //setCookie(pid, jsonStr);

            $.layer({
                shade: [0],
                area: ['auto', 'auto'],
                dialog: {
                    msg: "加入购物车成功,是否继续！",
                    btns: 2,
                    type: 9,//8难过，9开心，10正确,4问号
                    btn: ['去结算', '继续购物'],
                    yes: function () {
                        //location.reload();
                        location.href = "/cart/show";
                    }, no: function () {
                        //parent.$.fn.colorbox.close();
                    }
                }
            });
    }
}

function setCookie(name, value, options){
    var pnum = $("#buy_number").val();
    if (typeof value != 'undefined') { // name and value given, set cookie
        options = options || {};
        if (value === null) {
            value = '';
            options.expires = -1;
        }
        var expires = '';
        if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
            var date;
            if (typeof options.expires == 'number') {
                date = new Date();
                date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
            } else {
                date = options.expires;
            }
            expires = '; expires=' + date.toUTCString();
        }
        var path = options.path ? '; path=' + (options.path) : '; path=/';
        var domain = options.domain ? '; domain=' + (options.domain) : '';
        var secure = options.secure ? '; secure' : '';
        if(document.cookie && document.cookie != ""){ //cookie 存在
            var boolValue = getCookieByName(name);
            if(boolValue != "" || boolValue != ""){ //如果该商品已经存在，则在原来的数量上 +1
                var jsonStr = getCookieByName(name).replace('=','');
                var jsonObj = $.parseJSON(jsonStr);//stringToJSON(getCookieByName(name)); //如果有，把json字符串转换成对象d
                //jsonObj = jsonObj.replace('=','');
                for(var obj in jsonObj){
                    if(jsonObj[obj].PId == name){
                        jsonObj[obj].PAmount = parseInt(jsonObj[obj].PAmount) + parseInt(pnum); //数量 +1
                        document.cookie = [name, '=', JSON.stringify(jsonObj), expires, path, domain, secure].join(''); //要导入json2.js
                        //alert("该商品已经存在，则在原来的数量上 +增加的数量！document.cookie 为：" + decodeURIComponent(document.cookie));
                        break;
                    }
                }
            }else{ //如果该商品不存在，则将该商品添加到 cookie 中
                document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
                //alert("该商品不存在，则将该商品添加到 cookie 中！document.cookie 为：" + decodeURIComponent(document.cookie));
            }
        }else{
            //cookie 不存在
            document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
            //alert("cookie 不存在！document.cookie 为：" + decodeURIComponent(document.cookie));
        }
    }
}

//根据 name 查询 cookie 的值
function getCookieByName(name){
    var getValue = "";
    var cookie = decodeURIComponent(document.cookie).split(";");
    var search = name + "=";
    if(document.cookie && document.cookie != ""){ //cookie 存在
        for(var i = 0; i < cookie.length; i++){
            if(cookie[i].indexOf(search) != -1){
                getValue = cookie[i].substring(search.length);
            }
        }
    }
    //getValue = name + getValue;
    return getValue;
}


function DelCookie(sName){
    document.cookie = sName + "='';path=/; expires=Fri, 31 Dec 1999 23:59:59 GMT;";
};




//show.html

//根据 name 查询 cookie 的值
        var getCookieByName = function(name){
            var getValue = "";
            var cookie = decodeURIComponent(document.cookie).split(";");
            var search = name + "=";
            if(document.cookie && document.cookie != ""){ //cookie 存在
                for(var i = 0; i < cookie.length; i++){
                    if(cookie[i].indexOf(search) != -1){
                        getValue = cookie[i].substring(search.length);
                    }
                }
            }
            return getValue;
        };

        function showProduct(){

            var cookie = decodeURIComponent(document.cookie).split(";");
            if(cookie == "" || cookie == null){
                $("#CartItem").html("<tr><td colspan='5'>您的购物车中暂无商品，赶快选择心爱的商品吧！</td></tr>");
            }else{
                var CarHtml = "";
                for(var i = 2; i < cookie.length; i++){
                    var name = cookie[i].substring(0, cookie[i].indexOf("="));
                    var jsonObj = eval('(' + getCookieByName(name) + ')'); //如果有，把json字符串转换成对象
                    for(var obj in jsonObj){
                        //CarHtml += "<span>"+jsonObj[obj].PName+"</span><span>"+"￥" + jsonObj[obj].PPrice + "×" + jsonObj[obj].PAmount+"</span><br/>";
                        CarHtml += '<tr class="cart_item " id="P_'+jsonObj[obj].PId+'" product_id="'+jsonObj[obj].PId+'" item_price="'+jsonObj[obj].PPrice+'">';
                        CarHtml += '<td><div class="cart_item_desc clearfix"><a class="cart_item_pic" href="#" target="_blank">';
                        CarHtml += '<img src="'+jsonObj[obj].imgUrl+'" alt="'+jsonObj[obj].PName+'">';
                        CarHtml += '<span class="sold_out_pic"></span></a><a class="cart_item_link" title="'+jsonObj[obj].PName+'" href="#" target="_blank">'+jsonObj[obj].PName+'</a>';
                        CarHtml += '<p class="sku_info"></p><div class="sale_info clearfix"></div></div></td><td><div class="cart_item_price">';
                        CarHtml += '<p class="eofan_price">'+jsonObj[obj].PPrice+'</p><p class="market_price">'+jsonObj[obj].oprice+'</p>';
                        CarHtml += '</div></td><td><div class="cart_item_num "><div class="item_quantity_editer clearfix" data-item-key="1047672_d141104p550586">';
                        CarHtml += '<span class="noneid">'+jsonObj[obj].PId+'</span><span class="decrement ">-</span>';
                        CarHtml += '<input class="item_quantity" type="text" value="'+jsonObj[obj].PAmount+'" data="'+jsonObj[obj].PPrice+'" data-orginal="'+jsonObj[obj].oprice+'">';
                        CarHtml += '<span class="increment ">+</span></div><div class="item_shortage_tip"></div></div></td><td><div class="cart_item_total">';
                        CarHtml += '<p class="item_total_price">'+ parseInt(jsonObj[obj].PPrice) * parseInt(jsonObj[obj].PAmount) +'</p>';
                        CarHtml += '<p>省 <span class="item_saved_price">'+(parseInt(jsonObj[obj].oprice) * parseInt(jsonObj[obj].PAmount) - parseInt(jsonObj[obj].PPrice) * parseInt(jsonObj[obj].PAmount)) +'</span></p></div></td>';
                        CarHtml += '<td><div class="cart_item_option"><a class="icon_small delete_item png" data-item-key="'+jsonObj[obj].PId+'" href="javascript:void(0)" title="删除"></a></div></td></tr>';

                    }
                }
                $("#CartItem").html(CarHtml);
            }
        }
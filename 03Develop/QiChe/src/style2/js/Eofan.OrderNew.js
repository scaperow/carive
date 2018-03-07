window.Eofan = window.Eofan || {};
window._adwq = window._adwq || [];

function callback_fav_product(data){}
var _gaq  = new Array();
Eofan.OrderNew = {
    CartProductObj : '',//购物车产品列表 table 元素
    DefaultValue : [],
    WebSite:[],
	init : function() {
        if(RM_CONTROL == 'Cart' && RM_ACTION == 'show'){
            Eofan.OrderNew.CartProductObj = $('#cart_products');
            Eofan.OrderNew.enableCartProductAction();//为操作商品（改变数量等）的按钮绑定事件
            Eofan.OrderNew.RedrawCrossSale();
            Eofan.OrderNew.enableHuangouTabs();
            Eofan.OrderNew.enableCartShow();
            Eofan.OrderNew.cartBackTop();
            Eofan.OrderNew.enableHuangouTrack();
            if ( Eofan.Core.global_ajax ){
                Eofan.OrderNew.enableAjaxCrossale();
            }
            
            
            if ( is_semwinner ){
                Eofan.OrderNew.enableADWQTracking.track_add('cart');
            }
            
            Eofan.OrderNew.enableGATracking.track_add('view');
            $("#go_to_order").click(function(){
                var $this = $(this);
                Eofan.OrderNew.enableGATracking.track_add('clicked');

                try{
                    if (typeof (setCart.settle) == "function") {
                        setCart.settle();
                    }
                    if (typeof (setCart.settle2) == "function"){
                        var dataArray = [];
                        $("#cart_products .cart_item").each(function(){
                            var self = $(this),
                                data = {
                                    product_id : self.attr("product_id2"),
                                    brand_id : self.attr("brand_id"),
                                    price : self.attr("price"),
                                    sold : self.hasClass("sold_out")? 1 : 2//1 过期，2未过期，默认未过期
                                };
                            dataArray.push(data);
                        });
                        setCart.settle2(dataArray);
                    }
                }catch(e){}
            });
        }
        if(RM_CONTROL == 'Cart' && (RM_ACTION == 'confirmation'  || RM_ACTION == 'check')){
            Eofan.OrderNew.enableCartConfirmation();
            Eofan.OrderNew.enableDefaultValue();
        }
        
        // sorts of tracks
        if(RM_CONTROL == 'Cart' && RM_ACTION == 'confirmation' ){
            Eofan.OrderNew.enableGATracking.track_confirmation('view');
            $("#btn_confirm_pay").click(function(){
                Eofan.OrderNew.enableGATracking.track_confirmation('clicked');
            });
            /*发票功能*/
            Eofan.OrderNew.initInv();
        }
        if(RM_CONTROL == 'Cart' && RM_ACTION == 'check' ){
            Eofan.OrderNew.enableGATracking.track_check('view');
            $("#btn_confirm_pay").click(function(){
                Eofan.OrderNew.enableGATracking.track_check('clicked');
            });
        }
        if(RM_CONTROL == 'Cart' && RM_ACTION == 'pay' ){
            Eofan.OrderNew.enableGATracking.track_pay('view');
            if ( is_semwinner ){
                Eofan.OrderNew.enableADWQTracking.track_pay();
            }
        }
        if ( RM_CONTROL == 'Cart' && RM_ACTION=='payment_status' ){
            Eofan.OrderNew.enableAddCrossSaleToCart();
            Eofan.OrderNew.enablePaymentStatus();
            Eofan.OrderNew.enableGATracking.track_payment();
        }
        
        
        if(RM_CONTROL == 'Cart' && RM_ACTION=='shipping_single'){
			Eofan.OrderNew.enableCartConfirmation();
            Eofan.OrderNew.enableDefaultValue();
		}
        
        
        if(RM_CONTROL == 'Cart' && ( RM_ACTION=='pay' || RM_ACTION == 'check' )){
            Eofan.OrderNew.enableCreditTopupLightbox();
		}
        if(RM_CONTROL == 'Mobile' && (RM_ACTION == 'order' || RM_ACTION == 'Check')){
            if (RM_ACTION == 'Check'){
                Eofan.OrderNew.initGatewayToggle();
            }
            Eofan.OrderNew.enableCreditTopupLightbox('/payment_confirm_mobile.html');
        }
        if(RM_CONTROL == 'LotteryWheel' && RM_ACTION=='receive'){
            Eofan.OrderNew.enableCartConfirmation();
            Eofan.OrderNew.enableDefaultValue();
        }
		Eofan.OrderNew.cancel();

        Eofan.OrderNew.initCountdown();
	},
    /*初始化倒计时*/
    initCountdown :function(){
        Eofan.OrderNew.countDownInfo = {running:false,time_m:0,time_s:0,timeOutWrap:''};
        Eofan.OrderNew.cart_countdown_time = $(".cart_countdown_time");
        if(Eofan.OrderNew.cart_countdown_time.length){
            var time_ms = Eofan.OrderNew.cart_countdown_time.html().split("分"),time_m = Number(time_ms[0]),time_s = Number(time_ms[1].replace("秒",""));
            if(time_m>0 || time_s>0)
                Eofan.OrderNew.refreshCountdownTime(time_m,time_s);
            else{
                Eofan.OrderNew.countdownTimeout();
            }
        }
    },
    countdownTimeout:function(){
        if(Eofan.OrderNew.countDownInfo.timeOutWrap){
            Eofan.OrderNew.countDownInfo.timeOutWrap.show();
        }else{
            Eofan.OrderNew.countDownInfo.timeOutWrap = $("<strong>已超过购物车商品保留时间，请尽快结算。</strong>").insertAfter(Eofan.OrderNew.cart_countdown_time.parent());
        }
        Eofan.OrderNew.cart_countdown_time.parent().hide();
    },
    /*倒计时内部调用函数*/
    startCountdown : function(){
        if(Eofan.OrderNew.cart_countdown_time.length){
            if(Eofan.OrderNew.countDownInfo.timeOutWrap){
                Eofan.OrderNew.countDownInfo.timeOutWrap.hide();
                Eofan.OrderNew.cart_countdown_time.parent().show();
            }
            Eofan.OrderNew.countDownInfo.running = true;
            var timeInterval = setInterval(function(){
                if(Eofan.OrderNew.countDownInfo.time_s<=0 && Eofan.OrderNew.countDownInfo.time_m<=0){
                    clearInterval(timeInterval);
                    Eofan.OrderNew.countdownTimeout();
                    Eofan.OrderNew.countDownInfo.running = false;
                    return;
                }
                if(--Eofan.OrderNew.countDownInfo.time_s<0){
                    Eofan.OrderNew.countDownInfo.time_m --;
                    Eofan.OrderNew.countDownInfo.time_s = 59;
                }
                Eofan.OrderNew.cart_countdown_time.html((Eofan.OrderNew.countDownInfo.time_m<10 ? "0" : "") + Eofan.OrderNew.countDownInfo.time_m+"分" + (Eofan.OrderNew.countDownInfo.time_s<10 ? "0" : "") + Eofan.OrderNew.countDownInfo.time_s+"秒");
            },1000);
        }
    },
    /*倒计时API 需要刷新时间或者重新显示都调用该函数*/
    refreshCountdownTime : function(m,s){
        Eofan.OrderNew.cart_countdown_time.parent().parent().show();
        Eofan.OrderNew.countDownInfo.time_m = Number(m);
        Eofan.OrderNew.countDownInfo.time_s = Number(s);
        if(!Eofan.OrderNew.countDownInfo.running && (m>0 || s>0)){
            Eofan.OrderNew.startCountdown();
        }
    },
    /*倒计时API 需要刷新时间或者重新显示都调用该函数 只需要传总共秒数*/
    refreshCountdownTimeBySends : function(s){
        Eofan.OrderNew.refreshCountdownTime(Math.floor(s/60),s%60);
    },
    /*倒计时API 隐藏倒计时*/
    hideCountdown : function(){
        Eofan.OrderNew.refreshCountdownTime(0,0);
        Eofan.OrderNew.cart_countdown_time.parent().parent().hide();
    },

    /*发票功能*/
    initInv : function(){
        var needBtn = $(".is_need_inv"),
            invInfo = $(".inv_info"),
            invTypeName = $(".inv_type_name"),
            invError = $(".inv_error").hide(),
            typeNameTipsTxt = '请输入单位名称',
            invEditWrap = $(".inv_edit_wrap"),
            invEditBtn = $(".inv_edit_btn"),
            invQuesstionBtn = $(".inv_quesstion"),
            invQTip = invQuesstionBtn.find("div"),
            complanyTxt = invInfo.find("input:[type=text]");

        needBtn.click(function(){
            if(needBtn.attr("checked")){
                invInfo.show();
            }else{
                invInfo.hide();
            }
        });

        invInfo.find("input:[type=radio]").click(function(){
            if($(this).val()==1){
                complanyTxt.attr("disabled",true);
            }else{
                complanyTxt.attr("disabled",false).focus();
            }
        });
        if(invInfo.find("input:[type=radio]:checked").val()==1){
            complanyTxt.attr("disabled",true);
        }
        invQuesstionBtn.hover(function(){invQTip.show();},function(){invQTip.hide();});

        function inputFocusTip(ele,isWrap){
            var inputs = isWrap ? ele ? $(ele).find("input,textarea") : $("input,textarea") : $(ele);
            inputs.each(function(key,inputItem){
                inputItem = $(inputItem);
                var focusTxt = inputItem.attr("focusTxt");
                if(focusTxt){
                    if(!inputItem.val()){
                        inputItem.val(focusTxt).addClass("focus_txt");
                    }
                    inputItem.focus(function(){
                        if(inputItem.removeClass("focus_txt").val()==focusTxt){
                            inputItem.val("");
                        }
                    });
                    inputItem.blur(function(){
                        if(!inputItem.val()){
                            inputItem.val(focusTxt).addClass("focus_txt");
                        }
                    });
                }
            });
        };

        if(invEditWrap.is(":hidden")){
            window.needCheckInvOnSubmit = false;
            inputFocusTip(invTypeName.attr("focusTxt",typeNameTipsTxt));
            invEditBtn.click(function(){
                invEditBtn.parent().parent().remove();
                invEditWrap.show();
                window.needCheckInvOnSubmit = true;
            });

            invEditBtn.parent().hide().parent().hover(function(){
                invEditBtn.parent().show();
            },function(){invEditBtn.parent().hide();});
        }else{
        inputFocusTip(invTypeName.val(typeNameTipsTxt).addClass("focus_txt").attr("focusTxt",typeNameTipsTxt));
            window.needCheckInvOnSubmit = true;
        }

    },

    enableHuangouTrack: function(){
        $('.sale_gifts_tabs').delegate('a', 'click', function(){
            var $this = $(this),
                $li = $this.closest('li'),
                url = $this.attr('href');
            try{
                if (typeof (setCart.addToCart) == "function") {
                setCart.addToCart(1, {
                    pid: $this.attr('product_id'),
                    brand_id: $this.attr('brand_id'),
                        cid: $this.attr('category_id') || 0,
                    jm_price: $li.find('.price').find('span').first().text().substring(1),
                    url: url,
                    from: url.substring(url.indexOf('=') + 1),
                    result_cnt: $li.siblings().length + 1,
                    pos: $li.index() + 1
                });
                }
            }catch(e){}

            setTimeout(function(){
                window.location.href = $this.attr('href');
            }, 0);
            return false;
        });
    },
	enableCartProductAction: function(){
        //input 事件
		Eofan.OrderNew.CartProductObj.find('.item-buy-quantity-input').click(function() {
            $(this).select();
		}).blur(function(){
             Eofan.OrderNew.cart_item_quantity_change($(this), this.value);
		});

        //按钮 减 事件
		Eofan.OrderNew.CartProductObj.find('.buy_number_input').not('.disable').children('.decrease_num').click(function() {
            var obj_input = $(this).parent().find('.item-buy-quantity-input');
            var quantity = parseInt(obj_input.val())-1;
            if(quantity > 0){
                Eofan.OrderNew.cart_item_quantity_change(obj_input, quantity);
            }
		});
        //按钮 加 事件
		Eofan.OrderNew.CartProductObj.find('.buy_number_input').not('.disable').children('.increase_num').click(function() {
            var obj_input = $(this).parent().find('.item-buy-quantity-input');
            var quantity = parseInt(obj_input.val())+1;
            if(quantity > 0 && quantity < 21){
                Eofan.OrderNew.cart_item_quantity_change(obj_input, quantity);
            }
		});
        //删除某个商品   TODO::优化未完成
		Eofan.OrderNew.CartProductObj.find('.item-buy-delete').click(function (){
			//var is_confirmed = confirm('确定不购买此商品？');
			//if(is_confirmed){
                if ( is_semwinner ){
                    Eofan.OrderNew.enableADWQTracking.track_add('delete');
                }
                Eofan.OrderNew.enableGATracking.track_add('delete');
                
                var cur_tr = $('#' + $(this).attr('alt')),
                    self = $(this),
                    items = cur_tr.attr('items'),
                    num = cur_tr.find('.item-buy-quantity-input').val(),
                    from = 'cart_show_recover',
                    item_name = $.trim(cur_tr.find('.item_name a').html()),
                    link = cur_tr.find('.item_name a').attr('href'),
                    last_remove_node = cur_tr.clone(true),
                    style = '';

                if ( cur_tr.hasClass('giftflag') ){
                    item_name = $.trim(cur_tr.find('.item_name p').last().html());
                    link = 'javascript:;';
                    style = 'style="text-decoration:none;color:#333;cursor:text;"';
                }
                
                if ( num > 1 ){
                    items = items.slice( 0 , items.length - 1 ) + num;
                }

                var cal_amount = function(){
                    Eofan.OrderNew.RedrawCrossSale();
                    $.ajax({
                        url:'/i/cart/ajax_update_cart',
                        type:"GET",
                        dataType:"json",
                        data:{
                            "item_key":self.attr('alt'),"item_quantity":0,"cart_key":self.attr("cart_key"),"which_cart":"all"
                        },
                        success:function(data){
                            if(data.status == "success"){
                                $(add_again).insertBefore(cur_tr).find(".item_note").html(function(idx, old){
                                    return $.trim(old);
                                });
                                cur_tr.remove();

                                $('#add_again').click(function(e){
                                    addCart(items,'flow_cart_undorecover');
                                    e.preventDefault();
                                });

                                // 计算相关数字
                                $("#J_redeem_amount").val(data.redeem_amount);
                                Eofan.OrderNew.caculate_amount_func(data.redeem_amount);
                                Eofan.OrderNew.changeHuangouStatus(data.redeem_amount);

                                /*更新倒计时时间*/
                                if(!data.showcd){
                                    Eofan.OrderNew.hideCountdown();
                                }else{
                                    Eofan.OrderNew.refreshCountdownTimeBySends(Number(data.sec));
                                }
                            }else{
                                location.reload();
                            }
                        }
                    });
                };

                //加入购物车
                var addCart = function (items,from) {

                    $.getJSON('/i/cart/ajax_add_to_cart',
                        {
                            items: items,
                            from:from,
                            "which_cart":"all"
                        },
                        function(data){
                            if(data.type == "success"){
                                Eofan.OrderNew.CartProductObj.find('.add_again').replaceWith(last_remove_node);
                                $("#J_redeem_amount").val(data.redeem_amount);
                                Eofan.OrderNew.changeHuangouStatus(data.redeem_amount);

                                Eofan.OrderNew.caculate_amount_func(data.total_amount);
                                Eofan.Core.ga_event('cart_recover',RM_CONTROL+'_'+RM_ACTION , items);

                                /*更新倒计时时间*/
                                if(!data.showcd){
                                    Eofan.OrderNew.hideCountdown();
                                }else{
                                    Eofan.OrderNew.refreshCountdownTimeBySends(Number(data.sec));
                                }
                            } else if (data.type == "noInventory") {
                                alert("该商品已售光，无法撤销删除！");
                                location.reload();
                            }else{
                                alert("恢复失败，请重试！");
                            }
                        }
                    );
                };
                

                if ( Eofan.OrderNew.CartProductObj.find('.add_again') ){
                    Eofan.OrderNew.CartProductObj.find('.add_again').remove();
                }
                
                // 恢复已删除内容
                var add_again = '<tr class="add_again"><td colspan="6">您已删除<a href="'+link+'?from=flow_cart_undorecover" target="_blank" '+style+'>' + item_name +
                    '</a>，如有误，<a href="javascript:void(0);" id="add_again">撤销本次删除</a></td></tr>';

                cal_amount();
			//}
		});

        // 收藏某商品
        Eofan.OrderNew.CartProductObj.find('.item-buy-collect').click(function(){

            var self = $(this),
                pid = self.attr('product_id');


            callback_fav_product = function(data){
                var insert_node = $("#cart");
                if(data.isLogin == 'no') { // 没有登录的情况
                    
                    Eofan.Core.postAdhocNotification(insert_node, false, "prepend", {
                        type: "warning",
                        message: "您还没有登录,<a href='"+RM_SITE_MAIN_PASSPORTURL+"i/account/login/'>登录</a>后才能添加我收藏"
                    });
                    
                    setTimeout(function(){
                        $(".notification_center").remove();
                    },3000);

                } else { // 登录的情况
                    if(data.isOk == 'yes') { // 收藏成功
                        Eofan.Core.postAdhocNotification(insert_node, false, "prepend", {
                            type: "success",
                            message: "恭喜您，收藏成功！"
                        });

                        self.text('已收藏');
                        
                        setTimeout(function(){
                            $(".notification_center").remove();
                        },3000);

                    } else if(data.isOk == 'no') { //  收藏失败
                        Eofan.Core.postAdhocNotification(insert_node, false, "prepend", {
                            type: "error",
                            message: "对不起,最多只能收藏100个商品"
                        });

                        setTimeout(function(){
                            $(".notification_center").remove();
                        },3000);

                    }
                }
            };
            
            
            if( typeof(pid) != 'undefined' && pid != ''){
                
                
                $.getJSON(
                    RM_SITE_MAIN_WEBBASEURL + 'i/product/ajax_fav_product?product_id=' + pid + '&callback=?',
                    null,
                    function(){
                    }
                );
                

            }

        });
        
        
        
	},

    RedrawCrossSale: function(){
        var obj_cart_item = Eofan.OrderNew.CartProductObj.find(".cart_item");
		var deal_hash_ids = new Array();
		if(obj_cart_item.length > 0){
			obj_cart_item.each(function (){
				deal_hash_ids.push($(this).attr('deal_hash_id'));
			});
		}
		$('#product_list .cross_sale_deal').each(function (){
			var in_array = $.inArray($(this).attr('deal_hash_id'), deal_hash_ids);
			if(in_array != '-1'){
				$(this).css('display', 'none');
			}else{
				$(this).css('display', 'inline');
			}
		});
	},
    enableHuangouTabs:function(){
        if( $('.sale_gifts_tabs').length > 0 ){

            var redeem_amount = $("#J_redeem_amount").val();
            Eofan.OrderNew.changeHuangouStatus(redeem_amount);
            
            var tabs = $('.til','.sale_gifts_tabs');

            tabs.hover(function(){
                var level = $(this).attr('level');
                tabs.removeClass('current');
                $(this).addClass('current');
                $('.gifts_container','.sale_gifts_tabs').hide();
                $('#level_'+level).show();
            });

            $(".gifts_container .button").hover(function(e){
                if ( $(this).find(".btn_overlay").length > 0){
                    var level = $(".sale_gifts_tabs .current").attr("level"),
                        tip = $('<div class="gift_tips box_yellow">您购物车的商品金额不满足换购条件，需大于'+level+'元才可以购买喔</div>');

                    $("#cart").append(tip);

                    $(this).mousemove(function(e){
                        var top = $("#cart").scrollTop() + e.pageY -30,
                            left = $("#cart").scrollLeft() + e.pageX + 15;
                        tip.css("left",left).css("top",top);
                    });
                }
            },function(){
                $(".gift_tips").remove();
            });
            
        }
    },
    changeHuangouStatus:function(price){

        if( $('.sale_gifts_tabs').length > 0 ){
            var tabs = $('.title_tabs .til','.sale_gifts_tabs'),
                len = tabs.length,
                levels = [],
                overlay = $('<div class="btn_overlay">加入购物车</div>');


            // record every price's level
            for ( var i = 0 ; i < len ; i++){
                levels.push(parseFloat(tabs.eq(i).attr('level')));
            }

            // process the gifts_cointaner according to price 
            for ( var i = 0 ; i < len ; i++ ){

                if( price >= levels[i] ){
                    if ( $('.gifts_container').eq(i).find('.btn_overlay').length > 0 ){
                        $('.gifts_container').eq(i).find('.btn_overlay').remove();
                    }
                }else{
                    if( $('.gifts_container').eq(i).find('.btn_overlay').length == 0 ){
                        $('.gifts_container').eq(i).find('.button').append(overlay);
                    }
                }


            }

        }
    },
    enableAddCrossSaleToCart : function(){

        var product_list = $('.product_list');
        var mall_products = product_list.find("li.cross_sale_deal a.link");
        mall_products.click(function(e){
            e.preventDefault();
            var self = $(this),
                parent = self.closest("li.mall_product"),
                sku_select = parent.find(".sku_select"),
                href = self.attr('href'),
                from = '?from=payment_status_cross_addtocart',
                hash_id = typeof(self.attr("hash_id")) != 'undefined' ? self.attr("hash_id") :  '',
                id = self.attr("product_id");


        });
    },
    enableCartConfirmation : function (){
        //selector
        var express_selector = $('#express_selector');
        var address_selector = $('#address_selector');
        var shipping_selector = $('#shipping_selector');
        var prefer_delivery_day = $('#prefer_delivery_day');
        //cache obj
        var merge_shipping_delivery_fee_redcuction = $('#merge_shipping_delivery_fee_redcuction');
        var delivery_fee = $('#delivery_fee');
        //功能块
        var merge_shipping_list = $('#merge_shipping_list');
        var shipping_input_delay = $('#shipping_input_delay');

        //改变选中状态的样式
        var selected = function(obj){
            obj.parent().find('.option_box').removeClass('selected');
            //obj.parent().find('.option_box').find('input').removeAttr('checked');
            //obj.find('input').attr('checked','checked');
            obj.addClass('selected');
            //obj.attr('checked','checked');
            
            if ( obj.find('input').length > 0 ){
                obj.parent().find('.option_box').find('input').removeAttr('checked');
                obj.find('input').attr('checked','checked');
            }
            
        };

        //收货地址
        address_selector.find('.option_box').live('click',function(){
            var input_id = $(this).attr('selector'),
                val = $(this).find('.rdoAddress').first().val();

            if(!$(this).find(".id_wrap span").length && is_need_id){ //如果有身份证号码
               alert("由于法规要求，跨境购物需要您填写收件人身份证信息");
               $(this).find(".btnEditAddress_new").click(); //抛出修改地址弹窗事件 并阻止事件向下运行
               return false;
           } else {
               $('#address_table').hide();
               selected($(this));

               $(this).parent().siblings(".editAddressForm").hide();
               Eofan.OrderNew.load_shipping(express_selector.find('input[name=logistic_preference]:checked').val(),val);
           }
        });

        //快递
        express_selector.find('input[name=logistic_preference]').click(function(){
            if($(this).parent().hasClass('disable')){
                return false;
            }
            delivery_fee.val($(this).attr('delivery_fee'));
            if(parseInt(merge_shipping_delivery_fee_redcuction.val()) != 0){
                    merge_shipping_delivery_fee_redcuction.val($(this).attr('delivery_fee'));
            }
            Eofan.OrderNew.load_shipping($(this).val(),address_selector.find('input[name=address_id]:checked').val());
            Eofan.OrderNew.update_checkout_amount();
            //style
            selected($(this));
        });
        prefer_delivery_day.find('input[name=prefer_delivery_day]').click(function(){
            selected($(this).parent());
        });
        //发货设置
        shipping_selector.find("input[name='shipping_option']").click(function(){

			if($(this).val() == 'merge'){
				merge_shipping_list.show();
                shipping_input_delay.hide();
				merge_shipping_delivery_fee_redcuction.val(delivery_fee.val());
			}else if($(this).val() == 'delay'){
				merge_shipping_delivery_fee_redcuction.val(0);
                merge_shipping_list.hide();
				shipping_input_delay.show();
			}else{
				merge_shipping_delivery_fee_redcuction.val(0);
                merge_shipping_list.hide();
			    shipping_input_delay.hide();
			}
			Eofan.OrderNew.update_checkout_amount();
            //style
            selected($(this));
		});
        //时间控件
        var minPlus = 1;
        var maxPlus = 10;
        var now = new Date();
        var string = now.getFullYear()+"/"+(parseInt(now.getMonth())+1)+"/"+now.getDate();
        now = new Date(string);

        var minDate = new Date(now);
        var maxDate = new Date(now);
        minDate.setTime(minDate.getTime() + minPlus*(1000*3600*24));
        maxDate.setTime(maxDate.getTime() + maxPlus*(1000*3600*24));

        //绑定datepicker
        $("#target_shipping_date").mousedown(function (){
        	$(this).datepicker();
        	$(this).datepicker('option', {dateFormat: "yy-mm-dd", showAnim: '', minDate: minDate, maxDate: maxDate});
        }).change(function() {
            var stringValue = $(this).val();
            var dateValue = new Date(stringValue.replace(/-/g,   "/"));
            if ( dateValue == null || dateValue < minDate || dateValue > maxDate ) {
                alert("您输入的时间有误！");
                var month = parseInt(maxDate.getMonth())+1;
                var day = maxDate.getDate();
                var monthString = month > 9 ? month+"" : "0"+month;
                var dayString = day > 9 ? day+"" : "0"+day;
                $(this).val(maxDate.getFullYear()+"-"+monthString+"-"+dayString);
            }
        });

        //gateway list
        $('.gateway_ul>li').click(function(){
            var $this = $(this),
                $input = $this.find('>input');
            var rc = $($input).is(':radio');

            if(!rc && $($this).hasClass('ul_on'))
            {
                $($this).find(".right_Price").hide();
                $($this).removeClass('ul_on').addClass('ul_off').find('>input[name="'+$($input).attr('name')+'"]').attr('checked', false);
                $(".getewey_price").text($("#hidBalance").val());
                return;
            }
            if($input.attr('disabled') === false) {
                //$($this).find(".right_Price").show();
                $input.attr('checked', true);


                $this.siblings('li').removeClass('ul_on').addClass('ul_off').find('>input[name="'+$($input).attr('name')+'"]').attr('checked', false);
                $this.removeClass('ul_off').addClass('ul_on');
                $this.siblings('li').find(".rightPrice").hide();
                $this.find(".rightPrice").show();

            }
            var cb = $("#check-balance").attr("checked");
            var currentPrice = $("#hdCurrentPrice").val();

            if(cb){
                //如果是checkbox，则全部余额作为余额支付部分
                $('#hdBalance').val($('.hid_balance').val());
                var balance = parseFloat($('#hdBalance').val()).toFixed(2);
                $(".balance_price").text(balance);
                $(".getewey_price").text((parseFloat(currentPrice)-balance).toFixed(2));
            }
            else{
                //如不是不checkbox，判断是否全部使用余额
                var rb = $("#radio-balance").attr("checked");
                if(rb){
                    //余额支付
                    $('#hdBalance').val(currentPrice);
                }
                else{
                    $('#hdBalance').val('0');
                }
                $(".getewey_price").text(parseFloat(currentPrice).toFixed(2));
            }

            var gat=$('input:radio[name="gateway"]:checked').val();
            if($('#check-other').is(':checked') && (gat != 'Balance' && gat != 'Alipay' && gat != 'COD')){
                $("#radio-balance").removeAttr("checked");
                $("#choose_before").removeAttr("checked");
                $("#check-cod").removeAttr("checked");
            }
            var gat=$('input:radio[name="gateway"]:checked').val();
            if (gat == 'Balance' || gat == 'Alipay' || gat == 'COD'){
                $("#check-other").removeAttr("checked");
            }
        });


        $('.g_ul').delegate('li', 'click', function(){
            var $this = $(this),
                $input = $this.find('input');

            $this.addClass('selected');
            $input.attr('checked', true);
            $('input[name=gateway]').not(':checked').closest('li').removeClass('selected');
        });
    },

    enableDefaultValue : function (){
        $("#gateway_list input[value="+Eofan.OrderNew.DefaultValue.payment_method+"]").trigger('click');
        $("#address_selector input[value="+Eofan.OrderNew.DefaultValue.address_id+"]").trigger('click');
        $("#prefer_delivery_day input[value=" + Eofan.OrderNew.DefaultValue.prefer_delivery_day+"]").trigger('click');
    },

    setDefaultValue : function(data){
        if(data){
            Eofan.OrderNew.DefaultValue = data;
        }

        //如果默认地址为空 则 显示 地址输入
        if(Eofan.OrderNew.DefaultValue.address_id == '0'){
            $('#address_table').show();
        }
    },

    cart_item_quantity_change: function(cart_item_input_obj, expect){
		var user_purchase_limit = parseInt(cart_item_input_obj.attr('user_purchase_limit'));
		var item_quantity = expect;
        var cart_key = cart_item_input_obj.attr('cart_key');
        var item_key = cart_item_input_obj.attr('item_key');
        var tr = cart_item_input_obj.closest('.cart_item');
        var tr_id = tr.attr('id');

        if(isNaN(item_quantity)) item_quantity = 0;
        if(item_quantity < 1 ) item_quantity = 1;
        if(item_quantity > 20) item_quantity = 20;

		if (user_purchase_limit != 0 && item_quantity > user_purchase_limit) {
            item_quantity = user_purchase_limit;
			cart_item_input_obj.val(item_quantity);
            alert("您最多能够购买 "+user_purchase_limit+" 件该商品!");
		}else {
            $.ajax({
                url:'/i/cart/ajax_update_cart',//
                type:"GET",
                dataType:"json",
                data:{
                    "cart_key":cart_key,"item_quantity":item_quantity,"item_key":item_key,"which_cart":"all"
                },success:function(data){
                    if(data.status == "success"){
                        cart_item_input_obj.val(item_quantity);

                        if(item_quantity == 1){
                            cart_item_input_obj.prev(".decrease_num").addClass("turn_gray");
                            cart_item_input_obj.next(".increase_num").removeClass("turn_gray");
                        }else if(item_quantity > 1 && item_quantity < 20){
                            cart_item_input_obj.prev(".decrease_num").removeClass("turn_gray");
                            cart_item_input_obj.next(".increase_num").removeClass("turn_gray");
                        }else if(item_quantity == 20){
                            cart_item_input_obj.prev(".decrease_num").removeClass("turn_gray");
                            cart_item_input_obj.next(".increase_num").addClass("turn_gray");
                        }

                        if(item_quantity == user_purchase_limit){
                            cart_item_input_obj.next(".increase_num").addClass("turn_gray");
                        }

                        // 改变redeem_amount
                        $("#J_redeem_amount").val(data.redeem_amount);
                        //计算价格
                        Eofan.OrderNew.caculate_amount_func(data.redeem_amount);
                        Eofan.OrderNew.changeHuangouStatus(data.redeem_amount);

                        var saved_price = tr.find('.saved_price'),
                            saved_price_num = parseFloat(saved_price.attr('saved_per_price')).toFixed(2);

                        saved_price.html( (saved_price_num*item_quantity).toFixed(2) );

                        var per_price = parseFloat($('#item-buy-price-' + tr_id).html());

                        $('#item-buy-total-' + tr_id).html( (per_price*item_quantity).toFixed(2) );

                        /*更新倒计时时间*/
                        if(!data.showcd){
                            Eofan.OrderNew.hideCountdown();
                        }else{
                            Eofan.OrderNew.refreshCountdownTimeBySends(Number(data.sec));
                        }
                    }else{
                        alert("操作失败，请重试！");
                    }
                    
                    // track cart
                    if ( is_semwinner ){
                        Eofan.OrderNew.enableADWQTracking.track_add('cart');
                    }
                    Eofan.OrderNew.enableGATracking.track_add('quantity_change');
                }
            });
        }
	},

    caculate_amount_func: function (redeem_amount){
        var obj = $('#cart_products');
		var quantity = 0;
		var sub_total = 0;
		var has_lottery = false;
		var has_b2c_item = false;
        var focus_amount = $("#focus_amount");
        var focus_total_amount = 0;
		obj.find('.item-buy-quantity-input').each(function(){
            var self = $(this),
                parent = self.closest('tr');
            var v = parseInt($(this).val());
            if(isNaN(v)) v = 0;
            if(v < 1 ) v =1;
            if(v > 20) v = 20;

			quantity += v;
			var cart_index = $(this).attr('item_key');
			var item_total = parseFloat(v * $('#item-buy-price-' + cart_index).html());

			sub_total += item_total;

            if ( parent.hasClass('focus_item') ){
                focus_total_amount += item_total;
            }

			if($(this).attr('category') == 'lottery'){
                has_lottery = true;
            }

			if($(this).attr('is_b2c_item') == '1'){
				has_b2c_item = true;
			}
		    //$('#item-buy-total-' + cart_index).html(item_total.toFixed(2));
		});
		var cart_amount_after_discount = sub_total ;
        
		$('#item-buy-total-t').html(redeem_amount);
        //$("#J_redeem_amount").val(redeem_amount);

        if ( focus_amount.length ){
            focus_amount.html(focus_total_amount.toFixed(2));
        }

	},

    clear_cart: function(){
        $.ajax({
                url:'/i/cart/ajax_clear_cart',//
                type:"POST",
                dataType:"text",
                data:{}
            });
        Eofan.OrderNew.enableGATracking.track_pay('clicked');
    },

	load_shipping: function(express,address_id){
		var has_available_shipping = false;
        //selector
        var shipping_selector = $('#shipping_selector');
        //obj
        var merge_shipping_title = $('#merge_shipping_title');
        var merge_shipping_list = $('#merge_shipping_list');
        //delivery_fee view
        var delivery_fee_view = $('#delivery_fee_view');
        
		$("#merge_shipping_list .shipping_no").each(function (){
			var allowed_shipping_set = express + '_' + address_id;
			var is_available_shipping = false;
			if($(this).attr('alt') != allowed_shipping_set){
				$(this).css('display', 'none');
			}else{
				is_available_shipping = true;
				$(this).css('display', 'block');
			}
			has_available_shipping = has_available_shipping || is_available_shipping;
			if(!has_available_shipping){
				merge_shipping_title.hide();
				merge_shipping_list.hide();
				if(shipping_selector.find("input[name='shipping_option']:checked").val() == 'merge'){
					delivery_fee_view.html($('#delivery_fee').val());
                    var total_amount = parseFloat(delivery_fee_view.html()) + parseFloat($("#cart_total").val());
					$('#total_amount').text(total_amount.toFixed(2));
					shipping_selector.find("input[name='shipping_option'][value='instant']").attr("checked",true);
				}
			}else{
				merge_shipping_title.show();
				if(shipping_selector.find("input[name='shipping_option']:checked").val() == 'merge'){
					merge_shipping_list.show();
				}
			}
		});
	},

	cancel: function(){
		$('.order-cancel').click(function (){
            
            var text = '确定要取消这个订单吗？\n取消货到付款的订单，使用过的现金券会恢复正常';
            if ( $(this).hasClass('cancel-red-envelope') ){
                text = '红包每人仅限购买一个，\n若取消红包订单，将无法再次购买红包喔！';
            }
            
            var confirmation = confirm(text);
            
			var _self = $(this);
			if(confirmation){
				$.get(
					$(this).attr('href'),
					'',
					function(data){
						var obj = $.parseJSON(data);
						_self.closest("td").html(obj.msg);
					}
				);
			}else{
				//
			}
			return false;
		});
	},
	update_checkout_amount : function() {
		var cart_amount = parseFloat($("input[name='cart_total']").val());
		var delivery_fee = parseFloat($("input[name='delivery_fee']").val());
		var promo_cards_reduction_amount = parseFloat($("input[name='promo_cards_reduction_amount']").val());
		var merge_shipping_delivery_fee_redcuction = parseFloat($("input[name='merge_shipping_delivery_fee_redcuction']").val());
		var delivery_fee_reduction = parseFloat($("input[name='delivery_fee_reduction']").val());

		var final_delivery_fee_reduction = Math.max(delivery_fee_reduction, merge_shipping_delivery_fee_redcuction);

		if(final_delivery_fee_reduction > 0){
			$('#final_delivery_fee_redunction_notice').css('display', 'block');
			$('#final_delivery_fee_redunction_amount').html(final_delivery_fee_reduction);
		}else{
			$('#final_delivery_fee_redunction_notice').css('display', 'none');
		}

		if(promo_cards_reduction_amount > 0){
			$('#promo_card_reduction_notice').css('display', 'block');
			$('#promo_card_reduction_amount').html(promo_cards_reduction_amount);
		}else{
			$('#promo_card_reduction_notice').css('display', 'none');
		}
		$('#delivery_fee_view').html(delivery_fee);


		// set checkout amount to original amout
		var checkout_amount = Math.max(0, cart_amount + delivery_fee - final_delivery_fee_reduction - promo_cards_reduction_amount).toFixed(2);
		$('#total_amount').text(checkout_amount);

		var balance = parseFloat($("#account_balance").text());

        //浮点误差
		if (balance + 0.000001 < checkout_amount) {
			var proceed_notice = '帐户余额：<span><font>¥</font><span id="account_balance">'+balance.toFixed(2)
                                +"</span></span> 您的余额不够完成本次付款，还需支付 <span><font>¥</font>"+(checkout_amount-balance).toFixed(2)+"</span>。请选择支付方式";
            $("#paytype_balance_info").html(proceed_notice);
			$('#paytype_gateway').css('display', 'block');
		} else {
            var proceed_notice = '帐户余额：<span><font>¥</font><span id="account_balance">'+balance.toFixed(2)
                                 +'<span id="paytype_balance" style="color:#333;">您可以用余额支付本订单</span>';
			$("#paytype_balance_info").html(proceed_notice);
			$('#paytype_gateway').remove();
		}
	},
    cartBackTop:function(){
        // back to top
        var nav_backtotop = $('#home_nav_bar a.nav_backtotop'),
            home_nav_bar = $('#home_nav_bar');
        
        nav_backtotop.click(function(e){
            e.preventDefault();
            $('html,body').animate({scrollTop:0},500);
        });

        //显示回到顶部按钮
        var moveBackToTop = function(){
            if($(window).scrollTop()>400){
                home_nav_bar.fadeIn('fast');
            } else{
                home_nav_bar.fadeOut('fast');
            }
        };
        
        $(window).scroll(moveBackToTop);
    },
    
    addSaleGiftToCart : function (){
        /**
         * 添加换购到购物车 use 大促08-18
         * @param total_price
         */
            
        var add_sale0818_gift_to_cart = function (){
            var is_add_gift = false;
            var cart_url = RM_CURRENT_SITE_MAIN_WEBBASEURL+'/i/cart/new_items/';
            if( !$(this).parent().parent().hasClass('enable') ){
                return false;
            }
            if( $(this).hasClass('selected') ){
                return false;
            }
            if($(this).hasClass('sold_out')){
                alert('此商品已抢光，换一个吧');
                return false;
            }

            // 首先移除全部的selected,然后给当前选择的项目加上
            $('.sale_gifts_selector li').removeClass('selected');
            $(this).addClass('selected');

            var hash_id = $(this).attr('hash_id');
            var sku_no = $(this).attr('sku_no');
            var url = cart_url+sku_no+','+hash_id+',1';
            Eofan.Core.ga_event('addtocart', RM_CONTROL+'_'+RM_ACTION , hash_id);
            window.location.href = url;
        };

        //提交时检查赠品是否符合规则
        var check_gift = function (){
            var sale_box_obj = $('.sale_gifts_selector');
            if(sale_box_obj.length > 0){
                var check = true;
                $('.cart_products .cart_item').each(function(){
                    var hash_id = $(this).attr('deal_hash_id');
                    if($('#gift_'+hash_id).length > 0 && !$('#gift_'+hash_id).parent().parent().hasClass('enable')){
                        alert('请删除不符合满赠规则的商品，再去结算：）');
                        check = false;
                    }
                });
                if( sale_box_obj.find('.enable').length > 0 ){
                    if(sale_box_obj.find('.enable li.sold_out').length != 3){
                        if( sale_box_obj.find('li.selected').length== 0 ){
                            if(!confirm('您还没有选择赠品，确定不要赠品去支付么？')){
                                return false;
                            }
                        }
                    }
                }

                if(check){
                    window.location.href = "/i/cart/confirmation";
                }
            }else{
                window.location.href = "/i/cart/confirmation";
            }
            if(window.event) window.event.returnValue = false;
        };
        // 执行 code
        if($('.sale_gifts_selector').length>0){
            Eofan.OrderNew.changeSaleGiftBoxItemStatus();
            $('.sale_gifts_selector li').click(add_sale0818_gift_to_cart);

            $('#go_to_order').attr('href','javascript:void(0)').click(check_gift);
        }
    },
    /*
    *  购物车载入时，赠品判断。
    * */
    changeSaleGiftBoxItemStatus:function(){
        var cart_deals = $('.cart_products .cart_item'),
             gifts = $('.sale_gifts_selector .level li'),
             levels = $('.sale_gifts_selector .level'),
             i_len = cart_deals.length,
             j_len = gifts.length,
             has_gift = false;

        if (j_len < 1){
            return false;
        }
        
        for(var i = 0 ; i < i_len; i++){
            for(var j = 0 ; j < j_len;j++){
                if($(cart_deals[i]).attr('deal_hash_id') == $(gifts[j]).attr("hash_id")){
                    $(gifts[j]).addClass('selected');
                    has_gift = true;
                    break;
                }
            }
        }

        var redeem_amount = parseFloat($("#J_redeem_amount").val());
        levels.each(function(){
            var level = parseFloat($(this).attr('level'));
            if( redeem_amount >=level){
                $(this).addClass('enable');
            }else{
                $(this).removeClass('enable');
            }
        });

        if(!has_gift){
            $(gifts).removeClass('selected');
        }
    },
    enableCreditTopupLightbox: function(url) {
        url = url || '/payment_confirm.html';
        // pay页面
        if ($("#order-pay-form").length > 0 ) {
            $("#order-pay-form").submit(function() {
                try{
                    if (typeof (setCart.pay) == "function") {
                        setCart.pay($(this).attr("target") === "_blank");
                    }
                    if ((typeof (setCart.pay2) == "function")) {
                        var orderString = $(this).attr("order_ids") || "";
                        setCart.pay2(orderString.replace(/,/g, "|"), $(this).attr("target") === "_blank");
                    }
                }catch(e){}

                if($("#order-pay-form").attr('is_balance_payment') == '0'){
                    Eofan.Core.lightbox.init({
                        url: url + '?cache=0',
                        callback: function() {},
                        shadow: true,
                        sTop: 150
                    });
                    return true;
                }
            });
        }
        // check页面
        if( $("#check_pay_form").length > 0 ){
            $("#check_pay_form").submit(function(){
                //当从我的个人中心中-我的订单页面跳转到付款页面时判断是否勾选了余额付款，当未勾选时，点击结算按钮，则新页面打开到支付宝等相关支付平台，否则直接跳转到余额支付成功页面
                 if( $('#check_pay_form').attr('is_balance_payment') == '0'){
                    if($('input[name=gateway]', $(this)).filter(':checked').length){
                    Eofan.Core.lightbox.init({
                            url:  url + '?cache=0',
                        callback: function() {},
                        shadow: true,
                        sTop: 150
                    });
                    }else{
                        alert('请选择支付方式。');
                        return false;
                    }
                 }

                try{
                    if (typeof (setCart.pay_again) == "function") {
                        var type_arr = ['bank', 'platform', 'quick', 'balance'],
                            sub_type = $('#use_balance_checkbox').attr("checked") ? type_arr[type_arr.length - 1] : type_arr[$('.ul_on').index()];
                        setCart.pay_again(sub_type, $(this).attr("target") === "_blank");
                    }
                    if (typeof (setCart.pay_again2) == "function") {
                        var orderString = "",
                            orders = $(".cart_info .order_info");
                        orders.each(function(key, order){
                            order = $(order);

                            if (key != 0){
                                orderString += "|";
                            }

                            var orderId = order.attr("order_id");
                            orderString += (orderId ? orderId : 0);
                        });
                        setCart.pay_again2(orderString, $(this).attr("target") === "_blank");
                    }
                }catch(e){}

                    return true;
            });
        }
    },

    /*
    * 购物车ajax加载crosssale模块
    */
    enableAjaxCrossale:function(){
        
        var triggers = $('#cart_other_products .cart_cross_triggers a'),
            mall_box = $('#cart_other_products .mall_box');
        triggers.mouseenter(function(e){
            e.preventDefault();
            var self = $(this),
                tag = self.attr('tag');

            triggers.removeClass('current');
            self.addClass('current');

            mall_box.hide().removeClass('current');
            $('#' + tag).show().addClass('current');
            
        });

        var insert_data = function(objs,type_id){

            var product_list = $("#product_list_" + type_id),
                container = $('#featured_' + type_id);

            if( objs.length >= 4 ){
                var recent = objs,
                    recent_html = '',
                    l = recent.length,
                    i = 0;

                for(;i<l && i <10;i++){
                    var referer = '',
                        hash_id = recent[i].hash_id,
                        brand_id = recent[i].brand_id || 0,
                        category_id = recent[i].category_v3_3 || 0,
                        product_id = recent[i].product_id,
                        price = (new Number(recent[i].discounted_price)).toFixed(1),
                        pic_url = recent[i].image_url + '_std/' + product_id + '_160_160.jpg',
                        name = recent[i].short_name,
                        discount = recent[i].discount,
                        discount_html = '',
                        buyer_num = recent[i].buy_number,
                        buyer_num_html = '',
                        original_price = recent[i].original_price,
                        original_price_html = '',
                        type = recent[i].type;

                    if(type_id === 'recent'){
                        pic_url = recent[i].image_100.replace('100_100', '160_160');
                        hash_id = recent[i].deal_hash_id;
                    }

                    if ( parseFloat(discount) < 9.5 ){
                        discount_html = '<span class="discount">'+ discount +'折/</span>';
                    }

                    if ( buyer_num != '' && typeof(buyer_num)!= 'undefined' ){
                        buyer_num_html = '<p class="buyer_num">最近<span class="blue">'+buyer_num+'</span>人购买</p>';
                    }

                    if ( original_price != '' && original_price != null && parseFloat(discount) < 9.5){
                        original_price_html = '<span class="grey">¥'+original_price+'</span>'
                    }

                    if(type == 'deal'){
                        referer = 'flow_cart_'+type_id+'_addtocart_'+hash_id;

                        var url = RM_CURRENT_SITE_MAIN_WEBBASEURL + '/i/deal/'+hash_id+'.html?from='+referer+'_new',
                            li = '<li class="cross_sale_deal" deal_hash_id="' + hash_id + '"><div class="pic"><a href="'+ url +'" target="_blank"><img src="'+pic_url+'" /></a></div><div class="name"><a href="'+ url +'" target="_blank">'+discount_html+name+'</a></div><div class="price"><span>¥'+ price +'</span>'+original_price_html+'</div>'+buyer_num_html+'<div class="button"><a href="javascript:void(0)" class="link" category_id="'+ category_id +'" brand_id="'+ brand_id +'" product_type="'+ type +'" product_id="'+product_id+'" hash_id="'+ hash_id +'"><img alt="加入购物车" src="'+RM_IMGDIR+'/cart_v2/btn_small_pink.jpg" /></a></div></li>';
                    }else if(type == 'mall'){
                        referer = 'flow_cart_'+type_id+'_addtocart_'+product_id;

                        var url ='http://mall.'+ RM_SITE_MAIN_TOPLEVELDOMAINNAME + '/product_'+product_id+'.html?from='+referer+'_new',
                            li = '<li class="cross_sale_deal mall_product"><div class="pic"><a href="'+ url +'" target="_blank"><img src="'+pic_url+'" /></a></div><div class="name"><a href="'+ url +'" target="_blank">'+discount_html+name+'</a></div><div class="price"><span>¥'+ price +'</span>'+original_price_html+'</div>'+buyer_num_html+'<div class="button"><a href="'+url+'" class="link" category_id="'+ category_id +'" brand_id="'+ brand_id +'" product_type="'+ type +'" target="_blank" product_id="'+product_id+'"><img alt="加入购物车" src="'+RM_IMGDIR+'/cart_v2/btn_small_pink.jpg" /></a></div><select class="sku_select"></select></li>';
                    }
                    recent_html+=li;
                }



                product_list.html(recent_html);


                var mall_products = product_list.find("li.cross_sale_deal a.link");
                mall_products.click(function(e){
                    e.preventDefault();
                    var self = $(this),
                        parent = self.closest("li.cross_sale_deal"),
                        sku_select = parent.find(".sku_select"),
                        href = self.attr('href'),
                        from = '?from='+url_from+'|flow_cart_cross_'+type_id+'_addtocart',
                        hash_id = self.attr("hash_id") || '',
                        id = self.attr("product_id");

                    try{
                        if (typeof (setCart.addToCart) == "function") {
                        setCart.addToCart(1, {
                            pid: id,
                                cid: self.attr('category_id'),
                            brand_id: self.attr('brand_id'),
                                url: '?from=flow_cart_cross_'+type_id+'_addtocart',
                                from: 'flow_cart_cross_'+type_id+'_addtocart',
                            jm_price: parent.find('.price').find('span').first().text().substring(1),
                            product_type: self.attr('product_type'),
                            result_cnt: parent.siblings().length + 1,
                            pos: parent.index() + 1
                        });
                        }
                    }catch(e){}

                });
            }else{
                container.remove();
                $('#cart_other_products .cart_cross_triggers a[tag="featured_'+ type_id +'"]').remove();
            }
        };

        $.ajax({
            url: RM_SITE_MAIN_WEBBASEURL+"i/ajax/get_view_history?callback=?",
            type: 'GET',
            dataType: 'jsonp',
            jsonp: 'callback',
            success: function(data){
                insert_data(data, 'recent');
            }
        });

        
        var url_from = getUrlArgs('from') || '';//获取from参数
        $.ajax({
            type:"POST",
            url:"/i/cart/getCartRecommendations?" + (+new Date()),
            dataType: "json",
            success:function(data){
                if (data == null){
                    return ;
                }


                for ( var i in data ){
                    var objs = data[i],
                        type_id = i;
                    
                    insert_data(objs,type_id);

                }

                if ( $('#cart_other_products .cart_cross_triggers a').length > 0 ){
                    $('#cart_other_products .cart_cross_triggers a').first().mouseenter();
                    $('#cart_other_products').show();
                }
                
                


            }
        });
    },
    
    enableCartShow:function(){
        var search_input = $('#cart .search .search_input'),
            search_input_default = search_input.attr('default_val'),
            form = $('#cart .search form'),
            btn_cart_search = $('#cart .search .btn_cart_search');

        search_input.val(search_input_default);

        btn_cart_search.click(function(e){
            e.preventDefault();
            var search_input_val = $.trim(search_input.val());
            if ( search_input_val == search_input_default || search_input_val == '' ){
                alert('搜索字数太少，会影响搜索结果，重新填写一下吧');
                return false;
            }
            form.submit();
            
        });


        search_input.focus(function(){
            
            var search_input_val = $.trim(search_input.val());
            
            if ( search_input_val == search_input_default ){
                $(this).val('');
                $(this).addClass('active');
            }
            
        }).blur(function(){
            var search_input_val = $.trim(search_input.val());
            
            if ( search_input_val == '' ){
                $(this).val(search_input_default);
                $(this).removeClass('active');
            }
            
        });
        
        
        var sale_tags = $('#cart_products .cart_item .sale_info');
        
        sale_tags.hover(function(){
            $(this).addClass('sale_info_hover');
        },function(){
            $(this).removeClass('sale_info_hover');
        });

        
        
        // 促销倒计时
        var sale_info = $('#cart_products tr.sale_info'),
            timers = sale_info.find('.timer'),
            now_time,
            diffs = [],
            count_time = function (left,now, obj,day) {
                var ld,ls,lh,lm,html;
                left = parseInt(left*1000);
                ls = left ;

                if (ls > 0){
                    
                    ld =  parseInt(ls / 86400000).toString();
                    ld = ld.length > 1 ? ld: '0' + ld;

                    if(day){
                        ls = ls % 86400000;
                    }
                    lh = parseInt(ls / 3600000).toString();
                    lh = lh.length > 1 ? lh: '0' + lh;


                    ls = ls % 3600000;
                    lm = parseInt(ls / 60000).toString();
                    lm = lm.length > 1 ? lm: '0' + lm;

                    ls = parseInt((ls % 60000) / 1000);
                    ls = ls.toString().length > 1 ? ls: '0' + ls;


                    
                    html = ld + '天' +   lh + '时' + lm + '分' + ls + '秒';

                    $(obj).html(html);
                    
                }else {
                    $(obj).html('已结束');
                }

            };

        if ( timers.length > 0){

            for (var i = 0 ; i < timers.length ; i++){
                diffs.push(timers[i].getAttribute("diff"));
            }

            // 一个timer控制全部
            var $window = $(window);
            setInterval(function(){
                now_time = (new Date()).getTime();

                for (var i = 0 ; i < timers.length ; i++){
                    diffs[i] = diffs[i] - 1;
                }

                var winScrlTop = $window.scrollTop();

                var winScrlTopHeight = winScrlTop+ $window.height();

                for (var i = 0 ; i < timers.length ; i++){
                    var pos  = $(timers[i]).offset();
                    if(pos.top + 30 > winScrlTop && pos.top < winScrlTopHeight) {
                        count_time(diffs[i], now_time, timers[i],true);
                    }
                }
            },1000);
        };
        
        
        var count = $('#cart_amount_line'),
            $window = $(window),
            obj_top;

        if ( count.length ){
            obj_top = count.offset().top;

            $window.scroll(function(){
                var win_top = $window.height() + $window.scrollTop(),
                    obj_height = count.innerHeight();

                if ( obj_top + obj_height >= win_top){
                    if ($.browser.msie && $.browser.version == '6.0'){
                        var left = ($window.width() - 958) / 2;
                        count.css({'position':'absolute','top':(win_top - obj_height)+'px','left':left+'px','width':'958px',zIndex:'1000'});
                    }else{
                        count.css({'position':'fixed','bottom':'0px','width':'958px',zIndex:'1000'});
                    }
                }else{
                    count.removeAttr('style');
                }
            });
        }
    },
    enablePaymentStatus: function(){


        if ( $('.J_Collect').length > 0 ){
            // Collect product
            $('.J_Collect').click(function(e){

                e.preventDefault();

                var self = $(this),
                    pid = self.attr('pid');


                callback_fav_product = function(data){
                    if(data.isOk == 'yes') { // 收藏成功
                        alert('收藏成功！');
                    } else if(data.isOk == 'no') { //  收藏失败
                        alert(data.msg);
                    }
                };

            });
        }

        

        if ( $('.on_sale').length < 1 ){
            return false;
        }

        // add to cart again
        var btn_add_again = $('.J_AddAgain'),
            check_boxes,
            items_html = [],
            len;

        btn_add_again.click(function(e){
            e.preventDefault();

            check_boxes = $('.on_sale input:checked');
            len = check_boxes.length;

            if ( len < 1 ){
                alert('您没有选择任何商品！');
                return ;
            }

            for ( var i = 0 ; i < len ; i++ ){
                items_html.push(check_boxes.eq(i).attr('items'));
            }

            items_html = 'http://cart.'+RM_SITE_MAIN_TOPLEVELDOMAINNAME+'/i/cart/new_items/'  + items_html.join('|') + '?from=payment_status';

            location.href = items_html;

        });


        


    },
    enableGATracking:{
        // track add.tpl
        track_add:function(type){

            _gaq.push(['_trackEvent',
                'cart_add', // category of activity
                type // Action
            ]);
            
            
            var cart_items = $('#cart_products .cart_item'),
                len = typeof(cart_items) != 'undefined' ? cart_items.length : 0,
                item ,
                pid , // 商品编号 hash_id || product_id
                pname , // 商品名称 
                pprice , // 商品价格
                pnum , // 商品数量
                ptypeid , // 商品分类编号
                ptypename ; // 商品分类名称

            // 购物车为空的时候
            if ( len <= 0 ){
                return false;
            }

            for ( var i = 0 ; i < len ; i++ ){
                item = $(cart_items[i]);
                pid = item.attr('product_id') || item.attr('deal_hash_id');
                pname = $.trim(item.find('.name a').html());
                pprice = parseFloat(item.find('.price_box span').html());
                pnum = parseInt(item.find('.item-buy-quantity-input').val());
                ptypeid = typeof (item.attr('product_id')) != 'undefined' ? 'product' : 'deal';
                ptypename = ptypeid;
                // 下面代码是商品组代码，根据订单中包括多少种商品来部署，每种商品部署一组
                _gaq.push(['_addItem',
                    '',    // transaction ID - necessary to associate item with transaction
                    pid, //  SKU/code - required
                    pname,   // product name - necessary to associate revenue with product
                    ptypeid,     // category or variation
                    pprice,    // unit price - required
                    pnum        // quantity - required
                ]);
            }

            // 下面是提交订单代码，此段代码必须放在以上代码后面 - 必填项
            _gaq.push([ '_trackTrans' ]);
            
        },

        track_confirmation:function(type){
            
            _gaq.push(['_trackEvent',
                'cart_confirmation', // category of activity
                type // Action
            ]);
            
        },
        
        track_pay:function(type){
            
            _gaq.push(['_trackEvent',
                'cart_pay', // category of activity
                type // Action
            ]);
            
        },
        track_check:function(type){

            _gaq.push(['_trackEvent',
                'cart_check', // category of activity
                type // Action
            ]);

        },
        // track payment_status.tpl
        track_payment:function(){

            _gaq.push(['_trackEvent',
                'cart_payment_status', // category of activity
                'view' // Action
            ]);

            var orders = $('.pay_status .order_status tr'),
                len = typeof(orders) != 'undefined' ? orders.length : 0;

            if ( len > 0 ){

                var order_id , // 订单编号
                    order_info , // 订单数据
                    order_status , // 订单成功/失败
                    order_detail , // 订单详情
                    item_details , // 订单内容
                    real_payment, // 实际支付金额
                    order_time , // 下单时间
                    is_cod, // 是否为cod
                    pid , // 商品编号 hash_id || product_id
                    pname , // 商品名称 
                    pprice , // 商品价格
                    pnum , // 商品数量
                    ptypeid , // 商品分类编号
                    ptypename ; // 商品分类名称


                for ( var i = 0 ; i < len ; i++ ){
                    order_info = $(orders[i]).attr('order_info');
                    is_cod = $(orders[i]).attr('is_cod') == null ? 'normal' : 'cod';
                    order_status = $(orders[i]).closest('.order_status').hasClass('order_status_success') ? 'success' : 'fail';
                    
                    var data = $.parseJSON(order_info);
                    if (data && data.status == 1) {
                        order_detail = data.order;

                        // order id
                        order_id = parseInt(order_detail.order_id);

                        // real payment
                        real_payment = parseFloat(order_detail.total_price);

                        // 下单时间
                        order_time = new Date();
                        order_time.setTime(RM_SERVER_TIME*1000);

                        _gaq.push(['_addTrans',
                            order_id,           // transaction ID - required
                            order_time, // affiliation or store name
                            real_payment,          // total - required; Shown as "Revenue" in the Transactions report. Does not include Tax and Shipping.
                            order_status,           // tax
                            is_cod,          // is cod
                            '',       // city
                            '',     // state or province
                            ''             // country
                        ]);

                        // 订单中的items
                        item_details = order_detail.item_details;

                        for ( var item in item_details ){
                            var item = item_details[item];
                            pid = item.deal_hash_id.length > 0 ? item.deal_hash_id : item.product_id;
                            pname = item.deal_short_name;
                            pprice = item.deal_price;
                            pnum = item.quantity;
                            ptypeid = item.deal_hash_id.length > 0 ? 'deal' : 'product';
                            ptypename = ptypeid;


                            // 下面代码是商品组代码，根据订单中包括多少种商品来部署，每种商品部署一组
                            _gaq.push(['_addItem',
                                order_id, // transaction ID - necessary to associate item with transaction
                                pid,    // SKU/code - required
                                pname,   // 请填入商品名称  - 必填项
                                ptypeid,     // 请填入商品分类编号  - 必填项
                                pprice,    // 请填入商品金额  - 必填项
                                pnum        // 请填入商品数量  - 必填项
                            ]);

                        }

                    }

                }

                // 下面是提交订单代码，此段代码必须放在以上代码后面 - 必填项
                _gaq.push([ '_trackTrans' ]);

            }


        }

    },
    enableEcommerceTracking : function() {
        // enable GA ecommerce tracking
        var _$orderPaymentSuccess = $('#cart .order_status_success tr');
        if (_$orderPaymentSuccess.length > 0) {
            _$orderPaymentSuccess.each(function(){
                //var orderId = $(this).attr("order_id");
                var orderInfo = $(this).attr("order_info");
                if (orderInfo != null && orderInfo.length > 0) {
                    var data = jQuery.parseJSON(orderInfo);
                    if (data.status == 1) {
                        var order = data.order;
                        with(order) {
                            window._gaq = window._gaq || [];
                            _gaq.push(['_addTrans',
                                order_id,
                                // order ID - required
                                'cosmetics.store.eofan',
                                // affiliation or store name
                                total_price,
                                // total - required
                                '',
                                // tax
                                delivery_fee,
                                // shipping
                                '',
                                // city
                                '',
                                // state or province
                                ''
                                // country
                                ]);

                            for (var item in item_details) {
                                with(item_details[item]) {
                                    // add item might be called for every item in the shopping cart
                                    // where your ecommerce engine loops through each item in the cart and
                                    // prints out _addItem for each
                                    _gaq.push(['_addItem',
                                        order_id,
                                        // order ID - required
                                        deal_hash_id,
                                        // SKU/code - required
                                        deal_short_name,
                                        // product name
                                        attribute_selections,
                                        // category or variation
                                        deal_price,
                                        // unit price - required
                                        quantity
                                        // quantity - required
                                        ]);
                                    }
                            };
                        }
                        _gaq.push(['_trackTrans']); //submits transaction to the Analytics servers
                    }
                }
            });
        }
    },
    
    // all adwq tracking
    enableADWQTracking:{
        
        // track add.tpl
        track_add:function(type){
            
            var cart_items = $('#cart_products .cart_item'),
                len = typeof(cart_items) != 'undefined' ? cart_items.length : 0,
                item ,
                pid , // 商品编号 hash_id || product_id
                pname , // 商品名称 
                pprice , // 商品价格
                pnum , // 商品数量
                ptypeid , // 商品分类编号
                ptypename ; // 商品分类名称
                
            // 购物车为空的时候
            if ( len <= 0 ){
                return false;
            }

            _adwq.push([ '_setDataType',
                type
            ]);

            //当前登陆用户ID
            if ( RM_UID != null ){
                _adwq.push([ '_setCustomer',
                    RM_UID
                ]);
            }else{
                _adwq.push([ '_setCustomer',
                    'NOT_LOGIN'
                ]);
            }
            
            for ( var i = 0 ; i < len ; i++ ){
                item = $(cart_items[i]);
                pid = item.attr('product_id') || item.attr('deal_hash_id');
                pname = $.trim(item.find('.name a').html());
                pprice = parseFloat(item.find('.price_box span').html());
                pnum = parseInt(item.find('.item-buy-quantity-input').val());
                ptypeid = typeof (item.attr('product_id')) != 'undefined' ? 'product' : 'deal';
                ptypename = ptypeid;
                // 下面代码是商品组代码，根据订单中包括多少种商品来部署，每种商品部署一组
                _adwq.push(['_setItem',
                    pid,    // 请填入商品编号  - 必填项
                    pname,   // 请填入商品名称  - 必填项
                    pprice,    // 请填入商品金额  - 必填项
                    pnum,        // 请填入商品数量  - 必填项
                    ptypeid,     // 请填入商品分类编号  - 必填项
                    ptypename        // 请填入商品分类名称  - 必填项
                ]);
            }
            // 下面是提交订单代码，此段代码必须放在以上代码后面 - 必填项
            _adwq.push([ '_trackTrans' ]);
        },
        
        // track pay.tpl
        track_pay:function(){
            
            var orders = $('#cart .order_info_val'),
                len = typeof(orders) != 'undefined' ? orders.length : 0;
            
            if ( len > 0 ){

                var order_id = '', // 订单编号
                    order_info , // 订单数据
                    order_status = '' , // 订单成功/失败
                    order_detail , // 订单详情
                    item_details , // 订单内容
                    real_payment = 0, // 实际支付金额
                    order_time , // 下单时间
                    pid , // 商品编号 hash_id || product_id
                    pname , // 商品名称 
                    pprice , // 商品价格
                    pnum , // 商品数量
                    ptypeid , // 商品分类编号
                    ptypename , // 商品分类名称
                    end_tag = '_',
                    all_items = [];  // 所有商品
                
                
                for ( var i = 0 ; i < len ; i++ ){
                    
                    if ( i == len - 1 ){
                        end_tag = '';
                    }
                    
                    order_info = $(orders[i]).attr('order_info');
                    
                    var data = $.parseJSON(order_info);
                    if (data.status == 1) {
                        order_detail = data.order;

                        // order id
                        order_id += parseInt(order_detail.order_id) + end_tag;
                        
                        // real payment
                        real_payment += parseFloat(order_detail.total_price);
                        
                        
                        // 订单中的items
                        item_details = order_detail.item_details;
                        all_items.push(item_details);
                        
                        
                    }
                    
                }
                
                if ( order_id.length > 0 ){
                
                    _adwq.push([ '_setDataType',
                        'order'
                    ]);

                    //当前登陆用户ID
                    _adwq.push([ '_setCustomer',
                        RM_UID
                    ]);
                
                    _adwq.push(['_setOrder',
                        order_id,     // 12345678是一个例子，请填入订单编号  - 必填项
                        real_payment,   // 100.00是一个例子，请填入实际支付金额 – 必填项
                        '' // 自选
                    ]);
                
                    for ( var i = 0 ; i < all_items.length ; i++ ){
                        
                        var item_details = all_items[i];
                        for ( var item in item_details ){
                            var item = item_details[item];
                            pid = item.deal_hash_id.length > 0 ? item.deal_hash_id : item.product_id;
                            pname = item.deal_short_name;
                            pprice = item.deal_price;
                            pnum = item.quantity;
                            ptypeid = item.deal_hash_id.length > 0 ? 'deal' : 'product';
                            ptypename = ptypeid;
                            
                            
                            // 下面代码是商品组代码，根据订单中包括多少种商品来部署，每种商品部署一组
                            _adwq.push(['_setItem',
                                pid,    // 请填入商品编号  - 必填项
                                pname,   // 请填入商品名称  - 必填项
                                pprice,    // 请填入商品金额  - 必填项
                                pnum,        // 请填入商品数量  - 必填项
                                ptypeid,     // 请填入商品分类编号  - 必填项
                                ptypename        // 请填入商品分类名称  - 必填项
                            ]);

                        }
                        
                    }

                    // 下面是提交订单代码，此段代码必须放在以上代码后面 - 必填项
                    _adwq.push([ '_trackTrans' ]);
                }
                
            }
            
            

        }
        
    },

    initGatewayToggle: function(){
        $('.gateway_ul>li').click(function(){
            var $this = $(this),
                $input = $this.find('>input');

            if($input.attr('disabled') === false && !$this.hasClass('weihu')) {
                $input.attr('checked', true);
                $this.siblings('li').removeClass('ul_on').addClass('ul_off').find('>input').attr('checked', false);
                $this.removeClass('ul_off').addClass('ul_on');

                /*if ($input.attr("id") == "baidu-radio"){
                    $this.find(".g_ul li:first").trigger("click");
                }*/
            }
        });

        $('.g_ul').delegate('li', 'click', function(e){
            e.stopPropagation && e.stopPropagation();
            var $this = $(this),
                $input = $this.find('input');

            $this.addClass('selected');
            $input.attr('checked', true);
            $('input[name=gateway]').not(':checked').closest('li').removeClass('selected');
        });
    }
};
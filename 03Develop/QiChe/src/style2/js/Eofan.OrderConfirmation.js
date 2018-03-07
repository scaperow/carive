window.Eofan = window.Eofan || {};
window._adwq = window._adwq || [];

alert_message = "";
Eofan.OrderConfirmation = {
    DefaultValue : [],
/*
    setDefaultValue:function(){
        $(".option_box input[name='address_id']").each(function(){
            if(currentPageDefaultValue.address_id == $(this).val()){
                $(this).parent().addClass("selected");
                $(this).attr("checked","checked").click();
            }
        });
    },
*/
    WebSite:$("#J_WebSite").val()+"/",
    total_amount:1, //this mean that have been pay money.
    init : function() {
        Eofan.OrderConfirmation.enableOptionManager();
        Eofan.OrderConfirmation.changeDeliveryFee();
        Eofan.OrderConfirmation.show_promo_card_box();
        Eofan.OrderConfirmation.choose_promo_card();
        Eofan.OrderConfirmation.enableBalanceConfirm();
        Eofan.OrderConfirmation.choose_red_card();
        Eofan.OrderConfirmation.enableDiscountTooltip();
    },
    enableDiscountTooltip: function(){
        //满返详情 hover 提示信息
        var $a = $('.discount_detail').find('a');
        $a.hover(function(){
            $(this).closest('.discount_common').find('.discount_tooltip').show();
        }, function(){
            $(this).closest('.discount_common').find('.discount_tooltip').hide();
        });
    },
    enableOptionManager: function() {
        $(".cart_products_v2").each(function(){
            if( $(this).attr("cart_key").indexOf("luxury") > 0){
                currentPageDefaultValue.has_luxury_deal = true;
            }
        });


        //#shipping_instant, #shipping_delay, #shipping_merge
        $('.J_EMS, .J_Express, #sf-express').click(function(){
            Eofan.OrderConfirmation.update_cod_options();
        });
        // 初始化默认项调用
        var selected = $("div.selected[selector='old_address'] input");
        if(selected.length > 0){
            selected.click();
        }else{
            //没有默认选中项，很可能没有地址，这时弹出 新地址填写框//注释是因为添加地址变了方式
            //$('#address_selector .option_box_new').click();
        }

    },
    enableBalanceConfirm:function(){
        var mobile_confirm = $("#mobile_confirm"),
            input_box = $("#use_balance_checkbox"),
            close = $('.close',mobile_confirm),
            binded_boxs = $(".is_bind",mobile_confirm),
            not_binded_boxs = $(".not_bind",mobile_confirm),
            bind_box = $("#mobile"),
            step1_boxs = $(".step1",mobile_confirm),
            step2_boxs = $(".step2",mobile_confirm)//,
            //uid = $.cookie("uid");



        $("#bind_new_mobile").click(function(e){
            e.preventDefault();
            binded_boxs.hide();
            not_binded_boxs.hide();
            step1_boxs.show();
            $("#rebindcheck").val("下一步").show();
            $("#mobile_step1").show();
            Eofan.MobileBind.enableInput();
            //var mobile = $('<input name="mobile" id="mobile" type="text" class="not_bind"/>');
            //$("#get_confirm_code").before(mobile);
        });

    }
}

$(document).ready(function(){

    Eofan.OrderConfirmation.DefaultValue = currentPageDefaultValue;
    Eofan.OrderNew.setDefaultValue( currentPageDefaultValue );

});
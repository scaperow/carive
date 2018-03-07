/**
 * Created by KZK on 2014/11/20.
 */

var address_count = 1;
var is_need_id = 0 ? true : false;//是否有海淘商品-(需要验证身份证)
var addressID = 0;
var addDiv = null;
var confirm_site = {province: {}, city: {}, county: {}, street: {}},//四级地址选中值
    isStreetCode = false;//是否有第四个地址--false:没有,true：有
$(function(){
    var Wi = [ 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1 ];    // 加权因子
    /*
     * 判断收货姓名：姓名用字必须是汉字字符，并且应在2个汉字（含）以上、6个汉字（含）以下，同时不含有“先生”、“女士”、“小姐”、“太太”、“男士”字符
     * */
    var filterKeywords = ["先生","女士","小姐","太太","男士"];
    function checkName(name){
        name = $.trim(name);
        var reg = /^[\u4E00-\u9FA5]{2,6}$/;
        if(!reg.test(name)){
            return false;
        }
        for(var key in filterKeywords){
            if(name.match(filterKeywords[key])){
                return false;
            }
        }
        return true;
    }
    //拼接选择的地址
    var confirmHtml = function () {
        var confirmHtml = '';
        for (var k in confirm_site) {
            if (confirm_site[k] && confirm_site[k].name) {
                confirmHtml += '<span class="confirm_show">'+confirm_site[k].name+'</span>';
            }
        }
        $('#JS_confirm_show_box').html( confirmHtml );
    }
    var streetselected = function(){

        $('#JS_receiver_name').blur( function () {
            var $this = $(this),
                val = $.trim( $this.val() );

            //不为空+汉子和字母
            if (val == '' || !/^[\u4E00-\u9FA5A-Za-z]+$/.test(val)) {
                $this.addClass('error').parent().siblings('.JS_error_box').show();
                return
            } else {
                $this.removeClass('error').parent().siblings('.JS_error_box').hide();
            }
            //限制10字符
            var arrVal = val.split(''),
                strNum = 0;
            for (var i = 0, iLen = arrVal.length; i < iLen; i++) {
                if (/^[A-Za-z]$/.test( arrVal[i]) ) {
                    strNum += 1;
                } else {
                    strNum += 2;
                }
            }
            if (strNum > 20) {
                $this.addClass('error').parent().siblings('.JS_error_box').show();
            }

        });
        $('#JS_address').blur( function () {
            var $this = $(this),
                val = $.trim( $this.val() );

            //不为空+长度3+全部数字+汉子和字母 空格，- 中划线，/,[ ],( ),#
            if (val == '' || val.length < 3 || !/^[\u4E00-\u9FA5A-Za-z\d\-\s\/\[\]\(\)\#]+$/.test(val) || /^[A-Za-z\d]+$/.test(val)) {
                $this.addClass('error').parent().siblings('.JS_error_box').show();
                return
            } else {
                $this.removeClass('error').parent().siblings('.JS_error_box').hide();
            }
            //限制6-200字符
            var arrVal = val.split(''),
                strNum = 0;
            for (var i = 0, iLen = arrVal.length; i < iLen; i++) {
                if (/^[\u4E00-\u9FA5]$/.test( arrVal[i]) ) {
                    strNum += 2;
                } else {
                    strNum += 1;
                }
            }
            if (strNum > 200 || strNum < 6) {
                $this.addClass('error').parent().siblings('.JS_error_box').show();
            }
        });
        $('#JS_phone').blur( function () {
            var $this = $(this),
                val = $.trim( $this.val() ),
                $input = $this.parent().parent().find('input[type="text"]');

            if ( ( $('#JS_phone_number_new').val() != '' && val == '' ) || ( val == $this.attr('data') && val != '' ) ) {
                $this.removeClass('error').parent().siblings('.JS_error_box').hide();
                if (val == $this.attr('data') && $input.hasClass('error')) {
                    $this.parent().siblings('.JS_error_box').show().siblings('.JS_tips').hide();
                    return
                }
                if (!$input.hasClass('error')) return;
            }
            //不为空+长度11全部数字
            if ( val == '' || !/^[\d]{11}$/.test(val) || val.slice(0,1) != '1' ) {
                $this.addClass('error').parent().siblings('.JS_error_box').show().siblings('.JS_tips').hide();
            } else {
                if ( /^[\d]*$/.test( $('#JS_phone_area_new').val() ) ) {
                    $('#JS_phone_area_new').removeClass('error');
                }
                $this.removeClass('error').parent().siblings('.JS_error_box').hide();
            }
            if ($input.hasClass('error')) {
                $this.parent().siblings('.JS_error_box').show().siblings('.JS_tips').hide();
            }
        });

        $('#JS_phone_area_new').blur( function () {
            var $this = $(this),
                val = $.trim( $this.val() ),
                $input = $this.parent().parent().find('input[type="text"]');
            if ( $('#JS_phone').val() != '' ) {
                $this.removeClass('error').parent().siblings('.JS_error_box').hide();
                if (!$input.hasClass('error') && /^[\d]*$/.test(val)) return;
            }
            if ( val != '' && ( ( val.slice(0,1) != '0' || !/^[\d]+$/.test(val) ) || val.length <= 2 ) ) {
                $this.addClass('error').parent().siblings('.JS_error_box').show().siblings('.JS_tips').hide();
            } else {
                $this.removeClass('error').parent().siblings('.JS_error_box').hide();
            }
            if ($input.hasClass('error')) {
                $this.parent().siblings('.JS_error_box').show().siblings('.JS_tips').hide();
            }
        });
        //座机号
        $('#JS_phone_number_new').blur( function () {
            var $this = $(this),
                val = $.trim( $this.val() ),
                $input = $this.parent().parent().find('input[type="text"]');

            if (val == $this.attr('data')) return

            if ( $('#JS_phone').val() != '' ) {
                $this.removeClass('error').parent().siblings('.JS_error_box').hide();
                if (!$input.hasClass('error') && /^[\d]*$/.test(val)) return;
            }

            if (!/^[\d]*$/.test(val) ) {
                $this.addClass('error').parent().siblings('.JS_error_box').show().siblings('.JS_tips').hide();
            } else {
                $('#JS_phone').removeClass('error');
                $this.removeClass('error').parent().siblings('.JS_error_box').hide();
            }

            if ($input.hasClass('error')) {
                $this.parent().siblings('.JS_error_box').show().siblings('.JS_tips').hide();
            }
        });

        //分机号
        $('#JS_phone_ext_new').blur( function () {
            var $this = $(this),
                val = $.trim( $this.val() ),
                $input = $this.parent().parent().find('input[type="text"]');

            if ( !/^[\d]*$/.test(val) ) {
                $this.addClass('error').parent().siblings('.JS_error_box').show().siblings('.JS_tips').hide();
            } else {
                $this.removeClass('error').parent().siblings('.JS_error_box').hide();
            }

            if ($input.hasClass('error')) {
                $this.parent().siblings('.JS_error_box').show().siblings('.JS_tips').hide();
            }
        });


        $(document).click( function (e) {
            if ($('#JS_receiver_name:visible').length == 0) return

            if ( $( e.target ).closest(".JS_site_menu").length ) {
                return false;
            }

            for (var k in confirm_site) {
                if (!confirm_site[k].name && $('.JS_site_menu[data-name="'+k+'"]').attr('change') == 'true') {
                    $('#JS_error_sele_site').show();break;
                }
            }

            $('.JS_site_menu_cont').slideUp(100);
        });

        var addressStr = '';
        $('.JS_site_menu_cont').delegate('a', 'click', function () {
            var $this = $(this),
                $box = $this.parents('.JS_site_menu_box'),
                $txt = $box.find('.JS_site_txt'),
                $next = $box.next('.JS_site_menu_box'),
                site = $this.html(),
                code = $this.attr('code'),
                key = $box.find('.JS_site_menu').attr('data-name'),
                boxIndex = 0,
                _addressStr = '';

            switch (key) {
                case 'province':
                    boxIndex = 0;break;
                case 'city':
                    boxIndex = 1;break;
                case 'county':
                    boxIndex = 2;break;
                case 'street':
                    boxIndex = 3;break;
            }

            var _initMenu = function (index) {
                var _key = $('.JS_site_menu:eq('+index+')').attr('data-name');
                confirm_site[_key] = {};

                $('.JS_site_menu:eq('+index+')').attr('change', 'false')
                    .find('.JS_site_txt').html( $('.JS_site_txt:eq('+index+')').attr('data') );

                if (index > boxIndex + 1) {
                    $('.JS_site_menu_box:eq('+index+')').addClass('disabled');
                }

                if (_key != 'street') {
                    isStreetCode = false;
                }
            }

            $next.removeClass('disabled').find('.JS_site_menu').attr('parentcode', code);

            if (confirm_site[key].name != site && key != 'street') {
                for (var i = boxIndex; i <= 3; i++) {
                    _initMenu(i);
                }
            }

            $next.find('.JS_site_menu').click();

            confirm_site[key] = {name: site, parent_code: code};

            for (var k in confirm_site) {
                if (k != 'street') {
                    _addressStr += confirm_site[k].name + '-';
                }
            }
            _addressStr = _addressStr.slice(0, -1);

            confirmHtml();

            $txt.html(site);
            $this.parents('.JS_site_menu_cont').find('a').removeClass('active');
            $this.addClass('active');
            $('#JS_error_sele_site').hide();

            if ( ( key == 'county' || key == 'street' ) &&  addressStr != _addressStr) {
                $.post('/Confirmation/LogisticsInfoAndPaymentInfo', {addressStr: _addressStr}, function (res) {
                    if (res.CodShow != 1) {
                        $('#JS_no_cod_tips').show();
                    } else {
                        $('#JS_no_cod_tips').hide();
                    }
                    addressStr = _addressStr;
                }, 'json')
            } else if (key != 'street') {
                $('#JS_no_cod_tips').hide();
            }
        });

    };

    var debugIe6 = function () {
        //ie6 奇葩，如果不点。元素错位，
        if (!-[1,] && !window.XMLHttpRequest) {
            $('#JS_receiver_name').click();
        }
    }

    $(".address_more").click(function(){
        var _this = $(this),_a = _this.find("a");
        if(_a.hasClass("stri_open")){
            _a.removeClass("stri_open").addClass("stri_close").html("收起收货地址<span></span>");
            $("#address_selector .option_box:gt(3)").show();
        }else{
            _a.addClass("stri_open").removeClass("stri_close").html("展开收货地址<span></span>");
            $("#address_selector .option_box:gt(3)").hide();
        }
    });

    var addressWarpHtml = $('#first_add_address_wrap').html();
    var getColorboxContent = function(){
        return '<div class="add_newlight selected_newlight" style="padding-left: 0;width:auto;"><div class="cart_pop_tlt">修改地址</div>'+addressWarpHtml+'</div>';
    };
    var xsrf='{{handler.xsrf_token}}';
    var addAddressInit = function(wrap){
        streetselected();
        wrap.find("#JS_new_address_submit_new").live('click',function(){
            var _self = $(this);
            // var id =_self.attr("address_id");
            var addForm = wrap;

            if (_self.attr('disabled') == 'true') return;

            var recipient_name = addForm.find('#JS_receiver_name').val(),
                recipient_province = addForm.find("#ddlProvince option:selected").text(),
                recipient_city = addForm.find("#ddlCity option:selected").text(),
                recipient_dist = addForm.find("#ddlCounty option:selected").text(),
                street_code = addForm.find("#ddlStreet option:selected").text(),
                recipient_address = addForm.find('#JS_address').val(),
                recipient_hp = addForm.find('#JS_phone').val(),
                recipient_tel_area = addForm.find('#JS_phone_area_new').val(),
                recipient_tel_number = addForm.find('#JS_phone_number_new').val(),
                recipient_tel_ext = addForm.find('#JS_phone_ext_new').val(),
                china_id_number = $.trim(addForm.find('#JS_china_id_number').val()),
                recipient_structuredCode = (isStreetCode && confirm_site.street.parent_code != '-1') ?
                    confirm_site.street.parent_code : addForm.find('.JS_site_menu:eq(3)').attr('parentcode');//区域id

            if (recipient_name == null || recipient_name == "") {
                // alert("请输入收货人姓名");
                addForm.find('#JS_receiver_name').blur();
                return false;
            } else if(!checkName(recipient_name) && confirm("收件人请使用真实姓名，否则您的商品将可能无法正常投寄") && is_need_id){
                return false;
            } else if ($("#ddlCounty  option:selected").text() == "区/县") {
                addForm.find('#JS_error_sele_site').show();
                return false;
            } else if (recipient_address == null || recipient_address == "") {
                // alert("街道地址不能为空。");
                addForm.find('#JS_address').blur();
                return false;
            } else if (! (recipient_hp || recipient_tel_number)) {
                // alert("电话和手机必须填一个。");
                addForm.find('#JS_phone').blur();
                return false;
            }else{
                addForm.find('#JS_error_sele_site').hide();
            }

            var hasError = false;
            addForm.find('input').each( function () {
                if ($(this).hasClass('error')) {
                    hasError = true;
                    return
                }
            });
            if (hasError) {
                return false
            }

            var param = {
                recipient_name: recipient_name,
                recipient_province: recipient_province,
                recipient_city: recipient_city,
                recipient_dist: recipient_dist,
                street_code: street_code,
                recipient_address: recipient_address,
                recipient_hp: recipient_hp,
                recipient_tel_area:recipient_tel_area,
                recipient_tel_number: recipient_tel_number,
                recipient_tel_ext:recipient_tel_ext,
                recipient_id_num:china_id_number,
                is_need_id: is_need_id,
                recipient_structuredCode: recipient_structuredCode,
                address_id:addressID
            };
            // 防止多次点击。
            _self.attr("disabled","true").addClass('disabled_btn');

            $.ajax({
                url: '/ajax/AddAddress',
                type: 'GET',
                dataType: 'json',
                data: param,
                success:function(data){
                    var d = {};
                    if(data.status == 1){
                        d = $.parseJSON(data.addAddress);
                        var address_id = d._data.id;
                        $('#address_selector').find(".option_box").removeClass('selected');
                        if(addDiv)
                        {
                            $(addDiv).hide();
                            addDiv = null;
                        }
                        var add_html = '<div class="option_box selected" selector="old_address">' +
                            '<input type="radio" id="address_'+address_id+'" value="'+address_id+'" name="address_id" class="rdoAddress" onclick="" checked="checked">' +
                            '<label for="address_'+ address_id +'" data_address="'+ d._data.address +'" class="address_lbl">' +
                            '<span><span class="addr_name">'+ d._data.name +'</span>' +
                            '<span class="addr_con">'+ d._data.province + '-' + d._data.city + '-' + d._data.region + ' ' + d._data.address +'</span>' +
                            '<span class="addr_num">'+ d._data.mobile +'&nbsp;'+  (d._data.tel||'') +'</span></span>' +
                            '<span class="btnEditAddress_new" title="修改地址" addressid="'+ address_id +'">修改</span>' +
                            '<span class="btnEditAddress_del" title="删除地址" addressid="'+ address_id +'">删除</span>';
                        //check_store(address_id);
                        //if (d.id_num) {
                        // add_html += '<div class="id_wrap"><span>'+d.id_num+'</span></div>';
                        //}
                        add_html += '</label></div>';
                        $('#address_wrap').prepend(add_html);

                        $("#cboxClose").click();
                        $('#address_wrap .option_box:eq(0)').click();

                    }else {
                        alert(data.msg);
                    }
                    _self.removeAttr("disabled").removeClass('disabled_btn');
                    //Eofan.OrderConfirmation.on_address_changed();

                }
            });
        });
    };

    $('#address_selector .add_address_btn').click(function(){
        $('#address_table').hide();
        addressID = 0;
        addDiv = null;
        $.colorbox({
            html: getColorboxContent(),
            width: 960,
            onClosed: function(){
                $("#address_selector").find(".selected").find("input").attr("checked", true);
            },
            onComplete: function(){
                debugIe6();
                $(".cart_pop_tlt").html("使用新地址");
                var addr_id = $('input[name=address_id]:checked').val('0');
            }
        });
        initLocation({sheng_val:"陕西",shi_val:"西安",xian_val:"",xiang_val:""});
        $('.selected_newlight').find('.formbutton').after('<a id="add_cancel" href="#">取消</a>');
        addAddressInit($("#cboxContent"));
        $("#add_cancel").bind("click",function(e){
            e.preventDefault();
            $("#cboxClose").click();
            $("#address_selector").find(".selected").find("input").attr("checked", true);
        });

    });
    var changeToZeroAddAddress = function(){
        var _wrap = $("#first_add_address_wrap");
        _wrap.find("input:text").val(""); //避免再次删除了所有地址 变成这种添加地址方式还有上次数据
        addAddressInit(_wrap.show());
        $("#default_address_wrap").hide();

        $('#first_add_address_wrap .tips_tit').hide();//隐藏-有身份提示--只是没有地址情况，新建和修改需要

        debugIe6();
    };

    $('.btnEditAddress_new').live('click',function(){
        addAddressInit($("#cboxContent"));

        var optionbox = $(this).parents('.option_box');
        var addressId = $(this).attr('addressId');
        addDiv = $(this).parent().parent().parent().find('div.option_box.selected');
        addressID = addressId
        $('#address_table').hide();
        $.colorbox({
            html:getColorboxContent(),
            width: 960,
            onComplete: function(){
                $(".cart_pop_tlt").html("修改地址");
                debugIe6();

                $('.add_newlight').hide().parents('#cboxContent').find('#cboxLoadingOverlay').show();
                ajaxHander();
            }
        });

        var editWrap = $('.add_newlight');
        editWrap.find('.formbutton').after('<a id="add_cancel" href="#">取消</a>');

        streetselected();

        var self = $(this);
        var editForm = $('.add_newlight');
        var receiver_name = editWrap.find("#JS_receiver_name"); //收货人
        var recipient_address = editWrap.find("#JS_address"); //收获地址
        var recipient_hp = editWrap.find("#JS_phone");//手机
        var recipient_tel_area = editWrap.find("#JS_phone_area_new");
        var recipient_tel_number = editWrap.find("#JS_phone_number_new");
        var recipient_tel_ext = editWrap.find("#JS_phone_ext_new");
        var china_id_number_input = editWrap.find('#JS_china_id_number');//身份证
        var recipient_province = editWrap.find('#ddlProvince');//省
        var recipient_city = editWrap.find('#ddlCity');//市
        var recipient_region = editWrap.find('#ddlCounty');//区
        var recipient_street = editWrap.find('#ddlStreet');//街道
        //editWrap.find("#ddlProvince option:selected").text(),

        var ajaxHander = function () {
            $.ajax({
                url: '/ajax/GetOneAddress',
                type: 'POST',
                dataType: 'json',
                data: {
                    address_id: addressId
                },
                success:function(data){
                    var status = parseInt(data.status);

                    if(status==1){
                        var d = $.parseJSON(data.addAddress)._data;
                        initLocation({sheng_val:d.province,shi_val:d.city,xian_val:"",xiang_val:""});
                        receiver_name.val(d.name);
                        recipient_address.val(d.address);
                        china_id_number_input.attr("deValue",d.id||'').val(d.id||'');

                        recipient_hp.val(d.mobile).attr('data', d.mobile);
                        recipient_province.val(d.province);//省
                        recipient_city.val(d.city);//市
                        recipient_region.val(d.region);//区
                        recipient_region.change();
                        recipient_street.val(d.street);//街
                        recipient_street.show();


                        $('.JS_site_menu_box:eq(3)').show();

                        confirmHtml();
                        editWrap.show().parents('#cboxContent').find('#cboxLoadingOverlay').hide();

                        $('.JS_site_menu_box').each(function () {
                            var $this = $(this),
                                $menu = $this.find('.JS_site_menu'),
                                $txt = $this.find('.JS_site_txt'),
                                key = $menu.attr('data-name');
                            if (key == 'city') {
                                _parentcode = d.city_code;
                            } else if (key == 'county') {
                                _parentcode = d.district_code;
                            }
                            if (confirm_site[key] && confirm_site[key].name) {
                                $txt.html( confirm_site[key].name );
                                $this.next('.JS_site_menu_box').removeClass('disabled')
                                    .find('.JS_site_menu').attr('parentcode', _parentcode);
                                $this.removeClass('disabled').find('.JS_site_menu').attr('parentcode', confirm_site[key].parent_code);
                            } else {
                                $txt.html( $txt.attr('data') );
                            }
                        });

                        var recipient_tel_number_val = '';

                        if(d.mobile.length <= 1){
                            recipient_tel_area.val("");
                            recipient_tel_number.val("");
                            recipient_tel_ext.val("");
                        }else{
                            // 有2个 - 时
                            if (d.mobile.indexOf("-") >= 0 && d.mobile.indexOf("-") != d.mobile.lastIndexOf("-")){
                                recipient_tel_number_val = d.mobile.slice(d.phone.indexOf("-")+1, d.mobile.lastIndexOf("-"))
                                recipient_tel_area.val(d.mobile.indexOf("-")==0 ? "" : d.mobile.slice(0, d.mobile.indexOf("-")));
                                recipient_tel_ext.val(d.mobile.slice(d.mobile.lastIndexOf("-")+1 , d.mobile.length));
                            }
                            // 只有一个 - 时,无尾号
                            else if(d.mobile.indexOf("-") >= 0 && d.mobile.indexOf("-") == d.mobile.lastIndexOf("-") ){
                                recipient_tel_number_val = d.mobile.slice(d.mobile.indexOf("-")+1, d.mobile.length);
                                recipient_tel_area.val(d.mobile.indexOf("-")==0 ? "" : d.mobile.slice(0, d.mobile.indexOf("-")));
                                recipient_tel_ext.val("");
                            }else{
                                recipient_tel_number_val = d.mobile;
                            }
                            recipient_tel_number.val( recipient_tel_number_val ).attr('data', recipient_tel_number_val);
                        }

                    }else{
                        try{
                            alert(data.message);
                        }catch(e){}
                    }
                }
            });
        }

        editWrap.find("#add_cancel").bind("click",function(e){
            e.preventDefault();

            if ( confirm('选择“关闭”将清空您的修改并返回上次选择状态，是否继续？') ){
                $("#cboxClose").click();
            }

        });
        return false;
    });
    $(".btnEditAddress_del").live('click',function(){
        if(confirm("您确认要删除该地址吗？")){
            var _this = $(this);
            $.ajax({
                url: '/ajax/RemoveAddress?address_id='+_this.attr("addressid"),
                type: 'POST',
                dataType: 'json',
                data: {},
                success:function(data){
                    var status = parseInt(data.status);
                    if(status==1 || data.type=='unknow_address'){
                        var _par = _this.parent().parent();
                        var _classStartus = _par.hasClass("selected"),_addressWrap = $("#address_wrap");
                        _par.remove();
                        //如果地址大于4个，删除一个还剩下4个以上，把紧挨的显示出来，如果已经显示了全部收货地址再执行一遍没关系
                        if(address_count>5){
                            //删除后只剩下4个  更多收货地址隐藏
                            if(address_count==6){
                                $(".address_more").hide();
                            }
                            _addressWrap.find(".option_box:eq(3)").show();
                        }
                        address_count = data.count;
                        //如果当前删除的是被选中的收货地址，重新选一个作为默认地址
                        if(_classStartus && address_count){
                            _addressWrap.find(".option_box:eq(0)").click();
                        }
                        //如果没有了地址，切换到添加地址
                        if(!address_count){
                            changeToZeroAddAddress();
                        }
                        if(address_count<6){
                            $(".address_more").hide();
                        }
                    }else{
                        try{
                            alert(data.msg);
                        }catch(e){}
                    }
                }
            });
        }
        return false;
    });



    if(address_count==0){
        changeToZeroAddAddress();
    }
});

















$(function(){
    var firstlen = $('.aplipay_first').length;
    var secondlen = $('.aplipay_second').length;

    var aplipay_click = function(name,num,ids,str1,str2){
        $('.'+ name +':gt('+ num +')').hide();
        $('.'+ name).last().after('<li class="aplipay_more"><a href="javascript:void(0)" id="'+ ids +'"><span class="stri stri_open"></span>'+ str2 +'</a></li>');
        $('#'+ ids).toggle(function(){
            $('.'+ name).show();
            $(this).html('<span class="stri stri_close"></span>'+ str1);
        },function(){
            $('.'+ name +':gt('+ num +')').hide();
            $(this).html('<span class="stri stri_open"></span>' + str2 );
        });

    };
    if( $('.aplipay_first') && firstlen > 8 ){
        var name = 'aplipay_first';
        var num = 7;
        var ids = 'aplipay_first_open';
        var str1 = '收起网银支付';
        var str2 = '更多网银支付';
        aplipay_click(name,num,ids,str1,str2);
    }
    if( $('.aplipay_second') && secondlen > 4 ){
        var name = 'aplipay_second';
        var num = 3;
        var ids = 'aplipay_second_open';
        var str1 = '收起快捷支付';
        var str2 = '更多快捷支付';
        aplipay_click(name,num,ids,str1,str2);
    }

    /*如果勾选了我要留言*/
    var messageWrap = $(".inv_info_message");
    $('.is_message').change(function(){
        if($(".is_message").attr("checked")){
            messageWrap.show();
        }else{
            messageWrap.hide();
        }
    });
    messageWrap.hide();

    /*hover 样式*/
    $('#address_selector .address_lbl').live('mouseover',function(){
        if( !$(this).hasClass('address_lbl_old')){
            $(this).addClass('address_lbl_hover');
        }
        if($(this).hasClass('address_lbl_new')){
            $('.address_lbl_new').css('color','#ed145b');
        }
        //$(this).find('.btnEditAddress_new').show(); //CSS CONTROL
        //$(this).find('.btnEditAddress_del').show();
    }).live('mouseleave',function(){
        $(this).removeClass('address_lbl_hover');
        $('.address_lbl_new').css('color','#999999');
        /*if(!$(this).closest('.option_box').hasClass('selected')){ //CSS CONTROL
         $(this).find('.btnEditAddress_new').hide();
         $(this).find('.btnEditAddress_del').hide();
         }*/
    });

    $('.name_hover').hover(function(){
        $(this).parent().find('.pic_hover').addClass('pic_hover_now');
    },function(){
        $(this).parent().find('.pic_hover').removeClass('pic_hover_now');
    });

    $('#prefer_delivery_day .option_box').hover(function(){
        if( ! $(this).parent().hasClass('selected') && $(this).attr('disabled') != 'true'  && !$(this).parent().hasClass('weihu') ){
            $(this).addClass('now_hover');
        }
    },function(){
        $(this).removeClass('now_hover');
    });
});


/*点击'确认订单'的表单验证*/
function check_pay(){
    var address_valid = check_address();
    $("#check_pay_form #btn_confirm_pay").attr("disabled","true").val("提交中……").css("font-size","14px");

    if(address_valid && check_gateway() ) {
        //success
        var items = $('input[name="hdItems"]');
        var normalItems = [];
        var msItems = [];
        items.each(function(idx){
            var cart = $.parseJSON($(items[idx]).val());
            if(cart.flag==1){
                msItems.push(cart);
            }
            else
            {
                normalItems.push(cart);
            }
        });

        var postData = {
            _xsrf:xsrf,
            address_id: $('input:radio[name="address_id"]:checked').val(),
            prefer_delivery_day:$('input:radio[name="prefer_delivery_day"]:checked').val(),
            gateway:$('input:radio[name="gateway"]:checked').val(),
            message:$('#txtmessage').val(),
            coupon_code:$('.J_Promo_cardno').val(),
            items: JSON.stringify(normalItems),
            msitems: JSON.stringify(msItems),
            storeid:$('input[name="storeid"]').val(),
            isinvoice:$('input[name="is_need_invoice"]').val(),
            invoice_type:$('input:radio[name="invoice_type"]:checked').val(),
            invoicename:$('input[name="invoice_companyname"]').val(),

            shippingprice:$('input:radio[name="logistic_preference"]:checked').val(),
            price:$("#hidBalance").val(),
            currentprice:$('#hdCurrentPrice').val(),
            balance:$('#hdBalance').val(),
            gids:$('input[name="gids"]').val()
        };
        var w = '';
        var gateway = $('input:radio[name="gateway"]:checked').val();
        if (gateway != 'Balance' && gateway != 'COD'){
            $("#lightbox").show();
            $("#lightbox_shadow").show();
            w = window.open('/waiting');
        }
        $.ajax({
            url: "/cart/pay2nd",
            async: true,
            type:'POST',
            dataType: "json",
            data:     postData,
            success:  function(data) {
                if(data.flag == 0){
                    alert(data.msg);
                    $("#check_pay_form #btn_confirm_pay").removeAttr("disabled").val("确认订单").css("font-size","20px");
                    return false;
                }
                else if(data.flag == 1){
                    location.href = "/cart/pay?result=success&orderid="+data.orderid.toString();
                }
                else if(data.flag == 2){
                    $("#hidtn").val(data.tn);
                    $("#hidprice").val(data.price);
                    $("#hidblank").val(data.is_bank);
                    //$('#btnZf').click();
                    //document.getElementById("check_pay_form").submit();
                    //setTimeout( form_submit, 2000);
                    //document.getElementById("tf").onsubmit();
                    //window.open(data.url);
                    w.location.href = data.url;
                }
            }
        });
    }
    else{
        //地址或支付方式验证失败
        $("#check_pay_form #btn_confirm_pay").removeAttr("disabled").val("确认订单").css("font-size","20px");
        return false;
    }

}
function form_submit(){
    document.getElementById("check_pay_form").submit();
}
function check_gateway(){
    if($('#use_balance_checkbox').attr("checked") || $('input[name=gateway]').filter(':checked').length){
        return true;
    }

    alert('请选择支付方式。');
    return false;
}

function check_address(){
    var radios = document.getElementsByName("address_id");
    if ( checkRadioValue(radios) == null ){
        alert('请添加收货地址');
        return false;
    }

    /*如果勾选了需要发票并且勾选的单位发票*/
    var errorWrap = $(".inv_error");
    if(window.needCheckInvOnSubmit && $(".is_need_inv").attr("checked") && $(".inv_info").find("input:radio:eq(1)").attr("checked")){
        var invTypeName = $.trim($(".inv_type_name").val());
        if(!invTypeName || invTypeName == "请输入单位名称"){
            errorWrap.show();
            $(window).scrollTop(errorWrap.offset().top-50);
            alert("请输入单位名称");
            return false;
        }
    }
    errorWrap.hide();


    //2014-9-19 修改四级地址 未发现此处有用
    if(checkRadioValue(radios)== 0 || checkRadioValue(radios)== ''){
        var receiver_name = document.getElementById('receiver_name');
        var province = document.getElementById('province');
        var city = document.getElementById('city');
        var county = document.getElementById('county');
        var settings_address = document.getElementById('settings-address');
        var postalcode = document.getElementById('postalcode');
        var hp = document.getElementById('hp');
        var phone_area = document.getElementById('phone_area').value;
        var phone_number = document.getElementById('phone_number').value;
        var check_address = trim(settings_address.value);
        var check_phone_number = trim(phone_number);
        if(!checkObjNull(receiver_name,"收件人名称")){
            return false;
        }else if(!checkSelectValue(province)){
            alert("请选择省");
            return false;
        }else if(!checkSelectValue(city)){
            alert("请选择市县");
            return false;
        }else if(!checkSelectValue(county)){
            alert("请选择地区");
            return false;
        }else if(!checkObjNull(settings_address,"街道地址")){
            return false;
        }else if(check_address.length == 0){
            alert("街道地址不能为空。");
            return false;
        }else if(!checkObjNull(postalcode,"邮编")){
            return false;
        }else if(postalcode.value.length != 6 || isNaN(postalcode.value)){
            alert('邮编格式不对');
            return false;
        }else if(!checkNull(hp.value)){
            if(!checkNull(phone_area) ||  !checkNull(phone_number)){
                alert("电话和手机必须填一个。");
                return false;
            }
        }else if(!checkNull(phone_area) ||  !checkNull(phone_number)){
            if(!checkObjNull(hp,"手机")){
                alert("电话和手机必须填一个。");
                return false;
            }
        }

        document.getElementById('select_province').value = province.options[province.selectedIndex].text;
        document.getElementById('select_city').value = city.options[city.selectedIndex].text;
        document.getElementById('select_county').value = county.options[county.selectedIndex].text;

    }
    return true;
}


function checkObjNull(obj,msg){
    if(!checkNull(obj.value)){
        alert(msg + "不能为空");
        return false;
    }
    return true;
}

function checkNull(str) {
    if (null == str || str == "" )  {
        return false;
    }
    else {
        return true;
    }
}
function checkSelectValue(select){
    for (var i = 0; i < select.options.length; i++){
        if(select.options[i].value !="" && select.options[i].selected){
            return true;
        }
    }
    return false;
}

function checkRadioValue(radios){
    for(var i = 0; i < radios.length; i++){
        if(radios[i].checked){
            return radios[i].value;
        }
    }
    return null;
}
function trim(str){
    return str.replace(/(^\s*)|(\s*$)/g, "");
}

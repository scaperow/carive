$(document).ready(function() {
//	$("#sel_Money").change(function() {
//		$("#sel_Money").children("option:selected").val() > GoldMoney / 12E4 + HongBao ? $("#need_Money").html('<span style="color:red">您的账户金币不够</span>') : $("#need_Money").html("");
//		TotalMoney()
//	});
//	$("#inp_BankCode1").keydown(function(a) {
//		$("#need_BankCode1").html("");
//		if (isNaN(this.value.replace(/[ ]/g, ""))) {
//			if (8 == a.keyCode) return !0;
//			$("#need_BankCode1").html('<span style="color:red">您输入的银行卡号有误请按退格键清除</span>');
//			return !1
//		}
//		this.value = this.value.replace(/\s/g, "").replace(/(\d{4})(?=\d)/g, "$1 ")
//	});
//	$("#inp_BankCode2").keydown(function(a) {
//		$("#need_BankCode2").html("");
//		if (isNaN(this.value.replace(/[ ]/g, ""))) {
//			if (8 == a.keyCode) return !0;
//			$("#need_BankCode2").html('<span style="color:red">您输入的银行卡号有误请按退格键清除</span>');
//			return !1
//		}
//		this.value = this.value.replace(/\s/g, "").replace(/(\d{4})(?=\d)/g, "$1 ")
//	});
//	$("#sel_BackName").change(function() {
//		0 == $("#sel_Money").children("option:selected").val() ? $("#need_BackName").html('<span style="color:red">请选择你的开户行</span>') : $("#need_BackName").html("请选择你的开户行")
//	})
});

/*-------------------------------------------*/
var InterValObj; //timer变量，控制时间
var count = 120; //间隔函数，1秒执行
var curCount;//当前剩余秒数
function sendMessage() {
    var tx_type = $("#tx_type").val();
    $("#err_msg").text("");
    var isMobile = /^[1]([3][0-9]{1}|45|47|50|51|52|53|54|55|56|57|58|59|70|75|76|77|78|80|81|82|83|84|85|86|87|88|89)[0-9]{8}$/; //手机号码验证规则
    var dianhua = $("#mobile").val();
    //获得用户填写的号码值 赋值给变量dianhua
    if (isMobile.test(dianhua)==false) { //如果用户输入的值不同时满足手机号和座机号的正则
        alert("绑定的手机号格式错误！");
        return false;
    }

    curCount = count;
    $("#getvcode"+tx_type).attr("disabled", "true");
    $("#getvcode"+tx_type).val(" " + curCount + "秒后可重新获取验证码");
    InterValObj = window.setInterval(SetRemainTime, 1000); //启动计时器，1秒执行一次
    //向后台发送处理数据
    $.post("/ajax/bind_alipay/vcode",
            {
                mobile: $('#mobile').val(),
                        _xsrf: xsrf
            },
            function (data) {
                var obj = jQuery.parseJSON(data);
                if (!obj.status)  {
                    window.clearInterval(InterValObj);
                    $("#getvcode"+tx_type).removeAttr("disabled");//启用按钮
                    $("#getvcode"+tx_type).val("获取验证码");
                    alert(obj.msg);
                }
                return false;
            });
}
//timer处理函数
function SetRemainTime() {
    var tx_type = $("#tx_type").val();
    if (curCount == 0) {
        window.clearInterval(InterValObj);//停止计时器
        $("#getvcode"+tx_type).removeAttr("disabled");//启用按钮
        $("#getvcode"+tx_type).val("重新发送验证码");
        code = ""; //清除验证码。如果不清除，过时间后，输入收到的验证码依然有效
    }
    else {
        curCount--;
        $("#getvcode"+tx_type).val(" " + curCount + "秒后可重新获取验证码");
    }
}
function tabclick(tx_type){
    $("#tx_type").val(tx_type);
    $("#wytx div[id^='wy']").hide();
    $("#wy"+tx_type).show();
    $("#wytx th[data-id]").removeClass("thother");
    $("#wytx th[data-id]").removeClass("thcurrent");
    $("#wytx th[data-id]").addClass("thother");
    $("#wytx th[data-id='"+tx_type+"']").addClass("thcurrent");
}
function check_alipay_truename() {
	var a = $("#alipay_truename").val();
	if (0 >= a.length) return $("#alipay_truename_msg").html('<span style="color:red">请输入你的支付宝姓名</span>'), !1;
	if (isChinese(a)) $("#alipay_truename_msg").html("必须和支付宝实名认证信息一致");
	else return $("#alipay_truename_msg").html('<span style="color:red">请输入中文姓名</span>'), !1;
	return !0
}
function check_alipay_account() {
	var a = $("#alipay_account").val(),
		b = $("#alipay_account_sure").val();
	if (0 >= a.length) return $("#alipay_account_msg").html('<span style="color:red">请输入你的支付宝账号</span>'), !1;
	if (!isMobile(a) && !isEmail(a)) return $("#alipay_account_msg").html('<span style="color:red">请输入手机手机号码或电子邮箱</span>'), !1;
	if (a != b && 0 < b.length) return $("#alipay_account_sure_msg").html('<span style="color:red">账号不一致，请确认</span>'), !1;
	$("#alipay_account_msg").html("请输入手机手机号码或电子邮箱");
	$("#alipay_account_sure_msg").html("请再次确认账号");
	return !0
}
function check_alipay_account_sure() {
	var a = $("#alipay_account").val(),
		b = $("#alipay_account_sure").val();
	if (0 >= b.length) return $("#alipay_account_sure_msg").html('<span style="color:red">请输入你的支付宝账号</span>'), !1;
	if (!isMobile(b) && !isEmail(b)) return $("#alipay_account_sure_msg").html('<span style="color:red">请输入手机手机号码或电子邮箱</span>'), !1;
	if (a != b) return $("#alipay_account_sure_msg").html('<span style="color:red">账号不一致，请确认</span>'), !1;
	$("#alipay_account_sure_msg").html("请再次确认账号");
	return !0
}
function bind_alipay() {
    var tx_type = $("#tx_type").val();
	var alipay_truename = $("#alipay_truename").val(),
		alipay_account = $("#alipay_account").val(),
		alipay_account_sure = $("#alipay_account_sure").val(),
		vcode = $("#vcode"+tx_type).val();
    if(0 >= alipay_truename.length){
        $("#alipay_truename_msg").html('<span style="color:red">请输入你的支付宝姓名</span>')
    }
    else{
        if(0 >= alipay_account.length){
            $("#alipay_account_msg").html('<span style="color:red">请输入你的支付宝账号</span>');
        }
        else{
            if (alipay_account != alipay_account_sure){
                $("#alipay_account_sure_msg").html('<span style="color:red">账号不一致，请确认</span>')
            }
            else{
                if(0 >= vcode.length){
                    $("#vcode_msg"+tx_type).html('<span style="color:red">请输入你的手机验证码</span>')
                }
                else{
                    if(check_alipay_account() && check_alipay_truename()){
                        $.post("/ajax/bind_alipay",
                        {
                            _xsrf: xsrf,
                            alipay_truename: alipay_truename,
                            alipay_account: alipay_account,
                            vcode: vcode
                        },
                        function (data) {
                            var obj = jQuery.parseJSON(data);
                            if (!obj.status)  {
                                alert(obj.msg);
                            }
                            else{
                                alert(obj.msg);
                                location.reload();
                            }
                            return false;
                        });
                    }
                }
            }
        }
    }
}
function ChangAlipayBanding() {
	$("#alipay_yes_banding").hide();
	$("#alipay_no_banding").show()
}

function check_bank_turename() {
	var a = $("#bank_truename").val();
	if (0 >= a.length) return $("#bank_truename_msg").html('<span style="color:red">请输入你的银行卡姓名</span>'), !1;
	if (isChinese(a)) $("#bank_truename_msg").html("必须和银行卡姓名一致");
	else return $("#bank_truename_msg").html('<span style="color:red">请输入中文姓名</span>'), !1;
	return !0
}
function change_bank_name() {
	var a = $("#bank_name").val();
	if (0 == a) return $("#bank_name_msg").html('<span style="color:red">请选择你的开户行</span>'), !1;
	else return $("#bank_name_msg").html('请选择你的开户行'), !0;
	return !0
}
function check_bank_branchname() {
	var a = $("#bank_branchname").val();
	if (0 >= a.length) return $("#bank_branchname_msg").html('<span style="color:red">请输入你的银行卡支行名称</span>'), !1;
	else return $("#bank_branchname_msg").html('必须如实确切填写'), !0;
	return !0
}
function check_bank_account() {
	var a = $("#bank_account").val().replace(/\s/g, ""),
		b = $("#bank_account_sure").val().replace(/\s/g, "");
	if (0 >= a.length) return $("#bank_account_msg").html('<span style="color:red">请输入你的银行卡账号</span>'), !1;
	if (!/^[\u4e00-\u9fa5a-zA-Z0-9]{15,20}$/.test(a)) return $("#bank_account_msg").html('<span style="color:red">请正确输入你的银行卡账号</span>'), !1;
	if (a != b && 0 < b.length) return $("#bank_account_sure_msg").html('<span style="color:red">银行卡账号不一致，请确认</span>'), !1;
	$("#bank_account_msg").html("");
	$("#bank_account_sure_msg").html("请再次确认账号");
	return !0
}
function check_bank_account_sure() {
	var a = $("#bank_account").val().replace(/\s/g, ""),
		b = $("#bank_account_sure").val().replace(/\s/g, "");
	if (0 >= b.length) return $("#bank_account_sure_msg").html('<span style="color:red">请输入你的银行卡账号</span>'), !1;
	if (!/^[\u4e00-\u9fa5a-zA-Z0-9]{15,20}$/.test(b)) return $("#bank_account_sure_msg").html('<span style="color:red">请正确输入你的银行卡账号</span>'), !1;
	if (a != b) return $("#bank_account_sure_msg").html('<span style="color:red">银行卡账号不一致，请确认</span>'), !1;
	$("#bank_account_sure_msg").html("请再次确认账号");
	return !0
}
function change_bank_vcode() {
    var tx_type = $("#tx_type").val();
	var a = $("#vcode"+tx_type).val();
	if (0 == a.length) return $("#vcode_msg"+tx_type).html('<span style="color:red">请输入你的手机验证码</span>'), !1;
	else return $("#vcode_msg"+tx_type).html('请输入你的手机验证码'), !0;
	return !0
}
function bind_bank() {
    var tx_type = $("#tx_type").val();
    var bank_truename = $("#bank_truename").val(),
        bank_name = $("#bank_name").children("option:selected").val(),
        bank_branchname = $("#bank_branchname").val(),
        bank_account = $("#bank_account").val().replace(/\s/g, ""),
        bank_account_sure = $("#bank_account_sure").val().replace(/\s/g, ""),
        vcode_bank = $("#vcode"+tx_type).val();
    if(check_bank_turename()&&change_bank_name()&&check_bank_branchname()&&check_bank_account()&&check_bank_account_sure()&&change_bank_vcode()){
        $.post("/ajax/bind_bank",
        {
            _xsrf: xsrf,
            bank_truename: bank_truename,
            bank_name: bank_name,
            bank_branchname: bank_branchname,
            bank_account: bank_account,
            vcode: vcode_bank
        },
        function (data) {
            var obj = jQuery.parseJSON(data);
            if (!obj.status)  {
                alert(obj.msg);
            }
            else{
                alert(obj.msg);
                location.reload();
            }
            return false;
        });
    }
//    if(0 >= bank_truename.length){
//        $("#bank_truename_msg").html('<span style="color:red">请输入你的真实姓名</span>')
//    }
//    else{
//        if(0 == bank_name){
//            $("#bank_name_msg").html('<span style="color:red">请选择你的开户行</span>')
//        }
//        else{
//            if(3 >= bank_branchname.length){
//                $("#bank_branchname_msg").html('<span style="color:red">请正确输入你的支行名称</span>');
//            }
//            else{
//                if(/^[\u4e00-\u9fa5a-zA-Z0-9]{15,20}$/.test(bank_account)&&15 >= bank_account.length){
//                        $("#bank_account_msg").html('<span style="color:red">请正确输入你的银行卡账号</span>')
//                }
//                else{
//                    if(bank_account!=bank_account_sure){
//                        $("#need_BankCode2").html('<span style="color:red">银行卡账号不一致，请确认</span>')
//                    }
//                    else{
//                        if(0>=vcode_bank.length){
//                            $("#code_html").html('<span style="color:red">请输入你的手机验证码</span>');
//                        }
//                        else{
//                        }
//                    }
//                }
//            }
//        }
//    }
}
function ChangBankBanding() {
	$("#bank_yes_banding").hide();
	$("#bank_no_banding").show()
}

function check_alipay_tx_money() {
	var alipay_tx_money = $("#alipay_tx_money").val(),
		cashed_money = $("#cashed_money").val();
	if (0 >= alipay_tx_money.length) return $("#alipay_tx_money_msg").html('<span style="color:red">请输入要提现的金额</span>'), !1;
	if (!isMoney(alipay_tx_money)) return $("#alipay_tx_money_msg").html('<span style="color:red">请正确输入你的银行卡账号</span>'), !1;
	if (alipay_tx_money > cashed_money || 100 > alipay_tx_money) return $("#alipay_tx_money_msg").html('<span style="color:red">提现金额必须大于100且少于可提现金额</span>'), !1;
	$("#alipay_tx_money_msg").html("请输入要提现的金额");
	return !0
}
function alipay_tx_money() {
    var tx_type = $("#tx_type").val();
    var alipay_tx_money = $("#alipay_tx_money").val(),
        vcode = $("#vcode"+tx_type).val();
    if(check_alipay_tx_money()&&change_bank_vcode()){
        $.post("/ajax/withdraw",
        {
            _xsrf: xsrf,
            account_type:1,
            sum_money: alipay_tx_money,
            vcode: vcode
        },
        function (data) {
            var obj = jQuery.parseJSON(data);
            if (!obj.status)  {
                alert(obj.msg);
            }
            else{
                alert(obj.msg);
                location.reload();
            }
            return false;
        });
    }
}

function check_bank_tx_money() {
	var bank_tx_money = $("#bank_tx_money").val(),
		cashed_money = $("#cashed_money").val();
	if (0 >= bank_tx_money.length) return $("#bank_tx_money_msg").html('<span style="color:red">请输入要提现的金额</span>'), !1;
	if (!isMoney(bank_tx_money)) return $("#bank_tx_money_msg").html('<span style="color:red">请正确输入你的银行卡账号</span>'), !1;
	if (bank_tx_money > cashed_money || 100 > bank_tx_money) return $("#bank_tx_money_msg").html('<span style="color:red">提现金额必须大于100且少于可提现金额</span>'), !1;
	$("#bank_tx_money_msg").html("请输入要提现的金额");
	return !0
}

function bank_tx_money() {
    var tx_type = $("#tx_type").val();
    var alipay_tx_money = $("#bank_tx_money").val(),
        vcode = $("#vcode"+tx_type).val();
    if(check_bank_tx_money()&&change_bank_vcode()){
        $.post("/ajax/withdraw",
        {
            _xsrf: xsrf,
            account_type:0,
            sum_money: alipay_tx_money,
            vcode: vcode
        },
        function (data) {
            var obj = jQuery.parseJSON(data);
            if (!obj.status)  {
                alert(obj.msg);
            }
            else{
                alert(obj.msg);
                location.reload();
            }
            return false;
        });
    }
}
function isMobile(a) {
	return result = /1[3-9]{1}[0-9]{1}[0-9]{8}$/.test(a)
}
function isEmail(a) {
	return result = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(a)
}
function isChinese(a) {
	return result = /^[\u4e00-\u9fa5]+$/.test(a)
}
function isNumber(a) {
	return result = /^[1-9]\d{0,}$/.test(a)
}
function isMoney(a) {
	return result = /^\d+(\.\d+)?$/.test(a)
}
function commafy(a) {
	if (0 >= a.length || isNaN(a)) return "";
	a += "";
	if (/^.*\..*$/.test(a)) {
		varpointIndex = a.lastIndexOf(".");
		varintPart = a.substring(0, pointIndex);
		varpointPart = a.substring(pointIndex + 1, a.length);
		intPart += "";
		for (var b = /(-?\d+)(\d{3})/; b.test(intPart);) intPart = intPart.replace(b, "$1,$2");
		a = intPart + "." + pointPart
	} else for (a += "", b = /(-?\d+)(\d{3})/; b.test(a);) a = a.replace(b, "$1,$2");
	return a
};
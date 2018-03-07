/*
 * 改程序封装了GlobalProvinces_extend.js、GlobalProvinces_main.js两个文件中的对象和数组
 * 
 * 
 * 
 */


function initLocation(option)
{
	option = jQuery.extend({
		sheng:"ddlProvince",		//省的网页ID
		shi:"ddlCity",			//市的网页ID
		xian:"ddlCounty",		//县的网页ID
		xiang:"ddlStreet",		//乡的网页ID
		sheng_val:"",		//默认省份
		shi_val:"",			//默认地区
		xian_val:"",		//默认县
		xiang_val:""		//默认乡镇
	},option||{});
	
	
	if(option.sheng_val == ""){
		option.sheng_val == "-1";
	}
		
	var gpm = new GlobalProvincesModule;



	gpm.def_province = ["---", -1];

	gpm.initProvince(document.getElementById(option.sheng));
	
	gpm.initCity1(document.getElementById(option.shi), option.sheng_val);

	gpm.initCity2(document.getElementById(option.xian), option.sheng_val, option.shi_val);

	gpm.initCity3(document.getElementById(option.xiang), option.sheng_val, option.shi_val, option.xian_val);


	gpm.selectProvincesItem(document.getElementById(option.sheng), option.sheng_val);

	gpm.selectCity2Item(document.getElementById(option.xian), option.xian_val);

	gpm.selectCity1Item(document.getElementById(option.shi), option.shi_val);

	
	
	if(document.getElementById(option.xiang).options.length > 1){
		gpm.selectCity2Item(document.getElementById(option.xiang), option.xiang_val);
		document.getElementById(option.xiang).style.display ="inline";
		document.getElementById(option.xiang).style.display = "inline";
	}

	



	var onchgProv = function()
	{	
		gpm.initCity1(document.getElementById(option.shi), gpm.getSelValue(document.getElementById(option.sheng)));
		gpm.initCity2(document.getElementById(option.xian), '', '');		/* clear city2 select options*/
		gpm.initCity3(document.getElementById(option.xiang), '', '', '');
		$("#"+option.xiang).hide();
		
	}
	var onchgCity1 = function()
	{
		gpm.initCity2(document.getElementById(option.xian), gpm.getSelValue(document.getElementById(option.sheng)), gpm.getSelValue(document.getElementById(option.shi)));
		gpm.initCity3(document.getElementById(option.xiang), '', '', '');
		$("#"+option.xiang).hide();
		
	}

	var onchgStreet1 = function(){
		
		gpm.initCity3(document.getElementById(option.xiang), gpm.getSelValue(document.getElementById(option.sheng)), gpm.getSelValue(document.getElementById(option.shi)), gpm.getSelValue(document.getElementById(option.xian)));

		if($("#"+option.xiang).children().length > 1) {
				$("#"+option.xiang).show();
		} else {
				$("#"+option.xiang).hide();
		}
	}


	if(option.xiang_val == "") 
		$("#"+option.xiang).hide();
	$("#"+option.sheng).change(onchgProv);
	$("#"+option.shi).change(onchgCity1);
	$("#"+option.xian).change(onchgStreet1);
	
	



}



/**
 * 用户地区控制
 */

/* module object */
function GlobalProvincesModule ()
{
	this.debug = false;
	this.def_province = ["省/直辖市", ""];
	this.def_city1 = ["市", ""];
	this.def_city2 = ["区/县", ""];
	this.def_city3 = ["", ""];

	this.initProvince = function (obj1)
	{
		try{
			var i;
			for(i = obj1.options.length -1; i >= 0 ; i--)
			{
				removeOptionItem(obj1, i);
			}

			if(this.def_province)
				obj1.options.add(new Option(this.def_province[0], this.def_province[1]));

			if(!GP) return;

			for(i=0; i < GP.length; i++)
			{
				obj1.options.add(new Option(GP[i], GP[i]));
			}
		}catch(e){if(this.debug) alert("执行方法\"initProvince\"时，遇到" + e.message);}
	}

	this.initCity1 = function (obj1, key)
	{
		try{
			var i;
			for(i = obj1.options.length -1; i >= 0 ; i--)
			{
				this.removeOptionItem(obj1, i);
			}

			if(this.def_city1)
				obj1.options.add(new Option(this.def_city1[0], this.def_city1[1]));

			if(!GC1[key]) return;

			for(i=0; i < GC1[key].length; i++)
			{
				obj1.options.add(new Option(GC1[key][i], GC1[key][i]));
			}
		}catch(e){if(this.debug) alert("执行方法\"initCity1\"时，遇到" + e.message);}
	}

	this.initCity2 = function (obj1, key, key2)
	{
		try{
			var i;
			for(i = obj1.options.length -1; i >= 0 ; i--)
			{
				this.removeOptionItem(obj1, i);
			}

			if(this.def_city2)
				obj1.options.add(new Option(this.def_city2[0], this.def_city2[1]));

			if(!GC2[key]) return;
			if(!GC2[key][key2])
			{
				obj1.options[0].selected = true;
			}else{
				var equal_second_location = "";
				for(i=0; i < GC2[key][key2].length; i++)
				{
					if (GC2[key][key2][i] == key2 + "市") {
						equal_second_location = GC2[key][key2][i];
					} else {
						obj1.options.add(new Option(GC2[key][key2][i], GC2[key][key2][i]));
					}
				}
				if (equal_second_location != "") {
					obj1.options.add(new Option(equal_second_location, equal_second_location));
				}
				//obj1.options.add(new Option("其他", "其他"));

				if(GC2[key][key2].length == 1)
					obj1.options[GC2[key][key2].length - 1].selected = true;
			}

		}catch(e){if(this.debug) alert("执行方法\"initCity2\"时，遇到" + e.message);}
	}

	this.initCity3 = function (obj1, key, key2, key3)
	{
		try{
			var i;
			for(i = obj1.options.length -1; i >= 0 ; i--)
			{
				this.removeOptionItem(obj1, i);
			}

			if(this.def_city3)
				obj1.options.add(new Option(this.def_city3[0], this.def_city3[1]));

			if(!GC3[key][key2] || !GC3[key][key2][key3])
			{
				obj1.options[obj1.options.length - 1].selected = true;
			}else{
				var count = 0;
				for(i=0; i < GC3[key][key2][key3].length; i++)
				{
					obj1.options.add(new Option(GC3[key][key2][key3][i], GC3[key][key2][key3][i]));
					count++;
				}
				if (count > 0) {
					//obj1.options.add(new Option("其他", "其他"));
				}

				if(GC3[key][key2][key3].length == 1)
					obj1.options[GC3[key][key2][key3].length - 1].selected = true;
			}

		}catch(e){if(this.debug) alert("执行方法\"initCity2\"时，遇到" + e.message);}
	}

	this.selectProvincesItem = function (obj1, value)
	{
		try{
			var ret = false;
			for(var i = 0; i < obj1.options.length; i++)
			{
				if(obj1.options[i].text == value)
				{
					ret = obj1.options[i].selected = true;
					break;
				}
			}
			return ret;
		}catch(e){if(this.debug) alert("执行方法\"selectProvincesItem\"时，遇到" + e.message);}
	}

	this.selectCity1Item = function (obj1, value)
	{
		try{
			var ret = false;
			for(var i = 0; i < obj1.options.length; i++)
			{
				if(obj1.options[i].text == value)
				{
					ret = obj1.options[i].selected = true;
					break;
				}
			}
			return ret;
		}catch(e){if(this.debug) alert("执行方法\"selectCity1Item\"时，遇到" + e.message);}
	}

	this.selectCity2Item = function (obj1, value)
	{
		try{
			var ret = false;
			for(var i = 0; i < obj1.options.length; i++)
			{
				if(obj1.options[i].text == value)
				{
					ret = obj1.options[i].selected = true;
					break;
				}
			}
			return ret;
		}catch(e){if(this.debug) alert("执行方法\"selectCity2Item\"时，遇到" + e.message);}
	}

	this.getSelValue = function (obj1)
	{
		if(obj1 && obj1.options && obj1.options.length > 0)
			return obj1.options[obj1.selectedIndex].value;
		else
			return null;
	}

	this.getProvinceNameById = function (id)
	{
		try{
			var ret = "";
			for(var i = 0; i< GP.length; i++)
			{
				if(GP[i][1] == id)
				{
					ret = GP[i];
					break;
				}
			}

			return ret;
		}catch(e){if(this.debug) alert("执行方法\"getProvinceNameById\"时，遇到" + e.message);}
	}

	this.getProvinceIdByName = function (name)
	{
		try{
			var ret = -1;
			for(var i = 0; i< GP.length; i++)
			{
				if(GP[i] == name)
				{
					ret = GP[i][1];
					break;
				}
			}

			return ret;
		}catch(e){if(this.debug) alert("执行方法\"getProvinceIdByName\"时，遇到" + e.message);}
	}

	this.removeOptionItem = function(obj, index)
	{
		if(typeof obj.options.remove == "undefined")
		{
			obj.remove(index);
		}else{
			obj.options.remove(index);
		}
	}
}

/********** 省份数据 **********/
var GP = new Array("北京",'陕西');
/********** 市级数据 **********/
var GC1 = new Array();
GC1['陕西']=new Array('西安','安康','宝鸡','汉中','商洛','铜川','渭南','咸阳','延安','榆林');//,'安康','宝鸡','汉中','商洛','铜川','渭南','咸阳','延安','榆林'
GC1['北京']=new Array('昌平','朝阳','崇文','大兴','东城','房山','丰台','海淀','怀柔','门头沟','密云','平谷','石景山','顺义','通州','西城','宣武','延庆');
/********** 县乡数据 **********/
var GC2 = new Array();
GC2['陕西'] = new Array();
GC2['陕西']['西安'] = new Array('碑林区','莲湖区','新城区','雁塔区','未央区','灞桥区','长安区');//'高陵','户县','蓝田','西安市','周至','临潼区','阎良区',
GC2['陕西']['安康'] = new Array('安康市','白河','汉阴','岚皋','宁陕','平利','石泉','旬阳','镇坪','紫阳','汉滨区');
GC2['陕西']['宝鸡'] = new Array('宝鸡市','凤县','凤翔','扶风','麟游','陇县','眉县','岐山','千阳','太白','陈仓区','金台区','渭滨区');
GC2['陕西']['汉中'] = new Array('城固','佛坪','汉中市','留坝','略阳','勉县','南郑','宁强','西乡','洋县','镇巴','汉台区');
GC2['陕西']['商洛'] = new Array('丹凤','洛南','山阳','商洛市','商南','镇安','柞水','商州区');
GC2['陕西']['铜川'] = new Array('铜川市','宜君','王益区','耀州区','印台区');
GC2['陕西']['渭南'] = new Array('白水','澄城','大荔','富平','韩城','合阳','华县','华阴','蒲城','潼关','渭南市','临渭区');
GC2['陕西']['咸阳'] = new Array('彬县','长武','淳化','泾阳','礼泉','乾县','三原','武功','咸阳市','兴平','旬邑','永寿','秦都区','渭城区','杨陵区');
GC2['陕西']['延安'] = new Array('安塞','富县','甘泉','黄陵','黄龙','洛川','吴起','延安市','延长','延川','宜川','志丹','子长','宝塔区');
GC2['陕西']['榆林'] = new Array('定边','府谷','横山','佳县','靖边','米脂','清涧','神木','绥德','吴堡','榆林市','子洲','榆阳区');

GC2['北京'] = new Array();
GC2['北京']['昌平'] = new Array('昌平');
GC2['北京']['朝阳'] = new Array('朝阳');
GC2['北京']['崇文'] = new Array('崇文');
GC2['北京']['大兴'] = new Array('大兴');
GC2['北京']['东城'] = new Array('东城');
GC2['北京']['房山'] = new Array('房山');
GC2['北京']['丰台'] = new Array('丰台');
GC2['北京']['海淀'] = new Array('海淀');
GC2['北京']['怀柔'] = new Array('怀柔');
GC2['北京']['门头沟'] = new Array('门头沟');
GC2['北京']['密云'] = new Array('密云');
GC2['北京']['平谷'] = new Array('平谷');
GC2['北京']['石景山'] = new Array('石景山');
GC2['北京']['顺义'] = new Array('顺义');
GC2['北京']['通州'] = new Array('通州');
GC2['北京']['西城'] = new Array('西城');
GC2['北京']['宣武'] = new Array('宣武');
GC2['北京']['延庆'] = new Array('延庆');

var GC3 = new Array();
GC3['陕西'] = new Array();
GC3['陕西']['西安'] = new Array();
GC3['陕西']['西安']['碑林区'] = new Array('柏树林街道','长安路街道','长乐坊街道','东关南街街道','南院门街道','太乙路街道','文艺路街道','张家村街道');
GC3['陕西']['西安']['长安区'] = new Array('大兆街道','东大街道','斗门街道','杜曲街道','郭杜街道','黄良街道','滦镇街道','马王街道','太乙宫街道','王寺街道','韦曲街道','细柳街道','兴隆街道','引镇街道','子午街道');//'高桥乡','王莽乡','王曲镇','鸣犊镇','炮里乡','灵沼乡','魏寨乡','五台乡','五星乡','杨庄乡',
GC3['陕西']['西安']['莲湖区'] = new Array('北关街道','北院门街道','红庙坡街道','环城西路街道','青年路街道','桃园路街道','土门街道','西关街道','枣园街道');
GC3['陕西']['西安']['未央区'] = new Array('张家堡街道','三桥街道','辛家庙街道','徐家湾街道','大明宫街道','谭家街道','草滩街道','未央宫街道','汉城街道','六村堡街道');
GC3['陕西']['西安']['临潼区'] = new Array('北田镇','代王街道','何寨镇','交口镇','零口街道','马额街道','穆寨乡','秦陵街道','任留乡','铁炉乡','土桥乡','西泉街道','相桥街道','小金乡','斜口街道','新丰街道','新市街道','行者街道','徐杨街道','油槐镇','雨金街道','骊山街道','栎阳街道');
GC3['陕西']['西安']['新城区'] = new Array('长乐西路街道','长乐中路街道','韩森寨街道','胡家庙街道','解放门街道','太华路街道','西一路街道','中山门街道','自强路街道');
GC3['陕西']['西安']['阎良区'] = new Array('北屯街道','凤凰路街道','关山镇','武屯镇','新华路街道','新兴街道','振兴街道');
GC3['陕西']['西安']['雁塔区'] = new Array('长延堡街道','大雁塔街道','等驾坡街道','电子城街道','曲江街道','小寨路街道','鱼化寨街道','丈八沟街道');
GC3['陕西']['西安']['灞桥区'] = new Array('狄寨街道','纺织城街道','洪庆街道','红旗街道','十里铺街道','席王街道','新合街道','新筑街道','灞桥街道');
GC3['陕西']['西安']['高陵'] = new Array('崇皇乡','耿镇','鹿苑镇','通远镇','湾子乡','榆楚乡','张卜乡','泾渭镇');
GC3['陕西']['西安']['户县'] = new Array('苍游乡','草堂镇','大王镇','甘河镇','甘亭镇','蒋村镇','涝店镇','庞光镇','秦渡镇','石井镇','天桥乡','渭丰乡','五竹乡','余下镇','玉蝉乡','祖庵镇');
GC3['陕西']['西安']['蓝田'] = new Array('安村乡','葛牌镇','厚镇乡','华胥镇','焦岱镇','金山乡','九间房乡','蓝关镇','蓝桥乡','孟村乡','普化镇','前卫镇','三官庙乡','三里镇','史家寨乡','汤峪镇','小寨乡','泄湖镇','玉川乡','玉山镇','灞源乡','辋川乡');
GC3['陕西']['西安']['周至'] = new Array('板房子乡','陈河乡','翠峰乡','二曲镇','富仁乡','广济镇','侯家村乡','厚畛子镇','集贤镇','九峰乡','楼观镇','骆峪乡','马召镇','青化乡','尚村镇','司竹乡','四屯乡','王家河乡','辛家寨乡','哑柏镇','终南镇','竹峪乡');

GC3['北京'] = new Array();
GC3['北京']['昌平'] = new Array();
GC3['北京']['昌平']['昌平'] = new Array('百善镇','北七家镇','长陵镇','城北街道','城南街道','崔村镇','东小口地区','回龙观地区','流村镇','马池口地区','南口地区','南邵镇','沙河地区','十三陵镇','小汤山镇','兴寿镇','阳坊镇');
GC3['北京']['朝阳'] = new Array();
GC3['北京']['朝阳']['朝阳'] = new Array('安贞街道','奥运村地区奥运村乡','八里庄街道','常营回族地区常营回族乡','朝阳门外街道','崔各庄地区崔各庄乡','大屯街道','东坝地区东坝乡','东风地区东风乡','豆各庄地区豆各庄乡','高碑店地区高碑店乡','管庄地区管庄乡','和平街街道','黑庄户地区黑庄户乡','呼家楼街道','建国门外街道','将台地区将台乡','金盏地区金盏乡','劲松街道','酒仙桥街道','来广营地区来广营乡','六里屯街道','麦子店街道','南磨房地区南磨房乡','潘家园街道','平房地区平房乡','三间房地区三间房乡','三里屯街道','十八里店地区十八里店乡','首都机场街道','双井街道','孙河地区孙河乡','太阳宫地区太阳宫乡','团结湖街道','王四营地区王四营乡','望京街道','望京开发街道','香河园街道','小关街道','小红门地区小红门乡','亚运村街道','左家庄街道','垡头街道');
GC3['北京']['崇文'] = new Array();
GC3['北京']['崇文']['崇文'] = new Array('崇文门外街道','东花市街道','龙潭街道','前门街道','体育馆路街道','天坛街道','永定门外街道');
GC3['北京']['大兴'] = new Array();
GC3['北京']['大兴']['大兴'] = new Array('安定镇','北臧村镇','采育镇','长子营镇','黄村地区黄村镇','旧宫地区旧宫镇','礼贤镇','林校路街道','庞各庄镇','青云店镇','清源街道','魏善庄镇','西红门地区西红门镇','兴丰街道','亦庄地区亦庄镇','榆垡镇','瀛海镇');
GC3['北京']['东城'] = new Array();
GC3['北京']['东城']['东城'] = new Array('安定门街道','北新桥街道','朝阳门街道','东华门街道','东四街道','东直门街道','和平里街道','建国门街道','交道口街道','景山街道');
GC3['北京']['房山'] = new Array();
GC3['北京']['房山']['房山'] = new Array('长沟镇','长阳镇','城关街道','大安山乡','大石窝镇','东风街道','佛子庄乡','拱辰街道','韩村河镇','河北镇','良乡地区','琉璃河地区','南窖乡','蒲洼乡','青龙湖镇','十渡镇','石楼镇','史家营乡','西潞街道','霞云岭乡','向阳街道','新镇街道','星城街道','阎村镇','迎风街道','张坊镇','周口店地区','窦店镇');
GC3['北京']['丰台'] = new Array();
GC3['北京']['丰台']['丰台'] = new Array('长辛店街道','长辛店镇','大红门街道','东高地街道','东铁匠营街道','方庄地区','丰台街道','和义街道','花乡乡','卢沟桥街道','卢沟桥乡','马家堡街道','南苑街道','南苑乡','太平桥街道','宛平城地区','王佐镇','西罗园街道','新村街道','右安门街道','云岗街道');
GC3['北京']['海淀'] = new Array();
GC3['北京']['海淀']['海淀'] = new Array('万寿路街道','永定路街道','羊坊店街道','甘家口街道','八里庄街道','紫竹院街道','北下关街道','北太平庄街道','学院路街道','中关村街道','海淀街道','青龙桥街道','清华园街道','燕园街道','香山街道','清河街道','花园路街道','西三旗街道','马连洼街道','田村路街道','上地街道','万柳地区（海淀乡）','东升地区（东升乡）','曙光街道','温泉镇','四季青镇','西北旺镇','苏家坨镇','上庄镇');
GC3['北京']['怀柔'] = new Array();
GC3['北京']['怀柔']['怀柔'] = new Array('宝山镇','北房镇','渤海镇','长哨营满族乡','怀北镇','怀柔地区','九渡河镇','喇叭沟门满族乡','琉璃庙镇','龙山街道','庙城地区','桥梓镇','泉河街道','汤河口镇','雁栖地区','杨宋镇');
GC3['北京']['门头沟'] = new Array();
GC3['北京']['门头沟']['门头沟'] = new Array('城子街道','大台街道','大峪街道','东辛房街道','军庄镇','龙泉镇','妙峰山镇','清水镇','潭柘寺镇','王平地区','雁翅镇','永定镇','斋堂镇');
GC3['北京']['密云'] = new Array();
GC3['北京']['密云']['密云'] = new Array('北庄镇','不老屯镇','大城子镇','东邵渠镇','冯家峪镇','高岭镇','鼓楼街道','古北口镇','果园街道','河南寨镇','巨各庄镇','密云镇','穆家峪镇','十里堡镇','石城镇','太师屯镇','檀营地区檀营满族蒙古族乡','西田各庄镇','溪翁庄镇','新城子镇');
GC3['北京']['石景山'] = new Array();
GC3['北京']['石景山']['石景山'] = new Array('八宝山街道','八角街道','北辛安街道','古城街道','广宁街道','金顶街街道','老山街道','鲁谷街道','苹果园街道','五里坨街道');
GC3['北京']['顺义'] = new Array();
GC3['北京']['顺义']['顺义'] = new Array('北石槽镇','北务镇','北小营镇','大孙各庄镇','高丽营镇','光明街道','后沙峪地区','空港街道','李桥镇','李遂镇','龙湾屯镇','马坡地区','木林镇','南彩镇','南法信地区','牛栏山地区','仁和地区','胜利街道','石园街道','双丰街道','天竺地区','旺泉街道','杨镇地区','张镇','赵全营镇');
GC3['北京']['通州'] = new Array();
GC3['北京']['通州']['通州'] = new Array('漷县镇','北苑街道','梨园地区','潞城镇','马驹桥镇','宋庄镇','台湖镇','西集镇','新华街道','永乐店镇','永顺地区','于家务回族乡','玉桥街道','张家湾镇','中仓街道');
GC3['北京']['西城'] = new Array();
GC3['北京']['西城']['西城'] = new Array('德胜街道','金融街街道','什刹海街道','西长安街街道','新街口街道','月坛街道','展览路街道');
GC3['北京']['宣武'] = new Array();
GC3['北京']['宣武']['宣武'] = new Array('白纸坊街道','椿树街道','大栅栏街道','广安门内街道','广安门外街道','牛街街道','陶然亭街道','天桥街道');
GC3['北京']['延庆'] = new Array();
GC3['北京']['延庆']['延庆'] = new Array('八达岭镇','大榆树镇','大庄科乡','井庄镇','旧县镇','康庄镇','刘斌堡乡','千家店镇','沈家营镇','四海镇','香营乡','延庆镇','永宁镇','张山营镇','珍珠泉乡');

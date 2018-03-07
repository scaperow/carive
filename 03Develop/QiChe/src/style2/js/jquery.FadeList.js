/**
* jquery.FadeList.js
* 基于jQuery扩展插件 FadeList
* create : 2011.08.17
* update : 2012.05.31
* admin@laoshu133.com

-- 参数说明 --
	- @Param options {Object} #2011.12.05#
		- {
			shell: null,
			duration: 500,
			auto: true,
			delay: 6000,
			autoStop: true,
			onplay: noop
		}
-- 参数说明 end --
*/
;(function(global,document,$,undefined){var noop=function(){},_ops={shell:null,duration:500,auto:true,delay:6000,onplay:noop},FadeList=global.FadeList=function(ops){this.init(ops||{});};FadeList.prototype={constructor:FadeList,init:function(ops){var self=this,ops=this.ops=$.extend({},_ops,ops),shell=this.shell=$(ops.shell).eq(0),items=this.items=shell.find('li').css('opacity',0);this.playing=false;this.index=-1;this.play(0);if(ops.auto){this.shell.bind('mouseenter.fadeList',function(){self.stopAuto();}).bind('mouseleave.fadeList',function(){self.autoPlay();});}},play:function(inx){var self=this,ops=this.ops,items=this.items,len=items.length;inx=~~(inx===undefined?this.index+1:inx)%len;inx=inx<0?len+inx:inx;if(this.playing||inx===this.index){return this;}this.playing=true;items.eq(this.index).stop(true).animate({opacity:0},ops.duration,function(){this.style.zIndex=len;});items.eq(inx).css('zIndex',len+1).stop(true).animate({opacity:1},ops.duration,function(){ops.auto&&self.autoPlay();self.playing=false;self.index=inx;});(ops.onplay||noop).call(self,inx,self.index);return this;},next:function(){return this.play(this.index+1);},prev:function(){return this.play(this.index-1);},autoPlay:function(){var self=this;this.ops.auto=true;clearTimeout(this.timer);this.timer=setTimeout(function(){self.play();},this.ops.delay);},stopAuto:function(){clearTimeout(this.timer);this.ops.auto=false;}};})(window,document,jQuery);
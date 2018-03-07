/*
 * author: zhuangzhonglong
 * since: 2008-10-9
 */

/* 基于List<IdText>的json数据填充下拉框
 * 参数：
 *   combo: select对象
 *   nullItem: 空项的显示值  
 */
function fillCombo(combo, url, data, nullItem, completeCallback) {
    $.getJSON(url, data, function(idTexts) {
        combo = $(combo)[0];
        var baseIndex = 0;
        if (nullItem) {
            combo.options[baseIndex++] = new Option(nullItem, '');
        }
        combo.options.length = baseIndex;
        $.each(idTexts, function(index, item) {
            combo.options[index + baseIndex] = new Option(item.text, item.id);
        });
        if(completeCallback) {
            completeCallback();
        }
    });
}

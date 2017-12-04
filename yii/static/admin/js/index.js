/**
 layui模块预加载
 */
layui.define(['element', 'form'], function (exports) {
    var form = layui.form;
    // 全选
    form.on('checkbox(allChoose)', function (data) {
        var child = $(data.elem).parents('table').find('tbody input[type="checkbox"]');
        child.each(function (index, item) {
            item.checked = data.elem.checked;
        });
        form.render('checkbox');
    });
    exports('index', {});
});
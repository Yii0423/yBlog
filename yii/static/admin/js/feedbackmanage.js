/**
 * Created by Administrator on 2017/11/11.
 */
var yTable;
$(function () {
    //加载
    layui.use('table', function () {
        yTable = layui.table.render({
            id: 'yTable',
            elem: '.layui-table',
            url: '/admin/api/select_feedback/',
            skin: 'row',
            even: true,
            page: true,
            limits: [5, 10],
            limit: 10,
            height: 500,
            cols: [[
                {checkbox: true, LAY_CHECKED: false, fixed: true},
                {field: 'pk', title: '编号', width: 80, sort: true},
                {field: 'ip', title: '留言人IP', width: 150},
                {field: 'content', title: '内容', width: 250},
                {field: 'replycontent', title: '回复', width: 350},
                {field: 'create', title: '创建时间', width: 200, sort: true},
                {field: 'modify', title: '修改时间', width: 200, sort: true}
            ]]
        });
        //删除及编辑
        var $ = layui.$, active = {
            'pag_delete': function () {
                var checkStatus = layui.table.checkStatus('yTable'),
                    data = checkStatus.data;
                $(this).pag_delete({
                    type: 'post',
                    url_delete: '/admin/api/delete_feedback/'
                }, data);
            },
            'pag_modify': function () {
                var checkStatus = layui.table.checkStatus('yTable'),
                    data = checkStatus.data;
                if (data.length == 0) {
                    layer.msg('请至少选择一条数据进行操作', {time: 2000});
                    return;
                }
                layer.open({
                    type: 2,
                    title: '留言板 - 回复',
                    shade: 0.5,
                    area: ['750px', '540px'],
                    content: '/admin/edit_feedback/' + data[0]['pk']
                });
            }
        };
        //绑定删除及编辑
        $('.box-deal .layui-btn').on('click', function () {
            var type = $(this).data('type');
            active[type] ? active[type].call(this) : '';
        });
    });
});
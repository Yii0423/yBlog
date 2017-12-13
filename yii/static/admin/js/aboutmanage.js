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
            url: '/admin/api/select_about/',
            skin: 'row',
            even: true,
            page: true,
            limits: [5, 10],
            limit: 10,
            height: 500,
            cols: [[
                {checkbox: true, LAY_CHECKED: false, fixed: true},
                {field: 'pk', title: '编号', width: 80, sort: true},
                {field: 'title', title: '标题', width: 250},
                {field: 'type', title: '类型', width: 150, sort: true},
                {field: 'url', title: '链接', width: 300},
                {field: 'content', title: '描述', width: 500},
                {field: 'create', title: '创建时间', width: 200, sort: true},
                {field: 'modify', title: '修改时间', width: 200, sort: true}
            ]]
        });
        //删除及编辑
        var $ = layui.$, active = {
            'pag_add': function () {
                layer.open({
                    type: 2,
                    title: '关于 - 新增',
                    shade: 0.5,
                    area: ['750px', '540px'],
                    content: '/admin/edit_about/'
                });
            },
            'pag_delete': function () {
                var checkStatus = layui.table.checkStatus('yTable'),
                    data = checkStatus.data;
                $(this).pag_delete({
                    type: 'post',
                    url_delete: '/admin/api/delete_about/'
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
                    title: '关于 - 编辑',
                    shade: 0.5,
                    area: ['750px', '540px'],
                    content: '/admin/edit_about/' + data[0]['pk']
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
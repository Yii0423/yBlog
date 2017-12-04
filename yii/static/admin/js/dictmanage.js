/**
 * Created by Administrator on 2017/11/11.
 */
var yTable;
$(function () {
    $(".layui-nav>.layui-nav-item:last").addClass("layui-this").find("dd:eq(0)").addClass("layui-this");
    //加载
    layui.use('table', function () {
        yTable = layui.table.render({
            id: 'yTable',
            elem: '.layui-table',
            url: '/admin/api/select_dict/',
            skin: 'row',
            even: true,
            page: true,
            limits: [5, 10],
            limit: 10,
            height: 500,
            cols: [[
                {checkbox: true, LAY_CHECKED: false, fixed: true},
                {field: 'pk', title: '编号', width: 80, sort: true},
                {field: 'ptype', title: '父类型', width: 150},
                {field: 'key', title: '键', width: 150},
                {field: 'value', title: '值', width: 150},
                {field: 'sort', title: '排序', width: 80, sort: true},
                {field: 'create', title: '创建时间', width: 200, sort: true},
                {field: 'modify', title: '修改时间', width: 200, sort: true},
                {field: 'remarks', title: '备注', width: 500}
            ]]
        });
        //删除及编辑
        var $ = layui.$, active = {
            'pag_add': function () {
                layer.open({
                    type: 2,
                    title: '字典表 - 新增',
                    shade: 0.5,
                    area: ['750px', '480px'],
                    content: '/admin/_developer/edit_dict/'
                });
            },
            'pag_delete': function () {
                var checkStatus = layui.table.checkStatus('yTable'),
                    data = checkStatus.data;
                $(this).pag_delete({
                    type: 'post',
                    url_delete: '/admin/api/delete_dict/'
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
                    title: '字典表 - 编辑',
                    shade: 0.5,
                    area: ['750px', '480px'],
                    content: '/admin/_developer/edit_dict/' + data[0]['pk']
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
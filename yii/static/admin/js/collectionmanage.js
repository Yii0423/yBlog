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
            url: '/admin/api/select_collection/',
            skin: 'row',
            even: true,
            page: true,
            limits: [5, 10],
            limit: 10,
            height: 500,
            cols: [[
                {checkbox: true, LAY_CHECKED: false, fixed: true},
                {field: 'pk', title: '编号', width: 80, sort: true},
                {field: 'type', title: '收藏类型', width: 150, sort: true},
                {field: 'title', title: '标题', width: 250},
                {
                    field: 'url',
                    title: '链接',
                    width: 350,
                    templet: '<div><a href="{{d.url}}" class="layui-table-link" target="_blank">{{d.url}}</a></div>'
                },
                {field: 'visits', title: '浏览数', width: 80, sort: true},
                {field: 'agrees', title: '赞数', width: 80, sort: true},
                {field: 'disagrees', title: '踩数', width: 80, sort: true},
                {field: 'sort', title: '排序', width: 80, sort: true},
                {field: 'create', title: '创建时间', width: 200, sort: true},
                {field: 'modify', title: '修改时间', width: 200, sort: true}
            ]]
        });
        //删除及编辑
        var $ = layui.$, active = {
            'pag_add': function () {
                layer.open({
                    type: 2,
                    title: '收藏 - 新增',
                    shade: 0.5,
                    area: ['750px', '540px'],
                    content: '/admin/edit_collection/'
                });
            },
            'pag_delete': function () {
                var checkStatus = layui.table.checkStatus('yTable'),
                    data = checkStatus.data;
                $(this).pag_delete({
                    type: 'post',
                    url_delete: '/admin/api/delete_collection/'
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
                    title: '收藏 - 编辑',
                    shade: 0.5,
                    area: ['750px', '540px'],
                    content: '/admin/edit_collection/' + data[0]['pk']
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
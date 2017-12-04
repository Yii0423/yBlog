/**
 * Created by Administrator on 2017/11/11.
 */
//当前目录
var currentDir = '/static/uploadfiles';
$(function () {
    //菜单选中
    $(".layui-nav>.layui-nav-item:last").addClass("layui-this").find("dd:eq(1)").addClass("layui-this");
    //上传
    layui.use('upload', function () {
        layui.upload.render({
            elem: '.pag-upload',
            done: function (res) {
                if (res.code == 0) layer.msg('上传文件成功', {time: 2000, icon: 1});
                else layer.msg('上传文件失败', {time: 2000});
            },
            error: function () {
                layer.msg('上传文件失败', {time: 2000});
            }
        });
    });
    //新建文件夹
    $('.pag-add').bind('click', function () {
        layer.prompt({title: '请输入文件夹名'}, function (val, index) {
            layer.close(index);
            ajax('post', '/admin/api/create_dir/', {'name': currentDir + '/' + val}, function (data) {
                if (data['result'] == 'success') layer.msg('新建文件夹成功', {time: 2000, icon: 1});
                else layer.msg('新建文件夹失败', {time: 2000});
            });
        });
    });
    //删除
    $('.pag-delete').bind('click', function () {
        var dataSelected = []
        $(":checkbox[lay-filter!='allChoose']:checked").each(function () {
            dataSelected.push({'pk': $(this).attr("did")});
        });
        console.log(dataSelected);
        $(this).pag_delete({
            type: 'post',
            url_delete: '/admin/api/delete_files/'
        }, dataSelected);
    });
    //返回上一级
    $('.pag-back').bind('click', function () {
        if (currentDir == '/static/uploadfiles') {
            layer.msg('已处于最顶级目录', {time: 2000});
            return;
        }
        getFiles(currentDir.replace('/' + currentDir.split('/')[currentDir.split('/').length - 1], ''));
    });
    //刷新
    $('.pag-refresh').bind('click', function () {
        getFiles(currentDir);
    });
});

//获取目录下的文件
function getFiles(path) {
    $(this).pag_load({
        type: 'get',
        url_select: '/admin/api/select_files/',
        params: {'path': path},
        isFirst: false,
        Fn: function (data) {
            $('.files').html('');
            for (var i = 0; i < data.length; i++) {
                $('.files').append('<div class="file text-center layui-form">'
                    + '<p class="text-right"><input type="checkbox" name="" lay-skin="primary" did="'
                    + data[i]['path'] + '"/></p><div onclick="getMethod(\''
                    + data[i]['extension'] + '\',\'' + data[i]['path'] + '\',\'' + data[i]['name']
                    + '\')"><p><i class="layui-icon">'
                    + getIcon(data[i]['extension']) + '</i></p>'
                    + '<p class="filename">' + data[i]['name'] + '</p></div></div>'
                );
            }
            $('.pag-upload').attr('lay-data', "{url:'" + '/admin/api/upload_files/?dir=' + path + "'}");
            $(this).pag_refresh();
            var pathHtml = '<label class="label label-primary">文件管理器</label>';
            var paths = path.replace('/static/uploadfiles', '').split('/');
            for (var i = 0; i < paths.length; i++) {
                if (paths[i] == undefined || paths[i] == '') continue;
                pathHtml += '<label class="label label-info">' + paths[i] + '</label>';
            }
            $('.box-header>h3').html(pathHtml);
            currentDir = path;
        }
    });

}

//获取对应图标
function getIcon(type) {
    type = type.toLocaleLowerCase();
    if (type == '' || type == undefined || type == null)
        return '&#xe622;';
    if (audioType.indexOf(type) > -1)
        return '&#xe6fc;';
    if (videoType.indexOf(type) > -1)
        return '&#xe6ed;';
    if (imageType.indexOf(type) > -1)
        return '&#xe64a;';
    if (fileType.indexOf(type) > -1)
        return '&#xe61d;';
    if (textType.indexOf(type) > -1)
        return '&#xe621;';
    return '&#xe622;';
}

//获取对应方法
function getMethod(type, path, name) {
    type = type.toLocaleLowerCase();
    var area = ['500px', 'auto'];
    if (type == '' || type == undefined || type == null) {
        getFiles(path);
        return;
    }
    var html = '', skin = 'layui-layer-demo noscroll';
    if (audioType.indexOf(type) > -1)
        html = '<audio src="' + path + '" autoplay="autoplay" controls="controls" style="width:100%" />';
    if (videoType.indexOf(type) > -1) {
        area = ['800px', '450px'];
        html = '<video src="' + path + '" autoplay="autoplay" controls="controls" style="width:100%" />';
    }
    if (imageType.indexOf(type) > -1) {
        html = '<img src="' + path + '" style="width:100%" />';
        getImgSize(path, function (area) {
            layer.open({
                type: 1,
                title: name + '.' + type,
                skin: skin,
                closeBtn: 0,
                shadeClose: true,
                area: [area[0] + 'px', area[1] + 'px'],
                content: html
            });
        });
        return;
    }
    if (textType.indexOf(type) > -1) {
        skin = 'layui-layer-demo';
        area = ['800px', '500px'];
        $.ajax({
            url: path,
            dataType: 'text',
            beforeSend: function () {
                layer.load(1);
            },
            complete: function () {
                layer.closeAll('loading');
            },
            success: function (data) {
                setTimeout(function () {
                    $(".layui-layer-content").html('<div class="container-fluid margin-default" '
                        + 'style="word-break:break-all">'
                        + data.replace(new RegExp('\r\n', 'g'), '<br/>')
                        + '</div>');
                }, 500);
            }
        });
    }
    if (fileType.indexOf(type) > -1) {
        layer.msg('压缩包暂不支持预览', {time: 2000});
        return;
    }
    layer.open({
        type: 1,
        title: name + '.' + type,
        skin: skin,
        closeBtn: 0,
        shadeClose: true,
        area: area,
        content: html
    });
}
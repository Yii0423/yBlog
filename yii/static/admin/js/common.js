/**
 * Created by Administrator on 2017/8/3.
 */
;(function ($) {
    //声明插件
    $.fn.extend({
        //加载数据
        pag_load: function (option) {
            pag_ajax(option, 'select', function (data) {
                if (data !== null && data !== undefined && data !== '') {
                    var _data = eval(data['data']);
                    option.Fn(_data);
                }
            });
        },
        //刷新ui
        pag_refresh: function () {
            layui.use(['form'], function () {
                var form = layui.form;
                $(":checkbox[lay-filter='allChoose']").prop("checked", false);
                form.render();
            });
        },
        //删除
        pag_delete: function (option, data) {
            if (data.length == 0) {
                layer.msg('请至少选择一条数据进行操作', {time: 2000});
                return;
            }
            var ids = '';
            for (var i = 0; i < data.length; i++) {
                ids += data[i]['pk'] + ',';
            }
            option.params = {'ids': ids};
            layer.confirm('确认删除选中数据?', {title: '删除前确认'}, function () {
                pag_ajax(option, 'delete', function (data) {
                    if (data['result'] === 'success') {
                        layer.msg('选中数据删除成功', {time: 2000, icon: 1});
                        try {
                            if (yTable != null && yTable != undefined) yTable.reload();
                        }
                        catch (ex) {
                        }
                    }
                })
            });
        },
        //编辑/新增
        pag_edit: function (option) {
            pag_ajax(option, 'edit', function (data) {
                if (data['result'] === 'success') {
                    parent.layer.closeAll();
                    parent.layer.msg('编辑数据成功', {time: 1000, icon: 1});
                    try {
                        if (parent.yTable != null && parent.yTable != undefined) parent.yTable.reload();
                    }
                    catch (ex) {
                    }
                }
            })
        }
    });

    //默认配置
    $.fn.defaults = {
        type: 'get',    //ajax类型
        url_edit: '',    // edit链接
        url_delete: '',    // delete链接
        url_select: '',    // select链接
        params: {}, // 参数
        isFirst: true,  // 是否第一次加载
        Fn: null   //执行成功的回调函数
    };

    //pag_ajax
    function pag_ajax(option, type, Fn) {
        option = $.extend($.fn.defaults, option);
        layui.use('layer', function () {
            var layer = layui.layer;
            $.ajax({
                type: option.type,
                url: type === 'edit' ? option.url_edit : (type === 'delete' ? option.url_delete : option.url_select),
                data: option.params,
                dataType: 'json',
                beforeSend: function () {
                    changeAbled(true);
                    layer.load(1);
                },
                complete: function () {
                    changeAbled(false);
                    layer.closeAll('loading');
                },
                success: function (data) {
                    if (Fn !== null && Fn !== undefined) Fn(data);
                },
                error: function () {
                    layer.msg(errorMsg, {time: 2000});
                }
            });
        });
    }

    //禁用按钮防止重复提交
    function changeAbled(abled) {
        //noinspection JSJQueryEfficiency
        $('.box .layui-btn').attr('disabled', abled);
        if (abled) $('.box .layui-btn').addClass('layui-btn-disabled');
        else $('.box .layui-btn').removeClass('layui-btn-disabled');
    }

    //日期格式化yyyy-MM-dd HH:mm:ss
    Date.prototype.format = function (format) {
        var o = {
            "M+": this.getMonth() + 1, // month
            "d+": this.getDate(), // day
            "h+": this.getHours(), // hour
            "m+": this.getMinutes(), // minute
            "s+": this.getSeconds(), // second
            "q+": Math.floor((this.getMonth() + 3) / 3), // quarter
            "S": this.getMilliseconds()
        };
        if (/(y+)/.test(format)) {
            format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4
                - RegExp.$1.length));
        }
        for (var k in o) {
            if (new RegExp("(" + k + ")").test(format)) {
                format = format.replace(RegExp.$1, RegExp.$1.length === 1
                    ? o[k]
                    : ("00" + o[k]).substr(("" + o[k]).length));
            }
        }
        return format;
    }
})(jQuery);

//ajax错误提示语
var errorMsg = '服务器开小差了';

//类型配置
var audioType = 'mp3';//音频
var videoType = 'mp4|flv|avi|ogg';//视频
var imageType = 'jpg|png|gif|ico';//images
var fileType = 'rar|zip';//文件
var textType = 'txt|ini|html';//文本

$(function () {
    //默认选中菜单
    $('.layui-nav>.layui-nav-item').each(function (index) {
        var link = $(this).find("a").attr("href");
        if (index !== 0 && window.location.href.indexOf(link) > -1) {
            $(this).addClass('layui-this').siblings().removeClass('layui-this');
        }
    });
});

//图片最适合的显示比例(相对于window)
var imgRate = [0.3, 0.8];

//图片缩放比例
var rate = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1];

//获取最适合的图片尺寸
function getImgSize(path, Fn) {
    var realWidth = 0, realHeight = 0;
    var screenWidth = parseInt($(window).width());
    var screenHeight = parseInt($(window).height());
    var theImage = new Image();
    theImage.src = path;
    theImage.onload = function () {
        realWidth = parseInt(theImage.width);
        realHeight = parseInt(theImage.height);
        if (realWidth < screenWidth * imgRate[0]) {
            realHeight = realHeight * (screenWidth * imgRate[0] / realWidth);
            realWidth = screenWidth * imgRate[0];
        }
        if (realHeight < screenHeight * imgRate[0]) {
            realWidth = realWidth * (screenHeight * imgRate[0] / realHeight);
            realHeight = screenHeight * imgRate[0];
        }
        if (realWidth >= screenWidth * imgRate[1]) {
            //noinspection JSDuplicatedDeclaration
            for (var i = 0; i < rate.length; i++) {
                var nowWidth = realWidth * rate[i];
                if (nowWidth < screenWidth * imgRate[1]) {
                    realWidth = nowWidth;
                    realHeight = realHeight * rate[i];
                    break;
                }
            }
        }
        if (realHeight >= screenHeight * imgRate[1]) {
            //noinspection JSDuplicatedDeclaration
            for (var i = 0; i < rate.length; i++) {
                var nowHeight = realHeight * rate[i];
                if (nowHeight < screenHeight * imgRate[1]) {
                    realWidth = realWidth * rate[i];
                    realHeight = nowHeight;
                    break;
                }
            }
        }
        Fn([realWidth, realHeight]);
    }
}

//简单的ajax
function ajax(type, url, params, Fn) {
    layui.use('layer', function () {
        var layer = layui.layer;
        $.ajax({
            type: type,
            url: url,
            data: params,
            dataType: 'json',
            beforeSend: function () {
                layer.load(1);
            },
            complete: function () {
                layer.closeAll('loading');
            },
            success: function (data) {
                if (Fn !== null && Fn !== undefined) Fn(data);
            },
            error: function () {
                layer.msg(errorMsg, {time: 2000});
            }
        });
    });
}
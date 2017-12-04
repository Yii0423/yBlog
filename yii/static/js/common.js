/* ===================================================================
 * yii - Common JS
 *
 * ------------------------------------------------------------------- */

$(function () {
    /*选中菜单项*/
    $('.main-navigation').find('li').each(function () {
        if (window.location.href.indexOf($(this).find('a').prop('href')) > -1)
            $(this).addClass('current').siblings().removeClass('current');
    });
    /*提示*/
    $('[hint]').each(function () {
        $(this).tipso({width: $(this).attr('hint')});
    });
    /*处理文章中图片不居中的问题*/
    $('.primary-content img').parent().addClass('text-center');
});
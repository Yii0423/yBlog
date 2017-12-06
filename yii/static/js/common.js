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
    /*返回顶部*/
    $('#go-top').bind('click', function () {
        $('body,html').animate({scrollTop: 0}, 500);
    });
});
var pageIndex = 2;

/*添加元素后刷新瀑布*/
function refresh($elem) {
    $('.bricks-wrapper').append($elem);
    $elem.imagesLoaded(function () {
        $elem.addClass("animated fadeInUp");
        $('.bricks-wrapper').masonry('appended', $elem);
    });
}

/*瀑布流加载文章*/
function getArticle(category) {
    var type = '';
    if (category == 'news') {
        category = 'essay';
        type = '2';
    }
    if (category == 'codes') {
        category = 'essay';
        type = '3';
    }
    if (category == 'notes') {
        category = 'essay';
        type = '4';
    }
    var url = '/admin/api/select_' + category + '/?page=' + pageIndex + '&limit=10';
    if (type != '') url += '&categoryid=' + type;
    $.ajax({
        url: url,
        dataType: 'json',
        success: function (data) {
            if (data['data'].length == 0) {
                $('#loadingMore').attr('disabled', true).removeAttr("onclick");
                $('#loadingMore').text('没有更多了');
            }
            else {
                var $elem;
                if (category == 'essay') {
                    for (var i = 0; i < data['data'].length; i++) {
                        var model = data['data'][i];
                        if (model['typeid'] == 12) {
                            $elem = $('<article class="brick entry format-audio animate-this">' +
                                '                        <div class="entry-thumb">' +
                                '                            <a href="/essay/' + model['pk'] + '" class="thumb-link">' +
                                '                                <img src="' + model['imagesurl'].replace(',', '') + '" alt="南风喃 - essay - image" style="width:100%"/>' +
                                '                            </a>' +
                                '                            <div class="audio-wrap">' +
                                '                                <audio id="player2" src="' + model['filesurl'].replace(',', '') + '" width="100%"' +
                                '                                       height="42" controls="controls"></audio>' +
                                '                            </div>' +
                                '                        </div>' +
                                '                        <div class="entry-text">' +
                                '                            <div class="entry-header">' +
                                '                                <h1 class="entry-title"><a href="/essay/' + model['pk'] + '">' + model['seotitle'] + '</a></h1>' +
                                '                            </div>' +
                                '                            <div class="entry-excerpt">' + model['seodescription'] + '</div>' +
                                '                        </div>' +
                                '                    </article>');
                            //$('.bricks-wrapper').append();
                        } else if (model['typeid'] == 13) {
                            $elem = $('<article class="brick entry format-standard animate-this">' +
                                '                        <div class="entry-thumb">' +
                                '                            <a href="/essay/' + model['pk'] + '" class="thumb-link">' +
                                '                                <img src="' + model['imagesurl'].replace(',', '') + '" alt="南风喃 - essay - image" style="width:100%"/>' +
                                '                            </a>' +
                                '                        </div>' +
                                '                        <div class="entry-text">' +
                                '                            <div class="entry-header">' +
                                '                                <h1 class="entry-title"><a href="/essay/' + model['pk'] + '">' + model['seotitle'] + '</a></h1>' +
                                '                            </div>' +
                                '                            <div class="entry-excerpt">' + model['seodescription'] + '</div>' +
                                '                        </div>' +
                                '                    </article>');
                        } else if (model['typeid'] == 14) {
                            var imgs = '';
                            var images = model['imagesurl'].split(',');
                            for (var l = 0; l < images.length; l++) {
                                if (images[l] != '')
                                    imgs += '<li><img src="' + images[l] + '" alt="南风喃 - essay" style="width:100%"/></li>';
                            }
                            $elem = $('<article class="brick entry format-gallery group animate-this">' +
                                '                        <div class="entry-thumb">' +
                                '                            <div class="post-slider flexslider">' +
                                '                                <ul class="slides">' + imgs + '</ul>' +
                                '                            </div>' +
                                '                        </div>' +
                                '                        <div class="entry-text">' +
                                '                            <div class="entry-header">' +
                                '                                <h1 class="entry-title"><a href="/essay/' + model['pk'] + '">' + model['seotitle'] + '</a></h1>' +
                                '                            </div>' +
                                '                            <div class="entry-excerpt">' + model['seodescription'] + '</div>' +
                                '                        </div>' +
                                '                    </article>');
                        }
                        /*添加元素至尾部并刷新瀑布流*/
                        refresh($elem);
                    }
                } else if (category == 'collection') {
                    for (var i = 0; i < data['data'].length; i++) {
                        var model = data['data'][i];
                        if (model['imagesurl'] != '') {
                            $elem = $('<article class="brick entry format-standard animate-this">' +
                                '                        <div class="entry-thumb">' +
                                '                            <a href="' + model['url'] + '" class="thumb-link" target="_blank">' +
                                '                                <img src="' + model['imagesurl'].replace(',', '') + '" alt="南风喃 - collection - image"/>' +
                                '                            </a>' +
                                '                        </div>' +
                                '                        <div class="entry-text">' +
                                '                            <div class="entry-header">' +
                                '                                <h1 class="entry-title">' +
                                '                                    <a href="' + model['url'] + '" target="_blank">' + model['title'] + '</a></h1>' +
                                '                            </div>' +
                                '                            <div class="entry-excerpt">' + model['remarks'] + '</div>' +
                                '                        </div>' +
                                '                    </article>');
                        } else {
                            $elem = $('<article class="brick entry format-quote animate-this">' +
                                '                        <a href="' + model['url'] + '">' +
                                '                            <div class="entry-thumb">' +
                                '                                <blockquote>' +
                                '                                    <p>' + model['remarks'] + '</p>' +
                                '                                    <cite>' + model['title'] + '</cite>' +
                                '                                </blockquote>' +
                                '                            </div>' +
                                '                        </a>' +
                                '                    </article>');
                        }
                        /*添加元素至尾部并刷新瀑布流*/
                        refresh($elem);
                    }
                }
                /*重新优化video,audio*/
                $('video,audio').mediaelementplayer();
                /*当前页数+1*/
                pageIndex += 1;
            }
        }
    });
}
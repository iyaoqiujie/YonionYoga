/**
 * @param {侧边栏＋返回顶部}
 */
function goTop() {

    $('html,body').animate({
        'scrollTop': 0
    }, 600);

}
$(".side ul li").hover(function () {
    $(this).find(".sidebox").stop().animate({
        "width": "124px"
    }, 200).css({
        "opacity": "1",
        "filter": "Alpha(opacity=100)",
        "background": "#5478c4"
    })
}, function () {
    $(this).find(".sidebox").stop().animate({
        "width": "54px"
    }, 200).css({
        "opacity": "1",
        "filter": "Alpha(opacity=100)",
        "background": "#fff"
    })
});   
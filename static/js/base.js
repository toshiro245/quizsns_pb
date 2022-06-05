$(function(){

    $('.fa-th-list').click(function(){
        var $header_sm = $('.header-sm-wrapper')
        if($header_sm.hasClass('open')){
            $header_sm.removeClass('open');
            $header_sm.slideUp();
        } else {
            $header_sm.addClass('open');
            $header_sm.slideDown();
        }
    });

});
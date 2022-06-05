$(function(){
    // ヒントボタンが押された時の処理
    $('#btn-hint').click(function(){
        $('#hint-modal-wrapper').fadeIn();
    });

    // 答えボタンが押されたときの処理
    $('#btn-answer').click(function(){
        $('#answer-modal-wrapper').fadeIn();
    });

    // closeが押された時の処理
    $('.close-btn').click(function(){
        $("#hint-modal-wrapper").fadeOut();
        $("#answer-modal-wrapper").fadeOut();
    });

});
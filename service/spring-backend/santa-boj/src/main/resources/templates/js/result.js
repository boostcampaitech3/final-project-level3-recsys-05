let btn_like = document.getElementsByClassName("like_test");
btn_like.onclick = function(){ changeHeart(); }

/* 좋아요 버튼 눌렀을떄 */
function changeHeart(){
    $.ajax({
        type : "POST",
        url : "/clickLike",
        dataType : "json",
        data : "hello",
        success: function (data) {
            console.log(data);
            alert('좋아요 반영 성공!');
        }
    });
}

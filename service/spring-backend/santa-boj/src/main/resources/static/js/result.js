let btn_like = document.getElementsByClassName("like_button");

/* 좋아요 버튼 눌렀을떄 */
function changeHeart(value){
    console.log("clicked");

    $.ajax({
        type : "POST",
        url : "result/clickLike",
        contentType: 'application/json; charset=utf-8',
        dataType : "json",
        data : JSON.stringify({
            "modelName": value
        }),
        success: function (data) {
            console.log(data);
            alert('좋아요가 반영되었습니다!');
        }
    });
}

[].forEach.call(btn_like, function (btn) {
    let value = btn.attributes[1]["value"]
    btn.addEventListener("click", function (){
        changeHeart(value);
}
)})

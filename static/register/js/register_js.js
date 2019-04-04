
//提交注册信息
$("#submitBtn").click(function () {
    var formdata = new  FormData;
    formdata.append("user",$("#user").next().val());
    formdata.append("pwd",$("#pwd").next().val());
    formdata.append("re_pwd",$("#re_pwd").next().val());
    formdata.append("email",$("#email").next().val());
    formdata.append("telephone",$("#telephone").next().val());
    formdata.append("avatar",$("#avatar")[0].files[0]);

    $.ajax({
        url:'',
        type:"post",
        contentType:false,
        processData:false,
        async : false,
        data:formdata,
        success: function (data) {
            console.log(data["user"])
            if (data["user"]){
                window.event.returnValue =false
                window.location.href="/login";

            }
            else {
                //注册失败
                $("div.error").html("");
                $(".from-group input").removeClass("had_error");
                $.each(data.msg ,function (field, error_list) {

                      if (field=="__all__"){
                        $("#re_pwd").next().next().html(error_list[0])
                        $("#re_pwd").next().addClass("had_error")
                        $("#pwd").next().addClass("had_error")
                    }
                     $("#"+field).next().next().html(error_list[0])
                    $("#"+field).next().addClass("had_error")
                })
            }
        }
    })
})


$("#avatar").change(function () {

    //获取文件对象
    var file_obj =$(this)[0].files[0];
    console.log(123,$(this)[0].files[0],123)
    //获取文件路径
    new FormData()
    var reader = new FileReader();
    // 修改img的src属性

    reader.readAsDataURL(file_obj);
    console.log(reader.result,123)
    reader.onload =function(){
        $("#avatar_img").attr("src",reader.result)
    };


});

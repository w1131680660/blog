var user= $("#user_name").html()
console.log(user,typeof user)
if (user=="AnonymousUser"){
    var user =""
    $("#user_name").html("")
}
if (user) {
    $("#login").addClass("remove");
     $("#register").addClass("remove");
     $("#logout").removeClass("remove")

}

pid ="";
$(".acction").click(function ()
{
    var is_up =$(this).hasClass("digght");
    var nid =$("#nid").html()
    console.log(nid)
    $.ajax({
        url:"/digg/",
        type:"post",
        dataType: "json",
        data:{
            csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val(),
            is_up:is_up,
            article_id: nid,
        },
        success: function (data) {
                if(data.error){
                    $("#digg_tips").html(data.error);
                    setTimeout(function () {
                        $("#digg_tips").html("")
                    },2000)}
                else {
                    $("#digg_count").html(data.num_msg.up_num.up_count);
                    $("#bury_count").html(data.num_msg.down_num.down_num)
                }
        }
    })
});
// 评论按钮事件
$("#btn_comment_submit").click(function () {

    var comment_connet = $("#tbCommentBody").val();
    var article_id = $("#nid").html();
    console.log(pid);
    if (pid){
        var index =comment_connet.indexOf("\n");
        comment_connet=comment_connet.slice(index+1)
    }

    $.ajax({
        url:"/comment/",
        type: "post",
        dataType:"json",
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            article_id:article_id,
            content:comment_connet,
            pid:pid,
        },

        success: function (data) {
            var create_time =data.create_time;
            var username =data.username;
            var content =data.content;
            var buliding =$(".comment_list_content").children().length +1;
            var parent_id =data.partent_id;
            var comment_user =data.comment_uer;
            var nid =data.nid;
            pid='';
            $("#tbCommentBody").val("");
            if (parent_id){
                var partent_username = data.partent_username;
            var partent_conetent = data.partent_content;
                var s =` <div class="feedbackItem">
                    <div class="feedbackListSubtitle">
                        <div class="feedbackMange">
                            <span class="comment_actions" usernmae=${comment_user} comment_pk=${nid}>回复</span>
                        </div>
                        <span class="layer">#${buliding}楼</span> &nbsp;
                        <span class="comment_data">${ create_time }</span>
                        <span class="layer">${ username }</span>
                    </div>
                    
                        <div class="blog_comment_bod well" >
                            <p>${partent_username}: ${partent_conetent}</p>
                        </div>
                
                    <div class="feedbackCon">
                        <div class="blog_comment_body">${content}</div>
                    </div>
                </div>`
            }
            else {
                 var s =` <div class="feedbackItem">
                    <div class="feedbackListSubtitle">
                        <div class="feedbackMange">
                            <span class="comment_actions" usernmae=${comment_user} comment_pk=${nid}>回复</span>
                        </div>
                        <span class="layer">#${buliding}楼</span> &nbsp;
                        <span class="comment_data">${ create_time }</span>
                        <span class="layer">${ username }</span>
                    </div>
                    <div class="feedbackCon">
                        <div class="blog_comment_body">${content}</div>
                    </div>
                </div>`
            }

            $(".comment_list_content").append(s)
            pid =""
        }
    })
});

//回复按钮事件

$(".comment_list_content").on("click",".comment_actions",function () {
     console.log(123)
    $("#tbCommentBody").val("");
    $("#tbCommentBody").focus();
    var val ="@"+$(this).attr("username");
    $("#tbCommentBody").val(val);
    pid =$(this).attr("comment_pk");
})
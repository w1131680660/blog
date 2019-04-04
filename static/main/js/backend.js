
$("#create_content").click(function () {



    var title =$("#edit_title").val();
    var content = editor.html();
    var tag =$("#tag").val();
    var category=$("#category").val();

    $.ajax({
        url:"/create_article/",
        type:'post',
        dataType:'json',
        data:{
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            title:title,
            content:content,
            tag:tag,
            category:category,
        },
        success: function (data) {

             editor.html("");
             $("#tag").val("");
             $("#category").val("");
             alert("您已成功发表文章",title)
             $("#edit_title").val("");
        }
    })
})

 KindEditor.ready(function (K) {
        window.editor = K.create('#article_content', {
            width: "780",
            hegiht: "500",
            uploadJson: "/upload/",
            extraFileloadParams:{
               csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            },
            items: [
                'source', '|', 'undo', 'redo', '|', 'preview', 'print', 'template', 'code', 'cut', 'copy', 'paste',
                'plainpaste', 'wordpaste', '|', 'justifyleft', 'justifycenter', 'justifyright',
                'justifyfull', 'insertorderedlist', 'insertunorderedlist', 'indent', 'outdent', 'subscript',
                'superscript', 'clearhtml', 'quickformat', 'selectall', '|', 'fullscreen', '/',
                'formatblock', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold',
                'italic', 'underline', 'strikethrough', 'lineheight', 'removeformat', '|', 'image', 'multiimage',
                'flash', 'media', 'insertfile', 'table', 'hr', 'emoticons', 'baidumap', 'pagebreak',
                'anchor', 'link', 'unlink', '|', 'about'
            ],
        });

    });
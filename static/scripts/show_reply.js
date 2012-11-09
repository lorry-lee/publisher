
function ShowReplyCallback(response_dict) 
{ 
    // Clear the replies    
    $("#reply_div").html("");
    
    // Loop through the replies
    for (var i = 0; i < response_dict.reply_count; ++i) {
        var key = 'reply_' + i;
        var val = response_dict[key];
        if (val.user == "unknown_user") { val.user = "匿名用户" };
        $( "#ReplyTemplate" ).tmpl( val ).appendTo("#reply_div");
        document.getElementById(key).innerHTML = $.unescape(document.getElementById(key).innerHTML);
        
        for (var j = 0; j < val.reply_ref_count; ++j) {
            var reply_ref_key = 'parent_' + j;
            var reply_ref_val = val.ref_reply[reply_ref_key];
            if (reply_ref_val.user == "unknown_user") { reply_ref_val.user = "匿名用户" };
            $( "#ReplyRefTemplate" ).tmpl( reply_ref_val ).appendTo("#" + 'table_' + key);
        }
    }

    var ref_reply_divs = $("div[id^='ref_reply_']");
    for (var idx = 0; idx < ref_reply_divs.length; ++idx) {
        ref_reply_divs[idx].innerHTML = $.unescape(ref_reply_divs[idx].innerHTML);
    }
}

function ShowReply(post_id, page_id)
{
    temp_url = '/post/' + post_id + '/show_reply/' + page_id + '/page/';
    
    $("#reply_div").html("加载评论中...");

    $.ajax({
        url:temp_url,
        type:'get',
        error: function(){
            $("#reply_div").html("显示评论的时候网页产生错误");
        },
        success:function(data){
            response_dict = eval('('+data+')');
            ShowReplyCallback(response_dict);
        }
    });    
}

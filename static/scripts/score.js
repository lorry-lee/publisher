$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
function ScoreCallback(response_dict)
{
    vote_span_name = 'vote_' + response_dict.post_id;
    neg_vote_span_name = 'neg_vote_' + response_dict.post_id;
    document.getElementById(vote_span_name).innerHTML = response_dict.vote_num;
    document.getElementById(neg_vote_span_name).innerHTML = "-" + response_dict.neg_vote_num;
}

function Score(post_id, type)
{
    temp_url = '/post/' + post_id + '/' + type + '/?xhr';

    $.ajax({
        url:temp_url,
        type:'post',
        error: function(){
            alert("打分的时候网页产生错误");
        },
        success:function(data){
            response_dict = eval('('+data+')');
            ScoreCallback(response_dict);
        }
    });
}

function Vote(post_id)
{
    Score(post_id, 'vote');
}

function NegVote(post_id)
{
    Score(post_id, 'neg_vote')
}


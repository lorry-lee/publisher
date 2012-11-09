
var oldElement;

function ChangeToLocate(replyDiv)
{
    var newElement = document.getElementById(replyDiv);
    var temp = oldElement.innerHTML;
    oldElement.innerHTML = "";
    newElement.innerHTML = temp;
    oldElement = newElement;
}

function ChangeToReplyLocate(replyId)
{
    ChangeToLocate("ReplyFormDiv_" + replyId);
    document.getElementById("SubmitCommentDiv").innerHTML = "<a href='javascript:ChangeToDefaultLocate()'>点击这里单独发表评论</a>";
    document.getElementById("FormCommentParentId").value = replyId;
}

function ChangeToDefaultLocate()
{
    ChangeToLocate("SubmitCommentDiv");
    document.getElementById("FormCommentParentId").value = -1;
}

function InitLocateReply()
{
    oldElement = document.getElementById("SubmitCommentDiv");
}

$(document).ready(InitLocateReply);

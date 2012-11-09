function ReplaceAllTextAreaWithFckeditor(width, height)
{
    var nodeList = document.getElementsByTagName("textarea");

    for (var i=0; i<nodeList.length; i++) {
        var elm = nodeList.item(i);
        var oFCKeditor = new FCKeditor( elm.id ) ; 
        oFCKeditor.Width = width;
        oFCKeditor.Height = height;
        oFCKeditor.ToolbarSet = 'Customize' ;
        oFCKeditor.BasePath = "/fckeditor/fckeditor/" ; 
        oFCKeditor.ReplaceTextarea() ; 
    }
}

function SetImageId( id )
{
    document.getElementById('head_id').value = id;
}

function SetThumbUrl( url )
{
    document.getElementById('head_url').value = url;
    var imgElement = document.getElementById('img_preview');
    imgElement.src = document.getElementById('head_url').value;
}

function HeadBrowseServer()
{
    url = "/fckeditor/fckeditor/editor/gallery/browse/"
	var sOptions = "toolbar=no,status=no,resizable=yes,dependent=yes,scrollbars=yes" ;
	sOptions += ",width=" + 800 ;
	sOptions += ",height=" + 600 ;
	sOptions += ",left=" + 0 ;
	sOptions += ",top=" + 0 ;

	window.open( url, 'BrowseWindow', sOptions ) ;
}
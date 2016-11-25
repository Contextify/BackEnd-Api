function httpGet(theUrl) {
    var xmlHttp = null;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    if ( xmlHttp.readyState==1 )
        xmlHttp.send( null );
    return xmlHttp.responseText;
}
$(document).ready(function(){
	 $.ajax({
   	  url: 'http://home.sriramsv.com:5000/',
   	  //data: data,
   	  success: function(data) {
            console.log(data);
         },
         contentType : 'application/json'   
   	  //dataType: "json"
   	});
	
console.log("I m inside");	
//var dataObject = httpGet("http://localhost/json/timeline/");
//if ( dataObject != null )
{
   // var jsObject = eval("("+dataObject+")");
    createStoryJS({
       type:       'timeline',
       width:      '100%',
       height:     '100%',
       source:     jsObject,
       embed_id:   'my-timeline'
    });
}
});
$(document).ready(function(){
     $('a[@href$="mp3"]').each(function(){
        $(this).replaceWith(
            $('<object type="application/x-shockwave-flash" data="/static/media/player.swf" height="24" width="290">'
                + '<param name="movie" value="/static/media/player.swf">' 
                + '<param name="FlashVars" value="soundFile=' + this.href + '">'
                + '<param name="quality" value="high">'
                + '<param name="menu" value="false">'
                + '<param name="bgcolor" value="#FFFFFF">'
            + '</object>'));
            })
});
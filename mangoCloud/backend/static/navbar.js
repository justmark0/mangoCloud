var print = console.log;
print('he')
var active = null;
$('.nav_button').click(function() {
    if(active != null){
        DisActivate();
    }
    Activate(this);
})

function Activate(element){
    $(element).children("div.nav_button_text").css('color','#E57474');
    var active_s_src = $(element).children("div.nav_button_img").children("img.nav_button_img").attr("src").replace("_over.",".").replace("_active.",".");
    $(element).children("div.nav_button_img").children("img.nav_button_img").attr("src",active_s_src.replace(".","_active."));
    active = $(element);
    print($(element).attr("id"));

}
function DisActivate(){
    active.children("div.nav_button_text").css('color','#929292');
    var active_s_src = active.children("div.nav_button_img").children("img.nav_button_img").attr("src").replace("_over.",".").replace("_active.",".");
    active.children("div.nav_button_img").children("img.nav_button_img").attr("src",active_s_src);
}


$('.nav_button').mouseover(function () {
    if(active == null || $(this).attr("id") != active.attr("id")){
        $(this).children("div.nav_button_text").css('color','#FFD86E');
        var hover_src = $(this).children("div.nav_button_img").children("img.nav_button_img").attr("src").replace("_over.",".").replace("_active.",".");
        $(this).children("div.nav_button_img").children("img.nav_button_img").attr("src",hover_src.replace(".","_over."));
    }
})
.mouseout(function () {
    if(active == null || $(this).attr("id") != active.attr("id")){
        $(this).children("div.nav_button_text").css('color','#929292');
        var hover_src = $(this).children("div.nav_button_img").children("img.nav_button_img").attr("src").replace("_over.",".").replace("_active.",".");
        $(this).children("div.nav_button_img").children("img.nav_button_img").attr("src",hover_src);
    }
});

Activate($('.nav_button#Main'));

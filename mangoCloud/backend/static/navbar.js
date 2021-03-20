var print = console.log;
var active = null;
$('.nav_button').click(function() {
    if(active != null){
        DisActivate();
    }
    Activate(this);
});

function Activate(element){
    $(element).children("div.nav_button_text").css('color','#E57474');
    var active_s_src = $(element).children("div.nav_button_img").children("img.nav_button_img").attr("src").replace("_over.svg",".svg").replace("_active.svg",".svg");
    $(element).children("div.nav_button_img").children("img.nav_button_img").attr("src",active_s_src.replace(".svg","_active.svg"));
    active = $(element);
    print($(element).attr("id"));
    if($(element).attr("id") == 'Files'){
        Files();
    }
}
function DisActivate(){
    active.children("div.nav_button_text").css('color','#929292');
    var active_s_src = active.children("div.nav_button_img").children("img.nav_button_img").attr("src").replace("_over.svg",".svg").replace("_active.svg",".svg");
    active.children("div.nav_button_img").children("img.nav_button_img").attr("src",active_s_src);
}


$('.nav_button').mouseover(function () {
    if(active == null || $(this).attr("id") != active.attr("id")){
        $(this).children("div.nav_button_text").css('color','#FFD86E');
        var hover_src = $(this).children("div.nav_button_img").children("img.nav_button_img").attr("src").replace("_over.svg",".svg").replace("_active.svg",".svg");
        $(this).children("div.nav_button_img").children("img.nav_button_img").attr("src",hover_src.replace(".svg","_over.svg"));
    }
})
.mouseout(function () {
    if(active == null || $(this).attr("id") != active.attr("id")){
        $(this).children("div.nav_button_text").css('color','#929292');
        var hover_src = $(this).children("div.nav_button_img").children("img.nav_button_img").attr("src").replace("_over.svg",".svg").replace("_active.svg",".svg");
        $(this).children("div.nav_button_img").children("img.nav_button_img").attr("src",hover_src);
    }
});

Activate($('.nav_button#Files'));

function Files(){
    
}

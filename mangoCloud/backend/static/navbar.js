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
    if($(element).attr("id") == 'Main'){
        ListView();
    }
    if($(element).attr("id")  in functional){
        functional[$(element).attr("id")]();
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



var folder_src = "../static/img/tabler-icon-folder.svg";
var folder_open_src = "../static/img/tabler-icon-chevron-right.svg";
var HEARAHY = {};
var LEVELS = [];

async function Files(){
    HEARAHY = {};

    var data = await get_all_files();
    for(var arc in data){
        if(!(data[arc]['parent'] in HEARAHY)){
            HEARAHY[data[arc]['parent']] = [];
        }
        HEARAHY[data[arc]['parent']].push(data[arc]);
    }
    closeColumnMac(0);
    createColumnMac();
}
function createElamenMac(name = '', file_id = '', is_folder = false,level = 0){
    const item_use = document.createElement('div');
    item_use.className = "item_use";
    const item_name = document.createElement('div');
    item_name.className = "item_name";
    const img1 = document.createElement('img');
    img1.className = "item_icon";
    item_use.appendChild(item_name);
    item_use.appendChild(img1);
    item_name.innerHTML = name;
    if(is_folder){
        const img2 = document.createElement('img');
        img2.className = "item_folder_open";
        item_use.appendChild(img2);
        img2.src = folder_open_src;
        img1.src = folder_src;
        item_use.onclick = function(){
            closeColumnMac(level+1);
            createColumnMac(file_id,level+1);
        }
    }
    return item_use;
}
async function createColumnMac(fold_id = 'root',level = 0){
    LEVELS[level] = fold_id;
    const column_use = document.createElement('div');
    column_use.className = "column_use";
    column_use.id = fold_id;
    const column_list = document.createElement('div');
    column_list.className = "column_list";
    
    document.getElementById('space_use').appendChild(column_use);
    column_use.appendChild(column_list);
    column_list.id = fold_id;
    for(arc in HEARAHY[fold_id]){
        column_list.appendChild(createElamenMac(HEARAHY[fold_id][arc]['name'],HEARAHY[fold_id][arc]['file_id'],HEARAHY[fold_id][arc]['is_folder'],level));
    }


    // <div class="column_use">
    // <div class="column_list" id="path"></div>
}
function closeColumnMac(level){
    while(level < LEVELS.length){
        print(LEVELS[level]);
        document.getElementById(LEVELS[level]).remove()

        level ++;
    }
}

function ListViewElment(element){
    print(element)
    const list_elament = document.createElement('div');
    list_elament.className = "list_elament";
    const list_elament_file_name = document.createElement('div');
    list_elament_file_name.className = "list_elament_file_name";
    list_elament_file_name.innerHTML = element['name'];
    const list_elament_date = document.createElement('div');
    list_elament_date.className = "list_elament_date";
    list_elament_date.innerHTML = element['name'];
    const list_elament_type = document.createElement('div');
    list_elament_type.className = "list_elament_type";
    list_elament_type.innerHTML = element['name'];
    const list_elament_size = document.createElement('div');
    list_elament_size.className = "list_elament_size";
    list_elament_size.innerHTML = '-';
    list_elament.appendChild(list_elament_file_name);
    list_elament.appendChild(list_elament_date);
    list_elament.appendChild(list_elament_type);
    list_elament.appendChild(list_elament_size);
    return list_elament;
}
async function ListView(){
    
    var data = await get_all_files();
    for(var arc in data){
        if(data[arc]['is_folder'] == true){
            continue;
        }
        document.getElementById('space_use').appendChild(ListViewElment(data[arc]));
    }
}



function Exit(){
    HEARAHY = {};
    closeColumnMac(0);
    show_login_pop_up();
    USER_LOGIN = '';
    USER_PASSWORD = '';
    USER_TOKEN = '';
    $("#Login_name").text('');
    $("#space_use").text('');
    save_cookie();
}


var functional = {
    'Exit':Exit,
    'Files':ListView,
};


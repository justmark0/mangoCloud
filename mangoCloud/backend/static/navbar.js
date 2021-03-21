var print = console.log;
var NOW_ACTIVE = '';
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
    updateProcessBar();
    if($(element).attr("id")  in functional){
        functional[$(element).attr("id")]();
        NOW_ACTIVE = $(element).attr("id");
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
    $('#rename_m').css('display','none');
    $('#share_m').css('display','none');
    $('#access_m').css('display','none');
    $('#downloud_m').css('display','none');
    HEARAHY = {};document.getElementById('space_use').innerHTML = '';

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
    item_use.id = file_id;
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
    if (item_use.addEventListener) {
        item_use.addEventListener('contextmenu', showmenu, false);
    } else {
        item_use.attachEvent('oncontextmenu', showmenu);
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
}
function closeColumnMac(level){
    print(level)
    print(LEVELS)
    while(LEVELS.length > level){
        print(LEVELS[LEVELS.length-1]);
        try{
        document.getElementById(LEVELS[LEVELS.length-1]).remove();
        }catch(e){};
        LEVELS.splice(LEVELS.length-1,1);
    }
    print(LEVELS)
}
function calcualteSize(bites){
    var res = '';
    if(bites < 1024){
        return bites.toString() + "B";
    }else if(bites < 1048576){
        return ((bites/1024)>>1).toString() + "KB";
    }else if(bites < 1073741824){
        return ((bites/1048576)>>1).toString() + "MB";
    }
    return '';
}
function findType(name){
    var x = name.split('.');
    return x[x.length-1].toUpperCase();
}
var OPEN_TYPES = ['JPG', 'PDF', 'JPG'];
function ListViewElment(element){
    const list_elament = document.createElement('div');
    list_elament.className = "list_elament";
    const list_elament_file_name = document.createElement('div');
    list_elament_file_name.className = "list_elament_file_name";
    list_elament_file_name.innerHTML = element['name'];
    const list_elament_date = document.createElement('div');
    list_elament_date.className = "list_elament_date";
    list_elament_date.innerHTML = element['date_of_creation'];
    const list_elament_type = document.createElement('div');
    list_elament_type.className = "list_elament_type";
    list_elament_type.innerHTML = element['type'];
    const list_elament_size = document.createElement('div');
    list_elament_size.className = "list_elament_size";
    list_elament_size.innerHTML = calcualteSize(element['size']);
    list_elament.appendChild(list_elament_file_name);
    list_elament.appendChild(list_elament_date);
    list_elament.appendChild(list_elament_type);
    list_elament.appendChild(list_elament_size);
    list_elament.id = element['file_id'];
    list_elament.onclick = function(){
        // print(element)
        openFile(element['file_id'])
    }
    if (list_elament.addEventListener) {
        list_elament.addEventListener('contextmenu', showmenu, false);
    } else {
        list_elament.attachEvent('oncontextmenu', showmenu);
    }
    // list_elament.addEventListener('contextmenu', showmenu);
    return list_elament;
}
async function ListView(type = ''){
    SORT_TYPE = '';
    $('#rename_m').css('display','block');
    $('#share_m').css('display','block');
    $('#access_m').css('display','block');
    $('#downloud_m').css('display','block');
    SORTING_ARRAY = [];
    var data = await get_all_files();
    for(arc in data){
        if(data[arc]['is_folder'] == true){
            continue;
        }
        data[arc]['type'] = findType(data[arc]['name']);
        SORTING_ARRAY.push(data[arc]);
    }
    if(type == ''){
        showList();
    }else{
        ListSorted(type)
    }
}
var TYPE_ORIENTATED = 0
function ListSorted(Type = ''){
    if(Type == ''){
        ListView();
        return;
    }
    if(SORT_TYPE == Type){
        TYPE_ORIENTATED = !TYPE_ORIENTATED;
        SORTING_ARRAY = SORTING_ARRAY.reverse();
    }else{
        TYPE_ORIENTATED = true;
        SORT_TYPE = Type;
        merge_spite(0,SORTING_ARRAY.length);
    }
    showList();
}

function showList(){
    const icon = document.createElement('img');
    icon.className = 'list_menu_item_icon';
    const icon2 = document.createElement('div');
    icon2.className = 'list_menu_item_icon';
    if(TYPE_ORIENTATED){
        icon.src = '../static/img/tabler-icon-caret-up.svg';
    }else{
        icon.src = '../static/img/tabler-icon-caret-down.svg';
    }

    document.getElementById('space_use').innerHTML = '';
    const list_elament = document.createElement('div');
    list_elament.className = "list_elament";
    const list_elament_file_name = document.createElement('div');
    list_elament_file_name.className = "list_elament_file_name";
    if(SORT_TYPE == 'NAME'){
        list_elament_file_name.appendChild(icon);
    }else{
        list_elament_file_name.appendChild(icon2);
    }
    list_elament_file_name.innerHTML += 'Name';
    list_elament_file_name.onclick = function(){
        ListSorted('NAME');
    }
    const list_elament_date = document.createElement('div');
    list_elament_date.className = "list_elament_date";
    if(SORT_TYPE == 'DATE'){
        list_elament_date.appendChild(icon);
    }else{
        list_elament_date.appendChild(icon2);
    }
    list_elament_date.innerHTML += 'Date';
    list_elament_date.onclick = function(){
        ListSorted('DATE');
    }
    const list_elament_type = document.createElement('div');
    list_elament_type.className = "list_elament_type";
    if(SORT_TYPE == 'TYPE'){
        list_elament_type.appendChild(icon);
    }else{
        list_elament_type.appendChild(icon2);
    }
    list_elament_type.innerHTML += 'Type';
    list_elament_type.onclick = function(){
        ListSorted('TYPE');
    }
    const list_elament_size = document.createElement('div');
    list_elament_size.className = "list_elament_size";
    if(SORT_TYPE == 'SIZE'){
        list_elament_size.appendChild(icon);
    }else{
        list_elament_size.appendChild(icon2);
    }
    list_elament_size.innerHTML += 'Size';
    list_elament_size.onclick = function(){
        ListSorted('SIZE');
    }
    list_elament.appendChild(list_elament_file_name);
    list_elament.appendChild(list_elament_date);
    list_elament.appendChild(list_elament_type);
    list_elament.appendChild(list_elament_size);
    document.getElementById('space_use').appendChild(list_elament);

    const srcoll_blabla = document.createElement('div');
    srcoll_blabla.className = "srcoll_blabla";
    srcoll_blabla.id = 'srcoll_blabla';
    document.getElementById('space_use').appendChild(srcoll_blabla);
    for(var arc in SORTING_ARRAY){
        document.getElementById('srcoll_blabla').appendChild(ListViewElment(SORTING_ARRAY[arc]));
    }
}

async function Trash(type = ''){
    $('#rename_m').css('display','none');
    $('#share_m').css('display','none');
    $('#access_m').css('display','none');
    $('#downloud_m').css('display','block');
    SORT_TYPE = '';
    SORTING_ARRAY = [];
    var data = await get_all_in_trash();
    for(arc in data){
        if(data[arc]['is_folder'] == true){
            continue;
        }
        data[arc]['type'] = findType(data[arc]['name']);
        SORTING_ARRAY.push(data[arc]);
    }
    if(type == ''){
        showList();
    }else{
        ListSorted(type)
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
    'Main':ListView,
    'Trash':Trash,
    'Album':Files,
};
// tabler-icon-caret-down.svg
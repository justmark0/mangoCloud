var SORTING_ARRAY = []; // element firstpart - value , secound - data
var SORTING_ARRAY2 = [];
var SORT_TYPE = '';

function compare(a,b){
    if(SORT_TYPE == 'DATE'){
        for(var i=0;i<a['date_of_creation'].length;i++){
            if(a['date_of_creation'][i] > b['date_of_creation'][i]){
                return false;
            }
            if(a['date_of_creation'][i] < b['date_of_creation'][i]){
                return true;
            }
        }
        return true;
    }else if(SORT_TYPE == 'SIZE'){
        return a['size']<=b['size'];
    }else if(SORT_TYPE == 'NAME'){
        if(a['name'].length != b['name'].length){
            return a['name'].length <= b['name'].length;
        }
        for(var i=0;i<a['name'].length;i++){
            if(a['name'][i] > b['name'][i]){
                return false;
            }
            if(a['name'][i] < b['name'][i]){
                return true;
            }
        }
        return true;
    }else if(SORT_TYPE == 'TYPE'){

        if(a['type'].length != b['type'].length){
            return a['type'].length <= b['type'].length;
        }
        for(var i=0;i<a['type'].length;i++){
            if(a['type'][i] > b['type'][i]){
                return false;
            }
            if(a['type'][i] < b['type'][i]){
                return true;
            }
        }
        return true;
    }
}
function merge(l1,r1,l2,r2){
    var l = l1, x = l1;
    while(l1<r1 || l2<r2){
        if(l2 == r2 || (l1 != r1 && compare(SORTING_ARRAY[l1],SORTING_ARRAY[l2]))){
            SORTING_ARRAY2[x] = SORTING_ARRAY[l1];
            x++; 
            l1++;
        }else{
            SORTING_ARRAY2[x] = SORTING_ARRAY[l2];
            x++; 
            l2++;
        }
    }
    for(var i = l;i<r2;i++){
        SORTING_ARRAY[i] = SORTING_ARRAY2[i];
    }
}
function merge_spite(l,r){
    if(l == r){
        return;
    }
    var mid = Math.floor((l+r)/2);
    if(l != mid){
        merge_spite(l,mid);
        merge_spite(mid,r);
    }
    merge(l,mid,mid,r);
}

var RIGHT_MENU = null;
function addMenuListeners(){
    document.getElementById('rename_m').addEventListener('click', workRightMenu);
    document.getElementById('share_m').addEventListener('click', workRightMenu);
    document.getElementById('access_m').addEventListener('click', workRightMenu);
    document.getElementById('downloud_m').addEventListener('click', workRightMenu);
    document.getElementById('delete_m').addEventListener('click', workRightMenu);
}

function workRightMenu(ev){
    print(this.id);
    if('delete_m' == this.id){
        deleteFile(FILE_ID_OPERATION);
        if(Files_or_List){
            var type = SORT_TYPE
            ListView()
            
            ListSorted(type);
        }
        FILE_ID_OPERATION = '';
        RIGHT_MENU.classList.add('off');
        RIGHT_MENU.style.top = '-200%';
        RIGHT_MENU.style.left = '-200%';
    }
}
RIGHT_MENU = document.querySelector('.menu');
function showmenu(ev){

    print(this.id)
    FILE_ID_OPERATION = this.id;
    //stop the real right click menu
    ev.preventDefault(); 
    //show the custom menu
    RIGHT_MENU.style.top = `${ev.clientY - 20}px`;
    RIGHT_MENU.style.left = `${ev.clientX - 20}px`;
    addMenuListeners();
    // RIGHT_MENU.classList.remove('off');
}

function hidemenu(ev){
    FILE_ID_OPERATION = '';
    RIGHT_MENU.classList.add('off');
    RIGHT_MENU.style.top = '-200%';
    RIGHT_MENU.style.left = '-200%';
}
RIGHT_MENU = document.querySelector('.menu');
RIGHT_MENU.classList.add('off');
RIGHT_MENU.addEventListener('mouseleave', hidemenu);
addMenuListeners();
// print(RIGHT_MENU.classList);



$(".add_button").click(function(){
    
})
var fileSelect = document.getElementById("fileSelect"),
  fileElem = document.getElementById("fileElem");
fileSelect.addEventListener("click", function (e) {
    if(USER_TOKEN == ''){
        popupErrorMessage("To do this operation you need to be login in system");
        return;
    }
    if (fileElem) {
        fileElem.click();
    }
    e.preventDefault();
}, false);

async function handleFiles(files){
    for(var i=0;i<files.length;i++){
        var formData = new FormData();
        formData.append('file',files[i]);
        formData.append('token',USER_TOKEN);
        formData.append('file_name',files[i].name);

        var res = await $.ajax({
            url : '/api/upload_file',
            type : 'POST',
            data : formData,
            processData: false,
            contentType: false,
            success : function(data) {
            },
            error:function(error_data){
                popupErrorMessage(error_data);
            }
        });
        if(!res){
            return;
        }
        if('Error' in res){
            popupErrorMessage(res['Error']);
            return;
        }
    }
}
async function loadignFiles(folder_id = "1"){
    if(USER_TOKEN == ''){
        popupErrorMessage("To do this operation you need to be login in system");
        return;
    }

    var myHeaders = new Headers();
    // myHeaders.append("Content-Type", "application/json");
    var raw = JSON.stringify({'token': USER_TOKEN,'file_id': folder_id});
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow',
        responseType: 'arraybuffer'
    };
    var filename = '';
    var response = await fetch('api/get_file',requestOptions)
    try {
        filename = response.headers
          .get("content-disposition")
          .split('"')[1];
        return [await response.blob(), filename]
    } catch (error) {
        try{
            return [(await response.json())['Error'], ''];
        }catch(error){
            return ["Unexpected Error" , ''];
        }
    }
}
function saveFile(blob){
    try{
        const url = window.URL.createObjectURL(blob[0]);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        // the filename you want
        a.download = blob[1];
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        popupErrorMessage(blob[0]);
    }
}

// loadignFiles();
async function makeDirectory(dir_name = 'root'){
    if(USER_TOKEN == ''){
        popupErrorMessage("To do this operation you need to be login in system");
        return;
    }
    $.ajax({

        type : "POST",
        mode    : "no-cors",
        url    : "/api/mkdir",
        dataType: "json",
        headers : {"Access-Control-Allow-Origin" : "*"},
        contentType: "application/json; charset=utf-8",
        data   : JSON.stringify({"token":USER_TOKEN,"file_name":dir_name}),
        success: function(data){
            return data;
        },

        error: function(error_data){
            popupErrorMessage(error_data);
        }
    });
}
function closeImg(){
    $(".show_window").css('display','none');
    $(".filter").css('display','none');
    $(".filter").click(()=>{});
}
async function showImg(blob,file_id){
    
    try{
        const url = await window.URL.createObjectURL(blob[0]);
        $("#show_img").attr('src',url);
        print(url)
        $(".filter").click(()=>closeImg());
        $("#show_window_file_name").text(blob[1]);
        $("#show_nav_close").click(() => closeImg());
        $("#show_nav_download").click(() => saveFile(blob));
        $("#show_nac_sheare").click(function(){
            print('lol');
            closeImg();
            show_access_pop_up(file_id);
        });
        
    }catch(error){
    }
}
async function openFile(file_id = '10f872afb93c0f9cad41e6c4fca837b1e8793ebbac5862ce898b9676b21c47ba'){
    $(".show_window").css('display','block');
    $(".filter").css('display','block');
    file_data = await loadignFiles(file_id);
    // saveFile(file_data);
    showImg(file_data,file_id);
}
async function get_all_files(){
    const data = await $.ajax({

        type : "POST",
        mode    : "no-cors",
        url    : "/api/get_all_files",
        dataType: "json",
        headers : {"Access-Control-Allow-Origin" : "*"},
        contentType: "application/json; charset=utf-8",
        data   : JSON.stringify({"token":USER_TOKEN}),
        success: function(data){
            return data;
        },

        error: function(error_data){
            popupErrorMessage(error_data);
        }
    }); 
    if('Error' in data){
        popupErrorMessage(data['Error']);
        return null;
    }
    return data;
}
async function makedir(file_name){
    const data = await $.ajax({

        type : "POST",
        mode    : "no-cors",
        url    : "/api/mkdir",
        dataType: "json",
        headers : {"Access-Control-Allow-Origin" : "*"},
        contentType: "application/json; charset=utf-8",
        data   : JSON.stringify({"token":USER_TOKEN, 'file_name': file_name}),
        success: function(data){
            return data;
        },

        error: function(error_data){
            popupErrorMessage(error_data);
        }
    }); 
    if('Error' in data){
        popupErrorMessage(data['Error']);
        return null;
    }
    // print(data);
}
async function give_accsess(file_id, username){
    const data = await $.ajax({
        type : "POST",
        mode    : "no-cors",
        url    : "/api/give_accsess",
        dataType: "json",
        headers : {"Access-Control-Allow-Origin" : "*"},
        contentType: "application/json; charset=utf-8",
        data   : JSON.stringify({"token":USER_TOKEN, 'file_id': file_id, 'username': username}),
        success: function(data){
            return data;
        },

        error: function(error_data){
            popupErrorMessage(error_data);
        }
    }); 
    if('Error' in data){
        popupErrorMessage(data['Error']);
        return null;
    }
    popupErrorMessage(data['message'],true);
}


// var folder_src = "../static/img/tabler-icon-folder.svg";
// var folder_open_src = "../static/img/tabler-icon-chevron-right.svg";
// makedir("LOLLL");
// get_all_files();


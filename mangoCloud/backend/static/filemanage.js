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

function handleFiles(files){
    for(var i=0;i<files.length;i++){
        var data = {
            "token":USER_TOKEN,
            "file_name":files[i].name
        };
        var formData = new FormData();
        formData.append('file',files[i]);
        formData.append('token',USER_TOKEN);
        formData.append('file_name',files[i].name);

        $.ajax({
            url : '/api/upload_file',
            type : 'POST',
            data : formData,
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success : function(data) {
                console.log(data);
            },
            error:function(error_data){
                popupErrorMessage(error_data);
            }
        });
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
          print(filename)
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
        print(error)
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
async function showImg(blob){
    
    try{
        const url = await window.URL.createObjectURL(blob[0]);
        $("#show_img").attr('src',url);
        $(".filter").click(()=>closeImg());
        $("#show_window_file_name").text(blob[1]);
        $("#show_nav_close").click(() => closeImg());
        $("#show_nav_download").click(() => saveFile(blob));
    }catch(error){
        print(error);
    }
}
async function openFile(file_id = 'e0a89c8845e2f6417e9f209291f7368b579021b0f16de7a47a50b25ce0d23346'){
    $(".show_window").css('display','block');
    $(".filter").css('display','block');
    file_data = await loadignFiles(file_id);
    // saveFile(file_data);
    // print(file_data[0]);
    showImg(file_data);
}

// openFile();

var folder_src = "../static/img/tabler-icon-folder.svg";
var folder_open_src = "../static/img/tabler-icon-chevron-right.svg";
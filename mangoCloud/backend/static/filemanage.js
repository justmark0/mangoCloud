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
    print(files);
    var data = {
        "token":USER_TOKEN,
        "file_name":files[0].name
    };
    print(data['file_name']);
    var formData = new FormData();
    formData.append('file',files[0]);
    formData.append('token',USER_TOKEN);
    formData.append('file_name',files[0].name);

    $.ajax({
        url : '/api/upload_file',
        type : 'POST',
        data : formData,
        processData: false,  // tell jQuery not to process the data
        contentType: false,  // tell jQuery not to set contentType
        success : function(data) {
            console.log(data);
            alert(data);
        }
    });
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
        redirect: 'follow'
    };
    var filename = '';
    var error_text = await fetch('api/get_file',requestOptions)
    .then(resp => {
        // print(await ( resp.json()));
        try {
            filename = resp.headers
              .get("content-disposition")
              .split('"')[1];
              print(filename)
            return resp.blob()
        } catch (error) {
            return resp.json()
        }
    })
    .then(blob => {
        try{
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            // the filename you want
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            alert('your file has downloaded!');
        } catch (error) {
            return blob['Error']
        }
    })
    .catch(() => 'Un expected error');
    if(error_text != null){
        popupErrorMessage(error_text);
    }
}
function popupErrorMessage(message){
    const error_msg = document.createElement('div');
    const error_msg_text = document.createElement('div');
    const error_msg_close = document.createElement('img');
    error_msg.className = "error_msg";
    error_msg_text.className = "error_msg_text";
    error_msg_text.innerHTML = message;
    error_msg_close.className = "error_msg_close";
    error_msg_close.src = "../static/img/cancel.svg";
    document.getElementById('error_space').appendChild(error_msg);
    error_msg.appendChild(error_msg_text);
    error_msg.appendChild(error_msg_close);
}
$(".error_msg_close").click(function(){
    print($(this).parent());
})
loadignFiles();
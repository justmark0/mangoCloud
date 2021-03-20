function popupErrorMessage(message){
    const error_msg = document.createElement('div');
    const error_msg_text = document.createElement('div');
    const error_msg_close = document.createElement('img');
    error_msg.className = "error_msg";
    error_msg_text.className = "error_msg_text";
    error_msg_text.innerHTML = message;
    error_msg_close.className = "error_msg_close";
    error_msg_close.src = "../static/img/cancel.svg";
    error_msg_close.onclick = function(){
        error_msg.remove()
    }
    document.getElementById('error_space').appendChild(error_msg);
    error_msg.appendChild(error_msg_text);
    error_msg.appendChild(error_msg_close);
}

let loc = window.location 
let wsStart = 'ws://'
let input_message = $('#input-message')
let threadid = $('#thread_id').val()

let message_body = $('#msg-card-body')
let send_message_form = $('#send-message-form')
let senderimg = document.getElementById('sender_img').value
let sendedtoimg = document.getElementById('sendedto_img').value

const USER_ID_SEND_TO = $('#send-to-user')


const USER_ID = $('#logged-in-user').val()
if(loc.protocol == 'https') {
    wsStart = 'wss://'
}

//let endpoint = wsStart + loc.host + loc.pathname
let endpoint = 'wss://' + 'mapuamates.herokuapp.com' + loc.pathname

var socket = new WebSocket(endpoint)

socket.onopen = async function(e){
    console.log('open', e)
    send_message_form.on('submit', function(e){
        e.preventDefault()
        let message = input_message.val()
        let send_to = USER_ID_SEND_TO.val();
        let thread_id = threadid
        let sender_img = senderimg
        let data = {
            'message' : message,
            'sent_by' : USER_ID,
            'send_to' : send_to,
            'thread_id':thread_id,
            'sender_img':sender_img
        }
        
        data = JSON.stringify(data)
        socket.send(data)
        $(this)[0].reset()
    })
}

socket.onmessage = async function(e){
    console.log('message', e)
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let sender_img = data['sender_img']
    newMessage(message, sent_by_id, senderimg, sendedtoimg)
}

socket.onerror = async function(e){
    console.log('error', e)
}

socket.onclose  = async function(e){
    console.log('close', e)
}




function newMessage(message, sent_by_id, senderimg){
    if ($.trim(message) === ''){
        return false;
    };
    let message_element;
    if (sent_by_id == USER_ID){
        message_element = `<div class="ml-auto w-[50%] mt-2"><!--right-->
        <div class="w-[95%] m-auto flex flex-row">
            <div class="border-[1px] rounded-[5px] border-transparent bg-gray-300 h-auto w-full mr-3">
                <div id="message" class="p-2">
                    ${message}
                </div> 
            </div>
            <div>
                <img src="${senderimg}" class="profile-picture-comments">
            </div>
        </div>
    </div>`
        
    }
    else{
        message_element=`<div class="mr-auto  w-[50%] mt-2"><!--left-->
                    <div class="w-[95%] m-auto flex flex-row">
                        <div>
                            <img src="${sendedtoimg}" class="profile-picture-comments">
                        </div>
                        <div class="border-[1px] rounded-[5px] border-transparent bg-gray-300 h-auto w-full ml-3">
                            <div id="message" class="p-2">
                            ${message}
                            </div>
                        </div>
                    </div>
                </div>`
    }
    message_body.append((message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
    input_message.val(null)
}






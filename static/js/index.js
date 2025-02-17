window['vue-advanced-chat'].register();

const CONTENT_COMPONENT = new Vue({
    el: '#main_content',
    data: {
        currentUserId: '1',
        rooms: [
            {
                roomId: '1',
                roomName: '聊天室',
                users: [
                    { _id: '1', username: 'user' },
                    { _id: '2', username: 'AI' }
                ]
            }
        ],
        messages: [],
        messagesLoaded: false,
    },
    mounted: function(){
        this.messagesLoaded = true;

        this.messages.push({
            _id: 1,
            content: '嗨！可以跟我聊聊天喔～',
            senderId: '2',
            timestamp: new Date().toDateString()
        })
    },
    methods: {
        async sendMessage(message) {
            this.messages.push({
              _id: `msg-${this.messages.length + 1}`,
              content: message.content,
              senderId: '1',
              timestamp: new Date().toDateString()
            })

            this.messagesLoaded = false;
            let res = await fetch("http://localhost:8000/chat/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message.content })
            });
            let result = await res.json();
            this.messagesLoaded = true;

            this.messages.push({
                _id: `msg-${this.messages.length + 1}`,
                content: result.reply || result.error,
                senderId: '2',
                timestamp: new Date().toDateString()
            })
        },
    }
  })

var diPSClient = {
    websocket: null,
    Ready: false,
    Error: false,
    Url: '',
    ClientId: '',
    Subscriptions: new Array(),
    Publish: function (eventName, payLoad) {
        //send the message as json
        var msg = {
            EventName: eventName,
            ClientId: diPSClient.ClientId,
            MessageType: 'publish',
            EventParameter: JSON.stringify(payLoad)
        };
        diPSClient.waitForSocketReady(JSON.stringify(msg));
    },
    Subscribe: function (eventName, action) {

        if (diPSClient.Subscriptions[eventName] == undefined) {
            diPSClient.Subscriptions[eventName] = action;
            //send the subscription to the server
            var msg = {
                EventName: eventName,
                ClientId: diPSClient.ClientId,
                MessageType: 'subscribe'
            };
            var m = JSON.stringify(msg);
            diPSClient.waitForSocketReady(m);
        }
    },
    Unubscribe: function (eventName) {
        if (diPSClient.Subscriptions[eventName] != undefined) {
            diPSClient.Subscriptions[eventName] = undefined;
            //send the subscription to the server
            var msg = {
                EventName: eventName,
                ClientId: diPSClient.ClientId,
                MessageType: 'unsubscribe'
            };
            diPSClient.waitForSocketReady(JSON.stringify(msg));
        }
    },
    Connect: function (url) {
        diPSClient.ClientId = diPSClient.createGuid();
        diPSClient.Url = url + '/?clientid=' + diPSClient.ClientId;
        diPSClient.websocket = new WebSocket(diPSClient.Url);
        diPSClient.websocket.onopen = function (evt) {
            diPSClient.Ready = true;
        };

        diPSClient.websocket.onclose = function (evt) {
            //do nothing
            diPSClient.Ready = false;
        };

        diPSClient.websocket.onmessage = function (evt) {
            //evt.data;
            var msg = JSON.parse(evt.data);
            if (msg.MessageType == 'eventfired' && diPSClient.Subscriptions[msg.EventName] != null) {
                diPSClient.Subscriptions[msg.EventName](msg.PayLoad);
            }
        };

        diPSClient.websocket.onerror = function (evt) {
            diPSClient.Error = true;
            console.log(evt);
        };

    },
    Disconnect: function () {
        diPSClient.websocket.close();
    },
    createGuid: function () {
        function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
              .toString(16)
              .substring(1);
        }
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
          s4() + '-' + s4() + s4() + s4();
    },
    waitForSocketReady: function (message) { //this is only to hold a call to the websocket if is not ready to be used
        var socket = diPSClient.websocket;
        if (socket != undefined && socket != null && socket.readyState === 1) {
            socket.send(message);
            return;
        } else {
            setTimeout(
                function () {
                    diPSClient.waitForSocketReady(message);
                }, 5); // wait 5 milisecond for the connection...    
        }
    }
};

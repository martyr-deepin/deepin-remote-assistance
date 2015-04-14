
// To mark cmd message
var cmdMsg = 'CMD';

// To mark keyboard message
var keyboardMsg = 'KEYBOARD';

window.addEventListener("OxideSendMessage", function(e){
	oxide.sendMessage(e.detail.msgId, {"detail": e.detail.args});
});

window.addEventListener("OxideSendMessageNoReply", function(e){
	oxide.sendMessageNoReply(e.detail.msgId, {"detail": e.detail.args});
});

oxide.addMessageHandler(cmdMsg, function(msg){
	var newEvent = new CustomEvent("OxideSignalCMD", {detail: msg.args.detail});
	window.dispatchEvent(newEvent);
});

oxide.addMessageHandler(keyboardMsg, function(msg){
	var newEvent = new CustomEvent("OxideSignalKEYBOARD", {detail: msg.args.detail});
	window.dispatchEvent(newEvent);
});


function generateURL(key) {
	var seed = Math.floor(Math.random() * 10000);
	var payload = [seed, key];
	var data = Base64.encode(JSON.stringify(payload));
	return '_' + encodeURI(data);
}

function generateDirectImageURL(payload) {
	var data = encodeURIComponent(Base64.encode(JSON.stringify(payload)));
	return '/image?payload=' + data;
}

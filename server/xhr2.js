function sendRequest(reqnum) {
  if ((reqnum<0) || (reqnum > 10)) {
      throw new Error("Unhandled num=="+reqnum+" for sendRequest(num)")
  }
  // Case 9 and 10 use fetch, others use XHR
  if (reqnum === 9 || reqnum === 10) {
    if (reqnum === 9) {
      // NS_BINDING_ABORTED with AbortController
      const controller = new AbortController();
      // must point to 127.0.0.1 in /etc/hosts btw!
      fetch('http://alsonotmyserver.com:8080/ping', {
        method: 'POST',
        body: JSON.stringify({ events: [{ eventName: 'test', time: Date.now() }] }),
        headers: { 'Content-Type': 'application/json' },
        signal: controller.signal
      })
      .then(res => console.log('Success:', res))
      .catch(err => console.log('Error:', err));
      setTimeout(() => controller.abort(), 10); // Abort after 10ms, 50ms makes it abort even tho it has response headers received but not the response payload! or second variant that happens is: it let it go thru fully like it was allowed.
    } else if (reqnum === 10) {
      // CORS Failed
      // must point to 127.0.0.1 (ie. ourselves aka this server) in /etc/hosts btw!
      fetch('http://notmyserver.com/api/no-cors', {
        method: 'POST',
        body: JSON.stringify({ events: [{ eventName: 'cors_test', time: Date.now() }] }),
        headers: { 'Content-Type': 'application/json' }
      })
      .then(res => console.log('Success:', res))
      .catch(err => console.log('Error:', err));
    } else {
      throw new Error("impossible branch: unhandled num=="+reqnum+" for sendRequest(num)")
    }
    return; // Exit early for fetch cases
  }


  var xhr = new XMLHttpRequest();
  xhr.addEventListener("load", function() {
    const response = `${new Date()} ${xhr.responseText}`;
    console.log("Response: " + response);
    const p = document.createElement("p");
    p.textContent = response;
    document.body.appendChild(p);
  });
  where="/ping";
  switch (reqnum) {
    case 0:
    case 1:
    case 2:
    default:
      contenttype='application/x-www-form-urlencoded'
      break;
    case 3:
    case 4:
      contenttype='application/octet-stream'
      break;
    case 5:
      contenttype='text/plain;charset=UTF-8'
      break;
    case 6:
    case 7:
    case 8:
      contenttype='application/x-www-form-urlencoded'
      break;
  }
  switch (reqnum) {
    case 0:
      //actual "Form data" but we added a raw ' and \ to see our capture does give the proper printf cmd from it!
      data = "name=John's%20nam\\e&comment=theaprostrophewouldbe%27tho%20in%20normal%20urlencoding&time=" + new Date().getTime();
      break;
    case 1:
    default:
      data = "name=John's%20nam\\e&achar=\x02&time=" + new Date().getTime();
      break;
    case 2:
      data = "binary due to this \x03 time=" + new Date().getTime();
      break;
    case 3:
      data = "binary due to content type but it has no binary bytes, time=" + new Date().getTime();
      break;
    case 4:
      data = "well=ithasnobinarybytesbtw&name=John's%20nam\\e&comment=theaprostrophewouldbe%27tho%20in%20normal%20urlencoding&time=" + new Date().getTime();
      break;
    case 5:
      data = "[]";
      break;
    case 6:
    case 7:
    case 8:
      where="http://doubleclick.net/ads"
      break;
  }
  switch (reqnum) {
    case 6:
      data="foo=bar";
      break;
    case 7:
      data="";
      break;
    case 8:
      data="[]";
      break;
    default:
      break;
  }

  xhr.open('POST', where, true);
  xhr.setRequestHeader('Content-Type', contenttype);
  xhr.send(data);
}

// Add event listener to button when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('xhrButton').addEventListener('click', function() { sendRequest(0); });
  document.getElementById('xhrButton1').addEventListener('click', function() { sendRequest(1); });
  document.getElementById('xhrButton2').addEventListener('click', function() { sendRequest(2); });
  document.getElementById('xhrButton3').addEventListener('click', function() { sendRequest(3); });
  document.getElementById('xhrButton4').addEventListener('click', function() { sendRequest(4); });
  document.getElementById('xhrButton5').addEventListener('click', function() { sendRequest(5); });
  document.getElementById('xhrButton8').addEventListener('click', function() { sendRequest(8); });
  document.getElementById('xhrButton6').addEventListener('click', function() { sendRequest(6); });
  document.getElementById('xhrButton7').addEventListener('click', function() { sendRequest(7); });
  //9 is next!
  document.getElementById('xhrButton9').addEventListener('click', function() { sendRequest(9); });
  document.getElementById('xhrButton10').addEventListener('click', function() { sendRequest(10); });
  document.getElementById('xhrButton100').addEventListener('click', function() { sendRequest(100); });

});


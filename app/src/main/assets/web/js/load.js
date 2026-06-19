(function() {
    'use strict';

    function loadScript(url, callback) {
        var script = document.createElement('script');
        script.src = url;
        script.onload = callback;
        document.body.appendChild(script);
    }

    var choice = Math.floor(Math.random() * 2) + 1;
    var textUrl = choice === 1 ? 'js/text-1.js' : 'js/text-2.js';

    loadScript(textUrl, function() {
        document.getElementById('result').textContent = 'J\'ai choisi : ' + chooseText();
    });

})();

// 所有站外链接在新窗口打开
(function() {
    var links = document.querySelectorAll('a[href^="http://"], a[href^="https://"]');
    for (var i = 0; i < links.length; i++) {
        links[i].target = '_blank';
        links[i].setAttribute('rel', 'noopener noreferrer');
    }
})();

// 站外链接在新窗口打开；部分页面内所有链接在新窗口打开
(function() {
    function fixLinks() {
        var path = window.location.pathname;
        var isWeekly = path.indexOf('/weekly-update/') !== -1;
        var isProject = path.indexOf('/projects/smart-router/') !== -1;
        // 每周更新页 & 智能路由项目页：所有链接都新窗口
        if (isWeekly || isProject) {
            var allLinks = document.querySelectorAll('.md-content a');
            for (var i = 0; i < allLinks.length; i++) {
                if (!allLinks[i].getAttribute('target')) {
                    allLinks[i].target = '_blank';
                    allLinks[i].setAttribute('rel', 'noopener noreferrer');
                }
            }
        }
        // 所有页面：外部链接新窗口
        var extLinks = document.querySelectorAll('a[href^="http://"], a[href^="https://"]');
        for (var i = 0; i < extLinks.length; i++) {
            if (!extLinks[i].getAttribute('target')) {
                extLinks[i].target = '_blank';
                extLinks[i].setAttribute('rel', 'noopener noreferrer');
            }
        }
    }
    fixLinks();
    var obs = new MutationObserver(fixLinks);
    obs.observe(document.body, { childList: true, subtree: true });
})();

// 侧边栏导航层级深度计算 —— 为每个 .md-nav__item 添加 data-depth 属性
(function() {
    function calcDepth() {
        var root = document.querySelector('.md-sidebar--primary .md-nav');
        if (!root) return;
        var items = root.querySelectorAll('.md-nav__item');
        items.forEach(function(item) {
            var depth = 0;
            var el = item;
            while (el && el !== root) {
                if (el.classList && el.classList.contains('md-nav')) depth++;
                el = el.parentElement;
            }
            if (depth > 0) item.setAttribute('data-depth', depth);
        });
    }
    calcDepth();
    new MutationObserver(calcDepth).observe(document.body, { childList: true, subtree: true });
})();

// 修复侧边栏 label 的 tabindex —— MkDocs 有时会渲染为空字符串导致无法点击
(function() {
    function fixTabindex() {
        var sidebar = document.querySelector('.md-sidebar--primary');
        if (!sidebar) return;
        var labels = sidebar.querySelectorAll('label.md-nav__link');
        labels.forEach(function(label) {
            var ti = label.getAttribute('tabindex');
            if (ti === '' || ti === null) {
                label.setAttribute('tabindex', '0');
            }
        });
    }
    fixTabindex();
    new MutationObserver(fixTabindex).observe(document.body, { childList: true, subtree: true });
})();

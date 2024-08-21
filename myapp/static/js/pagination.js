document.addEventListener('DOMContentLoaded', function () {
  function handlePaginationClick(event) {
      event.preventDefault();
      const url = this.getAttribute('href');

      fetch(url)
          .then(response => response.text())
          .then(html => {
              const parser = new DOMParser();
              const doc = parser.parseFromString(html, 'text/html');
              const newEventList = doc.querySelector('#event-list-container').innerHTML;
              document.querySelector('#event-list-container').innerHTML = newEventList;

              // 更新历史记录
              window.history.pushState({ path: url }, '', url);

              // 重新绑定分页点击事件，确保新内容中也有相同的交互
              bindPaginationLinks();
          });
  }

  function bindPaginationLinks() {
      document.querySelectorAll('.pagination a').forEach(function (link) {
          link.removeEventListener('click', handlePaginationClick); // 避免重复绑定
          link.addEventListener('click', handlePaginationClick);
      });
  }

  // 初始绑定分页链接的点击事件
  bindPaginationLinks();

  // 监听浏览器的返回和前进按钮操作
  window.addEventListener('popstate', function (event) {
      if (event.state && event.state.path) {
          fetch(event.state.path)
              .then(response => response.text())
              .then(html => {
                  const parser = new DOMParser();
                  const doc = parser.parseFromString(html, 'text/html');
                  const newEventList = doc.querySelector('#event-list-container').innerHTML;
                  document.querySelector('#event-list-container').innerHTML = newEventList;

                  // 重新绑定分页点击事件，确保新内容中也有相同的交互
                  bindPaginationLinks();
              });
      }
  });
});

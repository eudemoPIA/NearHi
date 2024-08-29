/*
update the event list without reloading the whole page by pagination
*/


document.addEventListener('DOMContentLoaded', function () {

    // Handling Pagination Click Events
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
  
                window.history.pushState({ path: url }, '', url);

                bindPaginationLinks();
            });
    }
  
    // Binding Pagination Links
    function bindPaginationLinks() {
        document.querySelectorAll('.pagination a').forEach(function (link) {
            link.removeEventListener('click', handlePaginationClick);
            link.addEventListener('click', handlePaginationClick);
        });
    }
  
    // Initial Binding on Page Load
    bindPaginationLinks();
  
    // Handling Browser Back and Forward Navigation
    window.addEventListener('popstate', function (event) {
        if (event.state && event.state.path) {
            fetch(event.state.path)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newEventList = doc.querySelector('#event-list-container').innerHTML;
                    document.querySelector('#event-list-container').innerHTML = newEventList;
  
                    bindPaginationLinks();
                });
        }
    });
  });
  
  
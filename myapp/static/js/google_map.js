function initAutocomplete(inputId, types) {
    const locationInput = document.getElementById(inputId);
    if (!locationInput) return;

    const options = {
        types: types || ['geocode'], // 默认是详细地址
    };

    const autocomplete = new google.maps.places.Autocomplete(locationInput, options);

    // 不需要处理经纬度，只需让用户选择地点即可
}

document.addEventListener('DOMContentLoaded', function() {
    // 搜索栏的地点选择只需要城市级别
    initAutocomplete('search_location', ['(cities)']); 

    // Create Event 需要详细地址信息
    initAutocomplete('id_location', ['geocode']);
});

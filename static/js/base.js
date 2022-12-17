document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.item').forEach(el => el.addEventListener('click', el => {
        document.querySelector('.item.active') ? document.querySelector('.item.active').classList.remove('active') : '';
        var active_item = el.target;
        document.getElementById('img-url').value = active_item.firstElementChild.getAttribute('src');
        active_item.classList.add('active');
    }));
    var item_grid = document.getElementById('item-grid');
    if (item_grid) {
        item_grid.addEventListener('submit', function (e) {
            if (document.getElementById('img-url').value == '') {
                e.preventDefault();
                e.stopPropagation();
                alert('Please select an item before saving');
            }
        });
    }
    var import_item_list_form = document.getElementById('import-item-list-form')
    if (import_item_list_form) {
        import_item_list_form.addEventListener('submit', function(e) {
            document.querySelector('.import-overlay').classList.remove('hidden');
        })
    }
})
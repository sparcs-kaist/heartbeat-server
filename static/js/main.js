$(document).ready(function() {
    var current_tab = $('.tab:first').data('name');
    var load_data = function(tab_name) {
        $.get('/api/server/' + tab_name, function(data) {
            console.log(data);
        });
    };

    $('.tabs').tabs({'onShow': function(e) {
        new_tab = e[0].id;
        if (current_tab == new_tab)
            return;

        load_data(new_tab);
        current_tab = new_tab;
    }});
    load_data(current_tab);
});

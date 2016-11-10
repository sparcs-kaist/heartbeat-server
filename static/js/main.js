$(document).ready(function() {
    var current_tab = $('.tab:first').data('name');
    var load_data = function(name) {
        $.get('/api/server/' + name, function(data) {
            var res_time = data['res']['time'];
            var res_data = {
                cpu: {
                    system: [],
                    user: [],
                },
                mem: {
                    swap: [],
                    virt: [],
                },
                net: {
                    sent: [],
                    recv: [],
                },
                disk: {
                },
            };

            var dt_cpu = data['res']['cpu'];
            var dt_mem = data['res']['mem'];
            var dt_net = data['res']['net'];
            var dt_disk = data['res']['disk'];
            for (var dev_name in dt_disk) {
                res_data['disk'][dev_name] = {
                    name: dev_name + ' (' +  dt_disk[dev_name]['mount_point'] + ')',
                    used: []
                };
            }

            for (var i = 0; i < res_time.length; i++) {
                res_data['cpu']['system'].push({'x': res_time[i],
                    'y': dt_cpu['system'][i]});
                res_data['cpu']['user'].push({'x': res_time[i],
                    'y': dt_cpu['user'][i]});

                res_data['mem']['virt'].push({'x': res_time[i],
                    'y': dt_mem['virt_used'][i] / dt_mem['virt_total'][i] * 100});
                res_data['mem']['swap'].push({'x': res_time[i],
                    'y': dt_mem['swap_used'][i] / dt_mem['swap_total'][i] * 100});

                res_data['net']['recv'].push({'x': res_time[i],
                    'y': dt_net['bytes_recv'][i]});
                res_data['net']['sent'].push({'x': res_time[i],
                    'y': dt_net['bytes_sent'][i]});

                for (var dev_name in dt_disk) {
                    res_data['disk'][dev_name]['used'].push({'x': res_time[i],
                    'y': dt_disk[dev_name]['used'][i] / dt_disk[dev_name]['total'][i] * 100});
                }
            }

            console.log(res_data['disk']);

            var datasets_net = [];
            for (var dev_name in dt_disk) {
                datasets_net.push({label: res_data['disk'][dev_name]['name'], data: res_data['disk'][dev_name]['used']});
            }

            var chart_res_x_axis = [{
                type: 'time',
                time: {
                    displayFormats: {
                        hour: 'M-D hA'
                    },
                    tooltipFormat: 'MM-DDTHH:mm:ss'
                },
                unit: 'hour',
                position: 'bottom'
            }];

            var cpu_chart = new Chart($('#' + name + '-cpu'), {
                type: 'line',
                data: {
                    datasets: [{
                        label: 'system',
                        data: res_data['cpu']['system'],
                    },
                    {
                        label: 'user',
                        data: res_data['cpu']['user'],
                        borderColor: "rgba(75,192,192,1)",
                        backgroundColor: "rgba(75,192,192,0.4)"
                    }],
                },
                options: {
                    scales: {
                        xAxes: chart_res_x_axis,
                        yAxes: [{
                            stacked: true
                        }]
                    }
                }
            });

            var mem_chart = new Chart($('#' + name + '-mem'), {
                type: 'line',
                data: {
                    datasets: [{
                        label: 'swap',
                        data: res_data['mem']['swap'],
                    },
                    {
                        label: 'virtual',
                        data: res_data['mem']['virt'],
                        borderColor: "rgba(75,192,192,1)",
                        backgroundColor: "rgba(75,192,192,0.4)"
                    }],
                },
                options: {
                    scales: {
                        xAxes: chart_res_x_axis,
                    }
                }
            });

            var net_chart = new Chart($('#' + name + '-net'), {
                type: 'line',
                data: {
                    datasets: [{
                        label: 'sent',
                        data: res_data['net']['sent'],
                    },
                    {
                        label: 'received',
                        data: res_data['net']['recv'],
                        borderColor: "rgba(75,192,192,1)",
                        backgroundColor: "rgba(75,192,192,0.4)"
                    }],
                },
                options: {
                    scales: {
                        xAxes: chart_res_x_axis,
                    }
                }
            });

            var disk_chart = new Chart($('#' + name + '-disk'), {
                type: 'line',
                data: {
                    datasets: datasets_net,
                },
                options: {
                    scales: {
                        xAxes: chart_res_x_axis,
                    }
                }
            });

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

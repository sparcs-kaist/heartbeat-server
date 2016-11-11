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

            var datasets_net = [];
            for (var dev_name in dt_disk) {
                datasets_net.push({label: res_data['disk'][dev_name]['name'], data: res_data['disk'][dev_name]['used'], pointRadius: 0});
            }

            var chart_res_x_axis = [{
                type: 'time',
                time: {
                    displayFormats: {
                        hour: 'hA'
                    },
                    tooltipFormat: 'MM-DDTHH:mm:ss',
                    unit: 'hour',
                },
                position: 'bottom'
            }];

            var chart_y_axis_tick = function(end) {
                return  {};
            };

            var cpu_chart = new Chart($('#' + name + '-cpu'), {
                type: 'line',
                data: {
                    datasets: [{
                        label: 'system',
                        data: res_data['cpu']['system'],
                        pointRadius: 0,
                    },
                    {
                        label: 'user',
                        data: res_data['cpu']['user'],
                        borderColor: "rgba(75,192,192,1)",
                        backgroundColor: "rgba(75,192,192,0.4)",
                        pointRadius: 0,
                    }],
                },
                options: {
                    title: {
                        display: true,
                        text: 'CPU Usages',
                    },
                    scales: {
                        xAxes: chart_res_x_axis,
                        yAxes: [{
                            stacked: true,
                            ticks: chart_y_axis_tick('%'),
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
                        pointRadius: 0,
                    },
                    {
                        label: 'virtual',
                        data: res_data['mem']['virt'],
                        borderColor: "rgba(75,192,192,1)",
                        backgroundColor: "rgba(75,192,192,0.4)",
                        pointRadius: 0,
                    }],
                },
                options: {
                    title: {
                        display: true,
                        text: 'Memory Usages',
                    },
                    scales: {
                        xAxes: chart_res_x_axis,
                        yAxes: [{
                            ticks: chart_y_axis_tick('%'),
                        }],
                    }
                }
            });

            var net_chart = new Chart($('#' + name + '-net'), {
                type: 'line',
                data: {
                    datasets: [{
                        label: 'sent',
                        data: res_data['net']['sent'],
                        pointRadius: 0,
                    },
                    {
                        label: 'received',
                        data: res_data['net']['recv'],
                        borderColor: "rgba(75,192,192,1)",
                        backgroundColor: "rgba(75,192,192,0.4)",
                        pointRadius: 0,
                    }],
                },
                options: {
                    title: {
                        display: true,
                        text: 'Network Usages',
                    },
                    scales: {
                        xAxes: chart_res_x_axis,
                        yAxes: [{
                            ticks: chart_y_axis_tick('B'),
                        }],
                    }
                }
            });

            var disk_chart = new Chart($('#' + name + '-disk'), {
                type: 'line',
                data: {
                    datasets: datasets_net,
                },
                options: {
                    title: {
                        display: true,
                        text: 'Disk Usages',
                    },
                    scales: {
                        xAxes: chart_res_x_axis,
                        yAxes: [{
                            ticks: chart_y_axis_tick('%'),
                        }],
                    }
                }
            });
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

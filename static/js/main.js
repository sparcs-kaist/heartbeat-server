$(document).ready(function() {
    $.get('/api/server/overall', function(data) {
        var danger_count = 0;
        var message_list = [];
        for (var server_name in data) {
            var ping_ok = data[server_name]['ping_ok'];
            if (ping_ok === false) {
                message_list.push("Server " + server_name + " does not respond");
                danger_count += 1;
            }

            var backup_dt = data[server_name]['backup_ok'];
            for (var target_name in backup_dt) {
                if (backup_dt[target_name] === false) {
                    message_list.push("Backup " + target_name + " for server " + server_name + " does not exist");
                    danger_count += 1;
                }
            }
        }
        console.log(message_list);
    });

    var current_tab = $('.tab:first').data('name');
    var load_data = function(name) {
        $.get('/api/server/' + name, function(data) {
            $('#most_useage_click').click(function(){
              var state = $('#most_cpu_useage').toggle();
              var state = $('#most_mem_useage').toggle();
            });
            for(var i=1 ; i<=3; i++){
              $('#' + name + "-proc" + i.toString() + "-cpu-name").html(data['proc']['C' + i.toString()]['name']);
              $('#' + name + "-proc" + i.toString() + "-cpu-cpu").html(data['proc']['C' + i.toString()]['cpu']);
              $('#' + name + "-proc" + i.toString() + "-cpu-mem").html(data['proc']['C' + i.toString()]['mem']);
            }
            for(var i=1 ; i<=3; i++){
              $('#' + name + "-proc" + i.toString() + "-mem-name").html(data['proc']['M' + i.toString()]['name']);
              $('#' + name + "-proc" + i.toString() + "-mem-cpu").html(data['proc']['M' + i.toString()]['cpu']);
              $('#' + name + "-proc" + i.toString() + "-mem-mem").html(data['proc']['M' + i.toString()]['mem']);
            }
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

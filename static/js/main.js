$(document).ready(function() {
    var pretty_size = function(size) {
        var postfix = ['B', 'KB', 'MB', 'GB', 'TB', 'PB'];

        index = 0;
        while (size >= 1024) {
            index += 1;
            size /= 1024;
        }
        return Math.round(size * 100) / 100 + postfix[index];
    };

    $.get('/api/server/overall', function(data) {
        var danger_count = 0;
        var message_list = [];
        for (var server_name in data) {
            var ping_ok = data[server_name]['ping_ok'];
            if (ping_ok === false) {
                message_list.push("server " + server_name + " does not respond");
                danger_count += 1;
            }

            var backup_dt = data[server_name]['backup_ok'];
            for (var target_name in backup_dt) {
                if (backup_dt[target_name] === false) {
                    message_list.push("backup " + target_name + " of server " + server_name + " was old");
                    danger_count += 1;
                }
            }
        }
        if (message_list.length > 0) {
            $('#overall-status').html('Overall Status: FAIL');
            $('#overall-status').addClass('red-text darken-4');
        } else {
            $('#overall-status').html('Overall Status: OK');
            $('#overall-status').addClass('teal-text darken-4');
        }

        for (var i in message_list) {
            $('#overall-status-list').append('<li>!' + message_list[i] + '!</li>');
        }
    });

    var current_tab = $('.tab:first').data('name');
    var load_data = function(name) {
        $.get('/api/server/' + name, function(data) {
            /* Most CPU/MEM Usage Processes */
            $('#most-usage-toggle').click(function(){
              var show = $('.most-usage').is(":visible");
              $('.most-usage').toggle();
              $('#most-usage-toggle-icon').html(show ? '&#x25B2' : '&#x25BC');
            });
            for (var i=1; i<=3; i++){
              $('#' + name + "-proc" + i + "-cpu-name").html(data['proc']['C' + i]['name']);
              $('#' + name + "-proc" + i + "-cpu-cpu").html(data['proc']['C' + i]['cpu'] + "%");
              $('#' + name + "-proc" + i + "-cpu-mem").html(data['proc']['C' + i]['mem'] + "%");
            }
            for (var i=1; i<=3; i++){
              $('#' + name + "-proc" + i + "-mem-name").html(data['proc']['M' + i]['name']);
              $('#' + name + "-proc" + i + "-mem-cpu").html(data['proc']['M' + i]['cpu'] + "%");
              $('#' + name + "-proc" + i + "-mem-mem").html(data['proc']['M' + i]['mem'] + "%");
            }

            /* Backup Status */
            $('#backup-toggle').click(function(){
              var show = $('.backup').is(":visible");
              $('.backup').toggle();
              $('#backup-toggle-icon').html(show ? '&#x25B2' : '&#x25BC');
            });

            var backup = data['backup'];
            $('.backup tbody').html('');
            for (var n in backup) {
                var success_b = '<td><i class="material-icons green-text backup-row-icon">done</i></td>';
                if (backup[n]['success'] === false)
                    success_b = '<td><i class="material-icons orange-text backup-row-icon">report_problem</i></td>';
                var name_b = '<td>' + n + '</td>';
                var time_b = '<td>' + backup[n]['time'] + '</td>';
                var size_b = '<td>' + pretty_size(backup[n]['size']) + '</td>';
                var total_b = '<td>' + pretty_size(backup[n]['total_size']) + '</td>';
                $('.backup tbody').append('<tr>' + success_b + name_b + time_b + size_b + total_b + '</tr>');
            }

            /* Resource Graph */
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

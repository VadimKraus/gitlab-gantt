<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card card-default">
                    <div class="card-header">里程碑</div>

                    <div class="card-body">
                        <div id="milestones_chart"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                milestones: [
                    // ['Washington', new Date(1789, 3, 30), new Date(1797, 2, 4)],
                    // ['Adams', new Date(1797, 2, 4), new Date(1801, 2, 4)],
                    // ['Jefferson', new Date(1801, 2, 4), new Date(1809, 2, 4)]
                ],
                options: {height: 275}
            }
        },
        mounted() {
            console.log('Component mounted.');
            this.getMilestones();
        },
        methods: {
            drawChart() {
                let data = new google.visualization.DataTable();
                data.addColumn('string', '编号');
                data.addColumn('string', '名称');
                data.addColumn('string', '资源');
                data.addColumn('date', '开始日期');
                data.addColumn('date', '结束日期');
                data.addColumn('number', '时长');
                data.addColumn('number', '完成百分比');
                data.addColumn('string', '依赖');

                data.addRows(this.milestones);

                var options = {
                    height: data.getNumberOfRows() * 41 + 30,
                    gantt: {
                        trackHeight: 30
                    }
                };

                let chart = new google.visualization.Gantt(document.getElementById('milestones_chart'));

                chart.draw(data, options);
            },
            getMilestones() {
                this.$http.get(`/api/milestones`).then(response => {
                    let milestones = response.data;
                    milestones.forEach(milestone => {
                        this.milestones.push(
                            [
                                'milestone' + milestone['id'],
                                milestone['title'],
                                milestone['title'].toLocaleLowerCase().replace(' ', ''),
                                new Date(milestone['start_date']),
                                new Date(milestone['due_date']),
                                null,
                                100,
                                null
                            ]
                        )
                    });
                    // this.milestones.push(['Fletcher', new Date('1911-10-10'), new Date('2018-6-13')]);
                    console.log(this.milestones);

                    google.charts.load('current', {'packages': ['gantt'], 'language': 'zh'});
                    google.charts.setOnLoadCallback(this.drawChart);
                }).catch(e => {
                    this.errors.push(e)
                });
            }
        }
    }
</script>

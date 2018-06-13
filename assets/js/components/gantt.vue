<template>
    <div class="card-body" v-bind:class="{ height: options.height }">
        <div v-if="loading">
            <div class="loader d-flex justify-content-center"></div>
            <h1>{{ message }}</h1>
        </div>
        <div id="milestones_chart"></div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                message: '',
                loading: true,
                milestones: [],
                options: {height: 275}
            }
        },
        mounted() {
            this.message = '载入中...';
            this.getMilestones();
            window.onresize = () => {
                this.drawChart();
            }

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

                this.options = {
                    height: data.getNumberOfRows() * 41 + 30,
                    gantt: {
                        trackHeight: 30
                    }
                };

                let chart = new google.visualization.Gantt(document.getElementById('milestones_chart'));

                chart.draw(data, this.options);
                this.loading = false;
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

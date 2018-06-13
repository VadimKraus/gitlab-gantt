<template>
    <div class="card-body" v-bind:class="{ height: options.height }">
        <div class="d-flex justify-content-center" v-if="loading">
            <div class="sk-folding-cube">
                <div class="sk-cube1 sk-cube"></div>
                <div class="sk-cube2 sk-cube"></div>
                <div class="sk-cube4 sk-cube"></div>
                <div class="sk-cube3 sk-cube"></div>
            </div>
        </div>
        <div id="issues_chart"></div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                loading: true,
                issues: [],
                options: {height: 275}
            }
        },
        mounted() {
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

                data.addRows(this.issues);

                this.options = {
                    height: data.getNumberOfRows() * 41 + 30,
                    gantt: {
                        trackHeight: 30
                    }
                };

                let chart = new google.visualization.Gantt(document.getElementById('issues_chart'));

                chart.draw(data, this.options);
                this.loading = false;
            },
            getMilestones() {
                this.$http.get(`/api/issues`).then(response => {
                    let issues = response.data;
                    issues.forEach(issue => {
                        try {
                            this.issues.push(
                                [
                                    'issue' + issue['id'],
                                    issue['title'],
                                    issue['milestone']['title'],
                                    new Date(issue['created_at']),
                                    new Date(issue['due_date']),
                                    null,
                                    100,
                                    null
                                ]
                            )
                        } catch (e) {
                            // console.error(e);
                        }
                    });

                    google.charts.load('current', {'packages': ['gantt'], 'language': 'zh'});
                    google.charts.setOnLoadCallback(this.drawChart);
                }).catch(e => {
                    this.errors.push(e)
                });
            }
        }
    }
</script>

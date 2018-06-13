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
                var container = document.getElementById('milestones_chart');
                var chart = new google.visualization.Timeline(container);
                var dataTable = new google.visualization.DataTable();

                dataTable.addColumn({type: 'string', id: '里程牌名称'});
                dataTable.addColumn({type: 'date', id: '开始'});
                dataTable.addColumn({type: 'date', id: '结束'});
                dataTable.addRows(this.milestones);

                chart.draw(dataTable);
            },
            getMilestones() {
                this.$http.get(`/api/milestones`).then(response => {
                    let milestones = response.data;
                    milestones.forEach(m => {
                        let milestone = m['milestone'];
                        this.milestones.push(
                            [
                                milestone['title'],
                                new Date(milestone['start_date']),
                                new Date(milestone['due_date'])
                            ]
                        )
                    });
                    // this.milestones.push(['Fletcher', new Date('1911-10-10'), new Date('2018-6-13')]);
                    console.log(this.milestones);

                    google.charts.load('current', {'packages': ['timeline']});
                    google.charts.setOnLoadCallback(this.drawChart);
                }).catch(e => {
                    this.errors.push(e)
                });
            }
        }
    }
</script>

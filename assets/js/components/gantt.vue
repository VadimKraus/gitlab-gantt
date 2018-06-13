<template>
    <div class="card-body" v-bind:class="{ height: card.height }">
        <div id="milestones_chart"></div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                milestones: [],
                // options: {height: 275}
                card: {
                    height: 50
                }
            }
        },
        mounted() {
            console.log('Component mounted.');
            this.getMilestones();
        },
        methods: {
            drawChart() {
                const container = document.getElementById('milestones_chart');
                let chart = new google.visualization.Timeline(container);
                let dataTable = new google.visualization.DataTable();

                dataTable.addColumn({type: 'string', id: '里程牌名称'});
                dataTable.addColumn({type: 'date', id: '开始'});
                dataTable.addColumn({type: 'date', id: '结束'});
                dataTable.addRows(this.milestones);

                this.card.height = dataTable.getNumberOfRows() * 41 + 30;

                let options = {
                    height: this.card.height
                };

                chart.draw(dataTable, options);
            },
            getMilestones() {
                this.$http.get(`/api/milestones`).then(response => {
                    let milestones = response.data;
                    milestones.forEach(milestone => {
                        this.milestones.push(
                            [
                                milestone['title'],
                                new Date(milestone['start_date']),
                                new Date(milestone['due_date'])
                            ]
                        )
                    });
                    google.charts.load('current', {'packages': ['timeline'], 'language': 'zh'});
                    google.charts.setOnLoadCallback(this.drawChart);
                }).catch(e => {
                    this.errors.push(e)
                });
            }
        }
    }
</script>

<script>
import { Line, mixins } from 'vue-chartjs'
export default {
    name:'LineChart',
    extends: Line,
    mixins:[mixins.reactiveProp],
    props:['chartData', 'options'],
    mounted: function(){
        this.renderChart(this.chartData, this.options)
    },
    watch:{
        chartData:function() {
            this.renderChart(this.chartData, this.options)
        },
        options:function() {
            this.renderChart(this.chartData, this.options)
        }
    }
}
</script>

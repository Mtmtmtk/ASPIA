<script>
import { Line } from 'vue-chartjs'
export default {
    name:'LineChart',
    extends: Line,
    props:['data', 'options'],
    mounted: function(){
        this.renderChart(this.data, this.options)
    },
    watch:{
        data:function() {
            this.renderChart(this.data, this.options)
        },
        options:function() {
            this.renderChart(this.data, this.options)
        }
    }
}
</script>

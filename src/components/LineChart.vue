<script>
import { Line } from 'vue-chartjs'

export default {
  extends: Line,
  props: ['data'],
  data () {
    return {
      datacollection: {
        labels: this.data.labels,
        datasets: [
          {
            label: 'Prix',
            data: this.data.data,
            fill: false,
            backgroundColor: '#FF6600',
            borderColor: '#FF6600',
            pointBackgroundColor: '#FFFFFF',
            pointBorderColor: '#FF6600',
            lineTension: 0
          }
        ]
      },
      options: {
        scales: {
          xAxes: [{
            gridLines: {
              color: '#CCCCCC',
              zeroLineColor: '#CCCCCC'
            }
          }],
          yAxes: [{
            ticks: {
              beginAtZero: true
            },
            gridLines: {
              color: '#CCCCCC',
              zeroLineColor: '#CCCCCC'
            }
          }]
        },
        tooltips: {
          enabled: true,
          mode: 'single',
          callbacks: {
            label: function (tooltipItems, data) {
              return data.datasets[0].label + ' : ' + tooltipItems.yLabel + ' ' + this.data.currency
            }.bind(this)
          }
        },
        responsive: true,
        maintainAspectRatio: false
      }
    }
  },
  mounted () {
    this.renderChart(this.datacollection, this.options)
  }
}
</script>

<style scoped>

</style>

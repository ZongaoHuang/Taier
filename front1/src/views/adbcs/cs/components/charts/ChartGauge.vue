<template>
  <div ref="chartRef" :style="{ width: '60%', height: '60px' }"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';

interface Props {
  color: string;
  value: number;
}

const props = withDefaults(defineProps<Props>(), {
  color: '#7846e5',
  value: 0
});

const chartRef = ref<HTMLElement | null>(null);
let chart: echarts.ECharts | null = null;

const initChart = () => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value);
    updateChart();
  }
};

const updateChart = () => {
  if (chart) {
    chart.setOption({
      series: [
        {
          type: 'gauge',
          startAngle: 180,
          endAngle: 0,
          min: 0,
          max: 100,
          splitNumber: 10,
          itemStyle: {
            color: props.color
          },
          progress: {
            show: true,
            roundCap: true,
            width: 8
          },
          pointer: {
            show: false
          },
          axisLine: {
            roundCap: true,
            lineStyle: {
              width: 8
            }
          },
          axisTick: {
            show: false
          },
          splitLine: {
            show: false
          },
          axisLabel: {
            show: false
          },
          title: {
            show: false
          },
          detail: {
            offsetCenter: [0, '70%'],
            fontSize: 16,
            fontWeight: 'bold',
            formatter: '{value}%',
            color: 'inherit'
          },
          data: [
            {
              value: props.value
            }
          ]
        }
      ]
    });
  }
};

watch(() => props.value, updateChart);

onMounted(() => {
  initChart();
});
</script>
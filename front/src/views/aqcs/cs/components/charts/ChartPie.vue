<script setup lang="ts">
import { type PropType, ref, computed } from "vue";
import { useDark, useECharts } from "@pureadmin/utils";

const props = defineProps({
  data: {
    type: Array as PropType<Array<{ label: string; value: number }>>,
    default: () => []
  },
  color: {
    type: String,
    default: "#41b6ff"
  }
});

const { isDark } = useDark();

const theme = computed(() => (isDark.value ? "dark" : "light"));

const chartRef = ref();
const { setOptions } = useECharts(chartRef, {
  theme,
  renderer: "svg"
});

setOptions({
  container: ".line-card",
  series: [
    {
      name: '测试类型',
      type: 'pie',
      radius: '100%',
      data: props.data.map(item => ({
        value: item.value,
        name: item.label
      })),
      label: {
        show:true,
        position:"outside",
        color: isDark.value ? "#ffffff" : "#000000"
      },// 如果需要，可以为每个数据项设置不同的颜色
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
});
</script>

<template>
  <div ref="chartRef" style="width: 100%; height: 60px" />
</template>

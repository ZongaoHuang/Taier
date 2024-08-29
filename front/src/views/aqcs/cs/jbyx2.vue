<script setup lang='ts'>
import { onMounted, ref } from 'vue';
import { Terminal } from '@xterm/xterm';
import '@xterm/xterm/css/xterm.css';
import { ElMessage, ElNotification } from 'element-plus';
import { createTest, executeTest, getTestStatus, getRandomDataset } from '@/api/csgj1';

let terminal: Terminal;
const currentStep = ref('inputTestName');
const testName = ref('');
const testType = ref('');
const datasetID = ref('');

onMounted(() => {
  terminal = new Terminal({
    cursorBlink: true,
    rows: 20,
    cols: 80,
  });

  terminal.open(document.getElementById('terminal') as HTMLElement);

  terminal.write("╔═══════════════════════════════════════╗\r\n");
  terminal.write("║                                       ║\r\n");
  terminal.write("║        欢迎使用 准确性测试工具        ║\r\n");
  terminal.write("║                                       ║\r\n");
  terminal.write("╚═══════════════════════════════════════╝\r\n");
  terminal.write("\r\n请输入测试名称：");

  terminal.onData((data) => {
    if (currentStep.value === 'inputTestName') {
      handleTestNameInput(data);
    } else if (currentStep.value === 'selectTestType') {
      handleTestTypeSelection(data);
    } else if (currentStep.value === 'confirmExecution') {
      handleExecutionConfirmation(data);
    }
  });
});

function handleTestNameInput(data: string) {
  if (data.charCodeAt(0) === 13) {
    if (testName.value.trim().length > 0) {
      terminal.write(`\r\n测试名称已输入：${testName.value}\r\n`);
      terminal.write("请选择测试类型：\r\n");
      terminal.write("1. 越狱测试\r\n");
      terminal.write("2. 目标劫持测试\r\n");
      terminal.write("3. 泄露测试\r\n");
      terminal.write("4. 等效绕过测试\r\n");
      terminal.write("请输入选项编号：");
      currentStep.value = 'selectTestType';
    } else {
      terminal.write("\r\n测试名称不能为空，请重新输入：");
    }
  } else {
    testName.value += data;
    terminal.write(data);
  }
}

function handleTestTypeSelection(data: string) {
  if (data.trim() === '1' || data.trim() === '2' || data.trim() === '3') {
    if (data.trim() === '1') {
      testType.value = '越狱测试';
    } else if (data.trim() === '2') {
      testType.value = '目标劫持测试';
    } else if (data.trim() === '3') {
      testType.value = '泄露测试';
    } else if (data.trim() === '4') {
      testType.value = '等效绕过测试';
    }
    terminal.write(`\r\n您选择的测试类型是：${testType.value}\r\n`);
    generateDataset();
  } else {
    terminal.write("\r\n无效的选择，请输入 1, 2, 3 或 4：");
  }
}

async function generateDataset() {
  terminal.write(`\r\n正在生成数据集，请稍候...\r\n`);

  try {
    const response = await getRandomDataset(testType.value);
    if (response.ret === 0) {
      datasetID.value = response.id;
      terminal.write(`数据集选择成功！选中的数据集: ${response.dataset}\r\n`);
      createTest1(response.dataset);
    } else {
      terminal.write(`\r\n生成数据集失败：${response.msg || '未知错误'}\r\n`);
    }
  } catch (error) {
    console.error('Error selecting dataset:', error);
    terminal.write(`\r\n生成数据集时出错：${error.message}\r\n`);
  }
}

async function createTest1(dataset: string) {
  terminal.write(`\r\n正在创建测试，请稍候...\r\n`);

  try {
    const response = await createTest({
      name: testName.value,
      suite: testType.value,
      dataset: datasetID.value,
      model: 'gpt-3.5-turbo', // You might want to allow user to choose this
      evaluator: 'gpt-3.5-turbo' // You might want to allow user to choose this
    });

    if (response.ret === 0) {
      terminal.write(`\r\n测试 "${testName.value}" 创建成功！\r\n`);
      terminal.write("\r\n是否立即执行测试？(y/n): ");
      currentStep.value = 'confirmExecution';
    } else {
      terminal.write(`\r\n创建测试失败：${response.msg || '未知错误'}\r\n`);
      resetTerminal();
    }
  } catch (error) {
    console.error('Error creating test:', error);
    terminal.write(`\r\n创建测试时出错：${error.message}\r\n`);
  }
}

function handleExecutionConfirmation(data: string) {
  const input = data.trim().toLowerCase();
  if (input === 'y' || input === 'yes') {
    executeTestSuite();
  } else if (input === 'n' || input === 'no') {
    terminal.write("\r\n测试已创建，但未执行。\r\n");
    // Reset the terminal for a new test
    resetTerminal();
  } else {
    terminal.write("\r\n无效的选择，请输入 y 或 n：");
  }
}

function resetTerminal() {
  terminal.write("\r\n\r\n新的测试：\r\n");
  terminal.write("请输入测试名称：");
  currentStep.value = 'inputTestName';
  testName.value = '';
  testType.value = '';
  datasetID.value = '';
}

async function executeTestSuite() {
  terminal.write(`\r\n正在执行测试，请稍候...\r\n`);

  try {
    const response = await executeTest(testName.value);

    if (response.ret === 0) {
      terminal.write(`\r\n测试开始执行。正在检查测试状态...\r\n`);
      checkTestStatus();
    } else {
      terminal.write(`\r\n执行测试失败：${response.msg}\r\n`);
      resetTerminal();
    }
  } catch (error) {
    console.error('Error executing test:', error);
    terminal.write(`\r\n执行测试时出错：${error.message}\r\n`);
    resetTerminal();
  }
}

async function checkTestStatus() {
  try {
    const statusResponse = await getTestStatus(testName.value);
    if (statusResponse.ret === 0) {
      if (statusResponse.state === 'finished') {
        terminal.write(`\r\n测试 "${testName.value}" 已完成。\r\n`);
        terminal.write(`状态: ${statusResponse.state}\r\n`);
        terminal.write(`逃逸率: ${statusResponse.escape_rate}\r\n`);
      } else if (statusResponse.state === 'running') {
        terminal.write('.');
        setTimeout(checkTestStatus, 5000); // Check again after 5 seconds
      } else {
        terminal.write(`\r\n测试执行失败：${statusResponse.state}\r\n`);
      }
    } else {
      terminal.write(`\r\n获取测试状态失败：${statusResponse.msg}\r\n`);
    }
  } catch (error) {
    console.error('Error checking test status:', error);
    terminal.write(`\r\n检查测试状态时出错：${error.message}\r\n`);
  }
}
</script>

<template>
  <div id="terminal" style="height: 100%; width: 100%;"></div>
</template>

<style scoped>
#terminal {
  background-color: #000;
  border-radius: 5px;
  padding: 10px;
}
</style>

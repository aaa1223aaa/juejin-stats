// chart.js: 从 history.json 读取数据并渲染折线图

async function loadHistory() {
  try {
    // index.html 位于 web/ 目录，历史数据位于上一级 data/history.json
    const response = await fetch('../data/history.json');
    const data = await response.json();
    // 根据日期排序
    data.sort((a, b) => (a.date < b.date ? -1 : 1));
    return data;
  } catch (err) {
    console.error('读取历史数据失败', err);
    return [];
  }
}

function extractSeries(data, key) {
  return data.map((item) => (item[key] != null ? Number(item[key]) : null));
}

function createLineChart(ctx, labels, datasetLabel, dataPoints) {
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: datasetLabel,
          data: dataPoints,
          fill: false,
          tension: 0.1,
        },
      ],
    },
    options: {
      responsive: true,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: '日期',
          },
        },
        y: {
          display: true,
          beginAtZero: true,
          title: {
            display: true,
            text: datasetLabel,
          },
        },
      },
    },
  });
}

async function renderCharts() {
  const history = await loadHistory();
  if (history.length === 0) {
    return;
  }
  const labels = history.map((item) => item.date);
  const followers = extractSeries(history, 'followers');
  const articles = extractSeries(history, 'articles');
  const likes = extractSeries(history, 'likes');
  const views = extractSeries(history, 'views');
  createLineChart(document.getElementById('followersChart'), labels, '粉丝数', followers);
  createLineChart(document.getElementById('articlesChart'), labels, '文章数', articles);
  createLineChart(document.getElementById('likesChart'), labels, '被点赞数', likes);
  createLineChart(document.getElementById('viewsChart'), labels, '阅读量', views);
}

// 页面加载完毕后执行
window.addEventListener('DOMContentLoaded', renderCharts);
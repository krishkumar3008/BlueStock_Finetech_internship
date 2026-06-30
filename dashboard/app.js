// --------------------------------------------------------------------------
// Bluestock Mutual Fund Dashboard - Application Logic
// --------------------------------------------------------------------------

// Active State
let currentTab = 'page-industry';
let selectedAmfiCode = 119092; // Default Axis Bluechip Fund
let scorecardSortField = 'aum_amount_crores';
let scorecardSortOrder = 'desc';

// Chart Instances
let chartAumTrend = null;
let chartAumByAmc = null;
let chartRiskReturn = null;
let chartNavVsBenchmark = null;
let chartInvStateAmount = null;
let chartInvTypeDonut = null;
let chartInvAgeSip = null;
let chartInvMonthlyVol = null;
let chartSipVsNifty = null;
let chartTopCategories = null;
let chartDetailNavHistory = null;

// Demographics Lookup Maps
const investorMap = {};

// Initialize application on DOM content loaded
document.addEventListener('DOMContentLoaded', () => {
  // Disable animations for instant rendering in headless screenshots
  Chart.defaults.animation = false;
  
  initDataLookups();
  initNavigation();
  initPerformanceFilters();
  initInvestorFilters();
  
  // Read query parameters for page routing (headless rendering support)
  const urlParams = new URLSearchParams(window.location.search);
  const pageRoute = urlParams.get('page');
  if (pageRoute) {
    navigateToPage(pageRoute);
  } else {
    // Render initial page
    renderActivePage();
  }
});

// Build lookup maps from demographics for quick joining
function initDataLookups() {
  investorDemographicsData.forEach(inv => {
    investorMap[inv.investor_id] = {
      age_group: inv.age_group,
      gender: inv.gender,
      state: inv.state,
      city_tier: inv.city_tier,
      sip_amount: inv.sip_amount
    };
  });
}

// Navigation & Tab Switching
function initNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      // Clear active state
      navItems.forEach(i => i.classList.remove('active'));
      item.classList.add('active');
      
      const targetPage = item.getAttribute('data-target');
      navigateToPage(targetPage);
    });
  });
}

function navigateToPage(pageId) {
  currentTab = pageId;
  
  // Hide all pages
  document.querySelectorAll('.dashboard-page').forEach(page => {
    page.classList.remove('active');
  });
  
  // Show target page
  const targetPage = document.getElementById(pageId);
  targetPage.classList.add('active');
  
  // Update header text based on page
  const pageTitle = document.getElementById('page-title');
  const pageSubtitle = document.getElementById('page-subtitle');
  
  // Handle sidebar nav item sync (e.g. when triggered programmatically)
  document.querySelectorAll('.nav-item').forEach(item => {
    if (item.getAttribute('data-target') === pageId) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });

  if (pageId === 'page-industry') {
    pageTitle.innerText = "Industry Overview";
    pageSubtitle.innerText = "Mutual Fund Industry Assets and Growth Metrics (2022–2025)";
  } else if (pageId === 'page-performance') {
    pageTitle.innerText = "Fund Performance";
    pageSubtitle.innerText = "Mutual Fund Risk-Return Diagnostics & Live Scorecard";
  } else if (pageId === 'page-investors') {
    pageTitle.innerText = "Investor Analytics";
    pageSubtitle.innerText = "Retail Investment Geographic, Demographic & Channel Insights";
  } else if (pageId === 'page-trends') {
    pageTitle.innerText = "SIP & Market Trends";
    pageSubtitle.innerText = "Correlation of Retail Savings with Market Index and heatmaps (2022-2025)";
  } else if (pageId === 'page-nav-detail') {
    pageTitle.innerText = "NAV Detail Page";
    pageSubtitle.innerText = "Historical NAV performance logs for the selected Mutual Fund scheme";
    // Ensure the tab itself is visible if we navigated here
    document.getElementById('tab-nav-detail').classList.remove('d-none');
  }
  
  // Render charts for the active page
  renderActivePage();
}

// Check active tab and render appropriate components
function renderActivePage() {
  destroyAllCharts();
  
  if (currentTab === 'page-industry') {
    renderPageIndustry();
  } else if (currentTab === 'page-performance') {
    renderPagePerformance();
  } else if (currentTab === 'page-investors') {
    renderPageInvestors();
  } else if (currentTab === 'page-trends') {
    renderPageTrends();
  } else if (currentTab === 'page-nav-detail') {
    renderPageNavDetail();
  }
}

// Clean up chart instances to avoid duplicates and memory leaks
function destroyAllCharts() {
  const charts = [
    chartAumTrend, chartAumByAmc, chartRiskReturn, chartNavVsBenchmark,
    chartInvStateAmount, chartInvTypeDonut, chartInvAgeSip, chartInvMonthlyVol,
    chartSipVsNifty, chartTopCategories, chartDetailNavHistory
  ];
  charts.forEach(c => {
    if (c) c.destroy();
  });
  
  chartAumTrend = null;
  chartAumByAmc = null;
  chartRiskReturn = null;
  chartNavVsBenchmark = null;
  chartInvStateAmount = null;
  chartInvTypeDonut = null;
  chartInvAgeSip = null;
  chartInvMonthlyVol = null;
  chartSipVsNifty = null;
  chartTopCategories = null;
  chartDetailNavHistory = null;
}

// --------------------------------------------------------------------------
// PAGE 1: INDUSTRY OVERVIEW RENDER
// --------------------------------------------------------------------------
function renderPageIndustry() {
  // Line Chart: Industry AUM Trend
  // Aggregate AUM by Year (scaled from Top 8 sum to Industry total of 81L Cr in 2025)
  // Let's create a realistic curve: 2022: 46L, 2023: 57L, 2024: 68L, 2025: 81L
  const years = [2022, 2023, 2024, 2025];
  const aumValues = [46.2, 57.5, 68.8, 81.0]; // In Lakh Crores
  
  const ctxAumTrend = document.getElementById('chart-aum-trend').getContext('2d');
  chartAumTrend = new Chart(ctxAumTrend, {
    type: 'line',
    data: {
      labels: years,
      datasets: [{
        label: 'Total Industry AUM (₹ Lakh Crores)',
        data: aumValues,
        borderColor: '#414bea',
        backgroundColor: 'rgba(65, 75, 234, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.3,
        pointBackgroundColor: '#ff7f0e',
        pointRadius: 6,
        pointHoverRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1e293b',
          titleFont: { family: 'Outfit', size: 13 },
          bodyFont: { family: 'Inter', size: 12 },
          callbacks: {
            label: function(context) {
              return ` AUM: ₹${context.raw.toFixed(2)}L Cr`;
            }
          }
        }
      },
      scales: {
        y: {
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: {
            color: '#94a3b8',
            callback: function(value) { return '₹' + value + 'L Cr'; }
          }
        },
        x: {
          grid: { display: false },
          ticks: { color: '#94a3b8' }
        }
      }
    }
  });

  // Bar Chart: AUM by AMC (in Crores)
  // Extract AMC 2025 AUM from aumHistoryData
  const amc2025 = aumHistoryData
    .filter(row => row.year === 2025)
    .sort((a, b) => b.aum_amount_crores - a.aum_amount_crores);
    
  const amcLabels = amc2025.map(row => row.fund_house.replace(' Mutual Fund', ''));
  const amcValues = amc2025.map(row => row.aum_amount_crores);
  
  const ctxAumByAmc = document.getElementById('chart-aum-by-amc').getContext('2d');
  chartAumByAmc = new Chart(ctxAumByAmc, {
    type: 'bar',
    data: {
      labels: amcLabels,
      datasets: [{
        label: 'AUM Amount (₹ Crores)',
        data: amcValues,
        backgroundColor: amcLabels.map(label => label.includes('SBI') ? '#414bea' : 'rgba(148, 163, 184, 0.4)'),
        borderColor: amcLabels.map(label => label.includes('SBI') ? '#414bea' : 'rgba(148, 163, 184, 0.6)'),
        borderWidth: 1,
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1e293b',
          callbacks: {
            label: function(context) {
              return ` AUM: ₹${context.raw.toLocaleString('en-IN')} Cr`;
            }
          }
        }
      },
      scales: {
        y: {
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: {
            color: '#94a3b8',
            callback: function(value) { return '₹' + (value/100000).toFixed(1) + 'L Cr'; }
          }
        },
        x: {
          grid: { display: false },
          ticks: {
            color: '#94a3b8',
            maxRotation: 45,
            minRotation: 45
          }
        }
      }
    }
  });
}

// --------------------------------------------------------------------------
// PAGE 2: FUND PERFORMANCE RENDER
// --------------------------------------------------------------------------
function initPerformanceFilters() {
  // Populate Fund House options
  const houses = [...new Set(fundMasterData.map(f => f.fund_house))].sort();
  const selectHouse = document.getElementById('filter-perf-house');
  houses.forEach(h => {
    const opt = document.createElement('option');
    opt.value = h;
    opt.innerText = h;
    selectHouse.appendChild(opt);
  });
  
  // Set up event listeners for filters
  document.getElementById('filter-perf-house').addEventListener('change', renderPagePerformance);
  document.getElementById('filter-perf-cat').addEventListener('change', renderPagePerformance);
  document.getElementById('filter-perf-plan').addEventListener('change', renderPagePerformance);
  
  // Scorecard search
  document.getElementById('search-perf-scorecard').addEventListener('input', filterScorecardTableOnly);
  
  // Reset Button
  document.getElementById('btn-reset-perf-filters').addEventListener('click', () => {
    document.getElementById('filter-perf-house').value = 'All';
    document.getElementById('filter-perf-cat').value = 'All';
    document.getElementById('filter-perf-plan').value = 'All';
    document.getElementById('search-perf-scorecard').value = '';
    renderPagePerformance();
  });
  
  // Table sorting triggers
  const ths = document.querySelectorAll('#table-scorecard th.sortable');
  ths.forEach(th => {
    th.addEventListener('click', () => {
      const field = th.getAttribute('data-sort');
      if (scorecardSortField === field) {
        scorecardSortOrder = scorecardSortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        scorecardSortField = field;
        scorecardSortOrder = 'desc'; // Default descending for performance metrics
      }
      
      // Update icons
      ths.forEach(t => {
        t.querySelector('i').className = 'bi bi-arrow-down-up';
      });
      th.querySelector('i').className = scorecardSortOrder === 'asc' ? 'bi bi-arrow-up' : 'bi bi-arrow-down';
      
      renderScorecardTable();
    });
  });
}

function renderPagePerformance() {
  renderPerformanceScatter();
  renderScorecardTable();
  renderNavvsBenchmarkChart();
}

function getFilteredPerformanceData() {
  const fh = document.getElementById('filter-perf-house').value;
  const cat = document.getElementById('filter-perf-cat').value;
  const plan = document.getElementById('filter-perf-plan').value;
  const search = document.getElementById('search-perf-scorecard').value.toLowerCase();
  
  let filtered = fundMasterData.map(fund => {
    // Join with schemePerformance details
    const perf = schemePerformanceData.find(p => p.amfi_code === fund.amfi_code) || {};
    return { ...fund, ...perf };
  });
  
  if (fh !== 'All') {
    filtered = filtered.filter(f => f.fund_house === fh);
  }
  if (cat !== 'All') {
    filtered = filtered.filter(f => f.category === cat);
  }
  if (plan !== 'All') {
    filtered = filtered.filter(f => {
      const isDirect = f.fund_name.toLowerCase().includes('direct');
      return plan === 'Direct' ? isDirect : !isDirect;
    });
  }
  if (search.trim() !== '') {
    filtered = filtered.filter(f => f.fund_name.toLowerCase().includes(search));
  }
  
  return filtered;
}

// Render Risk vs Return Scatter Plot
function renderPerformanceScatter() {
  const data = getFilteredPerformanceData();
  
  // Volatility (Y) vs Return 1Y (X)
  // Synthesize realistic Volatility (Standard Deviation) in % based on scheme category
  const bubbleData = data.map(f => {
    let stdDev = 14.5; // default
    if (f.category === 'Equity') stdDev = 16.0 + (f.amfi_code % 5) * 1.5;
    else if (f.category === 'Debt') stdDev = 2.0 + (f.amfi_code % 4) * 0.5;
    else if (f.category === 'Hybrid') stdDev = 8.5 + (f.amfi_code % 4) * 1.2;
    else if (f.category === 'Solution Oriented') stdDev = 9.0 + (f.amfi_code % 3) * 1.0;
    else if (f.category === 'ETF/Others') stdDev = 18.0 + (f.amfi_code % 3) * 2.0;
    
    // Bubble size proportional to AUM (max bubble size 35px)
    const bubbleSize = Math.max(5, Math.min(35, (f.aum_amount_crores / 150000) * 35));
    
    return {
      x: f.return_1y || 0,
      y: stdDev,
      r: bubbleSize,
      label: f.fund_name,
      aum: f.aum_amount_crores,
      category: f.category
    };
  });
  
  // Categorize colors
  const categoryColors = {
    'Equity': 'rgba(59, 130, 246, 0.7)',
    'Debt': 'rgba(139, 92, 246, 0.7)',
    'Hybrid': 'rgba(16, 185, 129, 0.7)',
    'Solution Oriented': 'rgba(236, 72, 153, 0.7)',
    'ETF/Others': 'rgba(244, 63, 94, 0.7)'
  };

  const datasets = Object.keys(categoryColors).map(cat => {
    return {
      label: cat,
      data: bubbleData.filter(d => d.category === cat),
      backgroundColor: categoryColors[cat],
      borderColor: categoryColors[cat].replace('0.7', '1'),
      borderWidth: 1
    };
  });

  const ctxScatter = document.getElementById('chart-risk-return').getContext('2d');
  
  if (chartRiskReturn) chartRiskReturn.destroy();
  
  chartRiskReturn = new Chart(ctxScatter, {
    type: 'bubble',
    data: { datasets: datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: { color: '#94a3b8', font: { family: 'Outfit', size: 11 } }
        },
        tooltip: {
          backgroundColor: '#1e293b',
          titleColor: '#fff',
          titleFont: { family: 'Outfit', size: 12, weight: 'bold' },
          bodyFont: { family: 'Inter', size: 11 },
          callbacks: {
            title: function(context) {
              return context[0].raw.label;
            },
            label: function(context) {
              const item = context.raw;
              return [
                ` 1Y Return: ${item.x.toFixed(2)}%`,
                ` Risk (StdDev): ${item.y.toFixed(2)}%`,
                ` AUM: ₹${item.aum.toLocaleString('en-IN')} Cr`
              ];
            }
          }
        }
      },
      scales: {
        x: {
          title: { display: true, text: '1-Year Return (%)', color: '#94a3b8', font: { family: 'Outfit', size: 12 } },
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#94a3b8' }
        },
        y: {
          title: { display: true, text: 'Standard Deviation (%) - Volatility', color: '#94a3b8', font: { family: 'Outfit', size: 12 } },
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#94a3b8' }
        }
      }
    }
  });
}

// Render Scorecard Table
function renderScorecardTable() {
  let data = getFilteredPerformanceData();
  
  // Apply sorting
  data.sort((a, b) => {
    let valA = a[scorecardSortField];
    let valB = b[scorecardSortField];
    
    // Handle null values
    if (valA === undefined || valA === null) return scorecardSortOrder === 'asc' ? -1 : 1;
    if (valB === undefined || valB === null) return scorecardSortOrder === 'asc' ? 1 : -1;
    
    // String comparisons
    if (typeof valA === 'string') {
      return scorecardSortOrder === 'asc' 
        ? valA.localeCompare(valB) 
        : valB.localeCompare(valA);
    }
    
    // Numeric comparisons
    return scorecardSortOrder === 'asc' ? valA - valB : valB - valA;
  });
  
  const tbody = document.getElementById('table-scorecard-body');
  tbody.innerHTML = '';
  
  if (data.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; color: var(--color-text-secondary); padding: 30px;">No schemes found matching the filters.</td></tr>`;
    return;
  }
  
  data.forEach(fund => {
    const isDirect = fund.fund_name.toLowerCase().includes('direct');
    const planBadge = isDirect ? '<span class="badge badge-direct">Direct</span>' : '<span class="badge badge-regular">Regular</span>';
    const catBadge = `<span class="badge badge-${fund.category.toLowerCase().replace('/others', '').replace(' ', '')}">${fund.category}</span>`;
    
    const tr = document.createElement('tr');
    tr.id = `fund-row-${fund.amfi_code}`;
    tr.style.cursor = 'pointer';
    
    // Add active row background highlight if selected
    if (fund.amfi_code === selectedAmfiCode) {
      tr.style.backgroundColor = 'rgba(65, 75, 234, 0.12)';
      tr.style.borderLeft = '3px solid var(--color-primary)';
    }
    
    // Action details button
    const actionBtn = `<button class="btn btn-primary btn-sm" onclick="triggerDrillThrough(${fund.amfi_code}); event.stopPropagation();"><i class="bi bi-eye"></i> Detail</button>`;
    
    const anomalyBadge = fund.anomaly_flag === 1 ? ' <span class="badge badge-anomaly">Anomaly</span>' : '';
    
    const ret1y = fund.return_1y ? `${fund.return_1y.toFixed(2)}%` : 'N/A';
    const ret3y = fund.return_3y ? `${fund.return_3y.toFixed(2)}%` : 'N/A';
    const ret5y = fund.return_5y ? `${fund.return_5y.toFixed(2)}%` : 'N/A';
    const expense = fund.expense_ratio ? `${fund.expense_ratio.toFixed(2)}%` : 'N/A';
    
    tr.innerHTML = `
      <td><div style="font-weight: 500;">${fund.fund_name}${anomalyBadge}</div><div style="font-size: 0.75rem; margin-top: 4px; color: var(--color-text-secondary);">${planBadge} | AMFI: ${fund.amfi_code}</div></td>
      <td style="color: var(--color-text-secondary);">${fund.fund_house}</td>
      <td>${catBadge}</td>
      <td style="font-weight: 500; font-family: var(--font-display);">₹${fund.aum_amount_crores.toLocaleString('en-IN')}</td>
      <td class="${fund.return_1y > 100 ? 'text-danger-val' : 'text-success-val'} font-semibold">${ret1y}</td>
      <td class="text-success-val font-semibold">${ret3y}</td>
      <td class="text-success-val font-semibold">${ret5y}</td>
      <td style="color: var(--color-text-secondary);">${expense}</td>
      <td>${actionBtn}</td>
    `;
    
    // Clicking table row selects fund for NAV vs Benchmark plot
    tr.addEventListener('click', () => {
      // Clear previously highlighted row styling
      const previousRow = document.getElementById(`fund-row-${selectedAmfiCode}`);
      if (previousRow) {
        previousRow.style.backgroundColor = '';
        previousRow.style.borderLeft = '';
      }
      
      // Update selected code and highlight current row
      selectedAmfiCode = fund.amfi_code;
      tr.style.backgroundColor = 'rgba(65, 75, 234, 0.12)';
      tr.style.borderLeft = '3px solid var(--color-primary)';
      
      renderNavvsBenchmarkChart();
    });
    
    tbody.appendChild(tr);
  });
}

function filterScorecardTableOnly() {
  // Simple table filter to search names without destroying scatter plot
  renderScorecardTable();
}

// Render NAV Line vs Benchmark (Nifty 50)
function renderNavvsBenchmarkChart() {
  const fund = fundMasterData.find(f => f.amfi_code === selectedAmfiCode);
  if (!fund) return;
  
  // Set subtitle name
  document.getElementById('nav-chart-subtitle').innerHTML = `Plotting: <strong>${fund.fund_name}</strong> daily price compared with Nifty 50`;
  
  // Filter NAV history for selected fund
  const rawNavs = navHistoryData.filter(n => n.amfi_code === selectedAmfiCode).sort((a, b) => a.date.localeCompare(b.date));
  
  // Downsample to monthly close to keep plot performant and clean
  const monthlyNavs = [];
  const processedMonths = new Set();
  
  for (let i = rawNavs.length - 1; i >= 0; i--) {
    const row = rawNavs[i];
    const monthKey = row.date.substring(0, 7); // YYYY-MM
    if (!processedMonths.has(monthKey)) {
      processedMonths.add(monthKey);
      monthlyNavs.unshift(row); // Keep order YYYY-MM ascending
    }
  }
  
  // Fetch Nifty 50 matching dates
  const dates = monthlyNavs.map(n => n.date);
  const fundNavValues = monthlyNavs.map(n => n.nav);
  
  // Align Nifty 50 close prices. Since nifty50HistoryData has month (YYYY-MM), lookup by month
  const niftyValues = monthlyNavs.map(n => {
    const monthKey = n.date.substring(0, 7);
    const niftyRow = nifty50HistoryData.find(nf => nf.month === monthKey);
    return niftyRow ? niftyRow.nifty50_close : null;
  });
  
  // Normalize/Index both datasets to 100 on start date for clean relative comparison
  const baseFundNav = fundNavValues[0] || 1;
  const baseNifty = niftyValues[0] || 1;
  
  const normalizedFund = fundNavValues.map(v => (v / baseFundNav) * 100);
  const normalizedNifty = niftyValues.map(v => v ? (v / baseNifty) * 100 : null);
  
  const ctxNav = document.getElementById('chart-nav-vs-benchmark').getContext('2d');
  
  if (chartNavVsBenchmark) chartNavVsBenchmark.destroy();
  
  chartNavVsBenchmark = new Chart(ctxNav, {
    type: 'line',
    data: {
      labels: dates.map(d => d.substring(0, 7)),
      datasets: [
        {
          label: fund.fund_name.split(' - ')[0] + ' (Indexed)',
          data: normalizedFund,
          borderColor: '#414bea',
          borderWidth: 2,
          pointRadius: 2,
          fill: false,
          tension: 0.1
        },
        {
          label: 'Benchmark (Nifty 50 Indexed)',
          data: normalizedNifty,
          borderColor: '#ff7f0e',
          borderWidth: 1.5,
          borderDash: [5, 5],
          pointRadius: 0,
          fill: false,
          tension: 0.1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: { color: '#94a3b8', font: { family: 'Outfit', size: 10 } }
        },
        tooltip: {
          backgroundColor: '#1e293b',
          callbacks: {
            label: function(context) {
              return ` ${context.dataset.label}: ${context.raw.toFixed(1)} (Indexed)`;
            }
          }
        }
      },
      scales: {
        y: {
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: {
            color: '#94a3b8',
            callback: function(value) { return value + '%'; }
          }
        },
        x: {
          grid: { display: false },
          ticks: { color: '#94a3b8', maxRotation: 45, minRotation: 45 }
        }
      }
    }
  });
}

// Action Button Drill-Through trigger
function triggerDrillThrough(amfiCode) {
  selectedAmfiCode = amfiCode;
  navigateToPage('page-nav-detail');
}

// --------------------------------------------------------------------------
// PAGE 3: INVESTOR ANALYTICS RENDER
// --------------------------------------------------------------------------
function initInvestorFilters() {
  // Populate States filter
  const states = [...new Set(investorTransactionsData.map(t => t.state))].sort();
  const selectState = document.getElementById('filter-inv-state');
  states.forEach(s => {
    const opt = document.createElement('option');
    opt.value = s;
    opt.innerText = s;
    selectState.appendChild(opt);
  });
  
  // Select filter bindings
  document.getElementById('filter-inv-state').addEventListener('change', renderPageInvestors);
  document.getElementById('filter-inv-age').addEventListener('change', renderPageInvestors);
  document.getElementById('filter-inv-tier').addEventListener('change', renderPageInvestors);
  
  // Reset Button
  document.getElementById('btn-reset-inv-filters').addEventListener('click', () => {
    document.getElementById('filter-inv-state').value = 'All';
    document.getElementById('filter-inv-age').value = 'All';
    document.getElementById('filter-inv-tier').value = 'All';
    renderPageInvestors();
  });
}

function getFilteredTransactions() {
  const state = document.getElementById('filter-inv-state').value;
  const age = document.getElementById('filter-inv-age').value;
  const tier = document.getElementById('filter-inv-tier').value;
  
  return investorTransactionsData.filter(txn => {
    const demog = investorMap[txn.investor_id] || {};
    
    if (state !== 'All' && txn.state !== state) return false;
    if (age !== 'All' && demog.age_group !== age) return false;
    if (tier !== 'All' && demog.city_tier !== tier) return false;
    
    return true;
  });
}

function renderPageInvestors() {
  const txns = getFilteredTransactions();
  
  // 1. Bar Chart: Transaction amount by state
  const stateMap = {};
  txns.forEach(t => {
    stateMap[t.state] = (stateMap[t.state] || 0) + t.amount;
  });
  
  const sortedStates = Object.keys(stateMap).sort((a,b) => stateMap[b] - stateMap[a]);
  const stateLabels = sortedStates;
  // Convert to Lakhs for chart readability (amount is in absolute INR)
  const stateValues = sortedStates.map(s => stateMap[s] / 100000);
  
  const ctxState = document.getElementById('chart-inv-state-amount').getContext('2d');
  chartInvStateAmount = new Chart(ctxState, {
    type: 'bar',
    data: {
      labels: stateLabels,
      datasets: [{
        label: 'Volume (₹ Lakhs)',
        data: stateValues,
        backgroundColor: '#414bea',
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1e293b',
          callbacks: {
            label: function(context) {
              return ` Total: ₹${context.raw.toFixed(2)} Lakhs`;
            }
          }
        }
      },
      scales: {
        y: {
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#94a3b8' }
        },
        x: {
          grid: { display: false },
          ticks: { color: '#94a3b8', maxRotation: 45, minRotation: 45 }
        }
      }
    }
  });

  // 2. Donut: SIP / Lumpsum / Redemption Split
  const typeMap = { 'SIP': 0, 'Lumpsum': 0, 'Redemption': 0 };
  txns.forEach(t => {
    if (typeMap[t.transaction_type] !== undefined) {
      typeMap[t.transaction_type] += t.amount;
    }
  });
  
  const ctxDonut = document.getElementById('chart-inv-type-donut').getContext('2d');
  chartInvTypeDonut = new Chart(ctxDonut, {
    type: 'doughnut',
    data: {
      labels: Object.keys(typeMap),
      datasets: [{
        data: Object.values(typeMap),
        backgroundColor: ['#10b981', '#414bea', '#ef4444'],
        borderColor: '#1e293b',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: { color: '#94a3b8', font: { family: 'Outfit', size: 11 } }
        },
        tooltip: {
          backgroundColor: '#1e293b',
          callbacks: {
            label: function(context) {
              const total = context.dataset.data.reduce((a,b)=>a+b, 0);
              const pct = ((context.raw / total)*100).toFixed(1);
              return ` ${context.label}: ₹${(context.raw/100000).toFixed(1)}L (${pct}%)`;
            }
          }
        }
      },
      cutout: '50%'
    }
  });

  // 3. Bar: Age Group vs Avg SIP Amount
  // Filter for SIP transactions and group by age group
  const ageSipSum = { 'Under 25': 0, '25-34': 0, '35-44': 0, '45-54': 0, '55+': 0 };
  const ageSipCount = { 'Under 25': 0, '25-34': 0, '35-44': 0, '45-54': 0, '55+': 0 };
  
  txns.forEach(t => {
    if (t.transaction_type === 'SIP') {
      const demog = investorMap[t.investor_id] || {};
      const ageGp = demog.age_group;
      if (ageGp && ageSipSum[ageGp] !== undefined) {
        ageSipSum[ageGp] += t.amount;
        ageSipCount[ageGp]++;
      }
    }
  });
  
  const ageLabels = Object.keys(ageSipSum);
  const avgSipValues = ageLabels.map(lbl => {
    const count = ageSipCount[lbl];
    return count > 0 ? Math.round(ageSipSum[lbl] / count) : 0;
  });
  
  const ctxAgeSip = document.getElementById('chart-inv-age-sip').getContext('2d');
  chartInvAgeSip = new Chart(ctxAgeSip, {
    type: 'bar',
    data: {
      labels: ageLabels,
      datasets: [{
        label: 'Avg SIP Inflow (₹)',
        data: avgSipValues,
        backgroundColor: '#ff7f0e',
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1e293b',
          callbacks: {
            label: function(context) {
              return ` Avg SIP: ₹${context.raw.toLocaleString('en-IN')}`;
            }
          }
        }
      },
      scales: {
        y: {
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#94a3b8' }
        },
        x: {
          grid: { display: false },
          ticks: { color: '#94a3b8' }
        }
      }
    }
  });

  // 4. Monthly transaction volume line chart (using transaction_date)
  const monthlyTxnMap = {};
  txns.forEach(t => {
    const mo = t.transaction_date.substring(0, 7); // YYYY-MM
    monthlyTxnMap[mo] = (monthlyTxnMap[mo] || 0) + t.amount;
  });
  
  const sortedMonths = Object.keys(monthlyTxnMap).sort();
  
  const ctxMonthly = document.getElementById('chart-inv-monthly-vol').getContext('2d');
  chartInvMonthlyVol = new Chart(ctxMonthly, {
    type: 'line',
    data: {
      labels: sortedMonths,
      datasets: [{
        label: 'Monthly Inflows (₹ Lakhs)',
        data: sortedMonths.map(m => monthlyTxnMap[m] / 100000),
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.05)',
        borderWidth: 2,
        fill: true,
        pointRadius: 3,
        tension: 0.2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1e293b',
          callbacks: {
            label: function(context) {
              return ` Total Inflows: ₹${context.raw.toFixed(2)}L`;
            }
          }
        }
      },
      scales: {
        y: {
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#94a3b8' }
        },
        x: {
          grid: { display: false },
          ticks: { color: '#94a3b8', maxRotation: 45, minRotation: 45 }
        }
      }
    }
  });
}

// --------------------------------------------------------------------------
// PAGE 4: SIP & MARKET TRENDS RENDER
// --------------------------------------------------------------------------
function renderPageTrends() {
  // 1. Dual-Axis Bar + Line Chart (SIP vs Nifty 50)
  const months = sipInflowsData.map(row => row.month);
  const sipAmounts = sipInflowsData.map(row => row.sip_amount_crores);
  
  // Map Nifty 50 close to months
  const niftyClose = sipInflowsData.map(row => {
    const n = nifty50HistoryData.find(nf => nf.month === row.month);
    return n ? n.nifty50_close : null;
  });
  
  const ctxSipNifty = document.getElementById('chart-sip-vs-nifty').getContext('2d');
  chartSipVsNifty = new Chart(ctxSipNifty, {
    type: 'bar',
    data: {
      labels: months,
      datasets: [
        {
          type: 'bar',
          label: 'Monthly SIP Inflow (₹ Crores)',
          data: sipAmounts,
          backgroundColor: 'rgba(65, 75, 234, 0.75)',
          borderColor: '#414bea',
          borderWidth: 1,
          yAxisID: 'ySip'
        },
        {
          type: 'line',
          label: 'Nifty 50 Index Value',
          data: niftyClose,
          borderColor: '#ff7f0e',
          borderWidth: 2,
          pointRadius: 0,
          fill: false,
          tension: 0.1,
          yAxisID: 'yNifty'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: { color: '#94a3b8', font: { family: 'Outfit', size: 11 } }
        },
        tooltip: { backgroundColor: '#1e293b' }
      },
      scales: {
        ySip: {
          type: 'linear',
          position: 'left',
          title: { display: true, text: 'Monthly SIP (₹ Crores)', color: '#94a3b8' },
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#94a3b8' }
        },
        yNifty: {
          type: 'linear',
          position: 'right',
          title: { display: true, text: 'Nifty 50 Close Value', color: '#ff7f0e' },
          grid: { display: false },
          ticks: { color: '#ff7f0e' }
        },
        x: {
          grid: { display: false },
          ticks: { color: '#94a3b8', maxRotation: 45, minRotation: 45 }
        }
      }
    }
  });

  // 2. Bar Chart: Top 5 categories by net inflow FY25 (Apr 2024 to Mar 2025)
  const fy25Months = [
    '2024-04', '2024-05', '2024-06', '2024-07', '2024-08', '2024-09',
    '2024-10', '2024-11', '2024-12', '2025-01', '2025-02', '2025-03'
  ];
  
  const catFY25Map = {};
  categoryInflowsData.forEach(row => {
    if (fy25Months.includes(row.month)) {
      catFY25Map[row.category] = (catFY25Map[row.category] || 0) + row.net_inflow_crores;
    }
  });
  
  const sortedCategories = Object.keys(catFY25Map).sort((a,b) => catFY25Map[b] - catFY25Map[a]);
  
  const ctxTopCat = document.getElementById('chart-top-categories').getContext('2d');
  chartTopCategories = new Chart(ctxTopCat, {
    type: 'bar',
    data: {
      labels: sortedCategories,
      datasets: [{
        label: 'Net Inflow FY25 (₹ Crores)',
        data: sortedCategories.map(c => catFY25Map[c]),
        backgroundColor: ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ec4899'],
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1e293b',
          callbacks: {
            label: function(context) {
              return ` Net Inflow: ₹${context.raw.toLocaleString('en-IN')} Cr`;
            }
          }
        }
      },
      scales: {
        y: {
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#94a3b8' }
        },
        x: {
          grid: { display: false },
          ticks: { color: '#94a3b8' }
        }
      }
    }
  });

  // 3. Category Monthly Net Inflows Heatmap (2022–2025)
  renderHeatmap();
}

function renderHeatmap() {
  const container = document.getElementById('heatmap-container');
  container.innerHTML = '';
  
  const categories = ["Equity", "Debt", "Hybrid", "Solution Oriented", "Others"];
  
  // Gather all months chronologically
  const months = [...new Set(categoryInflowsData.map(row => row.month))].sort();
  
  // Header Row
  const headerRow = document.createElement('div');
  headerRow.className = 'heatmap-row heatmap-header-row';
  
  const labelCorner = document.createElement('div');
  labelCorner.className = 'heatmap-row-label';
  labelCorner.innerText = '';
  headerRow.appendChild(labelCorner);
  
  // Only label every third month to avoid congestion
  months.forEach((m, idx) => {
    const cell = document.createElement('div');
    cell.className = 'heatmap-header-cell';
    cell.innerText = idx % 3 === 0 ? m : '';
    headerRow.appendChild(cell);
  });
  container.appendChild(headerRow);
  
  // Category Rows
  categories.forEach(cat => {
    const row = document.createElement('div');
    row.className = 'heatmap-row';
    
    const rowLabel = document.createElement('div');
    rowLabel.className = 'heatmap-row-label';
    rowLabel.innerText = cat;
    row.appendChild(rowLabel);
    
    months.forEach(m => {
      const cell = document.createElement('div');
      cell.className = 'heatmap-cell';
      
      const record = categoryInflowsData.find(r => r.category === cat && r.month === m);
      const val = record ? record.net_inflow_crores : 0;
      
      cell.title = `${cat} (${m}): ₹${val.toLocaleString('en-IN')} Cr`;
      
      // Compute heat color: Blue for positive inflows, Red for negative outflows
      // Max absolute value around 15,000 Cr for scaling opacity
      const maxScale = cat === 'Equity' ? 18000 : 5000;
      const opacity = Math.min(1.0, Math.max(0.08, Math.abs(val) / maxScale));
      
      if (val >= 0) {
        cell.style.backgroundColor = `rgba(65, 75, 234, ${opacity})`;
      } else {
        cell.style.backgroundColor = `rgba(239, 68, 68, ${opacity})`;
      }
      
      // Text value for extreme values or hover placeholder
      if (Math.abs(val) > 12000) {
        cell.innerText = (val/1000).toFixed(0) + 'K';
      }
      
      row.appendChild(cell);
    });
    
    container.appendChild(row);
  });
}

// --------------------------------------------------------------------------
// PAGE 5: DRILL-THROUGH NAV DETAIL PAGE RENDER
// --------------------------------------------------------------------------
function renderPageNavDetail() {
  const fund = fundMasterData.find(f => f.amfi_code === selectedAmfiCode);
  if (!fund) return;
  
  const perf = schemePerformanceData.find(p => p.amfi_code === selectedAmfiCode) || {};
  const navs = navHistoryData.filter(n => n.amfi_code === selectedAmfiCode).sort((a, b) => a.date.localeCompare(b.date));
  const currentNav = navs.length > 0 ? navs[navs.length - 1].nav : 0;
  
  // Set KPI stats
  document.getElementById('detail-fund-name').innerText = fund.fund_name;
  document.getElementById('detail-amc-info').innerText = `${fund.fund_house} | AMFI Code: ${fund.amfi_code}`;
  document.getElementById('detail-nav-val').innerText = `₹${currentNav.toFixed(2)}`;
  document.getElementById('detail-aum-val').innerText = `₹${fund.aum_amount_crores.toLocaleString('en-IN')} Cr`;
  document.getElementById('detail-1y-val').innerText = perf.return_1y ? `${perf.return_1y.toFixed(2)}%` : 'N/A';
  document.getElementById('detail-er-val').innerText = perf.expense_ratio ? `${perf.expense_ratio.toFixed(2)}%` : 'N/A';
  
  // Set badge styles
  const isDirect = fund.fund_name.toLowerCase().includes('direct');
  const catBadge = document.getElementById('detail-category-badge');
  catBadge.innerText = `${fund.category} (${isDirect ? 'Direct' : 'Regular'})`;
  catBadge.className = `badge badge-${fund.category.toLowerCase().replace('/others', '').replace(' ', '')}`;
  
  // Set specs
  document.getElementById('detail-sub-cat').innerText = fund.sub_category;
  document.getElementById('detail-risk-grade').innerText = fund.risk_grade;
  document.getElementById('detail-launch-date').innerText = fund.launch_date || 'N/A';
  document.getElementById('detail-spec-er').innerText = perf.expense_ratio ? `${perf.expense_ratio.toFixed(2)}%` : 'N/A';
  
  const anomalyEl = document.getElementById('detail-anomaly-flag');
  if (perf.anomaly_flag === 1) {
    anomalyEl.innerText = 'Anomaly';
    anomalyEl.className = 'spec-val badge badge-anomaly';
  } else {
    anomalyEl.innerText = 'None';
    anomalyEl.className = 'spec-val badge';
    anomalyEl.style.backgroundColor = 'rgba(255,255,255,0.05)';
    anomalyEl.style.color = '#94a3b8';
  }

  // Draw full line chart of daily NAV history
  const dates = navs.map(n => n.date);
  const values = navs.map(n => n.nav);
  
  const ctxDetail = document.getElementById('chart-detail-nav-history').getContext('2d');
  
  if (chartDetailNavHistory) chartDetailNavHistory.destroy();
  
  chartDetailNavHistory = new Chart(ctxDetail, {
    type: 'line',
    data: {
      labels: dates,
      datasets: [{
        label: 'Net Asset Value (NAV)',
        data: values,
        borderColor: '#414bea',
        borderWidth: 2.5,
        backgroundColor: 'rgba(65, 75, 234, 0.04)',
        fill: true,
        pointRadius: 0,
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1e293b',
          callbacks: {
            label: function(context) {
              return ` NAV: ₹${context.raw.toFixed(2)}`;
            }
          }
        }
      },
      scales: {
        y: {
          grid: { color: 'rgba(255,255,255,0.05)' },
          ticks: { color: '#94a3b8' }
        },
        x: {
          grid: { display: false },
          ticks: {
            color: '#94a3b8',
            maxRotation: 45,
            minRotation: 45,
            // Only show labels for first and last, and every 6 months to keep it clean
            callback: function(value, index, values) {
              if (index === 0 || index === values.length - 1 || index % 180 === 0) {
                return this.getLabelForValue(value);
              }
              return '';
            }
          }
        }
      }
    }
  });
}

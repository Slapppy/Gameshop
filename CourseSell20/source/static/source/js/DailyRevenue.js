function updateDailyRevenue() {
fetch('/api/daily-revenue/')
  .then(response => response.json())
  .then(data => {
    const dailyRevenueElement = document.querySelector('.font-weight-bolder');
    const revenueChangeElement = document.querySelector('.text-success');
    const revenueChangePercentageElement = document.querySelector('.text-success');

    dailyRevenueElement.textContent = `$${data.daily_revenue}`;
    revenueChangeElement.textContent = `${data.revenue_change}%`;
    revenueChangePercentageElement.textContent = `since yesterday`;
  })
  .catch(error => {
    console.error('Ошибка при загрузке данных из API:', error);
  });
}

updateDailyRevenue();


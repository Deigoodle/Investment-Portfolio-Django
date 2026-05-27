const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export async function fetchPortfolioDates(portfolioId) {
    const response = await fetch(`${API_BASE}/portfolios/${portfolioId}/dates/`);
    if (!response.ok) throw new Error('Failed to fetch dates');
    return response.json();
}

export async function fetchPortfolioEvolution(portfolioId, startDate, endDate) {
    const url = `${API_BASE}/portfolios/${portfolioId}/evolution/?start=${startDate}&end=${endDate}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Failed to fetch evolution data');
    return response.json();
}

export function transformChartData(evolutionData) {
    if (!evolutionData || evolutionData.length === 0) return [];
    return evolutionData.map(day => ({
        date: day.date,
        totalValue: day.total_value,
        ...day.weights
    }));
}

export function getAssetNames(data) {
    if (!data || data.length === 0) return [];
    return Object.keys(data[0]).filter(key => key !== 'date' && key !== 'totalValue');
}
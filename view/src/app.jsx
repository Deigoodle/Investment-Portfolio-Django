import React, { useState, useEffect, useCallback } from 'react';
import { createRoot } from 'react-dom/client';
import { fetchPortfolioDates, fetchPortfolioEvolution, transformChartData, getAssetNames } from './api';
import { TotalValueChart, WeightsChart } from './charts';

function App() {
    const [portfolio, setPortfolio] = useState('1');
    const [dates, setDates] = useState({ start: null, end: null }); // Start with null
    const [availableDates, setAvailableDates] = useState({ first_date: null, last_date: null });
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [datesLoaded, setDatesLoaded] = useState(false); // Track if dates are loaded

    // Fetch available date range when portfolio changes
    useEffect(() => {
        let isMounted = true;
        
        const loadDates = async () => {
            setDatesLoaded(false);
            setLoading(true);
            
            try {
                const dateInfo = await fetchPortfolioDates(portfolio);
                if (isMounted) {
                    setAvailableDates(dateInfo);
                    if (dateInfo.first_date && dateInfo.last_date) {
                        setDates({
                            start: dateInfo.first_date,
                            end: dateInfo.last_date
                        });
                        setDatesLoaded(true);
                    }
                }
            } catch (err) {
                console.error('Error loading dates:', err);
                if (isMounted) {
                    setError('Failed to load portfolio dates');
                    setDatesLoaded(false);
                }
            } finally {
                if (isMounted) {
                    setLoading(false);
                }
            }
        };
        
        loadDates();
        
        return () => {
            isMounted = false;
        };
    }, [portfolio]);

    // Fetch evolution data ONLY when dates are loaded and valid
    const loadEvolutionData = useCallback(async () => {
        // Don't fetch if dates are not loaded or invalid
        if (!datesLoaded || !dates.start || !dates.end) {
            console.log('Skipping fetch: dates not ready', { datesLoaded, start: dates.start, end: dates.end });
            return;
        }
        
        setLoading(true);
        setError(null);
        
        try {
            const evolution = await fetchPortfolioEvolution(portfolio, dates.start, dates.end);
            const chartData = transformChartData(evolution);
            setData(chartData);
        } catch (err) {
            console.error('Error loading evolution:', err);
            setError('Failed to load portfolio data');
        } finally {
            setLoading(false);
        }
    }, [portfolio, dates.start, dates.end, datesLoaded]);

    // Load evolution data when dates are ready
    useEffect(() => {
        if (datesLoaded && dates.start && dates.end) {
            loadEvolutionData();
        }
    }, [datesLoaded, dates.start, dates.end, loadEvolutionData]);

    const assetNames = getAssetNames(data);
    const totalValueData = data;

    // Don't render controls until dates are loaded
    if (!datesLoaded && !error) {
        return (
            <div className="container">
                <h1>Investment Portfolio Dashboard</h1>
                <div className="loading">Loading portfolio data...</div>
            </div>
        );
    }

    return (
        <div className="container">
            <h1>Investment Portfolio Dashboard</h1>
            
            <div className="controls">
                <div>
                    <label>Portfolio: </label>
                    <select value={portfolio} onChange={(e) => setPortfolio(e.target.value)}>
                        <option value="1">Portfolio 1</option>
                        <option value="2">Portfolio 2</option>
                    </select>
                </div>
                
                <div>
                    <label>Start Date: </label>
                    <input 
                        type="date" 
                        value={dates.start || ''} 
                        onChange={(e) => setDates({...dates, start: e.target.value})}
                        min={availableDates.first_date || undefined}
                        max={availableDates.last_date || undefined}
                    />
                </div>
                
                <div>
                    <label>End Date: </label>
                    <input 
                        type="date" 
                        value={dates.end || ''} 
                        onChange={(e) => setDates({...dates, end: e.target.value})}
                        min={availableDates.first_date || undefined}
                        max={availableDates.last_date || undefined}
                    />
                </div>
                
                <button onClick={loadEvolutionData}>🔄 Update</button>
            </div>
            
            {loading && <div className="loading">Loading portfolio data...</div>}
            
            {error && <div className="error">{error}</div>}
            
            {!loading && !error && data.length > 0 && (
                <>
                    <TotalValueChart data={totalValueData} />
                    <WeightsChart data={data} assetNames={assetNames} />
                </>
            )}
            
            {!loading && !error && data.length === 0 && datesLoaded && (
                <div className="loading">No data available for selected date range</div>
            )}
        </div>
    );
}

const root = document.getElementById('root');
if (root) {
    createRoot(root).render(<App />);
}
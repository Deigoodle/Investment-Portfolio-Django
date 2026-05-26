import React, { useState, useEffect, useCallback } from 'react';
import { createRoot } from 'react-dom/client';
import { fetchPortfolioDates, fetchPortfolioEvolution, transformChartData, getAssetNames } from './api';
import { TotalValueChart, WeightsChart } from './charts';

function App() {
    const [portfolio, setPortfolio] = useState('1');
    const [dates, setDates] = useState({ start: null, end: null });
    const [availableDates, setAvailableDates] = useState({ first_date: null, last_date: null });
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [datesLoaded, setDatesLoaded] = useState(false);

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

    const loadEvolutionData = useCallback(async () => {
        if (!datesLoaded || !dates.start || !dates.end) {
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

    useEffect(() => {
        if (datesLoaded && dates.start && dates.end) {
            loadEvolutionData();
        }
    }, [datesLoaded, dates.start, dates.end, loadEvolutionData]);

    const assetNames = getAssetNames(data);

    if (!datesLoaded && !error) {
        return (
            <div className="text-center py-5">
                <div className="spinner-border text-primary" role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
                <p className="mt-3">Loading portfolio data...</p>
            </div>
        );
    }

    return (
        <div>
            <h1 className="text-center mb-4">Investment Portfolio Dashboard</h1>
            
            <div className="card p-3 mb-4">
                <div className="row g-3 align-items-end">
                    <div className="col-auto">
                        <label className="form-label mb-1">Portfolio</label>
                        <select 
                            className="form-select" 
                            value={portfolio} 
                            onChange={(e) => setPortfolio(e.target.value)}
                        >
                            <option value="1">Portfolio 1</option>
                            <option value="2">Portfolio 2</option>
                        </select>
                    </div>
                    
                    <div className="col-auto">
                        <label className="form-label mb-1">Start Date</label>
                        <input 
                            type="date" 
                            className="form-control"
                            value={dates.start || ''} 
                            onChange={(e) => setDates({...dates, start: e.target.value})}
                        />
                    </div>
                    
                    <div className="col-auto">
                        <label className="form-label mb-1">End Date</label>
                        <input 
                            type="date" 
                            className="form-control"
                            value={dates.end || ''} 
                            onChange={(e) => setDates({...dates, end: e.target.value})}
                        />
                    </div>
                    
                    <div className="col-auto">
                        <button className="btn btn-primary" onClick={loadEvolutionData}>
                            Update
                        </button>
                    </div>
                </div>
            </div>
            
            {loading && (
                <div className="text-center py-5">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </div>
                </div>
            )}
            
            {error && (
                <div className="alert alert-danger" role="alert">
                    {error}
                </div>
            )}
            
            {!loading && !error && data.length > 0 && (
                <>
                    <TotalValueChart data={data} />
                    <WeightsChart data={data} assetNames={assetNames} />
                </>
            )}
        </div>
    );
}

const root = document.getElementById('root');
if (root) {
    createRoot(root).render(<App />);
}
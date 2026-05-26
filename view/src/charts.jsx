// view/src/charts.jsx
import React from 'react';
import {
    LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid,
    Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const COLORS = [
    '#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#0088fe', 
    '#00c49f', '#ffbb28', '#ff8042', '#a4de6c', '#d0ed57',
    '#83a6ed', '#8dd1e1', '#fcb462', '#ff6b6b', '#4ecdc4',
    '#45b7d1', '#96ceb4'
];

export function TotalValueChart({ data }) {
    return (
        <div className="chart-card">
            <h2>Portfolio Value Over Time (Vₜ)</h2>
            <ResponsiveContainer width="100%" height={400}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis tickFormatter={(value) => `$${(value / 1e6).toFixed(0)}M`} />
                    <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Total Value']} />
                    <Legend />
                    <Line 
                        type="monotone" 
                        dataKey="totalValue" 
                        stroke="#1a73e8" 
                        strokeWidth={2}
                        name="Total Value (USD)" 
                        dot={false}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}

export function WeightsChart({ data, assetNames }) {
    return (
        <div className="chart-card">
            <h2>Asset Weights Evolution (wᵢ,ₜ)</h2>
            <ResponsiveContainer width="100%" height={500}>
                <AreaChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis 
                        tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
                        domain={[0, 1]}
                    />
                    <Tooltip formatter={(value) => `${(value * 100).toFixed(2)}%`} />
                    <Legend wrapperStyle={{ fontSize: '11px', maxHeight: '100px', overflowY: 'auto' }} />
                    {assetNames.map((asset, idx) => (
                        <Area
                            key={asset}
                            type="monotone"
                            dataKey={asset}
                            stackId="1"
                            stroke={COLORS[idx % COLORS.length]}
                            fill={COLORS[idx % COLORS.length]}
                            name={asset}
                        />
                    ))}
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
}
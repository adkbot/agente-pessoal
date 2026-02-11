'use client'

import { useState } from 'react'
import { X, Save, Trash2 } from 'lucide-react'

interface CredentialsModalProps {
    onClose: () => void
}

export default function CredentialsModal({ onClose }: CredentialsModalProps) {
    const [activeTab, setActiveTab] = useState<'binance' | 'bybit' | 'mt5' | 'tradingview'>('binance')
    const [credentials, setCredentials] = useState({
        binance: { apiKey: '', apiSecret: '' },
        bybit: { apiKey: '', apiSecret: '' },
        mt5: { account: '', password: '', server: '' },
        tradingview: { username: '', password: '' }
    })

    const handleSave = async () => {
        // TODO: Send to backend for encryption and storage
        console.log('Saving credentials for:', activeTab, credentials[activeTab])
        alert(`Credentials saved for ${activeTab}`)
    }

    const handleDelete = () => {
        if (confirm(`Delete ${activeTab} credentials?`)) {
            setCredentials(prev => ({
                ...prev,
                [activeTab]: activeTab === 'mt5'
                    ? { account: '', password: '', server: '' }
                    : activeTab === 'tradingview'
                        ? { username: '', password: '' }
                        : { apiKey: '', apiSecret: '' }
            }))
        }
    }

    return (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-gray-900 rounded-xl border border-purple-500/30 max-w-2xl w-full max-h-[90vh] overflow-auto shadow-2xl">
                {/* Header */}
                <div className="flex items-center justify-between p-6 border-b border-purple-500/30">
                    <h2 className="text-xl font-bold text-purple-300">Credential Management</h2>
                    <button onClick={onClose} className="p-2 hover:bg-gray-800 rounded-lg transition-colors">
                        <X size={20} />
                    </button>
                </div>

                {/* Tabs */}
                <div className="flex border-b border-purple-500/20">
                    {(['binance', 'bybit', 'mt5', 'tradingview'] as const).map(tab => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab)}
                            className={`flex-1 px-4 py-3 capitalize transition-colors ${activeTab === tab
                                    ? 'bg-purple-600/20 text-purple-300 border-b-2 border-purple-500'
                                    : 'text-gray-400 hover:text-white'
                                }`}
                        >
                            {tab}
                        </button>
                    ))}
                </div>

                {/* Content */}
                <div className="p-6 space-y-4">
                    {activeTab === 'binance' && (
                        <>
                            <div>
                                <label className="block text-sm text-gray-400 mb-2">API Key</label>
                                <input
                                    type="text"
                                    value={credentials.binance.apiKey}
                                    onChange={(e) => setCredentials(prev => ({
                                        ...prev,
                                        binance: { ...prev.binance, apiKey: e.target.value }
                                    }))}
                                    className="w-full px-4 py-2 bg-gray-800/50 border border-purple-500/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                                    placeholder="Enter Binance API Key"
                                />
                            </div>
                            <div>
                                <label className="block text-sm text-gray-400 mb-2">API Secret</label>
                                <input
                                    type="password"
                                    value={credentials.binance.apiSecret}
                                    onChange={(e) => setCredentials(prev => ({
                                        ...prev,
                                        binance: { ...prev.binance, apiSecret: e.target.value }
                                    }))}
                                    className="w-full px-4 py-2 bg-gray-800/50 border border-purple-500/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                                    placeholder="Enter Binance API Secret"
                                />
                            </div>
                        </>
                    )}

                    {activeTab === 'bybit' && (
                        <>
                            <div>
                                <label className="block text-sm text-gray-400 mb-2">API Key</label>
                                <input
                                    type="text"
                                    value={credentials.bybit.apiKey}
                                    onChange={(e) => setCredentials(prev => ({
                                        ...prev,
                                        bybit: { ...prev.bybit, apiKey: e.target.value }
                                    }))}
                                    className="w-full px-4 py-2 bg-gray-800/50 border border-purple-500/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                                    placeholder="Enter Bybit API Key"
                                />
                            </div>
                            <div>
                                <label className="block text-sm text-gray-400 mb-2">API Secret</label>
                                <input
                                    type="password"
                                    value={credentials.bybit.apiSecret}
                                    onChange={(e) => setCredentials(prev => ({
                                        ...prev,
                                        bybit: { ...prev.bybit, apiSecret: e.target.value }
                                    }))}
                                    className="w-full px-4 py-2 bg-gray-800/50 border border-purple-500/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                                    placeholder="Enter Bybit API Secret"
                                />
                            </div>
                        </>
                    )}

                    {activeTab === 'mt5' && (
                        <>
                            <div>
                                <label className="block text-sm text-gray-400 mb-2">Account</label>
                                <input
                                    type="text"
                                    value={credentials.mt5.account}
                                    onChange={(e) => setCredentials(prev => ({
                                        ...prev,
                                        mt5: { ...prev.mt5, account: e.target.value }
                                    }))}
                                    className="w-full px-4 py-2 bg-gray-800/50 border border-purple-500/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                                    placeholder="Enter MT5 Account Number"
                                />
                            </div>
                            <div>
                                <label className="block text-sm text-gray-400 mb-2">Password</label>
                                <input
                                    type="password"
                                    value={credentials.mt5.password}
                                    onChange={(e) => setCredentials(prev => ({
                                        ...prev,
                                        mt5: { ...prev.mt5, password: e.target.value }
                                    }))}
                                    className="w-full px-4 py-2 bg-gray-800/50 border border-purple-500/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                                    placeholder="Enter MT5 Password"
                                />
                            </div>
                            <div>
                                <label className="block text-sm text-gray-400 mb-2">Server</label>
                                <input
                                    type="text"
                                    value={credentials.mt5.server}
                                    onChange={(e) => setCredentials(prev => ({
                                        ...prev,
                                        mt5: { ...prev.mt5, server: e.target.value }
                                    }))}
                                    className="w-full px-4 py-2 bg-gray-800/50 border border-purple-500/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                                    placeholder="e.g., MetaQuotes-Demo"
                                />
                            </div>
                        </>
                    )}

                    {activeTab === 'tradingview' && (
                        <>
                            <div>
                                <label className="block text-sm text-gray-400 mb-2">Username</label>
                                <input
                                    type="text"
                                    value={credentials.tradingview.username}
                                    onChange={(e) => setCredentials(prev => ({
                                        ...prev,
                                        tradingview: { ...prev.tradingview, username: e.target.value }
                                    }))}
                                    className="w-full px-4 py-2 bg-gray-800/50 border border-purple-500/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                                    placeholder="Enter TradingView Username"
                                />
                            </div>
                            <div>
                                <label className="block text-sm text-gray-400 mb-2">Password</label>
                                <input
                                    type="password"
                                    value={credentials.tradingview.password}
                                    onChange={(e) => setCredentials(prev => ({
                                        ...prev,
                                        tradingview: { ...prev.tradingview, password: e.target.value }
                                    }))}
                                    className="w-full px-4 py-2 bg-gray-800/50 border border-purple-500/30 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                                    placeholder="Enter TradingView Password"
                                />
                            </div>
                        </>
                    )}
                </div>

                {/* Footer */}
                <div className="p-6 border-t border-purple-500/30 flex items-center justify-between">
                    <button
                        onClick={handleDelete}
                        className="px-4 py-2 text-red-400 hover:bg-red-600/20 rounded-lg transition-colors flex items-center gap-2"
                    >
                        <Trash2 size={18} />
                        Delete
                    </button>
                    <button
                        onClick={handleSave}
                        className="px-6 py-2 bg-gradient-to-r from-purple-600 to-pink-600 rounded-lg hover:from-purple-500 hover:to-pink-500 transition-all flex items-center gap-2"
                    >
                        <Save size={18} />
                        Save & Encrypt
                    </button>
                </div>
            </div>
        </div>
    )
}

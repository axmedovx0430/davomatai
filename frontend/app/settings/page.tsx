'use client'

import { useState, useEffect } from 'react'
import { ArrowLeft, Save, Clock, Timer, RefreshCw } from 'lucide-react'
import Link from 'next/link'
import { api } from '@/lib/api-client'

export default function SettingsPage() {
    const [loading, setLoading] = useState(true)
    const [saving, setSaving] = useState(false)
    const [settings, setSettings] = useState({
        work_start_time: '09:00',
        late_threshold_minutes: 30,
        duplicate_check_minutes: 120
    })
    const [history, setHistory] = useState([])

    useEffect(() => {
        loadSettings()
        loadHistory()
    }, [])

    const loadSettings = async () => {
        try {
            const response = await api.getTimeSettings()
            if (response.data.success && response.data.settings) {
                setSettings(response.data.settings)
            }
        } catch (error) {
            console.error('Error loading settings:', error)
        } finally {
            setLoading(false)
        }
    }

    const loadHistory = async () => {
        try {
            const response = await api.getTimeSettingsHistory()
            if (response.data.success) {
                setHistory(response.data.history)
            }
        } catch (error) {
            console.error('Error loading history:', error)
        }
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setSaving(true)

        try {
            const response = await api.updateTimeSettings(settings)
            if (response.data.success) {
                alert('Sozlamalar muvaffaqiyatli saqlandi!')
                loadHistory()
            }
        } catch (error: any) {
            alert('Xatolik: ' + (error.response?.data?.detail || error.message))
        } finally {
            setSaving(false)
        }
    }

    const handleChange = (field: string, value: any) => {
        setSettings({ ...settings, [field]: value })
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-50 to-blue-50">
            <header className="bg-white shadow-sm border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center gap-4">
                        <Link href="/" className="text-gray-600 hover:text-gray-900">
                            <ArrowLeft className="w-6 h-6" />
                        </Link>
                        <h1 className="text-3xl font-bold text-gray-900">Sozlamalar</h1>
                    </div>
                </div>
            </header>

            <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Settings Form */}
                <div className="card mb-6">
                    <h2 className="text-2xl font-bold mb-6">Vaqt Sozlamalari</h2>

                    {loading ? (
                        <div className="text-center py-12">
                            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
                        </div>
                    ) : (
                        <form onSubmit={handleSubmit} className="space-y-6">
                            {/* Work Start Time */}
                            <div>
                                <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                                    <Clock className="w-5 h-5 text-blue-600" />
                                    Dars Boshlanish Vaqti
                                </label>
                                <input
                                    type="time"
                                    required
                                    className="input max-w-xs"
                                    value={settings.work_start_time}
                                    onChange={(e) => handleChange('work_start_time', e.target.value)}
                                />
                                <p className="text-sm text-gray-500 mt-1">
                                    Dars qachon boshlanishini belgilang (masalan: 09:00)
                                </p>
                            </div>

                            {/* Late Threshold */}
                            <div>
                                <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                                    <Timer className="w-5 h-5 text-yellow-600" />
                                    Kechikish Chegarasi (daqiqalarda)
                                </label>
                                <input
                                    type="number"
                                    required
                                    min="1"
                                    max="180"
                                    className="input max-w-xs"
                                    value={settings.late_threshold_minutes}
                                    onChange={(e) => handleChange('late_threshold_minutes', parseInt(e.target.value))}
                                />
                                <p className="text-sm text-gray-500 mt-1">
                                    Dars boshlanganidan necha daqiqa ichida kelsa "keldi" hisoblanadi
                                </p>
                            </div>

                            {/* Duplicate Check */}
                            <div>
                                <label className="flex items-center gap-2 text-sm font-medium text-gray-700 mb-2">
                                    <RefreshCw className="w-5 h-5 text-green-600" />
                                    Qayta Davomat Taqiqi (daqiqalarda)
                                </label>
                                <input
                                    type="number"
                                    required
                                    min="1"
                                    max="1440"
                                    className="input max-w-xs"
                                    value={settings.duplicate_check_minutes}
                                    onChange={(e) => handleChange('duplicate_check_minutes', parseInt(e.target.value))}
                                />
                                <p className="text-sm text-gray-500 mt-1">
                                    Birinchi davomat qilingandan keyin necha daqiqa ichida qayta ko'rinsa ignore qilinadi
                                </p>
                                <p className="text-sm text-blue-600 mt-1">
                                    💡 Masalan: 120 daqiqa = 2 soat (tavsiya etiladi)
                                </p>
                            </div>

                            <button
                                type="submit"
                                disabled={saving}
                                className="btn btn-primary flex items-center gap-2"
                            >
                                <Save className="w-5 h-5" />
                                {saving ? 'Saqlanmoqda...' : 'Saqlash'}
                            </button>
                        </form>
                    )}
                </div>

                {/* Settings History */}
                {history.length > 0 && (
                    <div className="card">
                        <h2 className="text-xl font-bold mb-4">Sozlamalar Tarixi</h2>
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="bg-gray-50 border-b">
                                    <tr>
                                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                                            Vaqt
                                        </th>
                                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                                            Dars Boshlanishi
                                        </th>
                                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                                            Kechikish
                                        </th>
                                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                                            Qayta Taqiq
                                        </th>
                                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                                            Status
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {history.map((item: any) => (
                                        <tr key={item.id} className="hover:bg-gray-50">
                                            <td className="px-4 py-3 text-sm text-gray-600">
                                                {new Date(item.created_at).toLocaleString('uz-UZ')}
                                            </td>
                                            <td className="px-4 py-3 text-sm font-medium">
                                                {item.work_start_time}
                                            </td>
                                            <td className="px-4 py-3 text-sm text-gray-600">
                                                {item.late_threshold_minutes} daq
                                            </td>
                                            <td className="px-4 py-3 text-sm text-gray-600">
                                                {item.duplicate_check_minutes} daq
                                            </td>
                                            <td className="px-4 py-3 text-sm">
                                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${item.is_active
                                                        ? 'bg-green-100 text-green-800'
                                                        : 'bg-gray-100 text-gray-600'
                                                    }`}>
                                                    {item.is_active ? 'Faol' : 'Nofaol'}
                                                </span>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}
            </main>
        </div>
    )
}

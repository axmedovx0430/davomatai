'use client'

import { useDevices } from '@/hooks/use-api'
import { api } from '@/lib/api-client'
import { useState } from 'react'
import { ArrowLeft, Plus, Wifi, WifiOff } from 'lucide-react'
import Link from 'next/link'

export default function DevicesPage() {
    const { data, isLoading, refetch } = useDevices()
    const [showForm, setShowForm] = useState(false)
    const [formData, setFormData] = useState({ device_name: '', location: '' })

    const devices = data?.devices || []

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            const result = await api.createDevice(formData)
            alert(`Qurilma yaratildi!\n\nAPI Key: ${result.data.api_key}\n\nBu kalitni ESP32-CAM config.h fayliga kiriting.`)
            setShowForm(false)
            setFormData({ device_name: '', location: '' })
            refetch()
        } catch (error: any) {
            alert('Xatolik: ' + (error.response?.data?.detail || error.message))
        }
    }

    const regenerateKey = async (id: number, name: string) => {
        if (confirm(`${name} uchun yangi API key yaratilsinmi?`)) {
            try {
                const result = await api.regenerateApiKey(id)
                alert(`Yangi API Key:\n\n${result.data.api_key}\n\nBu kalitni ESP32-CAM config.h fayliga kiriting.`)
                refetch()
            } catch (error: any) {
                alert('Xatolik: ' + (error.response?.data?.detail || error.message))
            }
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-50 to-blue-50">
            <header className="bg-white shadow-sm border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <Link href="/" className="text-gray-600 hover:text-gray-900">
                                <ArrowLeft className="w-6 h-6" />
                            </Link>
                            <h1 className="text-3xl font-bold text-gray-900">Qurilmalar</h1>
                        </div>
                        <button
                            onClick={() => setShowForm(!showForm)}
                            className="btn btn-primary flex items-center gap-2"
                        >
                            <Plus className="w-5 h-5" />
                            Yangi Qurilma
                        </button>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {showForm && (
                    <div className="card mb-6">
                        <h2 className="text-xl font-bold mb-4">Yangi Qurilma Qo'shish</h2>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Qurilma Nomi *
                                </label>
                                <input
                                    type="text"
                                    required
                                    className="input"
                                    value={formData.device_name}
                                    onChange={(e) => setFormData({ ...formData, device_name: e.target.value })}
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Joylashuv
                                </label>
                                <input
                                    type="text"
                                    className="input"
                                    value={formData.location}
                                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                                />
                            </div>
                            <div className="flex gap-2">
                                <button type="submit" className="btn btn-primary">Saqlash</button>
                                <button
                                    type="button"
                                    onClick={() => setShowForm(false)}
                                    className="btn btn-secondary"
                                >
                                    Bekor qilish
                                </button>
                            </div>
                        </form>
                    </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {isLoading ? (
                        <div className="col-span-full text-center py-12">
                            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
                        </div>
                    ) : (
                        devices.map((device: any) => (
                            <div key={device.id} className="card">
                                <div className="flex items-start justify-between mb-4">
                                    <div>
                                        <h3 className="text-lg font-bold text-gray-900">{device.device_name}</h3>
                                        <p className="text-sm text-gray-600">{device.location || 'Joylashuv ko\'rsatilmagan'}</p>
                                    </div>
                                    {device.is_active ? (
                                        <Wifi className="w-6 h-6 text-green-500" />
                                    ) : (
                                        <WifiOff className="w-6 h-6 text-red-500" />
                                    )}
                                </div>
                                <div className="space-y-2 text-sm">
                                    <div className="flex justify-between">
                                        <span className="text-gray-600">Status:</span>
                                        <span className={device.is_active ? 'text-green-600 font-medium' : 'text-red-600 font-medium'}>
                                            {device.is_active ? 'Faol' : 'Nofaol'}
                                        </span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-600">Oxirgi ko\'rinish:</span>
                                        <span className="text-gray-900">
                                            {device.last_seen
                                                ? new Date(device.last_seen).toLocaleString('uz-UZ')
                                                : 'Hech qachon'
                                            }
                                        </span>
                                    </div>
                                </div>
                                <button
                                    onClick={() => regenerateKey(device.id, device.device_name)}
                                    className="mt-4 w-full btn btn-secondary text-sm"
                                >
                                    API Key Yangilash
                                </button>
                            </div>
                        ))
                    )}
                </div>
            </main>
        </div>
    )
}

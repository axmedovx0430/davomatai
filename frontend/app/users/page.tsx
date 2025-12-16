'use client'

import { useUsers, useCreateUser, useDeleteUser, useRegisterFace } from '@/hooks/use-api'
import { useState } from 'react'
import { UserPlus, Trash2, Upload, ArrowLeft, MessageCircle } from 'lucide-react'
import Link from 'next/link'

import { useSearchParams } from 'next/navigation'

export default function UsersPage() {
    const searchParams = useSearchParams()
    const groupId = searchParams.get('group_id')

    const params: any = { is_active: true }
    if (groupId) {
        params.group_id = groupId
    }

    const { data, isLoading } = useUsers(params)
    const createUser = useCreateUser()
    const deleteUser = useDeleteUser()
    const registerFace = useRegisterFace()

    const [showForm, setShowForm] = useState(false)
    const [formData, setFormData] = useState({
        full_name: '',
        employee_id: '',
        phone: '',
        email: '',
    })
    const [selectedFile, setSelectedFile] = useState<File | null>(null)
    const [selectedUserId, setSelectedUserId] = useState<number | null>(null)

    const users = data?.users || []

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            const result = await createUser.mutateAsync(formData)

            // If file is selected, register face
            if (selectedFile && result.data.user.id) {
                await registerFace.mutateAsync({
                    userId: result.data.user.id,
                    file: selectedFile,
                })
            }

            setShowForm(false)
            setFormData({ full_name: '', employee_id: '', phone: '', email: '' })
            setSelectedFile(null)
            alert('Foydalanuvchi muvaffaqiyatli qo\'shildi!')
        } catch (error: any) {
            alert('Xatolik: ' + (error.response?.data?.detail || error.message))
        }
    }

    const handleDelete = async (id: number, name: string) => {
        if (confirm(`${name}ni o'chirmoqchimisiz?`)) {
            try {
                await deleteUser.mutateAsync(id)
                alert('Foydalanuvchi o\'chirildi')
            } catch (error: any) {
                alert('Xatolik: ' + (error.response?.data?.detail || error.message))
            }
        }
    }

    const handleFaceUpload = async (userId: number) => {
        const input = document.createElement('input')
        input.type = 'file'
        input.accept = 'image/*'
        input.onchange = async (e: any) => {
            const file = e.target.files[0]
            if (file) {
                try {
                    await registerFace.mutateAsync({ userId, file })
                    alert('Yuz muvaffaqiyatli ro\'yxatdan o\'tkazildi!')
                } catch (error: any) {
                    alert('Xatolik: ' + (error.response?.data?.detail || error.message))
                }
            }
        }
        input.click()
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
                            <h1 className="text-3xl font-bold text-gray-900">Foydalanuvchilar</h1>
                        </div>
                        <button
                            onClick={() => setShowForm(!showForm)}
                            className="btn btn-primary flex items-center gap-2"
                        >
                            <UserPlus className="w-5 h-5" />
                            Yangi Foydalanuvchi
                        </button>
                    </div>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Add User Form */}
                {showForm && (
                    <div className="card mb-6">
                        <h2 className="text-xl font-bold mb-4">Yangi Foydalanuvchi Qo'shish</h2>
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        To'liq Ism *
                                    </label>
                                    <input
                                        type="text"
                                        required
                                        className="input"
                                        value={formData.full_name}
                                        onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        Xodim ID *
                                    </label>
                                    <input
                                        type="text"
                                        required
                                        className="input"
                                        value={formData.employee_id}
                                        onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        Telefon
                                    </label>
                                    <input
                                        type="tel"
                                        className="input"
                                        value={formData.phone}
                                        onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">
                                        Email
                                    </label>
                                    <input
                                        type="email"
                                        className="input"
                                        value={formData.email}
                                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    />
                                </div>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Yuz Rasmi (ixtiyoriy)
                                </label>
                                <input
                                    type="file"
                                    accept="image/*"
                                    className="input"
                                    onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                                />
                            </div>
                            <div className="flex gap-2">
                                <button type="submit" className="btn btn-primary" disabled={createUser.isPending}>
                                    {createUser.isPending ? 'Saqlanmoqda...' : 'Saqlash'}
                                </button>
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

                {/* Users List */}
                <div className="card">
                    <h2 className="text-xl font-bold mb-4">Barcha Foydalanuvchilar ({users.length})</h2>

                    {isLoading ? (
                        <div className="text-center py-12">
                            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="bg-gray-50 border-b">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Ism</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Telefon</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Telegram</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Yuzlar</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amallar</th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {users.map((user: any) => (
                                        <tr key={user.id} className="hover:bg-gray-50">
                                            <td className="px-6 py-4 whitespace-nowrap font-medium">{user.full_name}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{user.employee_id}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{user.phone || '-'}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{user.email || '-'}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm">
                                                {user.telegram_chat_id ? (
                                                    <div className="flex items-center gap-1 text-blue-600">
                                                        <MessageCircle className="w-4 h-4" />
                                                        <span>{user.telegram_username ? `@${user.telegram_username}` : 'Ullangan'}</span>
                                                    </div>
                                                ) : (
                                                    <span className="text-gray-400 text-xs">Ulanmagan</span>
                                                )}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm">
                                                <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                                                    {user.face_count || 0}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm">
                                                <div className="flex gap-2">
                                                    <button
                                                        onClick={() => handleFaceUpload(user.id)}
                                                        className="text-blue-600 hover:text-blue-800"
                                                        title="Yuz qo'shish"
                                                    >
                                                        <Upload className="w-5 h-5" />
                                                    </button>
                                                    <button
                                                        onClick={() => handleDelete(user.id, user.full_name)}
                                                        className="text-red-600 hover:text-red-800"
                                                        title="O'chirish"
                                                    >
                                                        <Trash2 className="w-5 h-5" />
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </main>
        </div>
    )
}

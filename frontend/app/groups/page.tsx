'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useQueryClient } from '@tanstack/react-query';
import apiClient from '@/lib/api-client';
import { useGroups } from '@/hooks/use-groups';


interface Group {
    id: number;
    name: string;
    code: string;
    description?: string;
    faculty?: string;
    course?: number;
    semester?: number;
    academic_year?: string;
    is_active: boolean;
    student_count: number;
}

export default function GroupsPage() {
    const queryClient = useQueryClient();
    const { data: groups = [], isLoading: loading } = useGroups();
    const [showAddModal, setShowAddModal] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        code: '',
        description: '',
        faculty: '',
        course: 1,
        semester: 1,
        academic_year: '2024-2025'
    });


    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await apiClient.post('/api/groups', formData);
            if (response.data.success) {
                setShowAddModal(false);
                queryClient.invalidateQueries({ queryKey: ['groups'] });
                setFormData({
                    name: '',
                    code: '',
                    description: '',
                    faculty: '',
                    course: 1,
                    semester: 1,
                    academic_year: '2024-2025'
                });
            }
        } catch (error) {
            console.error('Error creating group:', error);
        }
    };

    const deleteGroup = async (id: number) => {
        if (!confirm('Guruhni o\'chirmoqchimisiz?')) return;

        try {
            const response = await apiClient.delete(`/api/groups/${id}`);
            if (response.data.success) {
                queryClient.invalidateQueries({ queryKey: ['groups'] });
            }
        } catch (error) {
            console.error('Error deleting group:', error);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
                <div className="text-center">Yuklanmoqda...</div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-4xl font-bold text-gray-800 mb-2">Guruhlar</h1>
                        <p className="text-gray-600">Talabalar guruhlarini boshqarish</p>
                    </div>
                    <div className="flex gap-4">
                        <Link
                            href="/"
                            className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
                        >
                            ← Orqaga
                        </Link>
                        <button
                            onClick={() => setShowAddModal(true)}
                            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                        >
                            + Yangi Guruh
                        </button>
                    </div>
                </div>

                {/* Groups Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {groups.map((group: Group) => (
                        <div
                            key={group.id}
                            className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow"
                        >
                            <div className="flex justify-between items-start mb-4">
                                <div>
                                    <h3 className="text-xl font-bold text-gray-800">{group.name}</h3>
                                    <p className="text-sm text-gray-500">{group.code}</p>
                                </div>
                                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${group.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                                    }`}>
                                    {group.is_active ? 'Faol' : 'Nofaol'}
                                </span>
                            </div>

                            {group.faculty && (
                                <p className="text-sm text-gray-600 mb-2">
                                    <span className="font-semibold">Fakultet:</span> {group.faculty}
                                </p>
                            )}

                            {group.course && (
                                <p className="text-sm text-gray-600 mb-2">
                                    <span className="font-semibold">Kurs:</span> {group.course}-kurs
                                </p>
                            )}

                            {group.academic_year && (
                                <p className="text-sm text-gray-600 mb-4">
                                    <span className="font-semibold">O'quv yili:</span> {group.academic_year}
                                </p>
                            )}

                            <div className="flex items-center justify-between pt-4 border-t">
                                <div className="flex items-center gap-2">
                                    <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                                    </svg>
                                    <span className="text-sm text-gray-600">{group.student_count} talaba</span>
                                </div>

                                <div className="flex gap-2">
                                    <Link
                                        href={`/groups/${group.id}`}
                                        className="px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200 text-sm"
                                    >
                                        Ko'rish
                                    </Link>
                                    <button
                                        onClick={() => deleteGroup(group.id)}
                                        className="px-3 py-1 bg-red-100 text-red-700 rounded hover:bg-red-200 text-sm"
                                    >
                                        O'chirish
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                {groups.length === 0 && (
                    <div className="text-center py-12 bg-white rounded-xl shadow">
                        <p className="text-gray-500 text-lg">Hozircha guruhlar yo'q</p>
                        <button
                            onClick={() => setShowAddModal(true)}
                            className="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                        >
                            Birinchi guruhni qo'shing
                        </button>
                    </div>
                )}

                {/* Add Group Modal */}
                {showAddModal && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                        <div className="bg-white rounded-xl p-8 max-w-md w-full mx-4">
                            <h2 className="text-2xl font-bold mb-6">Yangi Guruh Qo'shish</h2>
                            <form onSubmit={handleSubmit}>
                                <div className="space-y-4">
                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Guruh nomi *
                                        </label>
                                        <input
                                            type="text"
                                            required
                                            value={formData.name}
                                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                                            placeholder="Masalan: Kompyuter Fanlari 101"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Guruh kodi *
                                        </label>
                                        <input
                                            type="text"
                                            required
                                            value={formData.code}
                                            onChange={(e) => setFormData({ ...formData, code: e.target.value })}
                                            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                                            placeholder="Masalan: CS-101"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Fakultet
                                        </label>
                                        <input
                                            type="text"
                                            value={formData.faculty}
                                            onChange={(e) => setFormData({ ...formData, faculty: e.target.value })}
                                            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                                            placeholder="Masalan: Kompyuter Fanlari"
                                        />
                                    </div>

                                    <div className="grid grid-cols-2 gap-4">
                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                                Kurs
                                            </label>
                                            <select
                                                value={formData.course}
                                                onChange={(e) => setFormData({ ...formData, course: parseInt(e.target.value) })}
                                                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                                            >
                                                <option value={1}>1-kurs</option>
                                                <option value={2}>2-kurs</option>
                                                <option value={3}>3-kurs</option>
                                                <option value={4}>4-kurs</option>
                                            </select>
                                        </div>

                                        <div>
                                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                                Semestr
                                            </label>
                                            <select
                                                value={formData.semester}
                                                onChange={(e) => setFormData({ ...formData, semester: parseInt(e.target.value) })}
                                                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                                            >
                                                <option value={1}>1-semestr</option>
                                                <option value={2}>2-semestr</option>
                                            </select>
                                        </div>
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            O'quv yili
                                        </label>
                                        <input
                                            type="text"
                                            value={formData.academic_year}
                                            onChange={(e) => setFormData({ ...formData, academic_year: e.target.value })}
                                            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                                            placeholder="2024-2025"
                                        />
                                    </div>

                                    <div>
                                        <label className="block text-sm font-medium text-gray-700 mb-1">
                                            Tavsif
                                        </label>
                                        <textarea
                                            value={formData.description}
                                            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                                            rows={3}
                                            placeholder="Guruh haqida qisqacha ma'lumot"
                                        />
                                    </div>
                                </div>

                                <div className="flex gap-4 mt-6">
                                    <button
                                        type="button"
                                        onClick={() => setShowAddModal(false)}
                                        className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                                    >
                                        Bekor qilish
                                    </button>
                                    <button
                                        type="submit"
                                        className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                                    >
                                        Qo'shish
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

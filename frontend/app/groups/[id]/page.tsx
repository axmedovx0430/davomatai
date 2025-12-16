'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import apiClient from '@/lib/api-client';

interface Student {
    id: number;
    full_name: string;
    employee_id: string;
}

interface Group {
    id: number;
    name: string;
    code: string;
    description?: string;
    faculty?: string;
    course?: number;
    semester?: number;
    academic_year?: string;
    student_count: number;
    students: Student[];
}

export default function GroupDetailPage() {
    const params = useParams();
    const router = useRouter();
    const groupId = params.id;

    const [group, setGroup] = useState<Group | null>(null);
    const [loading, setLoading] = useState(true);
    const [showAddStudent, setShowAddStudent] = useState(false);
    const [allUsers, setAllUsers] = useState<Student[]>([]);
    const [selectedUsers, setSelectedUsers] = useState<number[]>([]);
    useEffect(() => {
        fetchGroup();
        fetchAllUsers();
    }, [groupId]);

    const fetchGroup = async () => {
        try {
            const response = await apiClient.get(`/api/groups/${groupId}`);
            if (response.data.success) {
                setGroup(response.data.group);
            }
        } catch (error) {
            console.error('Error fetching group:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchAllUsers = async () => {
        try {
            const response = await apiClient.get('/api/users', { params: { is_active: true } });
            if (response.data.success) {
                setAllUsers(response.data.users);
            }
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    };

    const addStudents = async () => {
        try {
            const response = await apiClient.post(`/api/groups/${groupId}/students`, { user_ids: selectedUsers });
            if (response.data.success) {
                setShowAddStudent(false);
                setSelectedUsers([]);
                fetchGroup();
            }
        } catch (error) {
            console.error('Error adding students:', error);
        }
    };

    const removeStudent = async (userId: number) => {
        if (!confirm('Talabani guruhdan o\'chirmoqchimisiz?')) return;

        try {
            const response = await apiClient.delete(`/api/groups/${groupId}/students/${userId}`);
            if (response.data.success) {
                fetchGroup();
            }
        } catch (error) {
            console.error('Error removing student:', error);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
                <div className="text-center">Yuklanmoqda...</div>
            </div>
        );
    }

    if (!group) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
                <div className="text-center">Guruh topilmadi</div>
            </div>
        );
    }

    // Filter out students already in the group
    const availableUsers = allUsers.filter(
        user => !group.students.some(student => student.id === user.id)
    );

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="mb-8">
                    <Link
                        href="/groups"
                        className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-4"
                    >
                        ← Guruhlar ro'yxatiga qaytish
                    </Link>

                    <div className="bg-white rounded-xl shadow-lg p-6">
                        <div className="flex justify-between items-start">
                            <div>
                                <h1 className="text-3xl font-bold text-gray-800 mb-2">{group.name}</h1>
                                <p className="text-gray-600 mb-4">{group.code}</p>

                                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                                    {group.faculty && (
                                        <div>
                                            <span className="text-gray-500">Fakultet:</span>
                                            <p className="font-semibold">{group.faculty}</p>
                                        </div>
                                    )}
                                    {group.course && (
                                        <div>
                                            <span className="text-gray-500">Kurs:</span>
                                            <p className="font-semibold">{group.course}-kurs</p>
                                        </div>
                                    )}
                                    {group.semester && (
                                        <div>
                                            <span className="text-gray-500">Semestr:</span>
                                            <p className="font-semibold">{group.semester}-semestr</p>
                                        </div>
                                    )}
                                    {group.academic_year && (
                                        <div>
                                            <span className="text-gray-500">O'quv yili:</span>
                                            <p className="font-semibold">{group.academic_year}</p>
                                        </div>
                                    )}
                                </div>
                            </div>

                            <button
                                onClick={() => setShowAddStudent(true)}
                                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                            >
                                + Talaba Qo'shish
                            </button>
                        </div>
                    </div>
                </div>

                {/* Students List */}
                <div className="bg-white rounded-xl shadow-lg p-6">
                    <h2 className="text-2xl font-bold text-gray-800 mb-6">
                        Talabalar ({group.student_count})
                    </h2>

                    {group.students.length === 0 ? (
                        <div className="text-center py-12 text-gray-500">
                            <p className="text-lg mb-4">Bu guruhda hali talabalar yo'q</p>
                            <button
                                onClick={() => setShowAddStudent(true)}
                                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                            >
                                Birinchi talabani qo'shing
                            </button>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            #
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            ID
                                        </th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            To'liq Ism
                                        </th>
                                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Amallar
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {group.students.map((student, index) => (
                                        <tr key={student.id} className="hover:bg-gray-50">
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {index + 1}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                                {student.employee_id}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                                {student.full_name}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                                                <button
                                                    onClick={() => removeStudent(student.id)}
                                                    className="text-red-600 hover:text-red-900"
                                                >
                                                    O'chirish
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>

                {/* Add Students Modal */}
                {showAddStudent && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                        <div className="bg-white rounded-xl p-8 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
                            <h2 className="text-2xl font-bold mb-6">Talabalar Qo'shish</h2>

                            {availableUsers.length === 0 ? (
                                <p className="text-gray-500 text-center py-8">
                                    Qo'shish uchun talabalar yo'q
                                </p>
                            ) : (
                                <div className="space-y-2 mb-6">
                                    {availableUsers.map((user) => (
                                        <label
                                            key={user.id}
                                            className="flex items-center p-3 hover:bg-gray-50 rounded-lg cursor-pointer"
                                        >
                                            <input
                                                type="checkbox"
                                                checked={selectedUsers.includes(user.id)}
                                                onChange={(e) => {
                                                    if (e.target.checked) {
                                                        setSelectedUsers([...selectedUsers, user.id]);
                                                    } else {
                                                        setSelectedUsers(selectedUsers.filter(id => id !== user.id));
                                                    }
                                                }}
                                                className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                                            />
                                            <span className="ml-3 text-sm">
                                                <span className="font-medium">{user.full_name}</span>
                                                <span className="text-gray-500 ml-2">({user.employee_id})</span>
                                            </span>
                                        </label>
                                    ))}
                                </div>
                            )}

                            <div className="flex gap-4">
                                <button
                                    onClick={() => {
                                        setShowAddStudent(false);
                                        setSelectedUsers([]);
                                    }}
                                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                                >
                                    Bekor qilish
                                </button>
                                <button
                                    onClick={addStudents}
                                    disabled={selectedUsers.length === 0}
                                    className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
                                >
                                    Qo'shish ({selectedUsers.length})
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

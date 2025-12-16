"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { CalendarDays, Clock, CheckCircle2, XCircle, AlertCircle, User as UserIcon } from "lucide-react";

interface User {
    id: number;
    full_name: string;
    employee_id: string;
    telegram_chat_id: string;
}

interface Stats {
    present: number;
    late: number;
    absent: number;
    total: number;
    attendance_rate: number;
}

interface Schedule {
    id: number;
    name: string;
    start_time: string;
    end_time: string;
    room?: string;
}

interface Attendance {
    id: number;
    status: string;
    check_in_time: string;
    schedule?: Schedule; // Schedule might be null if not joined properly in backend, but usually present
    date: string;
}

export default function MobilePage() {
    const [user, setUser] = useState<User | null>(null);
    const [stats, setStats] = useState<Stats | null>(null);
    const [todayAttendance, setTodayAttendance] = useState<Attendance[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const initApp = async () => {
            try {
                // @ts-ignore
                const tg = window.Telegram?.WebApp;

                if (!tg) {
                    // For development in browser without Telegram
                    console.warn("Telegram WebApp not found, using mock ID if in dev mode");
                    // Uncomment to test in browser:
                    // fetchUserData("ADMIN004"); 
                    // return;

                    setError("Iltimos, ushbu ilovani Telegram orqali oching.");
                    setLoading(false);
                    return;
                }

                tg.ready();
                tg.expand();

                // Get user ID from initData
                const telegramUser = tg.initDataUnsafe?.user;
                const telegramId = telegramUser?.id?.toString();

                if (!telegramId) {
                    setError("Foydalanuvchi aniqlanmadi. Iltimos, bot orqali kiring.");
                    setLoading(false);
                    return;
                }

                await fetchUserData(telegramId);

            } catch (err) {
                console.error(err);
                setError(`Xatolik: ${err instanceof Error ? err.message : String(err)}`);
                setLoading(false);
            }
        };

        initApp();
    }, []);

    const fetchUserData = async (telegramId: string) => {
        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://69566cb51d2007b59d5fc3cae0117b1b.serveousercontent.com';

            // 1. Get User Details
            const userRes = await fetch(`${apiUrl}/api/users/telegram/${telegramId}`);

            if (!userRes.ok) {
                if (userRes.status === 404) {
                    setError("Siz ro'yxatdan o'tmagansiz. Iltimos, botda /start buyrug'ini bosing.");
                } else {
                    setError(`Server xatosi: ${userRes.status}`);
                }
                setLoading(false);
                return;
            }

            const userData = await userRes.json();
            const currentUser = userData.user;
            setUser(currentUser);

            // 2. Get User Stats (Last 30 days)
            const statsRes = await fetch(`${apiUrl}/api/attendance/user/${currentUser.id}/stats?days=30`);
            if (statsRes.ok) {
                const statsData = await statsRes.json();
                setStats(statsData.stats);
            }

            // 3. Get Today's Attendance
            const today = new Date().toISOString().split('T')[0];
            const attendanceRes = await fetch(`${apiUrl}/api/attendance/user/${currentUser.id}?start_date=${today}&end_date=${today}`);
            if (attendanceRes.ok) {
                const attendanceData = await attendanceRes.json();
                setTodayAttendance(attendanceData.attendance);
            }

        } catch (err) {
            console.error("Data fetch error:", err);
            setError("Ma'lumotlarni yuklashda xatolik yuz berdi.");
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="p-4 space-y-4 max-w-md mx-auto">
                <div className="flex items-center space-x-4">
                    <Skeleton className="h-12 w-12 rounded-full" />
                    <div className="space-y-2">
                        <Skeleton className="h-4 w-[200px]" />
                        <Skeleton className="h-4 w-[150px]" />
                    </div>
                </div>
                <Skeleton className="h-[120px] w-full rounded-xl" />
                <Skeleton className="h-[200px] w-full rounded-xl" />
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen p-6 text-center bg-gray-50">
                <AlertCircle className="h-12 w-12 text-red-500 mb-4" />
                <h1 className="text-xl font-bold mb-2 text-gray-900">Xatolik</h1>
                <p className="text-gray-600">{error}</p>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50/50 pb-20 font-sans">
            {/* Header */}
            <div className="bg-white p-6 shadow-sm border-b">
                <div className="flex items-center space-x-4 max-w-md mx-auto">
                    <div className="h-14 w-14 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 shadow-inner">
                        <UserIcon className="h-7 w-7" />
                    </div>
                    <div>
                        <h1 className="text-xl font-bold text-gray-900">{user?.full_name}</h1>
                        <Badge variant="secondary" className="mt-1 font-mono">
                            {user?.employee_id}
                        </Badge>
                    </div>
                </div>
            </div>

            <div className="p-4 space-y-6 max-w-md mx-auto mt-2">
                {/* Stats Cards */}
                <div className="grid grid-cols-3 gap-3">
                    <Card className="border-green-100 bg-green-50/50 shadow-sm">
                        <CardContent className="p-3 text-center">
                            <div className="text-2xl font-bold text-green-600">{stats?.present || 0}</div>
                            <div className="text-xs font-medium text-green-700 mt-1">Kelgan</div>
                        </CardContent>
                    </Card>
                    <Card className="border-yellow-100 bg-yellow-50/50 shadow-sm">
                        <CardContent className="p-3 text-center">
                            <div className="text-2xl font-bold text-yellow-600">{stats?.late || 0}</div>
                            <div className="text-xs font-medium text-yellow-700 mt-1">Kechikkan</div>
                        </CardContent>
                    </Card>
                    <Card className="border-red-100 bg-red-50/50 shadow-sm">
                        <CardContent className="p-3 text-center">
                            <div className="text-2xl font-bold text-red-600">{stats?.absent || 0}</div>
                            <div className="text-xs font-medium text-red-700 mt-1">Kelmagan</div>
                        </CardContent>
                    </Card>
                </div>

                {/* Today's Attendance */}
                <div className="space-y-3">
                    <div className="flex items-center justify-between px-1">
                        <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                            <CalendarDays className="h-5 w-5 text-blue-500" />
                            Bugungi davomat
                        </h2>
                        <span className="text-sm text-gray-500 bg-white px-2 py-1 rounded-md border shadow-sm">
                            {new Date().toLocaleDateString('uz-UZ')}
                        </span>
                    </div>

                    {todayAttendance.length > 0 ? (
                        todayAttendance.map((item) => (
                            <Card key={item.id} className="overflow-hidden border-l-4 border-l-blue-500 shadow-sm hover:shadow-md transition-shadow">
                                <CardContent className="p-4 flex justify-between items-center">
                                    <div>
                                        <h3 className="font-bold text-gray-900 text-lg">
                                            {item.schedule?.name || "Noma'lum dars"}
                                        </h3>
                                        <div className="flex items-center text-sm text-gray-500 mt-1 space-x-3">
                                            <span className="flex items-center gap-1 bg-gray-100 px-2 py-0.5 rounded">
                                                <Clock className="h-3 w-3" />
                                                {item.schedule?.start_time} - {item.schedule?.end_time}
                                            </span>
                                            {item.schedule?.room && (
                                                <span className="text-gray-400">| Xona: {item.schedule.room}</span>
                                            )}
                                        </div>
                                    </div>
                                    <div className="flex flex-col items-end gap-2">
                                        <Badge
                                            variant={
                                                item.status === 'present' ? 'default' :
                                                    item.status === 'late' ? 'secondary' : 'destructive'
                                            }
                                            className={`${item.status === 'present' ? 'bg-green-500 hover:bg-green-600' :
                                                    item.status === 'late' ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-red-500 hover:bg-red-600'
                                                }`}
                                        >
                                            {item.status === 'present' ? 'Keldi' :
                                                item.status === 'late' ? 'Kechikdi' : 'Kelmadi'}
                                        </Badge>
                                        <span className="text-xs font-mono text-gray-500 font-medium">
                                            {item.check_in_time.substring(0, 5)}
                                        </span>
                                    </div>
                                </CardContent>
                            </Card>
                        ))
                    ) : (
                        <Card className="border-dashed shadow-none bg-gray-50">
                            <CardContent className="p-8 text-center text-gray-500 flex flex-col items-center">
                                <Clock className="h-10 w-10 mb-3 text-gray-300" />
                                <p>Bugun uchun davomat ma'lumotlari yo'q</p>
                            </CardContent>
                        </Card>
                    )}
                </div>
            </div>
        </div>
    );
}

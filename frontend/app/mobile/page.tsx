"use client";

import { useEffect, useState, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import {
    CalendarDays,
    Clock,
    CheckCircle2,
    XCircle,
    AlertCircle,
    User as UserIcon,
    RefreshCw,
    History as HistoryIcon,
    Settings as SettingsIcon,
    ChevronLeft,
    Languages,
    Bell,
    BellOff
} from "lucide-react";
import { Language, getTranslation, translations } from "../../lib/i18n";

interface User {
    id: number;
    full_name: string;
    employee_id: string;
    telegram_chat_id: string;
    language: Language;
    telegram_notifications: boolean;
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
    schedule?: Schedule;
    date: string;
}

type View = 'dashboard' | 'history' | 'settings';

export default function MobilePage() {
    const [user, setUser] = useState<User | null>(null);
    const [stats, setStats] = useState<Stats | null>(null);
    const [todayAttendance, setTodayAttendance] = useState<Attendance[]>([]);
    const [historyAttendance, setHistoryAttendance] = useState<Attendance[]>([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [view, setView] = useState<View>('dashboard');
    const [lang, setLang] = useState<Language>('uz');

    const t = (key: keyof typeof translations['uz']) => getTranslation(lang, key);

    const fetchUserData = useCallback(async (telegramId: string, isRefresh = false) => {
        if (isRefresh) setRefreshing(true);
        else setLoading(true);

        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';

            // 1. Get User Details
            const userRes = await fetch(`${apiUrl}/api/users/telegram/${telegramId}`);

            if (!userRes.ok) {
                if (userRes.status === 404) {
                    setError(t('not_registered'));
                } else {
                    setError(`${t('error')}: ${userRes.status}`);
                }
                return;
            }

            const userData = await userRes.json();
            const currentUser = userData.user;
            setUser(currentUser);
            setLang(currentUser.language || 'uz');

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

            // 4. Get History (Last 7 days for history view)
            const weekAgo = new Date();
            weekAgo.setDate(weekAgo.getDate() - 7);
            const weekAgoStr = weekAgo.toISOString().split('T')[0];
            const historyRes = await fetch(`${apiUrl}/api/attendance/user/${currentUser.id}?start_date=${weekAgoStr}&end_date=${today}`);
            if (historyRes.ok) {
                const historyData = await historyRes.json();
                setHistoryAttendance(historyData.attendance);
            }

        } catch (err) {
            console.error("Data fetch error:", err);
            setError(t('error'));
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    }, [lang]);

    useEffect(() => {
        const initApp = async () => {
            try {
                // @ts-ignore
                const tg = window.Telegram?.WebApp;

                if (!tg || !tg.initDataUnsafe?.user) {
                    console.warn("Telegram WebApp not found or no user data");
                    // For development, you can set a mock ID
                    // await fetchUserData("7536540269"); 
                    setError(t('open_in_tg'));
                    setLoading(false);
                    return;
                }

                tg.ready();
                tg.expand();

                const telegramId = tg.initDataUnsafe.user.id.toString();
                await fetchUserData(telegramId);

            } catch (err) {
                console.error(err);
                setError(`${t('error')}: ${err instanceof Error ? err.message : String(err)}`);
                setLoading(false);
            }
        };

        initApp();
    }, []);

    const handleRefresh = () => {
        // @ts-ignore
        const telegramId = window.Telegram?.WebApp?.initDataUnsafe?.user?.id?.toString();
        if (telegramId) fetchUserData(telegramId, true);
    };

    const toggleNotifications = async () => {
        if (!user) return;
        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
            const tg = (window as any).Telegram?.WebApp;
            const telegramId = tg?.initDataUnsafe?.user?.id?.toString();

            if (!telegramId) return;

            const res = await fetch(`${apiUrl}/api/users/telegram/settings/${telegramId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ telegram_notifications: !user.telegram_notifications })
            });

            if (res.ok) {
                setUser({ ...user, telegram_notifications: !user.telegram_notifications });
            }
        } catch (err) {
            console.error(err);
        }
    };

    const changeLanguage = async (newLang: Language) => {
        if (!user) return;
        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
            const tg = (window as any).Telegram?.WebApp;
            const telegramId = tg?.initDataUnsafe?.user?.id?.toString();

            if (!telegramId) {
                setLang(newLang);
                return;
            }

            const res = await fetch(`${apiUrl}/api/users/telegram/settings/${telegramId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ language: newLang })
            });

            if (res.ok) {
                setLang(newLang);
                setUser({ ...user, language: newLang });
            }
        } catch (err) {
            console.error(err);
            setLang(newLang); // Fallback to local change
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
                <h1 className="text-xl font-bold mb-2 text-gray-900">{t('error')}</h1>
                <p className="text-gray-600">{error}</p>
                <Button variant="outline" className="mt-6" onClick={() => window.location.reload()}>
                    {t('refresh')}
                </Button>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50/50 pb-20 font-sans">
            {/* Header */}
            <div className="bg-white p-4 shadow-sm border-b sticky top-0 z-10">
                <div className="flex items-center justify-between max-w-md mx-auto">
                    {view !== 'dashboard' ? (
                        <Button variant="ghost" size="icon" onClick={() => setView('dashboard')}>
                            <ChevronLeft className="h-6 w-6" />
                        </Button>
                    ) : (
                        <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                            <UserIcon className="h-5 w-5" />
                        </div>
                    )}

                    <h1 className="text-lg font-bold text-gray-900">
                        {view === 'dashboard' ? t('welcome') : view === 'history' ? t('history') : t('settings')}
                    </h1>

                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={handleRefresh}
                        disabled={refreshing}
                        className={refreshing ? "animate-spin" : ""}
                    >
                        <RefreshCw className="h-5 w-5" />
                    </Button>
                </div>
            </div>

            <div className="p-4 space-y-6 max-w-md mx-auto">
                {view === 'dashboard' && (
                    <>
                        {/* User Info */}
                        <div className="flex items-center space-x-4 bg-white p-4 rounded-xl shadow-sm border">
                            <div className="h-12 w-12 rounded-full bg-blue-50 flex items-center justify-center text-blue-500">
                                <UserIcon className="h-6 w-6" />
                            </div>
                            <div>
                                <h2 className="font-bold text-gray-900">{user?.full_name}</h2>
                                <p className="text-xs text-gray-500 font-mono">{t('employee_id')}: {user?.employee_id}</p>
                            </div>
                        </div>

                        {/* Stats Cards */}
                        <div className="grid grid-cols-3 gap-3">
                            <Card className="border-green-100 bg-green-50/50 shadow-sm">
                                <CardContent className="p-3 text-center">
                                    <div className="text-2xl font-bold text-green-600">{stats?.present || 0}</div>
                                    <div className="text-[10px] font-medium text-green-700 mt-1 uppercase tracking-wider">{t('present')}</div>
                                </CardContent>
                            </Card>
                            <Card className="border-yellow-100 bg-yellow-50/50 shadow-sm">
                                <CardContent className="p-3 text-center">
                                    <div className="text-2xl font-bold text-yellow-600">{stats?.late || 0}</div>
                                    <div className="text-[10px] font-medium text-yellow-700 mt-1 uppercase tracking-wider">{t('late')}</div>
                                </CardContent>
                            </Card>
                            <Card className="border-red-100 bg-red-50/50 shadow-sm">
                                <CardContent className="p-3 text-center">
                                    <div className="text-2xl font-bold text-red-600">{stats?.absent || 0}</div>
                                    <div className="text-[10px] font-medium text-red-700 mt-1 uppercase tracking-wider">{t('absent')}</div>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Today's Attendance */}
                        <div className="space-y-3">
                            <div className="flex items-center justify-between px-1">
                                <h2 className="text-md font-semibold text-gray-900 flex items-center gap-2">
                                    <CalendarDays className="h-4 w-4 text-blue-500" />
                                    {t('today_attendance')}
                                </h2>
                                <Badge variant="outline" className="bg-white">
                                    {new Date().toLocaleDateString(lang === 'uz' ? 'uz-UZ' : lang === 'ru' ? 'ru-RU' : 'en-US')}
                                </Badge>
                            </div>

                            {todayAttendance.length > 0 ? (
                                todayAttendance.map((item) => (
                                    <AttendanceCard key={item.id} item={item} t={t} />
                                ))
                            ) : (
                                <Card className="border-dashed shadow-none bg-gray-50">
                                    <CardContent className="p-8 text-center text-gray-400 flex flex-col items-center">
                                        <Clock className="h-8 w-8 mb-2 opacity-20" />
                                        <p className="text-sm">{t('no_data_today')}</p>
                                    </CardContent>
                                </Card>
                            )}
                        </div>
                    </>
                )}

                {view === 'history' && (
                    <div className="space-y-4">
                        <h2 className="text-lg font-bold text-gray-900">{t('attendance_history')}</h2>
                        {historyAttendance.length > 0 ? (
                            historyAttendance.map((item) => (
                                <div key={item.id} className="space-y-2">
                                    <p className="text-[10px] font-bold text-gray-400 uppercase ml-1">{item.date}</p>
                                    <AttendanceCard item={item} t={t} />
                                </div>
                            ))
                        ) : (
                            <p className="text-center text-gray-500 py-10">{t('no_data_today')}</p>
                        )}
                    </div>
                )}

                {view === 'settings' && (
                    <div className="space-y-6">
                        <div className="space-y-3">
                            <h3 className="text-sm font-bold text-gray-400 uppercase tracking-widest ml-1">{t('language')}</h3>
                            <div className="grid grid-cols-1 gap-2">
                                {(['uz', 'ru', 'en'] as Language[]).map((l) => (
                                    <Button
                                        key={l}
                                        variant={lang === l ? "default" : "outline"}
                                        className="justify-start h-12 rounded-xl"
                                        onClick={() => changeLanguage(l)}
                                    >
                                        <Languages className="h-4 w-4 mr-3 opacity-70" />
                                        {l === 'uz' ? "O'zbekcha" : l === 'ru' ? "Русский" : "English"}
                                        {lang === l && <CheckCircle2 className="h-4 w-4 ml-auto" />}
                                    </Button>
                                ))}
                            </div>
                        </div>

                        <div className="space-y-3">
                            <h3 className="text-sm font-bold text-gray-400 uppercase tracking-widest ml-1">{t('notifications')}</h3>
                            <Button
                                variant="outline"
                                className="w-full justify-start h-12 rounded-xl"
                                onClick={toggleNotifications}
                            >
                                {user?.telegram_notifications ? (
                                    <Bell className="h-4 w-4 mr-3 text-green-500" />
                                ) : (
                                    <BellOff className="h-4 w-4 mr-3 text-gray-400" />
                                )}
                                {t('notifications')}
                                <Badge variant="secondary" className="ml-auto">
                                    {user?.telegram_notifications ? t('on') : t('off')}
                                </Badge>
                            </Button>
                        </div>
                    </div>
                )}
            </div>

            {/* Bottom Navigation */}
            <div className="fixed bottom-0 left-0 right-0 bg-white border-t p-2 flex justify-around items-center shadow-[0_-2px_10px_rgba(0,0,0,0.05)] max-w-md mx-auto">
                <NavButton
                    active={view === 'dashboard'}
                    onClick={() => setView('dashboard')}
                    icon={<UserIcon className="h-5 w-5" />}
                    label={t('welcome')}
                />
                <NavButton
                    active={view === 'history'}
                    onClick={() => setView('history')}
                    icon={<HistoryIcon className="h-5 w-5" />}
                    label={t('history')}
                />
                <NavButton
                    active={view === 'settings'}
                    onClick={() => setView('settings')}
                    icon={<SettingsIcon className="h-5 w-5" />}
                    label={t('settings')}
                />
            </div>
        </div>
    );
}

function AttendanceCard({ item, t }: { item: Attendance, t: any }) {
    return (
        <Card className="overflow-hidden border-l-4 border-l-blue-500 shadow-sm">
            <CardContent className="p-4 flex justify-between items-center">
                <div className="space-y-1">
                    <h3 className="font-bold text-gray-900 text-md leading-tight">
                        {item.schedule?.name || t('unknown_lesson')}
                    </h3>
                    <div className="flex items-center text-[10px] text-gray-500 space-x-2">
                        <span className="flex items-center gap-1 bg-gray-100 px-1.5 py-0.5 rounded">
                            <Clock className="h-3 w-3" />
                            {item.schedule?.start_time} - {item.schedule?.end_time}
                        </span>
                        {item.schedule?.room && (
                            <span className="text-gray-400">{t('room')}: {item.schedule.room}</span>
                        )}
                    </div>
                </div>
                <div className="flex flex-col items-end gap-1.5">
                    <Badge
                        variant={
                            item.status === 'present' ? 'default' :
                                item.status === 'late' ? 'secondary' : 'destructive'
                        }
                        className={`text-[10px] px-2 py-0 ${item.status === 'present' ? 'bg-green-500' :
                            item.status === 'late' ? 'bg-yellow-500' : 'bg-red-500'
                            }`}
                    >
                        {item.status === 'present' ? t('present') :
                            item.status === 'late' ? t('late') : t('absent')}
                    </Badge>
                    <span className="text-[10px] font-mono text-gray-400">
                        {item.check_in_time.substring(0, 5)}
                    </span>
                </div>
            </CardContent>
        </Card>
    );
}

function NavButton({ active, onClick, icon, label }: { active: boolean, onClick: () => void, icon: React.ReactNode, label: string }) {
    return (
        <button
            onClick={onClick}
            className={`flex flex-col items-center p-2 rounded-xl transition-all ${active ? 'text-blue-600 bg-blue-50' : 'text-gray-400 hover:text-gray-600'
                }`}
        >
            {icon}
            <span className="text-[10px] font-bold mt-1">{label}</span>
        </button>
    );
}

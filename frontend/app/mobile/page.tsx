"use client";

import { useEffect, useState, useCallback, useMemo } from "react";
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
import { UserInfo } from "@/components/mobile/UserInfo";
import { StatsGrid } from "@/components/mobile/StatsGrid";
import { AttendanceCard } from "@/components/mobile/AttendanceCard";
import { WeeklySchedule } from "@/components/mobile/WeeklySchedule";
import { SideDrawer } from "@/components/mobile/SideDrawer";
import { Card, CardContent } from "@/components/ui/card";

interface User {
    id: number;
    full_name: string;
    employee_id: string;
    telegram_chat_id: string;
    language: Language;
    telegram_notifications: boolean;
    course?: number;
    major?: string;
    faculty?: string;
    phone?: string;
    email?: string;
    groups?: { id: number; name: string; code: string }[];
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
    day_of_week: number;
    start_time: string;
    end_time: string;
    room?: string;
    teacher?: string;
}

interface Attendance {
    id: number;
    status: string;
    check_in_time: string;
    schedule_id?: number;
    schedule?: Schedule;
    date: string;
}

type View = 'dashboard' | 'history' | 'settings';

export default function MobilePage() {
    const [user, setUser] = useState<User | null>(null);
    const [stats, setStats] = useState<Stats | null>(null);
    const [schedules, setSchedules] = useState<Schedule[]>([]);
    const [todayAttendance, setTodayAttendance] = useState<Attendance[]>([]);
    const [historyAttendance, setHistoryAttendance] = useState<Attendance[]>([]);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [view, setView] = useState<View>('dashboard');
    const [lang, setLang] = useState<Language>('uz');
    const [loginId, setLoginId] = useState("");
    const [isManualLogin, setIsManualLogin] = useState(false);
    const [isProfileOpen, setIsProfileOpen] = useState(false);

    const t = (key: keyof typeof translations['uz']) => getTranslation(lang, key);

    const fetchUserData = useCallback(async (identifier: string, isTelegram = true, isRefresh = false) => {
        if (isRefresh) setRefreshing(true);
        else setLoading(true);

        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';

            let userRes;
            if (isTelegram) {
                userRes = await fetch(`${apiUrl}/api/users/telegram/${identifier}`);
            } else {
                userRes = await fetch(`${apiUrl}/api/users/employee/${identifier}`);
            }

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

            if (!isTelegram) {
                localStorage.setItem("davomatai_employee_id", identifier);
                setIsManualLogin(true);
            }

            // 2. Get User Stats (Last 30 days)
            const statsRes = await fetch(`${apiUrl}/api/attendance/user/${currentUser.id}/stats?days=30`);
            if (statsRes.ok) {
                const statsData = await statsRes.json();
                setStats(statsData.stats);
            }

            // 3. Get User Schedules
            const scheduleRes = await fetch(`${apiUrl}/api/schedules/user/${currentUser.id}`);
            if (scheduleRes.ok) {
                const scheduleData = await scheduleRes.json();
                setSchedules(scheduleData.schedules);
            }

            // 4. Get Today's Attendance
            const today = new Date().toISOString().split('T')[0];
            const attendanceRes = await fetch(`${apiUrl}/api/attendance/user/${currentUser.id}?start_date=${today}&end_date=${today}`);
            if (attendanceRes.ok) {
                const attendanceData = await attendanceRes.json();
                setTodayAttendance(attendanceData.attendance);
            }

            // 5. Get History (Last 30 days for history view)
            const monthAgo = new Date();
            monthAgo.setDate(monthAgo.getDate() - 30);
            const monthAgoStr = monthAgo.toISOString().split('T')[0];
            const historyRes = await fetch(`${apiUrl}/api/attendance/user/${currentUser.id}?start_date=${monthAgoStr}&end_date=${today}`);
            if (historyRes.ok) {
                const historyData = await historyRes.json();
                setHistoryAttendance(historyData.attendance);
            }

            setError(null);

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

                if (tg && tg.initDataUnsafe?.user) {
                    tg.ready();
                    tg.expand();
                    const telegramId = tg.initDataUnsafe.user.id.toString();
                    await fetchUserData(telegramId, true);
                } else {
                    console.warn("Telegram WebApp not found or no user data, checking localStorage");
                    const savedId = localStorage.getItem("davomatai_employee_id");
                    if (savedId) {
                        await fetchUserData(savedId, false);
                    } else {
                        setLoading(false);
                        setIsManualLogin(true);
                        setError(null); // Clear any potential error
                    }
                }

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
        if (telegramId) {
            fetchUserData(telegramId, true, true);
        } else {
            const savedId = localStorage.getItem("davomatai_employee_id");
            if (savedId) fetchUserData(savedId, false, true);
        }
    };

    const handleManualLogin = (e: React.FormEvent) => {
        e.preventDefault();
        if (loginId.trim()) {
            fetchUserData(loginId.trim(), false);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem("davomatai_employee_id");
        setUser(null);
        setIsManualLogin(true);
    };

    const toggleNotifications = async () => {
        if (!user) return;
        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
            const tg = (window as any).Telegram?.WebApp;
            const telegramId = tg?.initDataUnsafe?.user?.id?.toString();

            if (!telegramId && !isManualLogin) return;

            const identifier = telegramId || user.employee_id;
            const endpoint = telegramId
                ? `${apiUrl}/api/users/telegram/settings/${identifier}`
                : `${apiUrl}/api/users/${user.id}`; // Use standard update for manual

            const res = await fetch(endpoint, {
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
        if (!user) {
            setLang(newLang);
            return;
        }
        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
            const tg = (window as any).Telegram?.WebApp;
            const telegramId = tg?.initDataUnsafe?.user?.id?.toString();

            const identifier = telegramId || user.employee_id;
            const endpoint = telegramId
                ? `${apiUrl}/api/users/telegram/settings/${identifier}`
                : `${apiUrl}/api/users/${user.id}`;

            const res = await fetch(endpoint, {
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

    const groupedHistory = useMemo(() => {
        const groups: { [key: string]: Attendance[] } = {};
        historyAttendance.forEach(item => {
            const date = new Date(item.date);
            const month = date.toLocaleString(lang === 'uz' ? 'uz-UZ' : lang === 'ru' ? 'ru-RU' : 'en-US', { month: 'long', year: 'numeric' });
            if (!groups[month]) groups[month] = [];
            groups[month].push(item);
        });
        return groups;
    }, [historyAttendance, lang]);

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

    if (error && !isManualLogin) {
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

    if (!user && isManualLogin) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gray-50">
                <div className="w-full max-w-sm space-y-8">
                    <div className="text-center">
                        <div className="mx-auto h-16 w-16 rounded-2xl bg-blue-600 flex items-center justify-center text-white shadow-lg mb-4">
                            <UserIcon className="h-8 w-8" />
                        </div>
                        <h2 className="text-3xl font-extrabold text-gray-900 tracking-tight">DavomatAI</h2>
                        <p className="mt-2 text-sm text-gray-600">{t('login')}</p>
                    </div>

                    <Card className="border-none shadow-xl bg-white/80 backdrop-blur-sm">
                        <CardContent className="pt-6">
                            <form onSubmit={handleManualLogin} className="space-y-4">
                                <div className="space-y-2">
                                    <label className="text-xs font-bold text-gray-400 uppercase tracking-widest ml-1">
                                        {t('enter_employee_id')}
                                    </label>
                                    <input
                                        type="text"
                                        value={loginId}
                                        onChange={(e) => setLoginId(e.target.value)}
                                        placeholder="EMP001"
                                        className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all outline-none"
                                        required
                                    />
                                </div>

                                {error && (
                                    <div className="flex items-center gap-2 text-red-500 text-xs bg-red-50 p-3 rounded-lg">
                                        <AlertCircle className="h-4 w-4" />
                                        {error}
                                    </div>
                                )}

                                <Button type="submit" className="w-full h-12 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold shadow-md transition-all active:scale-95">
                                    {t('login')}
                                </Button>
                            </form>
                        </CardContent>
                    </Card>
                </div>
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
                        <Button variant="ghost" size="icon" onClick={() => setIsProfileOpen(true)} className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 p-0 hover:bg-blue-200">
                            <UserIcon className="h-5 w-5" />
                        </Button>
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
                        {/* UserInfo removed as per request */}
                        <StatsGrid stats={stats} t={t} />

                        <WeeklySchedule
                            schedules={schedules}
                            todayAttendance={todayAttendance}
                            t={t}
                            lang={lang}
                        />

                        <SideDrawer
                            user={user}
                            isOpen={isProfileOpen}
                            onClose={() => setIsProfileOpen(false)}
                            t={t}
                        />
                    </>
                )}

                {view === 'history' && (
                    <div className="space-y-6">
                        <div className="flex items-center justify-between px-1">
                            <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                                <HistoryIcon className="h-5 w-5 text-blue-500" />
                                {t('attendance_history')}
                            </h2>
                            <Badge variant="secondary" className="bg-blue-50 text-blue-600 border-blue-100">
                                Last 30 days
                            </Badge>
                        </div>

                        {Object.keys(groupedHistory).length > 0 ? (
                            Object.entries(groupedHistory).map(([month, records]) => (
                                <div key={month} className="space-y-4">
                                    <h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest sticky top-16 bg-gray-50/80 backdrop-blur-sm py-2 z-10">
                                        {month}
                                    </h3>
                                    <div className="space-y-3">
                                        {records.map((item) => (
                                            <div key={item.id} className="space-y-1">
                                                <p className="text-[10px] font-bold text-gray-400 uppercase ml-1">
                                                    {new Date(item.date).toLocaleDateString(lang === 'uz' ? 'uz-UZ' : lang === 'ru' ? 'ru-RU' : 'en-US', { day: 'numeric', weekday: 'short' })}
                                                </p>
                                                <AttendanceCard item={item} t={t} />
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="flex flex-col items-center justify-center py-20 text-gray-400">
                                <HistoryIcon className="h-12 w-12 mb-4 opacity-20" />
                                <p>{t('no_data_today')}</p>
                            </div>
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
                                        className={`justify-start h-12 rounded-xl ${lang === l ? 'bg-blue-600 hover:bg-blue-700' : ''}`}
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

                        {isManualLogin && (
                            <div className="pt-4 border-t">
                                <Button
                                    variant="destructive"
                                    className="w-full h-12 rounded-xl font-bold shadow-sm"
                                    onClick={handleLogout}
                                >
                                    <XCircle className="h-4 w-4 mr-2" />
                                    {t('logout')}
                                </Button>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Bottom Navigation */}
            <div className="fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-md border-t p-2 flex justify-around items-center shadow-[0_-2px_10px_rgba(0,0,0,0.05)] max-w-md mx-auto z-20">
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

function NavButton({ active, onClick, icon, label }: { active: boolean, onClick: () => void, icon: React.ReactNode, label: string }) {
    return (
        <button
            onClick={onClick}
            className={`flex flex-col items-center p-2 rounded-xl transition-all min-w-[64px] ${active ? 'text-blue-600 bg-blue-50' : 'text-gray-400 hover:text-gray-600'
                }`}
        >
            {icon}
            <span className="text-[10px] font-bold mt-1">{label}</span>
        </button>
    );
}

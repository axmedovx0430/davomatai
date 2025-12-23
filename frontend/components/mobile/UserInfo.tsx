import { User as UserIcon } from "lucide-react";

interface User {
    id: number;
    full_name: string;
    employee_id: string;
}

interface UserInfoProps {
    user: User | null;
    t: (key: any) => string;
    onClick?: () => void;
}

export function UserInfo({ user, t, onClick }: UserInfoProps) {
    if (!user) return null;

    return (
        <button
            onClick={onClick}
            className="w-full flex items-center space-x-4 bg-white p-4 rounded-xl shadow-sm border hover:bg-gray-50 transition-colors text-left"
        >
            <div className="h-12 w-12 rounded-full bg-blue-50 flex items-center justify-center text-blue-500">
                <UserIcon className="h-6 w-6" />
            </div>
            <div className="flex-1">
                <h2 className="font-bold text-gray-900">{user.full_name}</h2>
                <p className="text-xs text-gray-500 font-mono">{t('employee_id')}: {user.employee_id}</p>
            </div>
        </button>
    );
}

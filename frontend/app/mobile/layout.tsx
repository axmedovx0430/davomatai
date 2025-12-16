import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "DavomatAI Mobile",
    description: "DavomatAI Telegram Mini App",
};

export default function MobileLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
            <script src="https://telegram.org/js/telegram-web-app.js" async></script>
            {children}
        </div>
    );
}

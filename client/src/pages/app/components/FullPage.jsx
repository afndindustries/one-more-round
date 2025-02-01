import { Outlet } from "react-router-dom";
import Header from "./Header";
import Footer from "./Footer";

export default function FullPage() {
    return <>
        <Header />
        <main className="h-100">
            {/* This outlet component belongs to children in parent route */}
            <Outlet />
        </main>
        <Footer />
    </>
};
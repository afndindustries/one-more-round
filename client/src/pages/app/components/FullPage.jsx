import { Outlet } from "react-router-dom";
import Header from "./Header";
import Footer from "./Footer";

export default function FullPage() {
    return <>
        <header>
            <Header />
        </header>
        <main>
            {/* This outlet component belongs to children in parent route */}
            <Outlet />
        </main>
        <Footer />
    </>
};
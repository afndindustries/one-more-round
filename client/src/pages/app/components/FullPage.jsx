import { Outlet } from "react-router-dom";
import Header from "./Header";

export default function FullPage() {
    return <>
        <Header />
        <main>
            <Outlet />
        </main>
    </>
};
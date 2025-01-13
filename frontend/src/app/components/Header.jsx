import React from 'react';
import Link from "next/link";

function Header() {
    return (
        <header className="fixed top-0 left-0 right-0 bg-white shadow-md z-50">
            <nav className="container mx-auto p-4 flex justify-between items-center">
                <div className="flex items-center space-x-4">
                    <Link href="/">
                        <div className="flex items-center space-x-2">
                            <div className="text-xl text-gray-600 font-bold">GenX Tools:</div>
                            <div className="text-md font-light text-gray-700">Helps in growing businesses</div>
                        </div>
                    </Link>
                </div>
            </nav>
        </header>
    );
}

export default Header;

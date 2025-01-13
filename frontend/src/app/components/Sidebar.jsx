import React from 'react';
import Link from "next/link";
import Image from "next/image";
import { FaFileAlt, FaPlayCircle } from 'react-icons/fa';

function Sidebar({ cvDetection, textToVideo }) {
    return (
        <div className='h-full'>
            <nav className="bg-white text-gray-800 w-full lg:w-64 md:w-72 h-full p-4 shadow-lg rounded-lg">
                <div className="flex items-center justify-center mb-1 mt-16">
                    <div className="flex items-center justify-center rounded-full p-2 mt-28">
                        <Image src={`/assets/images/admin-logo.jpeg`} alt="Logo" width={90} height={90} />
                    </div>
                </div>
                <ul className="space-y-4 pt-6">
                    <li className="flex items-center space-x-3 ">
                        <FaFileAlt className="text-purple-900" size={20} />
                        <Link href={cvDetection} className="hover:text-gray-400 font-medium transition duration-200 ease-in-out">Cv Detection</Link>
                    </li>
                    <li className="flex items-center space-x-3 ">
                        <FaPlayCircle className="text-purple-900" size={20} />
                        <Link href={textToVideo} className="hover:text-gray-400 font-medium transition duration-200 ease-in-out">Text To Video</Link>
                    </li>
                </ul>
            </nav>
        </div>
    );
}

export default Sidebar;

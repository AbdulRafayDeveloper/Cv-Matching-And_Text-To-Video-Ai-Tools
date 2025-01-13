"use client"
import React, { useState } from 'react'
import Sidebar from '@/app/components/Sidebar';
import Header from '@/app/components/Header';
import Swal from "sweetalert2";
import axios from "axios";
import { useRouter } from 'next/navigation';

function page() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [formdata, setFormData] = useState({
        requirements: "",
        cv: "",
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        if (!formdata.requirements || !formdata.cv) {
            Swal.fire({
                icon: "error",
                title: "Validation Error",
                text: "Please fill the required fields",
            });
            setLoading(false);
            return;
        }

        const formData = new FormData();
        formData.append('requirements', formdata.requirements);
        formData.append('cv', formdata.cv);

        try {
            const response = await axios.post(`http://localhost:8000/api/cvDetection`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            console.log("response: ", response);
            console.log("Data: " + response.data.data);

            if (response.data.status === 200) {
                Swal.fire({
                    icon: "success",
                    title: "CV Match Analysis",
                    html: `
                        <div class="space-y-4">
                            <p>${response.data.data}</p>
                        </div>
                    `,
                    showCloseButton: true,
                    showConfirmButton: false,
                    customClass: {
                        popup: 'bg-white p-6 rounded-lg shadow-lg max-w-8xl mx-auto text-gray-800', // Increased max-width
                    }
                });
            } else {
                Swal.fire({
                    icon: "error",
                    title: "Error",
                    text: "CV does not match the requirements",
                });
            }
        } catch (error) {
            Swal.fire({
                icon: "error",
                title: "Error",
                text: "Something went wrong. Please try again later.",
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-screen overflow-hidden">
            <Sidebar
                cvDetection="../../cvDetect/add"
                textToVideo="../../"
            >
            </Sidebar>
            <div className="flex-1 overflow-auto relative">
                <Header></Header>
                <div className='absolute inset-0'>
                    <img
                        src="/assets/images/background.jpg"
                        className=' object-cover w-full h-52'
                        alt="Background"
                    />
                </div>
                <div className='relative z-10 p-4 overflow-y-auto h-full '>
                    <div className='bg-white shadow-md rounded-lg mx-auto max-w-xl p-8 mt-24'>
                        <h1 className='text-2xl font-medium  text-gray-600 mb-6 text-center'>CV Detection</h1>
                        <form
                            onSubmit={handleSubmit}
                            name="employeeForm"
                            id="employeeForm"
                            className="space-y-3"
                            method="post"
                            encType="multipart/form-data"
                        >
                            <div>
                                <label className="block text-gray-800 font-medium text-sm mb-2" htmlFor="requirements">Requirements</label>
                                <textarea
                                    rows={5}
                                    type="text"
                                    className="block w-full px-3 py-2 border rounded-lg text-gray-800 focus:ring focus:ring-blue-300"
                                    name="requirements"
                                    id="requirements"
                                    onChange={(e) => setFormData({ ...formdata, requirements: e.target.value })}
                                    placeholder="Enter Job Requirements"
                                />
                            </div>
                            <div>
                                <label className="block text-gray-800 font-medium text-sm mb-2" htmlFor="cv">Employee CV</label>
                                <input
                                    type="file"
                                    className="block w-full px-3 py-2 border rounded-lg text-gray-800 focus:ring focus:ring-blue-300"
                                    name="cv"
                                    id="cv"
                                    onChange={(e) => setFormData({ ...formdata, cv: e.target.files[0] })}
                                />
                            </div>
                            <div className="flex justify-end mt-4">
                                <button
                                    className={`bg-transparent border border-gray-400 text-gray-600 py-2 px-4 rounded-sm hover:bg-gray-500 hover:text-white focus:outline-none focus:shadow-outline transition duration-300 ease-in-out ${loading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-700'}`}
                                    type="submit"
                                    disabled={loading}
                                >
                                    {loading ? 'Detecting' : 'Check CV'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default page;

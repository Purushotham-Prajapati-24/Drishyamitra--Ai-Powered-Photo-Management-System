import React, { useState } from 'react';
import { Search, Upload, User, Image as ImageIcon } from 'lucide-react';
import MagicBento from '../components/ReactBits/MagicBento';

const Dashboard = () => {
    const [searchQuery, setSearchQuery] = useState('');

    const handleSearch = (e) => {
        e.preventDefault();
        // This will hit the Groq API endpoint built earlier
        console.log("Searching for:", searchQuery);
    };

    return (
        <div className="min-h-screen bg-void text-white p-6 md:p-12 font-sans md:ml-16">

            {/* Sidebar Navigation */}
            <nav className="fixed left-0 top-0 h-full w-16 bg-void border-r border-gray-800 hidden md:flex flex-col items-center py-8 gap-10 z-20">
                <div className="w-8 h-8 rounded-full bg-acid flex items-center justify-center text-void font-bold">D</div>
                <div className="flex flex-col gap-8 mt-4 text-gray-500">
                    <button className="hover:text-acid transition-colors cursor-pointer"><ImageIcon size={24} /></button>
                    <button className="hover:text-acid transition-colors cursor-pointer"><Search size={24} /></button>
                    <button className="hover:text-acid transition-colors cursor-pointer"><Upload size={24} /></button>
                </div>
                <div className="mt-auto">
                    <button className="hover:text-acid transition-colors text-gray-500 cursor-pointer"><User size={24} /></button>
                </div>
            </nav>

            <div className="max-w-7xl mx-auto">
                {/* Header & Conversational Search */}
                <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-6">
                    <div>
                        <h1 className="text-4xl font-bold tracking-tight">Your Archive</h1>
                        <p className="text-gray-400 mt-2">Relive your memories, intelligently curated.</p>
                    </div>

                    <form onSubmit={handleSearch} className="relative w-full md:w-96">
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            placeholder="Show me photos of Alice in London..."
                            className="w-full bg-gray-900 border border-gray-800 rounded-none py-3 pl-12 pr-4 text-white focus:outline-none focus:border-acid transition-colors placeholder:text-gray-500"
                        />
                        <button type="submit" className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 hover:text-acid transition-colors cursor-pointer">
                            <Search size={20} />
                        </button>
                    </form>
                </header>

                {/* Core Feature Area: Magic Bento Gallery */}
                <section className="mt-12">
                    <div className="flex justify-between items-end mb-6">
                        <h2 className="text-2xl font-bold">Spatial Curation</h2>
                        <button className="text-acid text-sm uppercase tracking-wider hover:underline cursor-pointer">View All</button>
                    </div>

                    <div className="w-full h-[600px] border border-gray-800 rounded-[24px] overflow-hidden bg-[#060010] p-4">
                        <MagicBento
                            glowColor="217, 246, 18" // Acid Green RGB (D9F612)
                            particleCount={15}
                            enableTilt={true}
                            enableSpotlight={true}
                        />
                    </div>
                </section>
            </div>
        </div>
    );
};

export default Dashboard;

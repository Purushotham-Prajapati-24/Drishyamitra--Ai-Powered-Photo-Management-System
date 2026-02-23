import React, { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { motion } from 'framer-motion';
import SplashCursor from '../components/ReactBits/SplashCursor';
import TiltedCard from '../components/ReactBits/TiltedCard';

gsap.registerPlugin(ScrollTrigger);

const LandingPage = () => {
    const heroRef = useRef(null);
    const textRef = useRef(null);
    const navigate = useNavigate();

    useEffect(() => {
        // Cinematic entrance animation
        const ctx = gsap.context(() => {
            gsap.from(textRef.current.children, {
                y: 100,
                opacity: 0,
                duration: 1.5,
                stagger: 0.2,
                ease: "power4.out",
                delay: 0.2
            });

            // Simple scroll trigger setup for the next section
            gsap.to(textRef.current, {
                yPercent: -50,
                opacity: 0,
                ease: "none",
                scrollTrigger: {
                    trigger: heroRef.current,
                    start: "top top",
                    end: "bottom top",
                    scrub: true,
                }
            });
        }, heroRef);

        return () => ctx.revert();
    }, []);

    return (
        <div className="relative bg-void w-full">
            {/* Splash Cursor for magical interactive experience */}
            <div className="fixed inset-0 pointer-events-none z-50 mix-blend-screen">
                <SplashCursor
                    COLOR_UPDATE_SPEED={10}
                    BACK_COLOR={{ r: 0.035, g: 0.035, b: 0.043 }} // Matches #09090B void
                    SPLAT_RADIUS={0.3}
                />
            </div>

            {/* Hero Section */}
            <section ref={heroRef} className="h-screen w-full flex flex-col items-center justify-center relative overflow-hidden">
                {/* Abstract Particle Background placeholder */}
                <div className="absolute inset-0 opacity-20 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-acid/20 via-void to-void pointer-events-none"></div>

                <div ref={textRef} className="z-10 text-center flex flex-col items-center gap-6 px-4">
                    <h1 className="text-7xl md:text-9xl font-bold tracking-tighter uppercase leading-[0.8] text-white mix-blend-difference">
                        Memory<br />
                        <span className="text-acid">Resurrected</span>
                    </h1>
                    <p className="max-w-xl text-lg md:text-xl text-gray-400 font-light mt-4">
                        Drishyamitra uses deep learning to breathe life into your static photos. Experience 3D spatial curation and narrative storytelling.
                    </p>
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => navigate('/auth')}
                        className="mt-8 px-8 py-4 bg-acid text-void font-bold text-lg rounded-none border border-acid hover:bg-transparent hover:text-acid transition-colors cursor-pointer"
                    >
                        Enter The Archive
                    </motion.button>
                </div>
            </section>

            {/* Scrollytelling Section */}
            <section className="h-[200vh] relative bg-void">
                <div className="sticky top-0 h-screen w-full flex flex-col md:flex-row items-center justify-center gap-12 p-8">
                    <div className="text-left w-full md:w-1/2">
                        <h2 className="text-5xl md:text-7xl font-bold text-white mb-6">Spatial <br /><span className="text-acid">Navigation</span></h2>
                        <p className="text-xl text-gray-400 max-w-md">
                            Break free from simple grids. Our AI understands the context, people, and emotions of your photos, creating a personalized spatial memory palace.
                        </p>
                    </div>
                    <div className="w-full md:w-1/2 flex justify-center">
                        <TiltedCard
                            imageSrc="https://images.unsplash.com/photo-1542038784456-1ea8e935640e?q=80&w=2670&auto=format&fit=crop"
                            altText="A beautiful spatial memory"
                            captionText="Resurrected Memory"
                            containerHeight="400px"
                            containerWidth="100%"
                            imageHeight="400px"
                            imageWidth="400px"
                            rotateAmplitude={12}
                            scaleOnHover={1.05}
                            showMobileWarning={false}
                            showTooltip={true}
                            displayOverlayContent={true}
                            overlayContent={
                                <p className="p-4 bg-void/80 backdrop-blur-md font-bold text-acid text-lg m-4 rounded-[4px]">
                                    AI Enhanced
                                </p>
                            }
                        />
                    </div>
                </div>
            </section>
        </div>
    );
};

export default LandingPage;

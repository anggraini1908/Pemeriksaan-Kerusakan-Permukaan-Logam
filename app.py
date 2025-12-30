# app.py - ENHANCED VERSION WITH HUMAN-FRIENDLY INTERPRETATION
import streamlit as st
import cv2
import numpy as np
import pywt
from PIL import Image
import io
import datetime
import zipfile

# ===============================
# KONFIGURASI HALAMAN
# ===============================
st.set_page_config(
    page_title="MetalAnalyzer Pro - Deteksi Kerusakan Logam",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===============================
# CSS CUSTOM - TEMA BIRU GRADASI PREMIUM + ENHANCEMENTS
# ===============================
st.markdown("""
<style>
:root {
    --primary-dark: #0A1A3A;
    --primary-blue: #1A3A7A;
    --secondary-blue: #2A5A9A;
    --accent-blue: #4A8AEA;
    --light-blue: #7AB6FF;
    --gradient-start: #0A1A3A;
    --gradient-middle: #1A3A7A;
    --gradient-end: #2A5A9A;
    --text-light: #FFFFFF;
    --text-semi: #E6F0FF;
    --text-muted: #B3CCFF;
    --card-bg: rgba(10, 26, 58, 0.85);
    --card-border: rgba(122, 182, 255, 0.2);
    --glow-color: rgba(122, 182, 255, 0.6);
    --status-good: #10B981;
    --status-warning: #F59E0B;
    --status-danger: #EF4444;
    --status-info: #3B82F6;
    --status-perfect: #8B5CF6;
}

/* Smooth transitions */
* {
    transition: background-color 0.3s ease, border-color 0.3s ease, transform 0.3s ease !important;
}

/* Background gradient premium */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, 
        var(--gradient-start) 0%, 
        var(--gradient-middle) 30%, 
        var(--primary-blue) 50%, 
        var(--secondary-blue) 70%, 
        var(--gradient-end) 100%
    );
    background-size: 300% 300%;
    animation: gradientFlow 20s ease infinite;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    position: relative;
    overflow-x: hidden;
    color: var(--text-light);
}

/* Animated background elements */
.background-glows {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
    overflow: hidden;
}

.glow {
    position: absolute;
    border-radius: 50%;
    background: radial-gradient(circle, var(--glow-color) 0%, transparent 70%);
    filter: blur(40px);
    opacity: 0.4;
    animation: floatGlow 15s infinite ease-in-out;
}

.glow-1 { 
    width: 300px; height: 300px; 
    top: 10%; left: 5%; 
    animation-delay: 0s; 
    background: radial-gradient(circle, rgba(74, 138, 234, 0.4) 0%, transparent 70%);
}
.glow-2 { 
    width: 400px; height: 400px; 
    bottom: 10%; right: 10%; 
    animation-delay: 2s; 
    background: radial-gradient(circle, rgba(26, 58, 122, 0.4) 0%, transparent 70%);
}
.glow-3 { 
    width: 250px; height: 250px; 
    top: 50%; right: 20%; 
    animation-delay: 4s; 
    background: radial-gradient(circle, rgba(122, 182, 255, 0.4) 0%, transparent 70%);
}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes floatGlow {
    0%, 100% { transform: translate(0, 0) scale(1); }
    25% { transform: translate(20px, 20px) scale(1.1); }
    50% { transform: translate(-15px, 10px) scale(0.9); }
    75% { transform: translate(10px, -15px) scale(1.05); }
}

/* Animasi teks dan elemen */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes float {
    0% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(5deg); }
    100% { transform: translateY(0px) rotate(0deg); }
}

@keyframes pulse {
    0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(122, 182, 255, 0.7); }
    70% { transform: scale(1.05); box-shadow: 0 0 0 20px rgba(122, 182, 255, 0); }
    100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(122, 182, 255, 0); }
}

@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes rotate-slow {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(-360deg); }
}

@keyframes buttonPress {
    0% { transform: scale(1); }
    50% { transform: scale(0.95); }
    100% { transform: scale(1); }
}

@keyframes ripple {
    0% {
        transform: scale(0, 0);
        opacity: 0.5;
    }
    20% {
        transform: scale(25, 25);
        opacity: 0.3;
    }
    100% {
        opacity: 0;
        transform: scale(40, 40);
    }
}

@keyframes dots {
    0%, 20% { content: ''; }
    40% { content: '.'; }
    60% { content: '..'; }
    80%, 100% { content: '...'; }
}

/* Title styles */
.main-title {
    font-size: 4.5rem;
    font-weight: 800;
    margin-bottom: 20px;
    background: linear-gradient(45deg, 
        #FFFFFF 25%, 
        #B3CCFF 50%, 
        #7AB6FF 75%, 
        #FFFFFF 100%
    );
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
    text-shadow: 0 0 30px rgba(122, 182, 255, 0.3);
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.5px;
    text-align: center;
}

.analysis-title {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 20px;
    background: linear-gradient(45deg, 
        #FFFFFF 25%, 
        #B3CCFF 50%, 
        #7AB6FF 75%, 
        #FFFFFF 100%
    );
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
    text-shadow: 0 0 25px rgba(122, 182, 255, 0.3);
    font-family: 'Inter', sans-serif;
    text-align: center;
    letter-spacing: -0.3px;
}

.main-subtitle {
    font-size: 1.8rem;
    color: var(--text-semi);
    margin-bottom: 40px;
    opacity: 0.95;
    font-weight: 500;
    animation: fadeInUp 1.2s ease-out 0.5s both;
    font-family: 'Inter', sans-serif;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
    text-align: center;
}

.analysis-subtitle {
    font-size: 1.6rem;
    color: var(--text-semi);
    margin-bottom: 30px;
    opacity: 0.95;
    font-weight: 500;
    animation: fadeInUp 1.2s ease-out 0.5s both;
    font-family: 'Inter', sans-serif;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
    text-align: center;
}

.time-stamp {
    font-size: 1rem;
    color: var(--text-muted);
    margin-top: 15px;
    letter-spacing: 1.5px;
    font-weight: 400;
    text-align: center;
    opacity: 0.9;
    animation: fadeInUp 1.5s ease-out 0.8s both;
    font-family: 'Inter', sans-serif;
}

.time-stamp::before {
    content: "🕒 ";
    margin-right: 8px;
}

/* SIDEBAR NAVIGASI */
[data-testid="stSidebar"] {
    background: rgba(10, 26, 58, 0.9) !important;
    backdrop-filter: blur(15px) !important;
    border-right: 2px solid rgba(122, 182, 255, 0.1) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

/* Navigation buttons premium */
.nav-container {
    background: rgba(10, 26, 58, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 15px;
    margin: 20px;
    border: 1px solid rgba(122, 182, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.nav-button {
    background: linear-gradient(135deg, 
        rgba(26, 58, 122, 0.8), 
        rgba(42, 90, 154, 0.8)
    );
    border: 2px solid rgba(122, 182, 255, 0.3);
    border-radius: 12px;
    padding: 15px 25px;
    color: var(--text-light) !important;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
    margin: 5px 0;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(5px);
    text-decoration: none !important;
}

.nav-button:hover {
    background: linear-gradient(135deg, 
        rgba(74, 138, 234, 0.9), 
        rgba(42, 90, 154, 0.9)
    );
    transform: translateY(-3px);
    border-color: var(--light-blue);
    box-shadow: 0 10px 25px rgba(74, 138, 234, 0.4);
}

.nav-button.active {
    background: linear-gradient(135deg, 
        var(--accent-blue), 
        var(--light-blue)
    );
    animation: pulse 2s infinite;
    border-color: var(--light-blue);
    box-shadow: 0 0 20px rgba(122, 182, 255, 0.5);
}

/* Hero section premium */
.hero-section {
    text-align: center;
    padding: 60px 20px;
    animation: fadeInUp 1s ease-out;
    position: relative;
    z-index: 1;
}

/* Animated elements container */
.animated-elements {
    position: relative;
    height: 200px;
    margin: 40px auto;
    width: 100%;
    max-width: 800px;
}

.gear-animated {
    animation: rotate 8s linear infinite;
    font-size: 100px;
    position: absolute;
    left: 20%;
    top: 20px;
    color: var(--light-blue);
    filter: drop-shadow(0 0 20px rgba(122, 182, 255, 0.6));
}

.gear-animated:nth-child(2) {
    animation: rotate-slow 6s linear infinite;
    font-size: 80px;
    right: 25%;
    top: 60px;
    color: var(--accent-blue);
}

.gear-animated:nth-child(3) {
    animation: rotate 4s linear infinite reverse;
    font-size: 60px;
    left: 40%;
    bottom: 20px;
    color: #FFFFFF;
}

.sparkle {
    position: absolute;
    font-size: 30px;
    animation: float 3s ease-in-out infinite;
    color: #FFFFFF;
    filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.8));
}

/* ENHANCED: Progress Ring */
.progress-ring {
    width: 120px;
    height: 120px;
    position: relative;
    margin: 0 auto 15px;
}

.progress-ring-circle {
    transform: rotate(-90deg);
    transform-origin: 50% 50%;
}

.progress-ring-bg {
    fill: none;
    stroke: rgba(122, 182, 255, 0.1);
    stroke-width: 8;
}

.progress-ring-fill {
    fill: none;
    stroke: var(--accent-blue);
    stroke-width: 8;
    stroke-linecap: round;
    transition: stroke-dashoffset 0.5s ease;
}

.progress-ring-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-light);
}

/* ENHANCED: Status Badges - UPDATED FOR HUMAN-FRIENDLY INTERPRETATION */
.status-badge {
    padding: 8px 20px;
    border-radius: 50px;
    font-weight: 700;
    font-size: 0.9rem;
    display: inline-block;
    margin: 5px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    color: var(--primary-dark) !important;
}

.status-perfect { 
    background: linear-gradient(135deg, var(--status-perfect), #A78BFA);
    color: white !important;
}
.status-good { 
    background: linear-gradient(135deg, var(--status-good), #34D399); 
}
.status-warning { 
    background: linear-gradient(135deg, var(--status-warning), #FBBF24); 
}
.status-danger { 
    background: linear-gradient(135deg, var(--status-danger), #F87171); 
}
.status-info { 
    background: linear-gradient(135deg, var(--status-info), #60A5FA); 
}

/* ENHANCED: Interpretasi Level */
.interpretation-level {
    display: flex;
    align-items: center;
    padding: 10px 20px;
    border-radius: 12px;
    margin: 10px 0;
    background: rgba(255, 255, 255, 0.1);
    border-left: 5px solid;
}

.interpretation-perfect { border-left-color: #8B5CF6; }
.interpretation-good { border-left-color: #10B981; }
.interpretation-minor { border-left-color: #F59E0B; }
.interpretation-moderate { border-left-color: #F97316; }
.interpretation-severe { border-left-color: #EF4444; }

.interpretation-icon {
    font-size: 2rem;
    margin-right: 15px;
}

.interpretation-content h4 {
    margin: 0 0 5px 0;
    color: var(--text-light);
}

.interpretation-content p {
    margin: 0;
    color: var(--text-semi);
    font-size: 0.9rem;
}

/* ENHANCED: Metric Box */
.metric-box {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    border: 1px solid rgba(122, 182, 255, 0.1);
    transition: all 0.3s ease;
}

.metric-box:hover {
    transform: translateY(-5px);
    border-color: var(--light-blue);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: var(--light-blue);
    margin-bottom: 5px;
}

.metric-label {
    font-size: 0.9rem;
    color: var(--text-muted);
    font-weight: 600;
}

/* ENHANCED: Image Grid */
.image-grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 25px;
    margin: 30px 0;
}

.image-card {
    background: var(--card-bg);
    border-radius: 15px;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid var(--card-border);
    cursor: pointer;
}

.image-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
    border-color: var(--light-blue);
}

.image-card-img {
    width: 100%;
    height: 250px;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.image-card:hover .image-card-img {
    transform: scale(1.05);
}

.image-card-content {
    padding: 20px;
}

.image-card-title {
    color: var(--text-light);
    font-weight: 700;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.image-card-badge {
    background: var(--accent-blue);
    color: var(--primary-dark);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
}

/* Features grid premium */
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    margin: 50px 0;
    padding: 20px;
}

.feature-card {
    background: var(--card-bg);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border: 1px solid var(--card-border);
    animation: fadeInUp 0.8s ease-out;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
}

.feature-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4),
                0 0 30px rgba(122, 182, 255, 0.3);
    border-color: var(--light-blue);
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, 
        var(--accent-blue), 
        var(--light-blue)
    );
    z-index: 2;
}

.feature-icon {
    font-size: 3.5rem;
    margin-bottom: 20px;
    display: inline-block;
    animation: float 3s ease-in-out infinite;
    filter: drop-shadow(0 0 10px rgba(122, 182, 255, 0.5));
}

.feature-title {
    font-size: 1.5rem;
    color: var(--text-light);
    margin-bottom: 15px;
    font-weight: 700;
    background: linear-gradient(45deg, #FFFFFF, #B3CCFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.feature-desc {
    color: var(--text-muted);
    line-height: 1.6;
    font-size: 1rem;
}

/* Stats counter premium */
.stats-container {
    background: var(--card-bg);
    border-radius: 25px;
    padding: 50px 40px;
    margin: 50px 0;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    animation: fadeInUp 1s ease-out 0.8s both;
    border: 1px solid var(--card-border);
    backdrop-filter: blur(10px);
}

.stats-title {
    text-align: center;
    font-size: 2.5rem;
    color: var(--text-light);
    margin-bottom: 50px;
    font-weight: 700;
    background: linear-gradient(45deg, #FFFFFF, #B3CCFF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 40px;
}

.stat-item {
    text-align: center;
    padding: 25px;
    background: rgba(10, 26, 58, 0.6);
    border-radius: 15px;
    border: 1px solid rgba(122, 182, 255, 0.1);
    transition: all 0.3s ease;
}

.stat-item:hover {
    transform: translateY(-5px);
    border-color: var(--light-blue);
    box-shadow: 0 10px 25px rgba(122, 182, 255, 0.2);
}

.stat-number {
    font-size: 3.5rem;
    font-weight: 800;
    color: var(--light-blue);
    margin-bottom: 15px;
    font-family: 'Inter', sans-serif;
    text-shadow: 0 0 20px rgba(122, 182, 255, 0.5);
}

.stat-label {
    font-size: 1.2rem;
    color: var(--text-muted);
    font-weight: 600;
}

/* CTA Button premium */
.cta-button {
    display: inline-block;
    background: linear-gradient(135deg, 
        var(--accent-blue), 
        var(--light-blue)
    );
    color: var(--primary-dark) !important;
    padding: 20px 50px;
    font-size: 1.4rem;
    font-weight: 700;
    border-radius: 15px;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(74, 138, 234, 0.4),
                0 0 20px rgba(122, 182, 255, 0.3);
    text-decoration: none;
    margin: 40px auto;
    animation: pulse 2s infinite;
    position: relative;
    overflow: hidden;
    font-family: 'Inter', sans-serif;
}

.cta-button:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 15px 35px rgba(74, 138, 234, 0.6),
                0 0 30px rgba(122, 182, 255, 0.5);
    color: var(--primary-dark) !important;
}

.cta-button::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, 
        transparent, 
        rgba(255, 255, 255, 0.3), 
        transparent
    );
    transition: left 0.7s ease;
}

.cta-button:hover::after {
    left: 100%;
}

/* Analysis container premium */
.analysis-container {
    background: var(--card-bg);
    border-radius: 25px;
    padding: 40px;
    margin: 30px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    border: 1px solid var(--card-border);
    backdrop-filter: blur(10px);
}

/* ENHANCED: Upload Section */
.upload-section {
    background: var(--card-bg);
    border-radius: 20px;
    padding: 40px;
    margin: 30px 0;
    border: 2px dashed var(--card-border);
    text-align: center;
    transition: all 0.3s ease;
}

.upload-section:hover {
    border-color: var(--light-blue);
    background: rgba(10, 26, 58, 0.95);
}

.result-card {
    background: rgba(10, 26, 58, 0.7);
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    border-left: 5px solid var(--accent-blue);
    animation: fadeInUp 0.5s ease-out;
    border: 1px solid rgba(122, 182, 255, 0.1);
    transition: all 0.3s ease;
}

.result-card:hover {
    transform: translateY(-3px);
    border-color: var(--light-blue);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3),
                0 0 20px rgba(122, 182, 255, 0.2);
}

/* About page styles premium */
.about-description {
    font-size: 1.3rem;
    line-height: 1.8;
    color: var(--text-semi);
    margin: 40px 0;
    padding: 40px;
    background: var(--card-bg);
    border-radius: 25px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    animation: fadeInUp 0.8s ease-out;
    border-left: 6px solid var(--accent-blue);
    font-family: 'Inter', sans-serif;
    backdrop-filter: blur(10px);
    border: 1px solid var(--card-border);
}

.about-description strong {
    color: var(--light-blue);
    font-weight: 700;
}

/* Tech items premium */
.tech-item {
    padding: 25px;
    background: rgba(10, 26, 58, 0.7);
    border-radius: 20px;
    text-align: center;
    border: 1px solid rgba(122, 182, 255, 0.1);
    transition: all 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.tech-item:hover {
    transform: translateY(-8px);
    border-color: var(--light-blue);
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3),
                0 0 25px rgba(122, 182, 255, 0.3);
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: rgba(10, 26, 58, 0.8);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(45deg, 
        var(--accent-blue), 
        var(--light-blue)
    );
    border-radius: 10px;
    border: 2px solid rgba(10, 26, 58, 0.8);
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(45deg, 
        var(--light-blue), 
        var(--accent-blue)
    );
}

/* Input and form elements styling - ENHANCED */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div,
.stSlider > div > div {
    background: rgba(10, 26, 58, 0.8) !important;
    color: white !important;
    border: 1px solid rgba(122, 182, 255, 0.3) !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--light-blue) !important;
    box-shadow: 0 0 0 2px rgba(122, 182, 255, 0.2) !important;
}

/* ENHANCED: Touch-friendly controls */
.stSlider > div > div > div > div {
    height: 12px !important;
}

.stSlider > div > div > div > div > div {
    width: 24px !important;
    height: 24px !important;
    transition: transform 0.2s ease !important;
}

.stSlider > div > div > div > div > div:hover {
    transform: scale(1.2);
}

.stCheckbox > label {
    padding: 12px 0 !important;
    font-size: 1.1rem !important;
}

.stSelectbox > div > div {
    min-height: 50px !important;
    padding: 12px !important;
}

/* ENHANCED: Button styles */
.stButton > button {
    background: linear-gradient(135deg, 
        rgba(26, 58, 122, 0.8), 
        rgba(42, 90, 154, 0.8)
    ) !important;
    color: white !important;
    border: 1px solid rgba(122, 182, 255, 0.3) !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    position: relative;
    overflow: hidden;
}

.stButton > button:hover {
    background: linear-gradient(135deg, 
        rgba(74, 138, 234, 0.9), 
        rgba(42, 90, 154, 0.9)
    ) !important;
    border-color: var(--light-blue) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 20px rgba(74, 138, 234, 0.4) !important;
}

.stButton > button:active {
    animation: buttonPress 0.2s ease !important;
}

/* Ripple effect for buttons */
.ripple-button {
    position: relative;
    overflow: hidden;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(10, 26, 58, 0.8) !important;
    border-radius: 12px !important;
    padding: 10px !important;
    border: 1px solid rgba(122, 182, 255, 0.2) !important;
}

.stTabs [data-baseweb="tab"] {
    color: var(--text-muted) !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, 
        var(--accent-blue), 
        var(--light-blue)
    ) !important;
    color: var(--primary-dark) !important;
    font-weight: 700 !important;
}

/* Progress bar styling */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, 
        var(--accent-blue), 
        var(--light-blue)
    ) !important;
    border-radius: 10px !important;
}

/* Expander styling */
.streamlit-expanderHeader {
    background: rgba(10, 26, 58, 0.8) !important;
    color: var(--text-light) !important;
    border: 1px solid rgba(122, 182, 255, 0.2) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.streamlit-expanderHeader:hover {
    border-color: var(--light-blue) !important;
    background: rgba(10, 26, 58, 0.9) !important;
}

.streamlit-expanderContent {
    background: rgba(10, 26, 58, 0.6) !important;
    border: 1px solid rgba(122, 182, 255, 0.1) !important;
    border-radius: 0 0 10px 10px !important;
    color: var(--text-semi) !important;
}

/* File uploader styling */
.stFileUploader > div {
    background: rgba(10, 26, 58, 0.8) !important;
    border: 2px dashed rgba(122, 182, 255, 0.3) !important;
    border-radius: 15px !important;
    color: var(--text-light) !important;
    transition: all 0.3s ease !important;
}

.stFileUploader > div:hover {
    border-color: var(--light-blue) !important;
    background: rgba(10, 26, 58, 0.9) !important;
}

/* Success and info messages */
.stAlert {
    background: rgba(10, 26, 58, 0.9) !important;
    border: 1px solid rgba(122, 182, 255, 0.3) !important;
    border-radius: 12px !important;
    color: var(--text-light) !important;
    backdrop-filter: blur(10px) !important;
}

/* Footer styling */
.app-footer {
    text-align: center;
    margin-top: 80px;
    padding: 40px;
    border-top: 1px solid rgba(122, 182, 255, 0.1);
    background: rgba(10, 26, 58, 0.7);
    border-radius: 20px 20px 0 0;
    backdrop-filter: blur(10px);
}

/* ENHANCED: Section Spacer */
.section-spacer {
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(122, 182, 255, 0.2), transparent);
    margin: 40px 0;
    border-radius: 10px;
}

/* ENHANCED: Processing Animation */
.processing-animation {
    display: inline-block;
    width: 80px;
    height: 80px;
    margin: 0 auto 30px;
    border: 4px solid var(--card-border);
    border-top: 4px solid var(--accent-blue);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

.processing-text {
    display: inline-block;
    font-size: 1.2rem;
    color: var(--text-light);
    font-weight: 600;
    background: linear-gradient(90deg, 
        var(--text-light) 0%, 
        var(--accent-blue) 50%, 
        var(--text-light) 100%
    );
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 2s linear infinite;
}

.processing-dots::after {
    content: '';
    animation: dots 1.5s steps(4, end) infinite;
}

/* ENHANCED: Timeline */
.timeline-step {
    text-align: center;
    margin: 0 5px;
}

.timeline-circle {
    width: 50px;
    height: 50px;
    margin: 0 auto 10px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

/* ENHANCED: Achievement Badge */
.achievement-badge {
    background: linear-gradient(135deg, rgba(122, 182, 255, 0.1), rgba(74, 138, 234, 0.1));
    border-radius: 15px;
    padding: 15px;
    text-align: center;
    border: 1px solid rgba(122, 182, 255, 0.2);
    transition: all 0.3s ease;
}

.achievement-badge:hover {
    transform: translateY(-5px);
    border-color: var(--light-blue);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

/* ENHANCED: Confidence Meter */
.confidence-meter {
    height: 20px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    margin: 10px 0;
    overflow: hidden;
}

.confidence-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 0.5s ease;
}

.confidence-high { background: linear-gradient(90deg, #10B981, #34D399); }
.confidence-medium { background: linear-gradient(90deg, #F59E0B, #FBBF24); }
.confidence-low { background: linear-gradient(90deg, #EF4444, #F87171); }

/* Responsive design - ENHANCED */
@media (max-width: 768px) {
    .main-title {
        font-size: 2.5rem;
        line-height: 1.2;
    }
    
    .analysis-title {
        font-size: 2rem;
    }
    
    .main-subtitle {
        font-size: 1.2rem;
    }
    
    .analysis-subtitle {
        font-size: 1.1rem;
    }
    
    .features-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
        gap: 20px;
    }
    
    .gear-animated {
        font-size: 60px;
    }
    
    .image-grid-container {
        grid-template-columns: 1fr;
        gap: 15px;
    }
    
    .metric-box {
        padding: 15px;
    }
    
    .metric-value {
        font-size: 1.5rem;
    }
    
    /* Floating action button untuk sidebar mobile */
    .fab-sidebar {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        background: var(--accent-blue);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.5rem;
        z-index: 10000;
        box-shadow: 0 10px 25px rgba(74, 138, 234, 0.4);
        animation: float 3s ease-in-out infinite;
    }
}
</style>

<div class="background-glows">
    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>
    <div class="glow glow-3"></div>
</div>
""", unsafe_allow_html=True)

# ===============================
# NAVIGASI PREMIUM
# ===============================
def create_navigation():
    """Menu: Home, Analisis, Tentang Kami dengan desain premium"""
    st.markdown("""
    <div class="nav-container">
        <div style="display: flex; gap: 20px; align-items: center; justify-content: center;">
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏠 HOME", use_container_width=True, key="nav_home", type="primary" if st.session_state.get('page') == 'home' else "secondary"):
            st.session_state.page = 'home'
            st.rerun()
    
    with col2:
        if st.button("🔧 ANALISIS", use_container_width=True, key="nav_analyze", type="primary" if st.session_state.get('page') == 'analyze' else "secondary"):
            st.session_state.page = 'analyze'
            st.rerun()
    
    with col3:
        if st.button("👨‍🔬 TENTANG KAMI", use_container_width=True, key="nav_about", type="primary" if st.session_state.get('page') == 'about' else "secondary"):
            st.session_state.page = 'about'
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ===============================
# FUNGSI INTERPRETASI HUMAN-FRIENDLY
# ===============================
def get_interpretation_info(cd_score, edge_count, num_detections):
    """
    Fungsi untuk interpretasi hasil yang lebih human-friendly
    Berdasarkan kombinasi multiple faktor, bukan hanya skor
    """
    
    # Faktor-faktor yang dipertimbangkan
    score_factor = cd_score
    edge_density = edge_count / 10000  # Normalisasi
    detection_density = num_detections / 10  # Normalisasi
    
    # Skor gabungan dengan bobot
    combined_score = (
        score_factor * 0.5 + 
        min(edge_density * 20, 100) * 0.3 + 
        min(detection_density * 30, 100) * 0.2
    )
    
    # =============== LEVEL INTERPRETASI ===============
    
    # 1. PERFECT CONDITION (0-5%)
    if combined_score <= 5:
        level = "PERFECT"
        color = "#8B5CF6"  # Ungu
        icon = "✨"
        status_class = "status-perfect"
        interpretation = "🟢 KONDISI SEMPURNA"
        detail = (
            "Permukaan logam dalam kondisi sangat baik. "
            "Tidak terdeteksi kerusakan yang signifikan. "
            "Tekstur permukaan normal, tidak ada retak, korosi, atau cacat yang terdeteksi."
        )
        recommendation = (
            "✅ TIDAK PERLU TINDAKAN\n"
            "• Lanjutkan penggunaan normal\n"
            "• Rutin lakukan inspeksi visual setiap 6 bulan\n"
            "• Pertahankan kondisi dengan cleaning rutin"
        )
        confidence = "Sangat Tinggi (95%)"
        next_check = "6 bulan"
        
    # 2. GOOD CONDITION (5-15%)
    elif combined_score <= 15:
        level = "GOOD"
        color = "#10B981"  # Hijau
        icon = "✅"
        status_class = "status-good"
        interpretation = "🟢 KONDISI BAIK"
        detail = (
            "Permukaan logam dalam kondisi baik. "
            "Terdeteksi sedikit variasi tekstur atau goresan superfisial yang tidak memengaruhi integritas struktural. "
            "Biasanya hanya noise pada gambar atau tekstur alami material."
        )
        recommendation = (
            "✅ PEMANTAUAN RUTIN\n"
            "• Lanjutkan penggunaan normal\n"
            "• Inspeksi visual setiap 3 bulan\n"
            "• Dokumentasikan perubahan kondisi"
        )
        confidence = "Tinggi (85%)"
        next_check = "3 bulan"
        
    # 3. MINOR ANOMALY (15-25%)
    elif combined_score <= 25:
        level = "MINOR"
        color = "#F59E0B"  # Kuning
        icon = "⚠️"
        status_class = "status-warning"
        interpretation = "🟡 ANOMALI MINOR"
        detail = (
            "Terdeteksi perubahan tekstur minor atau goresan ringan. "
            "Bisa berupa korosi awal, goresan permukaan, atau variasi manufaktur. "
            "Belum membahayakan struktural, tetapi perlu dipantau."
        )
        recommendation = (
            "🟡 PEMANTAUAN INTENSIF\n"
            "• Periksa area yang terdeteksi secara manual\n"
            "• Dokumentasi foto kondisi saat ini\n"
            "• Inspeksi ulang dalam 1 bulan\n"
            "• Pertimbangkan coating protective"
        )
        confidence = "Sedang (75%)"
        next_check = "1 bulan"
        
    # 4. MODERATE DAMAGE (25-40%)
    elif combined_score <= 40:
        level = "MODERATE"
        color = "#F97316"  # Oranye
        icon = "🔸"
        status_class = "status-warning"
        interpretation = "🟠 KERUSAKAN MODERAT"
        detail = (
            "Terdeteksi kerusakan sedang seperti korosi lokal, retak kecil, atau cacat permukaan. "
            "Masih dalam batas aman untuk penggunaan, tetapi perlu evaluasi lebih lanjut."
        )
        recommendation = (
            "🟠 EVALUASI MENDALAM\n"
            "• Lakukan inspeksi fisik oleh ahli\n"
            "• Ukur kedalaman kerusakan jika memungkinkan\n"
            "• Pertimbangkan perbaikan lokal\n"
            "• Batasi beban kerja jika perlu"
        )
        confidence = "Sedang (70%)"
        next_check = "2 minggu"
        
    # 5. SEVERE DAMAGE (40-100%)
    else:
        level = "SEVERE"
        color = "#EF4444"  # Merah
        icon = "🚨"
        status_class = "status-danger"
        interpretation = "🔴 KERUSAKAN BERAT"
        detail = (
            "Kerusakan signifikan terdeteksi! Kemungkinan retak besar, korosi parah, "
            "atau cacat struktural. Memerlukan perhatian segera untuk mencegah kegagalan."
        )
        recommendation = (
            "🔴 TINDAKAN SEGERA\n"
            "• Hentikan penggunaan sementara\n"
            "• Konsultasi dengan engineer material\n"
            "• Lakukan NDT testing (ultrasonic, x-ray)\n"
            "• Rencanakan perbaikan atau replacement"
        )
        confidence = "Tinggi (80%)"
        next_check = "SEGERA"
    
    return {
        "level": level,
        "color": color,
        "icon": icon,
        "status_class": status_class,
        "interpretation": interpretation,
        "detail": detail,
        "recommendation": recommendation,
        "confidence": confidence,
        "next_check": next_check,
        "combined_score": combined_score
    }

# ===============================
# HOMEPAGE PREMIUM
# ===============================
def create_homepage():
    """Homepage dengan desain premium"""
    
    # Header dengan animasi
    st.markdown("""
    <div class="hero-section">
        <div class="animated-elements">
            <div class="gear-animated">⚙️</div>
            <div class="gear-animated">🔧</div>
            <div class="gear-animated">✨</div>
            <div class="sparkle" style="left: 15%; top: 80px;">⭐</div>
            <div class="sparkle" style="right: 15%; top: 40px;">✨</div>
            <div class="sparkle" style="left: 30%; bottom: 60px;">🌟</div>
            <div class="sparkle" style="right: 30%; bottom: 100px;">💫</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Deskripsi aplikasi
    st.markdown("""
    <div class="about-description">
        <p style="text-align: center; font-size: 1.2rem; line-height: 1.8;">
            ✨ <strong style="color: var(--light-blue);">Platform revolusioner</strong> untuk analisis kerusakan permukaan logam dengan teknologi kecerdasan buatan terkini. 
            Sistem kami menyajikan perbandingan hasil analisis dan menghasilkan laporan otomatis untuk mendukung evaluasi material 
            yang lebih akurat dan efisien. Menggunakan algoritma computer vision terbaru untuk mendeteksi retakan, korosi, 
            dan berbagai jenis cacat pada permukaan logam dengan tingkat akurasi yang sangat tinggi. ✨
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features
    st.markdown("""
    <div style="text-align: center; margin: 50px 0;">
        <h2 style="font-size: 2.5rem; color: var(--text-light); margin-bottom: 30px; 
                   background: linear-gradient(45deg, #FFFFFF, #B3CCFF);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text;">
            🔥 FITUR UNGGULAN
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3 class="feature-title">AI INTERPRETASI</h3>
            <p class="feature-desc">
                Interpretasi hasil yang human-friendly dengan level kerusakan yang jelas
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3 class="feature-title">REAL-TIME</h3>
            <p class="feature-desc">
                Proses analisis dalam hitungan detik dengan hasil real-time
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">DETAILED REPORT</h3>
            <p class="feature-desc">
                Laporan lengkap dengan visualisasi dan rekomendasi tindakan
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Section Spacer
    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
    
    # LEVEL INTERPRETASI VISUAL
    st.markdown("""
    <div class="stats-container">
        <h2 class="stats-title">📊 SISTEM INTERPRETASI</h2>
        <div class="stats-grid">
            <div class="stat-item">
                <div style="font-size: 3rem; margin-bottom: 10px;">✨</div>
                <div class="stat-number">0-5%</div>
                <div class="stat-label">SEMPURNA</div>
                <div style="color: #8B5CF6; font-weight: 600; margin-top: 5px;">Kondisi Ideal</div>
            </div>
            <div class="stat-item">
                <div style="font-size: 3rem; margin-bottom: 10px;">✅</div>
                <div class="stat-number">5-15%</div>
                <div class="stat-label">BAIK</div>
                <div style="color: #10B981; font-weight: 600; margin-top: 5px;">Normal</div>
            </div>
            <div class="stat-item">
                <div style="font-size: 3rem; margin-bottom: 10px;">⚠️</div>
                <div class="stat-number">15-25%</div>
                <div class="stat-label">MINOR</div>
                <div style="color: #F59E0B; font-weight: 600; margin-top: 5px;">Pemantauan</div>
            </div>
            <div class="stat-item">
                <div style="font-size: 3rem; margin-bottom: 10px;">🔸</div>
                <div class="stat-number">25-40%</div>
                <div class="stat-label">MODERAT</div>
                <div style="color: #F97316; font-weight: 600; margin-top: 5px;">Evaluasi</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tombol mulai analisis
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 50px 0;">
        """, unsafe_allow_html=True)
        
        if st.button("🚀 MULAI ANALISIS SEKARANG", use_container_width=True, type="primary"):
            st.session_state.page = 'analyze'
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="app-footer">
        <div style="font-size: 3rem; margin-bottom: 20px; color: var(--light-blue);">
            ⚙️ 🔧 ✨
        </div>
        <h3 style="color: var(--text-light); margin-bottom: 15px; font-size: 1.8rem;">
            MetalAnalyzer Pro v2.0
        </h3>
        <p style="color: var(--text-muted); margin-bottom: 10px; font-size: 1.1rem;">
            Solusi Analisis Kerusakan Logam Berbasis AI
        </p>
        <p style="color: var(--text-muted); opacity: 0.8; font-size: 0.9rem;">
            © 2024 - All Rights Reserved | Precision in Every Pixel
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===============================
# HALAMAN TENTANG KAMI PREMIUM
# ===============================
def show_about_page():
    """Halaman tentang kami dengan desain premium"""
    
    # Header
    st.markdown("""
    <div class="hero-section">
        <div class="animated-elements">
            <div class="gear-animated">👨‍🔬</div>
            <div class="gear-animated">🔬</div>
            <div class="gear-animated">💡</div>
            <div class="sparkle" style="left: 15%; top: 80px;">⭐</div>
            <div class="sparkle" style="right: 15%; top: 40px;">✨</div>
            <div class="sparkle" style="right: 30%; bottom: 100px;">💫</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Deskripsi tentang kami
    st.markdown("""
    <div class="about-description">
        <p style="text-align: center;">
            <strong style="color: var(--light-blue); font-size: 1.4rem;">MetalAnalyzer Pro</strong> adalah platform analisis kerusakan logam berbasis kecerdasan buatan 
            yang dikembangkan untuk membantu insinyur, teknisi, dan profesional di bidang material science 
            dalam mendeteksi dan menganalisis kerusakan pada permukaan logam secara cepat dan akurat.
        </p>
        <p style="text-align: center;">
            Dengan menggunakan teknologi <strong>Computer Vision</strong> dan <strong>Machine Learning</strong> terkini, 
            aplikasi ini mampu mendeteksi berbagai jenis kerusakan seperti retak, korosi, goresan, 
            dan cacat permukaan lainnya dengan tingkat akurasi yang tinggi.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Misi dan Visi
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">MISI KAMI</h3>
            <p class="feature-desc">
                Menyediakan solusi analisis kerusakan logam yang cepat, akurat, dan mudah digunakan 
                untuk meningkatkan efisiensi dan akurasi dalam inspeksi material industri.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <h3 class="feature-title">VISI KAMI</h3>
            <p class="feature-desc">
                Menjadi platform terdepan dalam analisis material berbasis AI yang diakui secara global 
                untuk mendukung industri manufaktur yang lebih aman dan efisien.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Section Spacer
    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
    
    # Tombol kembali ke home
    st.markdown("""
    <div style="text-align: center; margin: 60px 0;">
    """, unsafe_allow_html=True)
    
    if st.button("🏠 KEMBALI KE HOME", use_container_width=True, type="primary"):
        st.session_state.page = 'home'
        st.rerun()

# ===============================
# FUNGSI UTILITAS VISUAL ENHANCED
# ===============================
def create_progress_ring(score, label, color="var(--accent-blue)"):
    """Create SVG progress ring"""
    circumference = 2 * 3.14159 * 45
    offset = circumference - (score / 100) * circumference
    
    return f"""
    <div class="progress-ring">
        <svg width="120" height="120" class="progress-ring-circle">
            <circle class="progress-ring-bg" cx="60" cy="60" r="45"></circle>
            <circle class="progress-ring-fill" 
                    cx="60" cy="60" r="45"
                    stroke="{color}"
                    stroke-dasharray="{circumference}"
                    stroke-dashoffset="{offset}"></circle>
        </svg>
        <div class="progress-ring-text">
            {int(score)}%
        </div>
    </div>
    <div style="text-align: center; margin-top: 10px; color: var(--text-muted);">
        {label}
    </div>
    """

def create_interpretation_card(info):
    """Create interpretation card with human-friendly info"""
    
    color_classes = {
        "PERFECT": "interpretation-perfect",
        "GOOD": "interpretation-good",
        "MINOR": "interpretation-minor",
        "MODERATE": "interpretation-moderate",
        "SEVERE": "interpretation-severe"
    }
    
    return f"""
    <div class="{color_classes.get(info['level'], 'interpretation-good')}">
        <div class="interpretation-icon">
            {info['icon']}
        </div>
        <div class="interpretation-content">
            <h4>{info['interpretation']}</h4>
            <p>{info['detail']}</p>
        </div>
    </div>
    """

def create_confidence_meter(confidence_text):
    """Create confidence meter based on confidence text"""
    if "Sangat Tinggi" in confidence_text:
        width = 95
        cls = "confidence-high"
    elif "Tinggi" in confidence_text:
        width = 85
        cls = "confidence-high"
    elif "Sedang" in confidence_text:
        width = 75
        cls = "confidence-medium"
    else:
        width = 65
        cls = "confidence-low"
    
    return f"""
    <div style="margin: 10px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span style="color: var(--text-light);">Tingkat Kepercayaan:</span>
            <span style="color: var(--text-light); font-weight: 600;">{confidence_text}</span>
        </div>
        <div class="confidence-meter">
            <div class="confidence-fill {cls}" style="width: {width}%;"></div>
        </div>
    </div>
    """

# ===============================
# HALAMAN ANALISIS PREMIUM - ENHANCED
# ===============================
def show_analysis_page():
    """Halaman analisis dengan desain premium enhanced"""
    
    # Header dengan styling yang diperbaiki
    current_time = datetime.datetime.now().strftime('%d %B %Y • %H:%M')
    
    st.markdown(f"""
    <div class="hero-section">
        <div class="animated-elements">
            <div class="gear-animated">🔍</div>
            <div class="gear-animated">📷</div>
            <div class="gear-animated">⚡</div>
            <div class="sparkle" style="left: 15%; top: 80px;">⭐</div>
            <div class="sparkle" style="right: 15%; top: 40px;">✨</div>
            <div class="sparkle" style="right: 30%; bottom: 100px;">💫</div>
    """, unsafe_allow_html=True)
    
    # SIDEBAR ENHANCED DENGAN SCROLLBAR
    with st.sidebar:
        # ===============================
        # CSS UNTUK SCROLLABLE SIDEBAR
        # ===============================
        scrollable_css = """
        <style>
            /* Scrollbar untuk seluruh sidebar */
            [data-testid="stSidebar"] > div:first-child {
                overflow-y: auto;
                overflow-x: hidden;
                height: 100vh;
                padding-bottom: 100px;
            }
            
            /* Custom scrollbar untuk sidebar */
            [data-testid="stSidebar"]::-webkit-scrollbar {
                width: 8px;
            }
            
            [data-testid="stSidebar"]::-webkit-scrollbar-track {
                background: rgba(10, 26, 58, 0.3);
                border-radius: 10px;
            }
            
            [data-testid="stSidebar"]::-webkit-scrollbar-thumb {
                background: linear-gradient(45deg, 
                    var(--accent-blue), 
                    var(--light-blue)
                );
                border-radius: 10px;
            }
            
            [data-testid="stSidebar"]::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(45deg, 
                    var(--light-blue), 
                    var(--accent-blue)
                );
            }
            
            /* Container untuk konten yang bisa discroll */
            .scrollable-container {
                max-height: 85vh;
                overflow-y: auto;
                padding-right: 10px;
                margin-bottom: 30px;
            }
            
            .scrollable-container::-webkit-scrollbar {
                width: 6px;
            }
            
            .scrollable-container::-webkit-scrollbar-track {
                background: rgba(10, 26, 58, 0.2);
                border-radius: 10px;
            }
            
            .scrollable-container::-webkit-scrollbar-thumb {
                background: linear-gradient(45deg, 
                    rgba(74, 138, 234, 0.7), 
                    rgba(122, 182, 255, 0.7)
                );
                border-radius: 10px;
            }
        </style>
        """
        st.markdown(scrollable_css, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, 
                rgba(10, 26, 58, 0.95),
                rgba(26, 58, 122, 0.95)
            );
            padding: 25px;
            border-radius: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(122, 182, 255, 0.3);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            position: sticky;
            top: 0;
            z-index: 100;
        ">
            <h2 style="
                color: var(--text-light); 
                margin-bottom: 10px;
                text-align: center;
                font-size: 1.8rem;
                background: linear-gradient(45deg, #7AB6FF, #4A8AEA);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            ">
                ⚙️ PENGATURAN ANALISIS
            </h2>
            <p style="
                color: var(--text-muted); 
                text-align: center;
                font-size: 0.9rem;
                margin-bottom: 0;
            ">
                Sesuaikan parameter sesuai kebutuhan
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # ===============================
        # CONTAINER SCROLLABLE UNTUK SEMUA KONTEN
        # ===============================
        st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
        
        # Tab untuk pengaturan dengan styling premium
        tab_style = """
        <style>
            /* Override Streamlit tabs styling */
            .stTabs [data-baseweb="tab-list"] {
                display: flex;
                flex-wrap: nowrap;
                overflow-x: auto;
                gap: 8px;
                background: rgba(10, 26, 58, 0.8) !important;
                border-radius: 15px !important;
                padding: 8px !important;
                border: 1px solid rgba(122, 182, 255, 0.2) !important;
                margin-bottom: 20px;
                min-width: max-content;
            }
        </style>
        """
        st.markdown(tab_style, unsafe_allow_html=True)
        
        # Buat tabs
        tab1, tab2, tab3 = st.tabs(["📊 **PREPROCESSING**", "🌀 **TRANSFORMASI**", "🔍 **DETEKSI**"])
        with tab1:
            st.markdown("""
            <div style="
                background: rgba(10, 26, 58, 0.6);
                padding: 20px;
                border-radius: 15px;
                margin: 10px 0 20px 0;
                border: 1px solid rgba(122, 182, 255, 0.1);
            ">
            """, unsafe_allow_html=True)
            
            # Section 1: Basic Preprocessing
            st.markdown("#### 🎨 **Enhancement Gambar**")
            
            col1, col2 = st.columns(2)
            with col1:
                do_grayscale = st.checkbox(
                    "Skala Abu-abu", 
                    value=True,
                    help="Konversi gambar ke grayscale untuk analisis yang lebih akurat",
                    key="grayscale_enhanced"
                )
                
                do_hist = st.checkbox(
                    "Equalisasi Histogram", 
                    value=True,
                    help="Tingkatkan kontras gambar secara global",
                    key="hist_enhanced"
                )
            
            with col2:
                do_clahe = st.checkbox(
                    "CLAHE Enhancement", 
                    value=False,
                    help="Enhancement kontras adaptif untuk area gelap dan terang",
                    key="clahe_enhanced"
                )
                
                do_median = st.checkbox(
                    "Filter Median", 
                    value=False,
                    help="Reduksi noise salt-and-pepper",
                    key="median_enhanced"
                )
            
            # Section 2: Blur Settings
            st.markdown("---")
            st.markdown("#### ⚡ **Pengaturan Blur**")
            
            do_blur = st.checkbox(
                "Aktifkan Gaussian Blur", 
                value=True,
                help="Reduksi noise dan smoothing gambar",
                key="blur_enhanced"
            )
            
            if do_blur:
                blur_ksize = st.slider(
                    "Ukuran Kernel Blur", 
                    min_value=1, 
                    max_value=11, 
                    value=5, 
                    step=2,
                    help="Ukuran kernel untuk Gaussian blur (harus ganjil)",
                    key="blur_size_enhanced"
                )
            else:
                blur_ksize = 1
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown("""
            <div style="
                background: rgba(10, 26, 58, 0.6);
                padding: 20px;
                border-radius: 15px;
                margin: 10px 0 20px 0;
                border: 1px solid rgba(122, 182, 255, 0.1);
            ">
            """, unsafe_allow_html=True)
            
            # Section 1: FFT Settings
            st.markdown("#### 🌀 **Transformasi Fourier (FFT)**")
            
            use_fft = st.checkbox(
                "Aktifkan Analisis FFT", 
                value=True,
                help="Gunakan Fast Fourier Transform untuk analisis frekuensi",
                key="fft_enhanced"
            )
            
            if use_fft:
                fft_cutoff = st.slider(
                    "Frekuensi Cutoff", 
                    min_value=1, 
                    max_value=200, 
                    value=40,
                    help="Radius cutoff untuk high-pass filter (piksel)",
                    key="fft_cutoff_enhanced"
                )
            else:
                fft_cutoff = 40
            
            # Section 2: Wavelet Settings
            st.markdown("---")
            st.markdown("#### 🌊 **Transformasi Wavelet**")
            
            use_wavelet = st.checkbox(
                "Aktifkan Wavelet Transform", 
                value=True,
                help="Analisis multi-resolusi untuk detail tekstur",
                key="wavelet_enhanced"
            )
            
            if use_wavelet:
                col_wave1, col_wave2 = st.columns(2)
                
                with col_wave1:
                    wavelet_level = st.slider(
                        "Level Dekomposisi", 
                        min_value=1, 
                        max_value=3, 
                        value=1,
                        help="Jumlah level dekomposisi wavelet",
                        key="wavelet_level_enhanced"
                    )
                
                with col_wave2:
                    wavelet_name = st.selectbox(
                        "Jenis Wavelet",
                        options=["db1", "db2", "haar", "coif1", "sym2"],
                        index=1,
                        help="Pilih jenis wavelet yang digunakan",
                        key="wavelet_name_enhanced"
                    )
            else:
                wavelet_level = 1
                wavelet_name = "db2"
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab3:
            st.markdown("""
            <div style="
                background: rgba(10, 26, 58, 0.6);
                padding: 20px;
                border-radius: 15px;
                margin: 10px 0 20px 0;
                border: 1px solid rgba(122, 182, 255, 0.1);
            ">
            """, unsafe_allow_html=True)
            
            # Section 1: Edge Detection
            st.markdown("#### 🔍 **Deteksi Tepi**")
            
            edge_method = st.selectbox(
                "Metode Deteksi",
                options=["Canny", "Sobel", "Laplacian", "Prewitt"],
                index=0,
                help="Pilih algoritma untuk deteksi tepi",
                key="edge_method_enhanced"
            )
            
            if edge_method == "Canny":
                col_canny1, col_canny2 = st.columns(2)
                
                with col_canny1:
                    canny_t1 = st.slider(
                        "Threshold Bawah", 
                        min_value=1, 
                        max_value=300, 
                        value=60,
                        help="Threshold bawah untuk hysteresis",
                        key="canny_t1_enhanced"
                    )
                
                with col_canny2:
                    canny_t2 = st.slider(
                        "Threshold Atas", 
                        min_value=1, 
                        max_value=400, 
                        value=130,
                        help="Threshold atas untuk hysteresis",
                        key="canny_t2_enhanced"
                    )
            else:
                canny_t1, canny_t2 = 60, 130
            
            # Section 2: Morphology
            st.markdown("---")
            st.markdown("#### 🔄 **Operasi Morfologi**")
            
            use_morph = st.checkbox(
                "Aktifkan Operasi Morfologi", 
                value=True,
                help="Pembersihan dan enhancement hasil deteksi",
                key="morph_enhanced"
            )
            
            if use_morph:
                col_morph1, col_morph2 = st.columns(2)
                
                with col_morph1:
                    morph_kernel = st.slider(
                        "Ukuran Kernel", 
                        min_value=1, 
                        max_value=15, 
                        value=3,
                        help="Ukuran kernel untuk operasi morfologi",
                        key="morph_kernel_enhanced"
                    )
                
                with col_morph2:
                    morph_op = st.selectbox(
                        "Jenis Operasi",
                        options=["Closing", "Opening", "Dilation", "Erosion"],
                        index=0,
                        help="Pilih jenis operasi morfologi",
                        key="morph_op_enhanced"
                    )
            else:
                morph_kernel = 3
                morph_op = "Closing"
            
            # Section 3: Contour Detection
            st.markdown("---")
            st.markdown("#### 🎯 **Deteksi Kontur**")
            
            min_contour_area = st.slider(
                "Area Minimum Kontur", 
                min_value=50, 
                max_value=5000, 
                value=200,
                step=50,
                help="Filter kontur berdasarkan area minimum (piksel)",
                key="contour_area_enhanced"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # ===============================
        # VISUALIZATION SETTINGS
        # ===============================
        st.markdown("---")
        st.markdown("""
        <div style="
            background: rgba(10, 26, 58, 0.7);
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0 20px 0;
            border: 1px solid rgba(122, 182, 255, 0.2);
        ">
            <h4 style="color: var(--text-light); margin-bottom: 15px; text-align: center;">
                🎨 VISUALISASI HASIL
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            display_width = st.slider(
                "Lebar Gambar", 
                min_value=100, 
                max_value=800, 
                value=320,
                step=20,
                help="Ukuran tampilan gambar di hasil",
                key="display_width_enhanced"
            )
            
            columns_per_row = st.selectbox(
                "Kolom per Baris",
                options=[2, 3, 4],
                index=1,
                help="Jumlah kolom untuk grid gambar",
                key="columns_per_row_enhanced"
            )
        
        with col_viz2:
            enable_heatmap = st.checkbox(
                "Tampilkan Heatmap", 
                value=True,
                help="Visualisasi heatmap untuk intensitas kerusakan",
                key="heatmap_enhanced"
            )
            
            show_explanations = st.checkbox(
                "Tampilkan Penjelasan", 
                value=True,
                help="Tampilkan penjelasan untuk setiap step",
                key="explanations_enhanced"
            )
        
        # ===============================
        # CLOSE SCROLLABLE CONTAINER
        # ===============================
        st.markdown('</div>', unsafe_allow_html=True)  # Tutup scrollable-container
        
        # ===============================
        # INFO FOOTER (di luar scrollable container)
        # ===============================
        st.markdown("""
        <div style="
            background: rgba(10, 26, 58, 0.5);
            padding: 15px;
            border-radius: 15px;
            margin-top: 10px;
            text-align: center;
            border: 1px solid rgba(122, 182, 255, 0.1);
            position: sticky;
            bottom: 0;
            backdrop-filter: blur(10px);
        ">
            <div style="color: var(--text-muted); font-size: 0.8rem;">
                <div>⚡ <strong>MetalAnalyzer Pro v2.0</strong></div>
                <div style="margin-top: 5px;">Interpretasi Human-Friendly</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # AREA UTAMA UNTUK HASIL ANALISIS ENHANCED
    st.markdown("""
    <div class="upload-section">
        <div style="font-size: 4rem; margin-bottom: 20px; color: var(--light-blue);">
            📤
        </div>
        <h3 style="color: var(--text-light); margin-bottom: 15px;">
            Unggah Gambar Logam
        </h3>
        <p style="color: var(--text-muted);">
            Pilih gambar permukaan logam yang ingin dianalisis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Drag & drop atau klik untuk memilih gambar (JPG, JPEG, PNG, BMP, TIFF)",
        type=["jpg", "jpeg", "png", "bmp", "tiff"],
        accept_multiple_files=True,
        help="Unggah gambar permukaan logam yang ingin dianalisis",
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.success(f"✅ **{len(uploaded_files)} gambar** berhasil diunggah!")
        
        # Tab untuk setiap gambar
        tabs = st.tabs([f"📷 Gambar {i+1}" for i in range(len(uploaded_files))])
        
        for idx, (tab, file) in enumerate(zip(tabs, uploaded_files)):
            with tab:
                st.markdown(f"#### Analisis Gambar {idx+1}: `{file.name[:50]}{'...' if len(file.name) > 50 else ''}`")
                
                # Progress bar dengan animasi
                with st.spinner("Memproses gambar..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # 1. Load image
                        status_text.text("📥 Memuat gambar...")
                        img_pil = Image.open(file)
                        
                        # Resize jika terlalu besar untuk performa
                        max_size = 1920
                        if max(img_pil.size) > max_size:
                            ratio = max_size / max(img_pil.size)
                            new_size = tuple(int(dim * ratio) for dim in img_pil.size)
                            img_pil = img_pil.resize(new_size, Image.Resampling.LANCZOS)
                        
                        img_rgb = np.array(img_pil.convert("RGB"))
                        progress_bar.progress(10)
                        
                        # 2. Preprocessing
                        status_text.text("🔧 Melakukan preprocessing...")
                        proc_img, prep_notes = apply_preprocessing(
                            img_rgb, do_grayscale, do_blur, blur_ksize, do_median, do_hist, do_clahe
                        )
                        proc_gray = proc_img if len(proc_img.shape) == 2 else cv2.cvtColor(proc_img, cv2.COLOR_RGB2GRAY)
                        progress_bar.progress(30)
                        
                        # 3. FFT
                        status_text.text("🌀 Analisis frekuensi (FFT)...")
                        if use_fft:
                            fft_img = fft_highpass(proc_gray, fft_cutoff)
                            prep_notes.append(f"✅ FFT high-pass (cutoff: {fft_cutoff}px)")
                        else:
                            fft_img = proc_gray
                        progress_bar.progress(45)
                        
                        # 4. Wavelet
                        status_text.text("🌊 Analisis multi-resolusi (Wavelet)...")
                        if use_wavelet:
                            wave_img = wavelet_detail(fft_img, wavelet_name, wavelet_level)
                            prep_notes.append(f"✅ Wavelet transform ({wavelet_name}, level: {wavelet_level})")
                        else:
                            wave_img = fft_img
                        progress_bar.progress(60)
                        
                        # 5. Edge Detection
                        status_text.text("🔍 Mendeteksi tepi...")
                        if len(wave_img.shape) == 2:
                            edges, edge_note = detect_edges(wave_img, edge_method, canny_t1, canny_t2)
                            prep_notes.append(f"✅ Edge detection: {edge_note}")
                        else:
                            edges = wave_img
                            edge_note = "No edge detection applied"
                        progress_bar.progress(75)
                        
                        # 6. Morphology
                        status_text.text("🔄 Operasi morfologi...")
                        if use_morph and len(edges.shape) == 2:
                            morph = morphological_process(edges, morph_kernel, morph_op)
                            prep_notes.append(f"✅ Morphology: {morph_op} (kernel: {morph_kernel}x{morph_kernel})")
                        else:
                            morph = edges
                        progress_bar.progress(85)
                        
                        # 7. Contour detection
                        status_text.text("🎯 Mendeteksi kontur...")
                        overlay, detections = detect_contours(morph, img_rgb, min_contour_area)
                        prep_notes.append(f"✅ {len(detections)} kontur terdeteksi (min area: {min_contour_area}px)")
                        progress_bar.progress(95)
                        
                        # 8. CD score
                        status_text.text("📊 Menghitung skor kerusakan...")
                        cd_score, edge_count = compute_cd_score(morph)
                        progress_bar.progress(100)
                        
                    except Exception as e:
                        st.error(f"❌ Error dalam memproses gambar: {str(e)}")
                        st.stop()
                
                # =============== INTERPRETASI HUMAN-FRIENDLY ===============
                interpret_info = get_interpretation_info(cd_score, edge_count, len(detections))
                
                # Section Spacer
                st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
                
                # HASIL UTAMA - INTERPRETASI
                st.markdown("### 📋 HASIL ANALISIS & INTERPRETASI")
                
                col_a, col_b = st.columns([1, 2])
                
                with col_a:
                    # Progress Ring untuk Damage Score dengan warna interpretasi
                    st.markdown(create_progress_ring(
                        interpret_info['combined_score'], 
                        "Skor Gabungan", 
                        interpret_info['color']
                    ), unsafe_allow_html=True)
                    
                    # Status Badge
                    st.markdown(f"""
                    <div style="text-align: center; margin-top: 20px;">
                        <div class="status-badge {interpret_info['status_class']}">
                            {interpret_info['icon']} {interpret_info['level']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Confidence Meter
                    st.markdown(create_confidence_meter(interpret_info['confidence']), unsafe_allow_html=True)
                
                with col_b:
                    # Interpretasi Card
                    st.markdown(create_interpretation_card(interpret_info), unsafe_allow_html=True)
                    
                    # Detail Metrics
                    col_metrics1, col_metrics2 = st.columns(2)
                    with col_metrics1:
                        st.metric("Pixel Edge", f"{edge_count:,}")
                        st.metric("Skor Awal", f"{cd_score}%")
                    with col_metrics2:
                        st.metric("Objek Terdeteksi", len(detections))
                        st.metric("Inspeksi Berikutnya", interpret_info['next_check'])
                
                # Section Spacer
                st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
                
                # REKOMENDASI DETAIL - PERBAIKAN BAGIAN INI
                st.markdown("### 💡 REKOMENDASI TINDAKAN")
                
                col_rec1, col_rec2 = st.columns([2, 1])
                
                with col_rec1:
                    # Memperbaiki bagian rekomendasi dengan menghilangkan f-string yang bermasalah
                    recommendation_html = interpret_info['recommendation'].replace('\n', '<br>')
                    st.markdown(f"""
                    <div class="result-card">
                        <h4 style="color: var(--light-blue); margin-bottom: 15px;">
                            {interpret_info['icon']} Langkah-langkah yang Disarankan
                        </h4>
                        <div style="color: var(--text-semi); line-height: 1.8;">
                            {recommendation_html}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_rec2:
                    # Level Interpretation Scale
                    st.markdown("""
                    <div class="result-card">
                        <h4 style="color: var(--light-blue); margin-bottom: 15px;">📊 Skala Interpretasi</h4>
                        <div style="color: var(--text-semi); line-height: 1.8;">
                            <div style="display: flex; align-items: center; margin: 5px 0;">
                                <div style="width: 15px; height: 15px; background: #8B5CF6; border-radius: 50%; margin-right: 10px;"></div>
                                <span>✨ 0-5% - SEMPURNA</span>
                            </div>
                            <div style="display: flex; align-items: center; margin: 5px 0;">
                                <div style="width: 15px; height: 15px; background: #10B981; border-radius: 50%; margin-right: 10px;"></div>
                                <span>✅ 5-15% - BAIK</span>
                            </div>
                            <div style="display: flex; align-items: center; margin: 5px 0;">
                                <div style="width: 15px; height: 15px; background: #F59E0B; border-radius: 50%; margin-right: 10px;"></div>
                                <span>⚠️ 15-25% - MINOR</span>
                            </div>
                            <div style="display: flex; align-items: center; margin: 5px 0;">
                                <div style="width: 15px; height: 15px; background: #F97316; border-radius: 50%; margin-right: 10px;"></div>
                                <span>🔸 25-40% - MODERAT</span>
                            </div>
                            <div style="display: flex; align-items: center; margin: 5px 0;">
                                <div style="width: 15px; height: 15px; background: #EF4444; border-radius: 50%; margin-right: 10px;"></div>
                                <span>🚨 40-100% - BERAT</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Section Spacer
                st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
                
                # Tampilkan gambar dalam grid ENHANCED
                st.markdown("### 🖼 VISUALISASI PROSES")
                
                images_for_show = [
                    ("Asli", to_display(img_rgb), "Gambar Asli"),
                    ("Preprocessing", to_display(proc_gray) if do_grayscale else to_display(proc_img), "Hasil preprocessing"),
                    ("FFT", to_display(fft_img) if use_fft else "FFT (disabled)", "FFT High-pass"),
                    ("Wavelet", to_display(wave_img) if use_wavelet else "Wavelet (disabled)", "Detail wavelet"),
                    ("Edges", to_display(edges), "Deteksi tepi"),
                    ("Morph", to_display(morph) if use_morph else "Morph (disabled)", "Morphology"),
                    ("Overlay", overlay, "Overlay deteksi")
                ]
                
                if enable_heatmap:
                    heatmap_img = heatmap_overlay(img_rgb, morph)
                    images_for_show.append(("Heatmap", heatmap_img, "Heatmap overlay"))
                
                # Filter out disabled images
                images_for_show = [(title, img, desc) for title, img, desc in images_for_show 
                                  if not isinstance(img, str) or "disabled" not in img]
                
                # Tampilkan dalam grid responsif
                cols_per_row = min(columns_per_row, len(images_for_show))
                cols = st.columns(cols_per_row)
                
                for i, (title, img, caption) in enumerate(images_for_show):
                    col = cols[i % cols_per_row]
                    with col:
                        st.markdown(f"""
                        <div class="image-card">
                            <img src="data:image/png;base64,{image_to_base64(pil_from_np(img))}" 
                                 class="image-card-img" 
                                 alt="{title}">
                            <div class="image-card-content">
                                <div class="image-card-title">
                                    {title}
                                    <span class="image-card-badge">Step {i+1}</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if show_explanations:
                            with st.expander(f"ℹ️ {title}", expanded=False):
                                st.write(caption)
                
                # Section Spacer
                st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
                
                # DOWNLOAD SECTION
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, 
                        rgba(10, 26, 58, 0.9),
                        rgba(26, 58, 122, 0.9)
                    );
                    border-radius: 20px;
                    padding: 30px;
                    margin: 30px 0;
                    border: 1px solid rgba(122, 182, 255, 0.2);
                    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
                ">
                    <h3 style="
                        color: var(--text-light); 
                        text-align: center;
                        margin-bottom: 30px;
                        font-size: 1.8rem;
                        background: linear-gradient(45deg, #FFFFFF, #B3CCFF);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                    ">
                        💾 DOWNLOAD HASIL ANALISIS
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Container untuk download buttons
                col_dl1, col_dl2, col_dl3 = st.columns(3)
                
                with col_dl1:
                    # Download Hasil Gambar
                    img_bytes = io.BytesIO()
                    pil_from_np(overlay).save(img_bytes, format="PNG")
                    
                    if st.download_button(
                        label="📥 **Download Gambar**",
                        data=img_bytes.getvalue(),
                        file_name=f"hasil_analisis_{idx + 1}.png",
                        mime="image/png",
                        use_container_width=True,
                        key=f"dl_img_{idx}"
                    ):
                        st.toast("✅ Gambar berhasil didownload!", icon="📥")
                
                with col_dl2:
                    # Download Laporan dengan interpretasi lengkap
                    report_txt = f"""==================================
        LAPORAN ANALISIS KERUSAKAN LOGAM
==================================
        
📁 FILE ANALISIS
• Nama File: {file.name}
• Tanggal Analisis: {datetime.datetime.now().strftime('%d %B %Y %H:%M')}
• Waktu Proses: {datetime.datetime.now().strftime('%H:%M:%S')}

📊 HASIL ANALISIS
• Status: {interpret_info['interpretation']}
• Level: {interpret_info['level']}
• Skor Gabungan: {interpret_info['combined_score']:.1f}%
• Skor Awal: {cd_score}%
• Pixel Edge Terdeteksi: {edge_count:,}
• Objek Terdeteksi: {len(detections)}
• Tingkat Kepercayaan: {interpret_info['confidence']}

📝 INTERPRETASI DETAIL
{interpret_info['detail']}

💡 REKOMENDASI
{interpret_info['recommendation']}

⚙️ PARAMETER YANG DIGUNAKAN
{chr(10).join(['• ' + note.replace('✅ ', '') for note in prep_notes])}

----------------------------------
MetalAnalyzer Pro v2.0
Sistem Interpretasi Human-Friendly
© 2024 - Precision in Every Pixel
=================================="""
                    
                    if st.download_button(
                        label="📋 **Download Laporan**",
                        data=report_txt,
                        file_name=f"laporan_analisis_{idx + 1}.txt",
                        mime="text/plain",
                        use_container_width=True,
                        key=f"dl_report_{idx}"
                    ):
                        st.toast("✅ Laporan berhasil didownload!", icon="📋")
                
                with col_dl3:
                    # Download ZIP
                    process_images = {
                        "original": img_pil,
                        "preprocessed": Image.fromarray(proc_img) if len(proc_img.shape) == 2 else Image.fromarray(proc_img),
                        "edges": Image.fromarray(edges),
                        "result": Image.fromarray(overlay)
                    }
                    
                    if enable_heatmap:
                        process_images["heatmap"] = Image.fromarray(heatmap_img)
                    
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for name, img in process_images.items():
                            img_bytes = io.BytesIO()
                            img.save(img_bytes, format='PNG')
                            zip_file.writestr(f"{file.name.split('.')[0]}_{name}.png", img_bytes.getvalue())
                    
                    if st.download_button(
                        label="📦 **Download Semua**",
                        data=zip_buffer.getvalue(),
                        file_name=f"hasil_analisis_{file.name.split('.')[0]}.zip",
                        mime="application/zip",
                        use_container_width=True,
                        key=f"dl_zip_{idx}"
                    ):
                        st.toast(f"✅ {len(process_images)} file berhasil dikompres!", icon="📦")
                
                # Section Spacer antar gambar
                if idx < len(uploaded_files) - 1:
                    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
                    st.markdown("---")
    
    else:
        # Tampilan jika belum ada gambar
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 30px; background: var(--card-bg); 
                        border-radius: 20px; border: 2px dashed var(--card-border);">
                <div style="font-size: 5rem; color: var(--light-blue); margin-bottom: 20px; 
                            animation: float 3s ease-in-out infinite;">
                    📁
                </div>
                <h3 style="color: var(--text-light); margin-bottom: 15px;">
                    Belum Ada Gambar
                </h3>
                <p style="color: var(--text-muted); margin-bottom: 25px;">
                    Unggah gambar permukaan logam untuk memulai analisis
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Tombol kembali ke home - ENHANCED
    st.markdown("""
    <div style="text-align: center; margin-top: 50px;">
    """, unsafe_allow_html=True)
    
    if st.button("🏠 Kembali ke Home", use_container_width=True, type="secondary"):
        st.session_state.page = 'home'
        st.rerun()

# ===============================
# FUNGSI UTILITAS UNTUK ANALISIS (TIDAK BERUBAH)
# ===============================
def to_np(img_pil: Image.Image):
    """Convert PIL Image to numpy array"""
    return np.array(img_pil.convert("RGB"))

def pil_from_np(arr: np.ndarray):
    """Convert numpy array to PIL Image"""
    arr = np.ascontiguousarray(arr.astype(np.uint8))
    return Image.fromarray(arr)

def image_to_base64(img):
    """Convert PIL image to base64 string"""
    import base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def apply_preprocessing(img_rgb: np.ndarray, do_grayscale, do_blur, blur_ksize, do_median, do_hist, do_clahe=False):
    """Apply preprocessing steps"""
    notes = []
    img_proc = img_rgb.copy()
    
    if do_grayscale:
        if len(img_proc.shape) == 3:
            img_proc = cv2.cvtColor(img_proc, cv2.COLOR_RGB2GRAY)
        notes.append("✅ Convert ke grayscale")
    
    if do_clahe and len(img_proc.shape) == 2:
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img_proc = clahe.apply(img_proc)
        notes.append("✅ CLAHE enhancement")
    
    if do_blur:
        k = blur_ksize if blur_ksize % 2 == 1 else blur_ksize + 1
        img_proc = cv2.GaussianBlur(img_proc, (k, k), 0)
        notes.append(f"✅ Gaussian blur ({k}x{k})")
    
    if do_median and len(img_proc.shape) == 2:
        img_proc = cv2.medianBlur(img_proc, 3)
        notes.append("✅ Median filter")
    
    if do_hist:
        if len(img_proc.shape) == 2:
            img_proc = cv2.equalizeHist(img_proc)
            notes.append("✅ Histogram equalization")
        else:
            ycrcb = cv2.cvtColor(img_proc, cv2.COLOR_RGB2YCrCb)
            ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
            img_proc = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)
            notes.append("✅ Histogram equalization (RGB)")
    
    return img_proc, notes

def fft_highpass(img_gray: np.ndarray, cutoff: int):
    """Apply FFT high-pass filter"""
    rows, cols = img_gray.shape
    f = np.fft.fft2(img_gray)
    fshift = np.fft.fftshift(f)
    crow, ccol = rows // 2, cols // 2
    mask = np.ones((rows, cols), np.uint8)
    cv2.circle(mask, (ccol, crow), cutoff, 0, -1)
    f_hp = fshift * mask
    ishift = np.fft.ifftshift(f_hp)
    img_back = np.abs(np.fft.ifft2(ishift))
    img_back = cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return img_back

def wavelet_detail(img_gray: np.ndarray, wavelet_name: str, level: int):
    """Apply wavelet transform"""
    coeffs = pywt.wavedec2(img_gray, wavelet_name, level=level)
    detail_sum = None
    for i in range(1, len(coeffs)):
        cH, cV, cD = coeffs[i]
        lvl = np.abs(cH) + np.abs(cV) + np.abs(cD)
        lvl_resized = cv2.resize(lvl, (img_gray.shape[1], img_gray.shape[0]))
        detail_sum = lvl_resized if detail_sum is None else detail_sum + lvl_resized
    detail_norm = cv2.normalize(detail_sum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return detail_norm

def morphological_process(edge_img: np.ndarray, kernel_size: int, operation: str = "Closing"):
    """Apply morphological operations"""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    
    if operation == "Closing":
        result = cv2.morphologyEx(edge_img, cv2.MORPH_CLOSE, kernel)
    elif operation == "Opening":
        result = cv2.morphologyEx(edge_img, cv2.MORPH_OPEN, kernel)
    elif operation == "Dilation":
        result = cv2.dilate(edge_img, kernel, iterations=1)
    else:  # Erosion
        result = cv2.erode(edge_img, kernel, iterations=1)
    
    return result

def detect_contours(binary_img: np.ndarray, orig_img_rgb: np.ndarray, min_area: int):
    """Detect contours in binary image"""
    if len(binary_img.shape) == 3:
        binary_img = cv2.cvtColor(binary_img, cv2.COLOR_RGB2GRAY)
    
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    overlay = orig_img_rgb.copy()
    detected = []
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area >= min_area:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.drawContours(overlay, [cnt], -1, (0, 255, 0), 2)
            
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = x + w//2, y + h//2
            
            cv2.circle(overlay, (cx, cy), 5, (0, 0, 255), -1)
            detected.append({
                "area": int(area),
                "bbox": (x, y, w, h),
                "centroid": (cx, cy)
            })
    
    return overlay, detected

def compute_cd_score(edge_img: np.ndarray):
    """Compute damage score"""
    if len(edge_img.shape) == 3:
        edge_img = cv2.cvtColor(edge_img, cv2.COLOR_RGB2GRAY)
    
    total = edge_img.size
    count = np.sum(edge_img > 0)
    frac = count / total if total > 0 else 0
    score = min(100, int(frac * 200))
    return score, int(count)

def to_display(img):
    """Convert image to display format"""
    if len(img.shape) == 2:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    return img

def heatmap_overlay(img_rgb, edge_img):
    """Create heatmap overlay"""
    if len(edge_img.shape) == 3:
        edge_img = cv2.cvtColor(edge_img, cv2.COLOR_RGB2GRAY)
    
    hm = cv2.normalize(edge_img, None, 0, 255, cv2.NORM_MINMAX)
    hm_color = cv2.applyColorMap(hm.astype(np.uint8), cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(img_rgb, 0.7, hm_color, 0.3, 0)
    return overlay

def detect_edges(img_gray, method, canny_t1=None, canny_t2=None):
    """Detect edges using specified method"""
    if method == "Canny":
        edges = cv2.Canny(img_gray, canny_t1, canny_t2)
        note = f"Canny (T1={canny_t1}, T2={canny_t2})"
    elif method == "Sobel":
        sobelx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
        edges = cv2.magnitude(sobelx, sobely)
        edges = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        note = "Sobel operator"
    elif method == "Laplacian":
        edges = cv2.Laplacian(img_gray, cv2.CV_64F)
        edges = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        note = "Laplacian operator"
    else:  # Prewitt
        kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
        kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
        prewittx = cv2.filter2D(img_gray, -1, kernelx)
        prewitty = cv2.filter2D(img_gray, -1, kernely)
        edges = cv2.addWeighted(prewittx, 0.5, prewitty, 0.5, 0)
        note = "Prewitt operator"
    
    return edges, note

# ===============================
# APLIKASI UTAMA
# ===============================
def main():
    # Inisialisasi state
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    # Navigasi (hanya 3 menu)
    create_navigation()
    
    # Tampilkan halaman berdasarkan state
    if st.session_state.page == 'home':
        create_homepage()
    elif st.session_state.page == 'analyze':
        show_analysis_page()
    elif st.session_state.page == 'about':
        show_about_page()

# ===============================
# JALANKAN APLIKASI
# ===============================
if __name__ == "__main__":
    main()
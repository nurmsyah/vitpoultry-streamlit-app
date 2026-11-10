import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="VitPoultry FL Simulator - Nurmansyah",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- EMBED CUSTOM HTML/JS DASHBOARD ---
html_dashboard = """
<!DOCTYPE html>
<html lang="en" class="dark h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flower FL Dashboard - VitPoultry Simulation by Nurmansyah</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts: Inter & JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace'],
                    },
                    colors: {
                        flower: {
                            50: '#f0fdf4',
                            500: '#10b981',
                            600: '#059669',
                            700: '#047857',
                            glow: '#00ffa3'
                        },
                        darkbg: '#0b0f17',
                        cardbg: '#111827',
                        cardborder: '#1f2937'
                    }
                }
            }
        }
    </script>
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #0b0f17; color: #f3f4f6; margin: 0; }
        .font-mono { font-family: 'JetBrains Mono', monospace; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #0b0f17; }
        ::-webkit-scrollbar-thumb { background: #1f2937; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #374151; }
        .glass-panel {
            background: rgba(17, 24, 39, 0.75);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
    </style>
</head>
<body class="h-full flex flex-col antialiased selection:bg-emerald-500 selection:text-white p-4">

    <!-- Top Header -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md rounded-2xl mb-6">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center text-white shadow-lg shadow-emerald-500/20">
                    <i class="fa-solid fa-seedling text-lg"></i>
                </div>
                <div>
                    <div class="flex items-center space-x-2">
                        <span class="font-bold text-lg text-white tracking-tight">VitPoultry FL Simulator <span class="text-xs font-normal text-emerald-400 font-mono ml-1">| Developer: Nurmansyah</span></span>
                        <span class="text-[10px] font-mono px-2 py-0.5 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-full">v1.10.0 Engine</span>
                    </div>
                    <p class="text-xs text-slate-400">Decentralized Poultry Diagnostics (1 Aggregator Server & 3 Farm Clients)</p>
                </div>
            </div>

            <div class="flex items-center space-x-4">
                <div class="flex items-center space-x-2 bg-slate-800/80 border border-slate-700/60 px-3 py-1.5 rounded-full text-xs font-medium">
                    <span id="status-dot" class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span id="status-text" class="text-slate-300">Flower SuperLink Active</span>
                </div>
                <div class="text-xs font-mono text-slate-400 bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-xl">
                    Port: <span class="text-emerald-400">8080 (gRPC)</span>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Workspace -->
    <main class="max-w-7xl w-full mx-auto space-y-6">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            <!-- Left: Control Panel -->
            <div class="lg:col-span-4 space-y-5">
                <div class="glass-panel rounded-2xl p-5 space-y-4">
                    <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                        <h2 class="font-bold text-base flex items-center space-x-2 text-slate-100">
                            <i class="fa-solid fa-sliders text-emerald-400"></i>
                            <span>Simulation Controls</span>
                        </h2>
                        <span id="strategy-badge" class="text-[10px] font-mono px-2 py-0.5 bg-slate-800 text-emerald-400 border border-emerald-500/30 rounded-full">FedAvg</span>
                    </div>

                    <div class="grid grid-cols-2 gap-2">
                        <button onclick="startSimulation()" id="btn-start" class="bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-2.5 px-3 rounded-xl transition-all shadow-lg shadow-emerald-600/20 flex items-center justify-center space-x-2 text-sm cursor-pointer">
                            <i class="fa-solid fa-play"></i><span>Run FL</span>
                        </button>
                        <button onclick="pauseSimulation()" id="btn-pause" class="bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold py-2.5 px-3 rounded-xl transition-all border border-slate-700 flex items-center justify-center space-x-2 text-sm opacity-50 cursor-not-allowed" disabled>
                            <i class="fa-solid fa-pause"></i><span>Pause</span>
                        </button>
                        <button onclick="stepRound()" id="btn-step" class="bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold py-2 px-3 rounded-xl transition-all border border-slate-700 flex items-center justify-center space-x-2 text-xs cursor-pointer">
                            <i class="fa-solid fa-forward-step text-emerald-400"></i><span>Step Round</span>
                        </button>
                        <button onclick="resetSimulation()" class="bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold py-2 px-3 rounded-xl transition-all border border-slate-700 flex items-center justify-center space-x-2 text-xs cursor-pointer">
                            <i class="fa-solid fa-rotate-left text-amber-400"></i><span>Reset</span>
                        </button>
                    </div>

                    <div class="space-y-3 pt-2 text-xs">
                        <div>
                            <div class="flex justify-between text-slate-400 mb-1">
                                <span>Max Training Rounds</span>
                                <span id="rounds-val" class="font-mono font-bold text-emerald-400">10</span>
                            </div>
                            <input type="range" id="param-rounds" min="1" max="20" value="10" class="w-full accent-emerald-500 bg-slate-800 rounded-lg h-1.5 cursor-pointer" oninput="document.getElementById('rounds-val').innerText = this.value">
                        </div>

                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="text-slate-400 block mb-1">Aggregation Strategy</label>
                                <select id="param-strategy" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500" onchange="document.getElementById('strategy-badge').innerText = this.value">
                                    <option value="FedAvg" selected>FedAvg</option>
                                    <option value="FedProx">FedProx (Mu=0.01)</option>
                                </select>
                            </div>
                            <div>
                                <label class="text-slate-400 block mb-1">Data Heterogeneity</label>
                                <select id="param-hetero" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500">
                                    <option value="IID">IID (Balanced)</option>
                                    <option value="NON-IID" selected>Non-IID (Skewed Data)</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Client Specs -->
                <div class="glass-panel rounded-2xl p-4 space-y-3 text-xs">
                    <h3 class="font-bold text-slate-300 flex items-center justify-between border-b border-slate-800 pb-2">
                        <span>Participating Nodes (3 Farms)</span>
                        <span class="text-[10px] text-slate-500">Decentralized Dataset</span>
                    </h3>
                    <div class="space-y-2">
                        <div class="flex items-center justify-between bg-slate-900/60 p-2 rounded-xl border border-slate-800">
                            <div class="flex items-center space-x-2">
                                <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
                                <span class="font-semibold text-slate-200">Client 1: Farm Alpha</span>
                            </div>
                            <span class="font-mono text-slate-400 text-[11px]">2,100 images (Clean)</span>
                        </div>
                        <div class="flex items-center justify-between bg-slate-900/60 p-2 rounded-xl border border-slate-800">
                            <div class="flex items-center space-x-2">
                                <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                                <span class="font-semibold text-slate-200">Client 2: Farm Beta</span>
                            </div>
                            <span class="font-mono text-slate-400 text-[11px]">850 images (Noisy)</span>
                        </div>
                        <div class="flex items-center justify-between bg-slate-900/60 p-2 rounded-xl border border-slate-800">
                            <div class="flex items-center space-x-2">
                                <span class="w-2 h-2 rounded-full bg-teal-500"></span>
                                <span class="font-semibold text-slate-200">Client 3: Farm Gamma</span>
                            </div>
                            <span class="font-mono text-slate-400 text-[11px]">1,450 images (Class Skew)</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right: Network Topology Canvas -->
            <div class="lg:col-span-8 glass-panel rounded-2xl p-5 flex flex-col justify-between relative overflow-hidden">
                <div class="flex items-center justify-between z-10">
                    <div class="flex items-center space-x-2">
                        <i class="fa-solid fa-network-wired text-emerald-400"></i>
                        <h2 class="font-bold text-base text-slate-100">Flower Network Topology Canvas</h2>
                    </div>
                    <div class="flex items-center space-x-4 text-xs font-mono">
                        <span class="text-slate-400">Round: <strong id="sim-round-curr" class="text-emerald-400 font-bold text-sm">0</strong>/<span id="sim-round-max">10</span></span>
                        <span class="text-slate-400">Phase: <strong id="sim-phase-text" class="text-indigo-400 font-bold">Idle</strong></span>
                    </div>
                </div>

                <div class="relative w-full h-[320px] my-2 bg-slate-950/80 rounded-2xl border border-slate-800/80 overflow-hidden">
                    <canvas id="networkCanvas" class="absolute inset-0 w-full h-full"></canvas>

                    <!-- Server Node Overlay -->
                    <div class="absolute top-4 left-1/2 -translate-x-1/2 bg-slate-900/90 border border-emerald-500/50 p-3 rounded-2xl shadow-xl flex items-center space-x-3 backdrop-blur-md z-10 w-64">
                        <div class="w-10 h-10 rounded-xl bg-emerald-600/20 border border-emerald-500/60 flex items-center justify-center text-emerald-400">
                            <i class="fa-solid fa-server text-lg"></i>
                        </div>
                        <div class="flex-1 min-w-0">
                            <div class="flex items-center justify-between">
                                <span class="font-bold text-xs text-white">Flower Server</span>
                                <span class="text-[9px] px-1.5 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-md">Aggregator</span>
                            </div>
                            <div class="text-[10px] font-mono text-slate-400 mt-0.5">
                                Acc: <span id="srv-acc" class="text-emerald-400 font-semibold">--</span> | Loss: <span id="srv-loss" class="text-amber-400 font-semibold">--</span>
                            </div>
                        </div>
                    </div>

                    <!-- Client Node Cards -->
                    <div class="absolute bottom-4 inset-x-4 grid grid-cols-3 gap-3 z-10">
                        <div class="bg-slate-900/90 border border-slate-800 p-2.5 rounded-2xl backdrop-blur-md space-y-1.5">
                            <div class="flex items-center justify-between">
                                <span class="font-bold text-xs text-indigo-400 flex items-center space-x-1"><i class="fa-solid fa-tractor text-[10px]"></i><span>Farm Alpha</span></span>
                                <span id="c1-status" class="text-[9px] px-1.5 py-0.2 bg-slate-800 text-slate-400 rounded-md">Idle</span>
                            </div>
                            <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden"><div id="c1-bar" class="bg-indigo-500 h-full rounded-full transition-all duration-300" style="width: 0%"></div></div>
                            <div class="flex justify-between text-[10px] font-mono text-slate-400"><span>Acc: <strong id="c1-acc" class="text-slate-200">--</strong></span><span>Loss: <strong id="c1-loss" class="text-slate-200">--</strong></span></div>
                        </div>
                        <div class="bg-slate-900/90 border border-slate-800 p-2.5 rounded-2xl backdrop-blur-md space-y-1.5">
                            <div class="flex items-center justify-between">
                                <span class="font-bold text-xs text-amber-400 flex items-center space-x-1"><i class="fa-solid fa-wheat-awn text-[10px]"></i><span>Farm Beta</span></span>
                                <span id="c2-status" class="text-[9px] px-1.5 py-0.2 bg-slate-800 text-slate-400 rounded-md">Idle</span>
                            </div>
                            <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden"><div id="c2-bar" class="bg-amber-500 h-full rounded-full transition-all duration-300" style="width: 0%"></div></div>
                            <div class="flex justify-between text-[10px] font-mono text-slate-400"><span>Acc: <strong id="c2-acc" class="text-slate-200">--</strong></span><span>Loss: <strong id="c2-loss" class="text-slate-200">--</strong></span></div>
                        </div>
                        <div class="bg-slate-900/90 border border-slate-800 p-2.5 rounded-2xl backdrop-blur-md space-y-1.5">
                            <div class="flex items-center justify-between">
                                <span class="font-bold text-xs text-teal-400 flex items-center space-x-1"><i class="fa-solid fa-warehouse text-[10px]"></i><span>Farm Gamma</span></span>
                                <span id="c3-status" class="text-[9px] px-1.5 py-0.2 bg-slate-800 text-slate-400 rounded-md">Idle</span>
                            </div>
                            <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden"><div id="c3-bar" class="bg-teal-500 h-full rounded-full transition-all duration-300" style="width: 0%"></div></div>
                            <div class="flex justify-between text-[10px] font-mono text-slate-400"><span>Acc: <strong id="c3-acc" class="text-slate-200">--</strong></span><span>Loss: <strong id="c3-loss" class="text-slate-200">--</strong></span></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Charts Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="glass-panel rounded-2xl p-4 space-y-3">
                <h3 class="font-bold text-xs text-slate-200 flex items-center space-x-2 border-b border-slate-800 pb-2">
                    <i class="fa-solid fa-chart-line text-amber-400"></i><span>Global Server Loss</span>
                </h3>
                <div class="h-48 relative"><canvas id="chartLoss"></canvas></div>
            </div>
            <div class="glass-panel rounded-2xl p-4 space-y-3">
                <h3 class="font-bold text-xs text-slate-200 flex items-center space-x-2 border-b border-slate-800 pb-2">
                    <i class="fa-solid fa-bullseye text-emerald-400"></i><span>Accuracy Comparison</span>
                </h3>
                <div class="h-48 relative"><canvas id="chartAcc"></canvas></div>
            </div>
            <div class="glass-panel rounded-2xl p-4 space-y-3">
                <h3 class="font-bold text-xs text-slate-200 flex items-center space-x-2 border-b border-slate-800 pb-2">
                    <i class="fa-solid fa-network-wired text-cyan-400"></i><span>Network Transfer & Latency</span>
                </h3>
                <div class="h-48 relative"><canvas id="chartNetwork"></canvas></div>
            </div>
        </div>

        <!-- Terminal Logs -->
        <div class="glass-panel rounded-2xl p-5 space-y-3">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                <div class="flex items-center space-x-2"><i class="fa-solid fa-terminal text-emerald-400"></i><h3 class="font-bold text-sm text-slate-100">Flower Protocol Live Logs</h3></div>
                <button onclick="clearLogs()" class="text-xs text-slate-400 hover:text-slate-200 cursor-pointer"><i class="fa-solid fa-trash-can mr-1"></i>Clear</button>
            </div>
            <div id="terminal-logs" class="bg-slate-950 rounded-xl p-4 font-mono text-xs text-emerald-400 space-y-1.5 h-36 overflow-y-auto border border-slate-800/80">
                <div class="text-slate-500">[SYSTEM] Flower SuperLink initialized by Nurmansyah on localhost:8080</div>
                <div class="text-emerald-400">[INFO] Ready to initiate Federated Learning process...</div>
            </div>
        </div>
    </main>

    <!-- JS Script -->
    <script>
        let isRunning = false;
        let currentRound = 0;
        let maxRounds = 10;
        let particles = [];
        const canvas = document.getElementById('networkCanvas');
        const ctx = canvas.getContext('2d');
        let chartLoss, chartAcc, chartNetwork;

        function resizeCanvas() {
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;
        }
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        function getNodeCoords() {
            const w = canvas.width;
            const h = canvas.height;
            return {
                server: { x: w / 2, y: 55 },
                c1: { x: w * 0.18, y: h - 65 },
                c2: { x: w * 0.50, y: h - 65 },
                c3: { x: w * 0.82, y: h - 65 }
            };
        }

        function drawCanvas() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const coords = getNodeCoords();
            [coords.c1, coords.c2, coords.c3].forEach(c => {
                ctx.beginPath();
                ctx.moveTo(coords.server.x, coords.server.y);
                ctx.lineTo(c.x, c.y);
                ctx.strokeStyle = '#1f2937';
                ctx.lineWidth = 2;
                ctx.setLineDash([4, 4]);
                ctx.stroke();
                ctx.setLineDash([]);
            });

            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.progress += p.speed;
                if (p.progress >= 1) { particles.splice(i, 1); continue; }
                const cx = p.startX + (p.endX - p.startX) * p.progress;
                const cy = p.startY + (p.endY - p.startY) * p.progress;
                ctx.beginPath();
                ctx.arc(cx, cy, 4, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.shadowColor = p.color;
                ctx.shadowBlur = 10;
                ctx.fill();
                ctx.shadowBlur = 0;
            }
            requestAnimationFrame(drawCanvas);
        }
        drawCanvas();

        function spawnParticles(from, toList, color) {
            toList.forEach(to => {
                for (let i = 0; i < 5; i++) {
                    setTimeout(() => {
                        particles.push({ startX: from.x, startY: from.y, endX: to.x, endY: to.y, progress: 0, speed: 0.025 + Math.random() * 0.01, color: color });
                    }, i * 150);
                }
            });
        }

        function initCharts() {
            const opts = {
                responsive: true, maintainAspectRatio: false,
                scales: {
                    x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9ca3af', font: { size: 9 } } },
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#9ca3af', font: { size: 9 } } }
                },
                plugins: { legend: { labels: { color: '#d1d5db', font: { size: 9 }, boxWidth: 8 } } }
            };
            chartLoss = new Chart(document.getElementById('chartLoss').getContext('2d'), { type: 'line', data: { labels: [], datasets: [{ label: 'Loss', data: [], borderColor: '#f59e0b', backgroundColor: 'rgba(245,158,11,0.1)', fill: true, tension: 0.3 }] }, options: opts });
            chartAcc = new Chart(document.getElementById('chartAcc').getContext('2d'), { type: 'line', data: { labels: [], datasets: [{ label: 'Global', data: [], borderColor: '#10b981', borderWidth: 2 }, { label: 'Alpha', data: [], borderColor: '#6366f1', borderDash: [2,2] }, { label: 'Beta', data: [], borderColor: '#f59e0b', borderDash: [2,2] }, { label: 'Gamma', data: [], borderColor: '#14b8a6', borderDash: [2,2] }] }, options: opts });
            chartNetwork = new Chart(document.getElementById('chartNetwork').getContext('2d'), { type: 'bar', data: { labels: [], datasets: [{ label: 'MB', data: [], backgroundColor: 'rgba(6,182,212,0.5)', borderColor: '#06b6d4', borderWidth: 1 }] }, options: opts });
        }
        initCharts();

        function logMsg(msg, type = 'info') {
            const logs = document.getElementById('terminal-logs');
            const time = new Date().toLocaleTimeString();
            let color = type === 'warn' ? 'text-amber-400' : (type === 'system' ? 'text-indigo-400' : 'text-emerald-400');
            logs.innerHTML += `<div class="${color}">[${time}] ${msg}</div>`;
            logs.scrollTop = logs.scrollHeight;
        }
        function clearLogs() { document.getElementById('terminal-logs').innerHTML = ''; }

        function startSimulation() {
            if (isRunning) return;
            isRunning = true;
            maxRounds = parseInt(document.getElementById('param-rounds').value);
            document.getElementById('sim-round-max').innerText = maxRounds;
            document.getElementById('btn-start').disabled = true;
            document.getElementById('btn-pause').disabled = false;
            document.getElementById('status-text').innerText = "Simulating FL Protocol";
            logMsg("[FL RUN] Starting Federated Simulation by Nurmansyah...", "system");
            executeRoundLoop();
        }

        function pauseSimulation() {
            isRunning = false;
            document.getElementById('btn-start').disabled = false;
            document.getElementById('btn-pause').disabled = true;
            document.getElementById('status-text').innerText = "Simulation Paused";
        }

        function resetSimulation() {
            isRunning = false;
            currentRound = 0;
            document.getElementById('sim-round-curr').innerText = '0';
            document.getElementById('sim-phase-text').innerText = 'Idle';
            ['c1','c2','c3'].forEach(c => {
                document.getElementById(`${c}-status`).innerText = 'Idle';
                document.getElementById(`${c}-bar`).style.width = '0%';
                document.getElementById(`${c}-acc`).innerText = '--';
                document.getElementById(`${c}-loss`).innerText = '--';
            });
            document.getElementById('srv-acc').innerText = '--';
            document.getElementById('srv-loss').innerText = '--';
            [chartLoss, chartAcc, chartNetwork].forEach(ch => { ch.data.labels = []; ch.data.datasets.forEach(d => d.data = []); ch.update(); });
            particles = [];
            logMsg("[FL RESET] Environment reset.", "system");
        }

        function stepRound() { if (!isRunning && currentRound < maxRounds) executeSingleRound(); }

        function executeRoundLoop() {
            if (!isRunning || currentRound >= maxRounds) {
                if (currentRound >= maxRounds) { logMsg("[FL COMPLETE] Training finished.", "system"); pauseSimulation(); }
                return;
            }
            executeSingleRound(() => { if (isRunning) setTimeout(executeRoundLoop, 1000); });
        }

        function executeSingleRound(cb) {
            currentRound++;
            document.getElementById('sim-round-curr').innerText = currentRound;
            const coords = getNodeCoords();
            document.getElementById('sim-phase-text').innerText = '1. Broadcast';
            logMsg(`--- ROUND ${currentRound}/${maxRounds} ---`, "system");
            spawnParticles(coords.server, [coords.c1, coords.c2, coords.c3], '#10b981');

            setTimeout(() => {
                document.getElementById('sim-phase-text').innerText = '2. Training';
                ['c1','c2','c3'].forEach(c => { document.getElementById(`${c}-status`).innerText = 'Training'; document.getElementById(`${c}-bar`).style.width = '100%'; });
                
                setTimeout(() => {
                    const factor = currentRound / maxRounds;
                    const c1A = (60 + factor*35 + Math.random()*2).toFixed(1);
                    const c2A = (48 + factor*32 + Math.random()*2).toFixed(1);
                    const c3A = (52 + factor*36 + Math.random()*2).toFixed(1);
                    const c1L = (1.5 - factor*1.2).toFixed(2);
                    const c2L = (1.8 - factor*1.1).toFixed(2);
                    const c3L = (1.6 - factor*1.2).toFixed(2);

                    document.getElementById('c1-acc').innerText = c1A+'%'; document.getElementById('c1-loss').innerText = c1L;
                    document.getElementById('c2-acc').innerText = c2A+'%'; document.getElementById('c2-loss').innerText = c2L;
                    document.getElementById('c3-acc').innerText = c3A+'%'; document.getElementById('c3-loss').innerText = c3L;

                    document.getElementById('sim-phase-text').innerText = '3. Uploading';
                    spawnParticles(coords.c1, [coords.server], '#f59e0b');
                    spawnParticles(coords.c2, [coords.server], '#f59e0b');
                    spawnParticles(coords.c3, [coords.server], '#f59e0b');

                    setTimeout(() => {
                        document.getElementById('sim-phase-text').innerText = '4. Aggregating';
                        const srvA = ((parseFloat(c1A)*2100 + parseFloat(c2A)*850 + parseFloat(c3A)*1450)/4400).toFixed(1);
                        const srvL = ((parseFloat(c1L)*2100 + parseFloat(c2L)*850 + parseFloat(c3L)*1450)/4400).toFixed(2);
                        
                        document.getElementById('srv-acc').innerText = srvA+'%';
                        document.getElementById('srv-loss').innerText = srvL;

                        ['c1','c2','c3'].forEach(c => { document.getElementById(`${c}-status`).innerText = 'Synced'; document.getElementById(`${c}-bar`).style.width = '0%'; });

                        chartLoss.data.labels.push(`R${currentRound}`);
                        chartLoss.data.datasets[0].data.push(srvL);
                        chartLoss.update();

                        chartAcc.data.labels.push(`R${currentRound}`);
                        chartAcc.data.datasets[0].data.push(srvA);
                        chartAcc.data.datasets[1].data.push(c1A);
                        chartAcc.data.datasets[2].data.push(c2A);
                        chartAcc.data.datasets[3].data.push(c3A);
                        chartAcc.update();

                        chartNetwork.data.labels.push(`R${currentRound}`);
                        chartNetwork.data.datasets[0].data.push((14.2 + Math.random()*1.5).toFixed(1));
                        chartNetwork.update();

                        logMsg(`[Server] Round ${currentRound} Aggregated -> Global Acc: ${srvA}%, Loss: ${srvL}`);
                        if (cb) cb();
                    }, 1200);
                }, 1200);
            }, 1000);
        }
    </script>
</body>
</html>
"""

# Render dashboard ke Streamlit
components.html(html_dashboard, height=950, scrolling=True)
"use client";

import { Settings, UserRound, Bot } from "lucide-react";
import Board from "./Board";

export default function GameScreen({ mode = "pve" }) {
	const topPlayerName = mode === "pvp" ? "Người B" : "Máy";
	const topPlayerIcon = mode === "pvp" ? <UserRound size={32} /> : <Bot size={32} />;

	return (
		<main className="min-h-screen relative flex flex-col items-center justify-between pb-12 pt-8" style={{ backgroundColor: "#f8f9fa" }}>
			{/* Mảng UI Top Left - Settings */}
			<button type="button" aria-label="Cài đặt" className="absolute top-6 left-6 text-black hover:opacity-70 transition-opacity">
				<Settings size={52} strokeWidth={2.2} />
			</button>

			{/* Mảng UI Top Right - Score */}
			<div className="absolute top-0 right-0 bg-[#d8d9de] text-black w-24 sm:w-32 h-20 sm:h-24 flex items-center justify-center text-4xl sm:text-5xl font-light">
				0
			</div>

			{/* Top Player Nametag */}
			<div className="flex bg-[#4285f4] text-white rounded-2xl px-8 py-3 items-center gap-4 shadow-sm w-auto min-w-[240px] justify-center mt-2 z-10">
				{topPlayerIcon}
				<span className="text-3xl font-semibold">{topPlayerName}</span>
			</div>

			{/* Game Board */}
			<div className="flex-1 flex items-center justify-center w-full z-10">
				<Board />
			</div>

			{/* Bottom Player Nametag */}
			<div className="flex bg-[#4285f4] text-white rounded-2xl px-8 py-3 items-center gap-4 shadow-sm w-auto min-w-[240px] justify-center mb-0 z-10">
				<UserRound size={32} />
				<span className="text-3xl font-semibold">Người A</span>
			</div>

			{/* Mảng UI Bottom Left - Score */}
			<div className="absolute bottom-0 left-0 bg-[#d8d9de] text-black w-24 sm:w-32 h-20 sm:h-24 flex items-center justify-center text-4xl sm:text-5xl font-light">
				0
			</div>
		</main>
	);
}

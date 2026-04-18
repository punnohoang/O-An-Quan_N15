"use client";

import { useCallback, useRef, useState } from "react";
import { Settings, UserRound, Bot } from "lucide-react";
import Board from "./Board";

export default function GameScreen({ mode = "pve" }) {
	const topPlayerName = mode === "pvp" ? "Người B" : "Máy";
	const topPlayerIcon = mode === "pvp" ? <UserRound size={32} /> : <Bot size={32} />;
	const [scores, setScores] = useState({ top: 0, bottom: 0 });
	const [activePlayer, setActivePlayer] = useState("bottom");
	const topScoreRef = useRef(null);
	const bottomScoreRef = useRef(null);
	const topPlayerRef = useRef(null);
	const bottomPlayerRef = useRef(null);

	const topIsActive = activePlayer === "top";
	const bottomIsActive = activePlayer === "bottom";
	const topBadgeClass = topIsActive
		? "bg-[#4285f4] text-white border-blue-400 shadow-blue-200/60"
		: "bg-white text-zinc-900 border-zinc-300";
	const bottomBadgeClass = bottomIsActive
		? "bg-[#ef5350] text-white border-rose-400 shadow-rose-200/60"
		: "bg-white text-zinc-900 border-zinc-300";

	const getScoreTargetPoint = useCallback((owner) => {
		const targetRef = owner === "top" ? topScoreRef.current : bottomScoreRef.current;
		if (!targetRef) return null;

		const rect = targetRef.getBoundingClientRect();
		return {
			x: rect.left + rect.width / 2,
			y: rect.top + rect.height / 2,
		};
	}, []);

	const getPlayerPickupPoint = useCallback((owner) => {
		const targetRef = owner === "top" ? topPlayerRef.current : bottomPlayerRef.current;
		if (!targetRef) return null;

		const rect = targetRef.getBoundingClientRect();
		return {
			x: rect.left + rect.width / 2,
			y: owner === "top" ? rect.bottom + 20 : rect.top - 20,
		};
	}, []);

	return (
		<main className="min-h-screen relative flex flex-col items-center justify-between pb-12 pt-8 bg-zinc-100 text-zinc-900">
			{/* Mảng UI Top Left - Settings */}
			<button type="button" aria-label="Cài đặt" className="absolute top-6 left-6 text-zinc-900 hover:text-black hover:opacity-80 transition-all">
				<Settings size={52} strokeWidth={2.2} />
			</button>

			{/* Mảng UI Top Right - Score */}
			<div ref={topScoreRef} className="absolute top-1/2 right-4 -translate-y-[150%] bg-white text-zinc-900 w-28 sm:w-36 h-20 sm:h-24 flex flex-col items-center justify-center border border-zinc-300 rounded-2xl shadow-xl">
				<span className="text-xs sm:text-sm uppercase tracking-wide text-zinc-400">Kho B</span>
				<span className="text-4xl sm:text-5xl font-light leading-none">{scores.top}</span>
			</div>

			{/* Top Player Nametag */}
			<div ref={topPlayerRef} className={`flex rounded-2xl px-8 py-3 items-center gap-4 shadow-sm border w-auto min-w-[240px] justify-center mt-2 z-10 transition-colors ${topBadgeClass}`}>
				{topPlayerIcon}
				<span className="text-3xl font-semibold">{topPlayerName}</span>
			</div>

			{/* Game Board */}
			<div className="flex-1 flex items-center justify-center w-full z-10">
				<Board mode={mode} onScoresChange={setScores} onTurnChange={setActivePlayer} getScoreTargetPoint={getScoreTargetPoint} getPickupTargetPoint={getPlayerPickupPoint} />
			</div>

			{/* Bottom Player Nametag */}
			<div ref={bottomPlayerRef} className={`flex rounded-2xl px-8 py-3 items-center gap-4 shadow-sm border w-auto min-w-[240px] justify-center mb-0 z-10 transition-colors ${bottomBadgeClass}`}>
				<UserRound size={32} />
				<span className="text-3xl font-semibold">Người A</span>
			</div>

			{/* Mảng UI Bottom Left - Score */}
			<div ref={bottomScoreRef} className="absolute top-1/2 left-4 translate-y-[50%] bg-white text-zinc-900 w-28 sm:w-36 h-20 sm:h-24 flex flex-col items-center justify-center border border-zinc-300 rounded-2xl shadow-xl">
				<span className="text-xs sm:text-sm uppercase tracking-wide text-zinc-400">Kho A</span>
				<span className="text-4xl sm:text-5xl font-light leading-none">{scores.bottom}</span>
			</div>
		</main>
	);
}

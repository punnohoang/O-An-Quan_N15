"use client";
import { useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

export default function Board() {
	const [selectedSquare, setSelectedSquare] = useState(null);

	const topRowIndices = [1, 2, 3, 4, 5];
	const bottomRowIndices = [11, 10, 9, 8, 7];

	const handleSquareClick = (index) => {
		// Ngăn không cho click vào ô Quan (index 0 và 6)
		if (index === 0 || index === 6) return;
		
		// Toggle ô
		if (selectedSquare === index) {
			setSelectedSquare(null);
		} else {
			setSelectedSquare(index);
		}
	};

	const handleDirectionSelect = (e, index, direction) => {
		e.stopPropagation();
		console.log(`Chọn hướng ${direction} từ ô ${index}`);
		setSelectedSquare(null);
		// TODO: Thực hiện logic di chuyển ở đây
	};

	// Danh sách các border-radius tạo hình dáng nhấp nhô giống viên sỏi
	const pebbleShapes = [
		"50% 50% 40% 60% / 60% 40% 50% 50%",
		"40% 60% 50% 50% / 50% 50% 60% 40%",
		"50% 40% 60% 50% / 60% 50% 40% 60%",
		"60% 40% 50% 50% / 40% 60% 50% 50%",
		"45% 55% 45% 55% / 55% 45% 55% 45%",
	];

	// Danh sách các màu sỏi đậm đà (Jewel tones) để lên màu nổi bật và dễ nhìn trên nền xám
	const richColors = [
		"radial-gradient(circle at 30% 30%, #ff5e62, #900c3f)", // Đỏ Ruby
		"radial-gradient(circle at 30% 30%, #56ccf2, #154360)", // Xanh Sapphire
		"radial-gradient(circle at 30% 30%, #58d68d, #145a32)", // Xanh Ngọc Lục
		"radial-gradient(circle at 30% 30%, #f4d03f, #9c640c)", // Vàng Hổ Phách
		"radial-gradient(circle at 30% 30%, #b39ddb, #4a235a)", // Tím Thạch Anh
		"radial-gradient(circle at 30% 30%, #7f8c8d, #1c2833)", // Đen Obsidian
	];

	// Trình bày quân: Sỏi nhỏ cho Dân, Quan sẽ to hơn và giống ngọc nhiều màu
	const renderPieces = (count, isQuan, index) => {
		if (isQuan) {
			// Quan trái Ngọc lục bảo đậm, Quan phải màu Đỏ Ruby/Hổ phách đậm
			const isLeftQuan = index === 0;
			const quanBackground = isLeftQuan 
				? "radial-gradient(circle at 30% 25%, #48c9b0, #117a65, #0b5345)"
				: "radial-gradient(circle at 30% 25%, #f1948a, #c0392b, #7b241c)";
				
			return (
				<div className="flex items-center justify-center w-full h-full">
					{count > 0 && (
						<div 
							className="w-10 h-20 lg:w-14 lg:h-24 shadow-md transition-all scale-100 hover:scale-[1.03]" 
							style={{
								background: quanBackground,
								borderRadius: "40% 60% 50% 50% / 50% 50% 60% 40%",
								boxShadow: "2px 4px 8px rgba(0,0,0,0.4), inset -1px -1px 4px rgba(0,0,0,0.4)"
							}} 
						/>
					)}
				</div>
			);
		}
		
		return (
			<div className="absolute inset-0 p-1 md:p-2 lg:p-3 pointer-events-none">
				{Array.from({ length: count }).map((_, i) => {
					// Lựa chọn màu đậm đà cho hạt
					const shape = pebbleShapes[(i + index) % pebbleShapes.length];
					const rotate = (i * 87 + index * 15) % 360;
					const colorGradient = richColors[(i + (index * 2)) % richColors.length];
					
					// Thuật toán trải "hỗn loạn" rải rác: dùng seed cố định
					const leftPos = ((i * 73 + index * 47) % 60) + 20; // 20% -> 80%
					const topPos = ((i * 97 + index * 13) % 60) + 20; // 20% -> 80%
					
					return (
						<div 
							key={i} 
							className="absolute w-4 h-4 lg:w-5 lg:h-5 transition-all pointer-events-auto cursor-pointer hover:scale-[1.2]" 
							style={{
								left: `${leftPos}%`,
								top: `${topPos}%`,
								background: colorGradient,
								borderRadius: shape,
								transform: `translate(-50%, -50%) rotate(${rotate}deg)`,
								boxShadow: "1px 2px 4px rgba(0,0,0,0.4)"
							}}
						/>
					);
				})}
			</div>
		);
	};

	const renderSquare = (index, isQuan = false, additionalClasses = "") => {
		const isSelected = selectedSquare === index;
		const pieceCount = isQuan ? 1 : 5;

		return (
			<div
				key={index}
				className={`relative flex items-center justify-center cursor-pointer transition-colors ${additionalClasses} ${isSelected ? 'bg-gray-300' : 'bg-[#d8d9de] hover:bg-gray-300'}`}
				onClick={() => handleSquareClick(index)}
			>
				{renderPieces(pieceCount, isQuan, index)}

				{/* Arrow Overlay if selected */}
				{isSelected && !isQuan && (
					<div className="absolute inset-0 flex items-center justify-between px-1 z-10 pointer-events-none">
						<button 
							type="button" 
							className="pointer-events-auto bg-white/70 text-black rounded-full p-1 border border-gray-400 hover:bg-white hover:scale-110 active:scale-95 transition-all shadow-md"
							onClick={(e) => handleDirectionSelect(e, index, "left")}
						>
							<ChevronLeft size={24} strokeWidth={2.5} />
						</button>
						<button 
							type="button" 
							className="pointer-events-auto bg-white/70 text-black rounded-full p-1 border border-gray-400 hover:bg-white hover:scale-110 active:scale-95 transition-all shadow-md"
							onClick={(e) => handleDirectionSelect(e, index, "right")}
						>
							<ChevronRight size={24} strokeWidth={2.5} />
						</button>
					</div>
				)}
			</div>
		);
	};

	return (
		<div className="w-[95%] max-w-[900px] h-48 sm:h-64 shadow-xl rounded-[100px] border border-gray-400 bg-[#d8d9de] overflow-hidden flex">
			{/* Left Quan */}
			<div className="w-[15%] min-w-[70px] h-full flex flex-col border-r border-gray-400">
				{renderSquare(0, true, "h-full w-full border-0")}
			</div>

			{/* Middle Dan Grid (10 squares) */}
			<div className="flex-1 grid grid-cols-5 grid-rows-2 h-full">
				<div className="contents row-start-1">
					{topRowIndices.map((i, idx) => 
						renderSquare(i, false, `border-b border-gray-400 ${idx !== 4 ? 'border-r' : ''}`)
					)}
				</div>
				<div className="contents row-start-2">
					{bottomRowIndices.map((i, idx) => 
						renderSquare(i, false, `${idx !== 4 ? 'border-r border-gray-400' : ''}`)
					)}
				</div>
			</div>

			{/* Right Quan */}
			<div className="w-[15%] min-w-[70px] h-full flex flex-col border-l border-gray-400">
				{renderSquare(6, true, "h-full w-full border-0")}
			</div>
		</div>
	);
}

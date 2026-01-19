"use client";

interface TickerItem {
  id: string;
  text: string;
  highlight?: string;
  icon?: string;
}

interface TickerTapeProps {
  items: TickerItem[];
  speed?: "slow" | "normal" | "fast";
  variant?: "primary" | "secondary";
}

export function TickerTape({
  items,
  speed = "normal",
  variant = "primary",
}: TickerTapeProps) {
  const speedClasses = {
    slow: "animate-ticker-slow",
    normal: "animate-ticker",
    fast: "animate-ticker-fast",
  };

  const variantClasses = {
    primary:
      "bg-gradient-to-r from-amber-500/20 via-yellow-500/20 to-amber-500/20 border-amber-500/30",
    secondary:
      "bg-gradient-to-r from-blue-500/20 via-purple-500/20 to-blue-500/20 border-blue-500/30",
  };

  // Duplicate items for seamless loop
  const duplicatedItems = [...items, ...items];

  return (
    <div
      className={`w-full overflow-hidden border-y ${variantClasses[variant]} backdrop-blur-sm`}
    >
      <div className={`flex gap-8 py-3 ${speedClasses[speed]}`}>
        {duplicatedItems.map((item, index) => (
          <div
            key={`${item.id}-${index}`}
            className="flex items-center gap-2 whitespace-nowrap px-4"
          >
            {item.icon && <span className="text-lg">{item.icon}</span>}
            <span className="text-sm font-medium">
              {item.text}
              {item.highlight && (
                <span className="ml-2 font-bold text-amber-400">
                  {item.highlight}
                </span>
              )}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

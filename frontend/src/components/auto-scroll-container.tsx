import { useEffect, useRef } from "react";

interface AutoScrollContainerProps
  extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export const AutoScrollContainer = ({
  children,
  ...props
}: AutoScrollContainerProps) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (container) {
      container.scrollTo({ top: container.scrollHeight, behavior: "smooth" });
    }
  }, [children]);

  return (
    <div {...props} ref={containerRef}>
      {children}
    </div>
  );
};

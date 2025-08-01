import clsx from "clsx";

export const Button = ({
  className,
  children,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement>) => {
  return (
    <button
      className={clsx(
        `flex h-9 w-fit items-center justify-center rounded-md border-2 border-green-500 bg-green-500 text-white px-3 py-1 text-base shadow-sm transition-colors hover:bg-green-600 hover:border-green-600 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 md:text-sm`,
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
};

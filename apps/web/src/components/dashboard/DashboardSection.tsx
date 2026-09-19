interface DashboardSectionProps {
  title: string;
  description?: string;
  children: React.ReactNode;
}

export default function DashboardSection({
  title,
  description,
  children,
}: DashboardSectionProps) {
  return (
    <section className="mb-10">
      <div className="mb-5 flex flex-col gap-1 border-l-4 border-blue-600 pl-4">
        <h2 className="text-xl font-bold tracking-tight text-slate-900 sm:text-2xl">
          {title}
        </h2>

        {description && (
          <p className="text-sm leading-relaxed text-slate-500">
            {description}
          </p>
        )}
      </div>

      {children}
    </section>
  );
}
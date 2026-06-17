import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | Date): string {
  return new Intl.DateTimeFormat("en-MY", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(date));
}

export function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function getRiskColor(level: string | null | undefined): string {
  switch (level?.toLowerCase()) {
    case "low":
      return "text-risk-low bg-risk-low/10 border-risk-low/30";
    case "medium":
      return "text-risk-medium bg-risk-medium/10 border-risk-medium/30";
    case "high":
      return "text-risk-high bg-risk-high/10 border-risk-high/30";
    case "critical":
      return "text-risk-critical bg-risk-critical/10 border-risk-critical/30";
    default:
      return "text-muted-foreground bg-muted border-border";
  }
}

export function getRiskBadgeVariant(level: string | null | undefined): "default" | "secondary" | "destructive" | "outline" {
  switch (level?.toLowerCase()) {
    case "critical":
    case "high":
      return "destructive";
    case "medium":
      return "secondary";
    default:
      return "outline";
  }
}

"use client";

import { useRouter } from "next/navigation";
import { LogOut, Menu, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { api, type User as ApiUser } from "@/lib/api";

interface NavbarProps {
  user: ApiUser | null;
  onMenuClick?: () => void;
}

export function Navbar({ user, onMenuClick }: NavbarProps) {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await api.logout();
    } catch {
      api.clearToken();
    }
    router.push("/login");
  };

  return (
    <header className="sticky top-0 z-40 flex h-16 items-center justify-between border-b bg-background/95 px-4 backdrop-blur supports-[backdrop-filter]:bg-background/60 lg:px-6">
      <div className="flex items-center gap-3">
        <Button variant="ghost" size="icon" className="lg:hidden" onClick={onMenuClick}>
          <Menu className="h-5 w-5" />
        </Button>
        <div>
          <h1 className="text-lg font-semibold">Compliance Dashboard</h1>
          <p className="text-xs text-muted-foreground hidden sm:block">
            AI-powered contract & policy intelligence
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {user && (
          <div className="hidden sm:flex items-center gap-2 rounded-lg border px-3 py-1.5">
            <User className="h-4 w-4 text-muted-foreground" />
            <div className="text-sm">
              <span className="font-medium">{user.full_name}</span>
              <span className="ml-2 text-xs capitalize text-muted-foreground">
                {user.role.replace("_", " ")}
              </span>
            </div>
          </div>
        )}
        <Button variant="outline" size="sm" onClick={handleLogout}>
          <LogOut className="h-4 w-4" />
          <span className="hidden sm:inline">Logout</span>
        </Button>
      </div>
    </header>
  );
}

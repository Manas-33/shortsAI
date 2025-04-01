"use client"; 

import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { createClient } from "@/utils/supabase/client";

export default function ProtectedRoute({ children }) {
  const router = useRouter();
  const pathname = usePathname();
  const supabase = createClient();

  useEffect(() => {
    async function checkUser() {
      const { data: { session } } = await supabase.auth.getSession();
      
      if (!session && pathname !== "/") {
        router.push("/login");
      } else if (pathname !== "/") {
        router.push("/dashboard");
      }
    }

    checkUser();
  }, [pathname]);

  return children;
}

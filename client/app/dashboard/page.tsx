"use client";
import React, { useEffect, useState } from "react";
import { createClient } from "@/utils/supabase/client";
import { redirect } from "next/navigation";

const Page = () => {
  const [user, setUser] = useState<any>(null);
  const supabase = createClient();
  useEffect(() => {
    const fetchUser = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser();
      setUser(user);
      console.log("User: ", user?.email);
    };
    fetchUser();
  }, []);

  return (
    <div>
      <div>user :{user?.email}</div>
    </div>
  );
};

export default Page;

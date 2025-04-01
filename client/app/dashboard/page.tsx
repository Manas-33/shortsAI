"use client"

import React, { useEffect, useState } from "react"
import { AppSidebar } from "@//components/app-sidebar"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@//components/ui/breadcrumb"
import { Separator } from "@//components/ui/separator"
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@//components/ui/sidebar"
import { PodcastForm } from "@//components/podcast-form"
import { ReelsResults } from "@//components/reels-results"
import { useToast } from "@/components/ui/use-toast"
import { createClient } from "@/utils/supabase/client"

export default function Page() {
  const [isLoading, setIsLoading] = useState(false)
  const [apiResponse, setApiResponse] = useState<{
    message: string
    video_path: string
    clips: Array<{ clip_number: number, url: string }>
  } | null>(null)
  const [username, setusername] = useState("")
  const { toast } = useToast()
  const supabase = createClient()

  useEffect(() => {
    const fetchUser = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser();
      console.log("User data in AppSidebar:", user);

      if (user) {
        setusername(user.email || "Unknown User");
      }
    };

    fetchUser();
  }, []);

  const handlePodcastSubmit = async (url: string, isYoutubeUrl: boolean) => {
    setIsLoading(true)
    
    try {
      const response = await fetch('http://localhost:8000/api/shorts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url,
          username: username,
          num_shorts: 2,
        }),
      })
  
      const data = await response.json()
      console.log('API Response:', data)
  
      if (response.ok) {
        setApiResponse(data)
        toast({
          title: 'Processing completed',
          description: "We've generated shorts from your podcast",
        })
      } else {
        toast({
          title: 'Something went wrong',
          description: data?.error || 'Please try again later',
          variant: 'destructive',
        })
      }
    } catch (error) {
      console.error('API Error:', error)
      toast({
        title: 'Something went wrong',
        description: 'Please try again later',
        variant: 'destructive',
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b">
          <div className="flex items-center gap-2 px-4">
            <SidebarTrigger className="-ml-1" />
            <Separator orientation="vertical" className="mr-2 h-4" />
            <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbItem className="hidden md:block">
                  <BreadcrumbLink href="#">Dashboard</BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator className="hidden md:block" />
                <BreadcrumbItem>
                  <BreadcrumbPage>Podcast to Shorts</BreadcrumbPage>
                </BreadcrumbItem>
              </BreadcrumbList>
            </Breadcrumb>
          </div>
        </header>
        
        <div className="flex flex-1 flex-col gap-6 p-6">
          <div className="mx-auto w-full max-w-3xl">
            <h1 className="mb-6 text-3xl font-bold tracking-tight">Create Shorts from Podcasts</h1>
            <PodcastForm onSubmit={handlePodcastSubmit} isLoading={isLoading} />
            <ReelsResults apiResponse={apiResponse} />
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}
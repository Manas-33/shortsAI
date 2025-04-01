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
import { createClient } from "@/utils/supabase/client"
import { useToast } from "@/components/ui/use-toast"
import { format } from "date-fns"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import Link from "next/link"
import { ArrowLeft, ExternalLink, Video } from "lucide-react"
import { Button } from "@/components/ui/button"

interface ProcessingData {
  id: string
  username: string
  youtube_url: string
  status: string
  cloudinary_url: string | null
  cloudinary_urls: Array<{ url: string, public_id: string }>
  num_shorts: number
  created_at: string
  updated_at: string
  error_message?: string | null
}

export default function HistoryPage() {
  const [isLoading, setIsLoading] = useState(true)
  const [userVideos, setUserVideos] = useState<ProcessingData[]>([])
  const [username, setUsername] = useState("")
  const { toast } = useToast()
  const supabase = createClient()
  const [selectedVideo, setSelectedVideo] = useState<ProcessingData | null>(null)

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const {
          data: { user },
        } = await supabase.auth.getUser();
        
        if (user) {
          const userEmail = user.email || "Unknown User";
          setUsername(userEmail);
          
          // Once we have the username, fetch the user's videos
          await fetchUserVideos(userEmail);
        } else {
          setIsLoading(false);
        }
      } catch (error) {
        console.error("Error fetching user:", error);
        setIsLoading(false);
      }
    };

    fetchUser();
  }, []);
  
  // Function to fetch user's videos
  const fetchUserVideos = async (userEmail: string) => {
    try {
      setIsLoading(true);
      const response = await fetch(`http://localhost:8000/api/shorts/user/${encodeURIComponent(userEmail)}/`);
      
      if (response.ok) {
        const videos = await response.json();
        // Sort by creation date - newest first
        const sortedVideos = videos.sort((a: ProcessingData, b: ProcessingData) => 
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
        setUserVideos(sortedVideos);
      } else {
        console.error("Failed to fetch user videos");
        toast({
          title: "Failed to load history",
          description: "Could not load your processing history",
          variant: "destructive",
        });
      }
    } catch (error) {
      console.error("Error fetching user videos:", error);
      toast({
        title: "Failed to load history",
        description: "Could not load your processing history",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'COMPLETED':
        return <Badge variant="success">Completed</Badge>;
      case 'PENDING':
        return <Badge variant="outline">Pending</Badge>;
      case 'PROCESSING':
        return <Badge variant="secondary">Processing</Badge>;
      case 'FAILED':
        return <Badge variant="destructive">Failed</Badge>;
      default:
        return <Badge>{status}</Badge>;
    }
  };

  const formatDate = (dateString: string) => {
    try {
      return format(new Date(dateString), 'MMM d, yyyy h:mm a');
    } catch (error) {
      return dateString;
    }
  };

  // Group videos by date
  const groupedVideos = userVideos.reduce<Record<string, ProcessingData[]>>((groups, video) => {
    const date = new Date(video.created_at).toDateString();
    if (!groups[date]) {
      groups[date] = [];
    }
    groups[date].push(video);
    return groups;
  }, {});

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
                <BreadcrumbItem>
                  <BreadcrumbLink href="/dashboard">Dashboard</BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator />
                <BreadcrumbItem>
                  <BreadcrumbPage>Processing History</BreadcrumbPage>
                </BreadcrumbItem>
              </BreadcrumbList>
            </Breadcrumb>
            <div className="ml-auto">
              <Button variant="ghost" size="sm" asChild>
                <Link href="/dashboard">
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Back to Dashboard
                </Link>
              </Button>
            </div>
          </div>
        </header>
        
        <div className="flex flex-1 flex-col gap-6 p-6">
          <div className="mx-auto w-full max-w-6xl">
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-3xl font-bold tracking-tight">Processing History</h1>
            </div>
            
            {isLoading ? (
              <div className="flex justify-center p-10">
                <p>Loading your history...</p>
              </div>
            ) : userVideos.length === 0 ? (
              <Card>
                <CardContent className="flex flex-col items-center justify-center p-10">
                  <Video className="h-16 w-16 mb-4 text-muted-foreground" />
                  <h3 className="text-xl font-semibold">No videos processed yet</h3>
                  <p className="text-muted-foreground">
                    Start creating shorts from your podcasts to see your history here
                  </p>
                  <Button asChild className="mt-6">
                    <Link href="/dashboard">
                      Create Your First Short
                    </Link>
                  </Button>
                </CardContent>
              </Card>
            ) : (
              <>
                {/* Video Details Modal */}
                {selectedVideo && (
                  <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4" onClick={() => setSelectedVideo(null)}>
                    <Card className="w-full max-w-3xl" onClick={(e) => e.stopPropagation()}>
                      <CardHeader>
                        <CardTitle>Video Processing Details</CardTitle>
                        <CardDescription>
                          Created on {formatDate(selectedVideo.created_at)}
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          <div>
                            <h3 className="font-medium">Source</h3>
                            <a href={selectedVideo.youtube_url} target="_blank" rel="noopener noreferrer" className="text-blue-500 flex items-center">
                              {selectedVideo.youtube_url}
                              <ExternalLink className="ml-1 h-3 w-3" />
                            </a>
                          </div>
                          
                          <div>
                            <h3 className="font-medium">Status</h3>
                            <div className="flex items-center gap-2">
                              {getStatusBadge(selectedVideo.status)}
                              {selectedVideo.error_message && <span className="text-red-500 text-sm">{selectedVideo.error_message}</span>}
                            </div>
                          </div>
                          
                          {selectedVideo.status === 'COMPLETED' && selectedVideo.cloudinary_urls && (
                            <div>
                              <h3 className="font-medium mb-2">Generated Clips ({selectedVideo.cloudinary_urls.length})</h3>
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {selectedVideo.cloudinary_urls.map((clip, index) => (
                                  <div key={clip.public_id} className="border rounded-md p-2">
                                    <video 
                                      src={clip.url} 
                                      className="w-full h-36 object-cover rounded-md mb-2" 
                                      controls 
                                    />
                                    <div className="flex justify-between items-center">
                                      <span>Clip {index + 1}</span>
                                      <a 
                                        href={clip.url} 
                                        target="_blank" 
                                        rel="noopener noreferrer" 
                                        className="text-blue-500 text-sm"
                                      >
                                        View
                                      </a>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </CardContent>
                      <CardFooter className="flex justify-end gap-2">
                        <Button variant="outline" onClick={() => setSelectedVideo(null)}>Close</Button>
                        {selectedVideo.status === 'COMPLETED' && (
                          <Button asChild>
                            <Link href={`/dashboard?id=${selectedVideo.id}`}>View in Dashboard</Link>
                          </Button>
                        )}
                      </CardFooter>
                    </Card>
                  </div>
                )}
                
                {/* History Table */}
                <Card>
                  <CardHeader>
                    <CardTitle>Processing History</CardTitle>
                    <CardDescription>
                      View all your previous video processing requests
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    {Object.entries(groupedVideos).map(([date, videos]) => (
                      <div key={date} className="mb-8">
                        <h3 className="text-lg font-medium mb-3">{formatDate(date)}</h3>
                        <Table>
                          <TableHeader>
                            <TableRow>
                              <TableHead>Source</TableHead>
                              <TableHead>Status</TableHead>
                              <TableHead>Created</TableHead>
                              <TableHead>Clips</TableHead>
                              <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                          </TableHeader>
                          <TableBody>
                            {videos.map((video) => (
                              <TableRow key={video.id}>
                                <TableCell className="max-w-[200px] truncate">
                                  {video.youtube_url}
                                </TableCell>
                                <TableCell>{getStatusBadge(video.status)}</TableCell>
                                <TableCell>{formatDate(video.created_at)}</TableCell>
                                <TableCell>
                                  {video.status === 'COMPLETED' ? 
                                    (video.cloudinary_urls?.length || 0) : 
                                    '-'}
                                </TableCell>
                                <TableCell className="text-right">
                                  <Button 
                                    variant="ghost" 
                                    size="sm" 
                                    onClick={() => setSelectedVideo(video)}
                                  >
                                    View Details
                                  </Button>
                                </TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </div>
                    ))}
                  </CardContent>
                </Card>
              </>
            )}
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
} 
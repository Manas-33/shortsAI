"use client"

import * as React from "react"
import { Play, Share2, Download } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

interface Clip {
  clip_number: number
  url: string
}

interface ApiResponse {
  message: string
  video_path: string
  clips: Clip[]
}

interface ReelsResultsProps {
  apiResponse: ApiResponse | null
}

export function ReelsResults({ apiResponse }: ReelsResultsProps) {
  const [currentPlayingIndex, setCurrentPlayingIndex] = React.useState<number | null>(null)
  const videoRefs = React.useRef<(HTMLVideoElement | null)[]>([])

  // Function to handle play button click
  const handlePlay = (index: number) => {
    // Pause any currently playing video
    if (currentPlayingIndex !== null && currentPlayingIndex !== index) {
      const currentVideo = videoRefs.current[currentPlayingIndex]
      if (currentVideo) {
        currentVideo.pause()
      }
    }
    
    // Play the selected video
    const video = videoRefs.current[index]
    if (video) {
      if (video.paused) {
        video.play()
        setCurrentPlayingIndex(index)
      } else {
        video.pause()
        setCurrentPlayingIndex(null)
      }
    }
  }

  // Function to handle download
  const handleDownload = (url: string, clipNumber: number) => {
    const a = document.createElement('a')
    a.href = url
    a.download = `clip-${clipNumber}.mp4`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }

  if (!apiResponse || !apiResponse.clips || apiResponse.clips.length === 0) return null

  // Set up videoRefs array based on clips length
  if (videoRefs.current.length !== apiResponse.clips.length) {
    videoRefs.current = Array(apiResponse.clips.length).fill(null)
  }

  return (
    <div id="results-section" className="mt-10">
      <div className="mb-6">
        <h2 className="text-2xl font-bold tracking-tight">Generated Shorts</h2>
        <p className="text-muted-foreground">
          {apiResponse.clips.length} shorts generated successfully
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {apiResponse.clips.map((clip, index) => (
          <Card key={`clip-${clip.clip_number}`} className="overflow-hidden">
            <CardHeader className="p-0">
              <div className="relative aspect-video bg-muted">
                <video
                  ref={(el) => {
                    videoRefs.current[index] = el;
                  }}
                  src={clip.url}
                  className="h-full w-full object-cover"
                  onEnded={() => setCurrentPlayingIndex(null)}
                  playsInline
                />
                <div className="absolute inset-0 flex items-center justify-center" onClick={() => handlePlay(index)}>
                  <Button size="icon" variant="secondary" className="h-12 w-12 rounded-full opacity-90">
                    <Play className="h-6 w-6" />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-4">
              <CardTitle className="line-clamp-2 text-base">Clip {clip.clip_number}</CardTitle>
            </CardContent>
            <CardFooter className="flex justify-between p-4 pt-0">
              <Button variant="outline" size="sm" onClick={() => handleDownload(clip.url, clip.clip_number)}>
                <Download className="mr-2 h-4 w-4" />
                Download
              </Button>
              <Button variant="ghost" size="icon" onClick={() => {
                navigator.clipboard.writeText(clip.url);
                // Could add a toast notification here
              }}>
                <Share2 className="h-4 w-4" />
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  )
}


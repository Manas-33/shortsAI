"use client"

import * as React from "react"
import { Play, Share2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

interface Reel {
  id: string
  title: string
  duration: string
  thumbnail: string
}

export function ReelsResults() {
  const [reels, setReels] = React.useState<Reel[]>([])
  const [source, setSource] = React.useState<string>("")
  const [isVisible, setIsVisible] = React.useState(false)

  React.useEffect(() => {
    const handleReelsGenerated = (event: CustomEvent<{ source: string; count: number }>) => {
      const { source, count } = event.detail
      setSource(source)

      // Generate mock reels data
      const newReels = Array.from({ length: count }).map((_, i) => ({
        id: `reel-${Date.now()}-${i}`,
        title: `Engaging clip ${i + 1} from podcast`,
        duration: `${Math.floor(Math.random() * 30) + 10}s`,
        thumbnail: `/placeholder.svg?height=180&width=320&text=Reel ${i + 1}`,
      }))

      setReels(newReels)
      setIsVisible(true)

      // Scroll to results
      setTimeout(() => {
        document.getElementById("results-section")?.scrollIntoView({ behavior: "smooth" })
      }, 100)
    }

    window.addEventListener("reelsGenerated", handleReelsGenerated as EventListener)

    return () => {
      window.removeEventListener("reelsGenerated", handleReelsGenerated as EventListener)
    }
  }, [])

  if (!isVisible) return null

  return (
    <div id="results-section" className="mt-10">
      <div className="mb-6">
        <h2 className="text-2xl font-bold tracking-tight">Generated Shorts</h2>
        <p className="text-muted-foreground">
          {reels.length} shorts generated from {source}
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {reels.map((reel) => (
          <Card key={reel.id} className="overflow-hidden">
            <CardHeader className="p-0">
              <div className="relative aspect-video bg-muted">
                <img
                  src={reel.thumbnail || "/placeholder.svg"}
                  alt={reel.title}
                  className="h-full w-full object-cover"
                />
                <div className="absolute inset-0 flex items-center justify-center">
                  <Button size="icon" variant="secondary" className="h-12 w-12 rounded-full opacity-90">
                    <Play className="h-6 w-6" />
                  </Button>
                </div>
                <div className="absolute bottom-2 right-2 rounded bg-black/70 px-2 py-1 text-xs text-white">
                  {reel.duration}
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-4">
              <CardTitle className="line-clamp-2 text-base">{reel.title}</CardTitle>
            </CardContent>
            <CardFooter className="flex justify-between p-4 pt-0">
              <Button variant="outline" size="sm">
                Download
              </Button>
              <Button variant="ghost" size="icon">
                <Share2 className="h-4 w-4" />
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  )
}


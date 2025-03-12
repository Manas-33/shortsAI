"use client"

import * as React from "react"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Loader2, Upload, Youtube } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useToast } from "@/components/ui/use-toast"

const youtubeUrlSchema = z.object({
  youtubeUrl: z
    .string()
    .min(1, { message: "YouTube URL is required" })
    .url({ message: "Please enter a valid URL" })
    .refine(
      (url) => {
        // Basic YouTube URL validation
        return (
          url.includes("youtube.com/watch") ||
          url.includes("youtu.be/") ||
          url.includes("youtube.com/v/") ||
          url.includes("youtube.com/embed/")
        )
      },
      { message: "Please enter a valid YouTube URL" },
    ),
})

const fileUploadSchema = z.object({
  file: z
    .instanceof(FileList)
    .refine((files) => files.length > 0, { message: "Please select a file" })
    .refine((files) => files[0].size <= 20 * 1024 * 1024, {
      message: "File size must be less than 20MB",
    })
    .refine(
      (files) => {
        const file = files[0]
        return ["video/mp4", "video/avi", "video/quicktime"].includes(file.type)
      },
      { message: "File must be in MP4, AVI, or MOV format" },
    ),
})

export function PodcastForm() {
  const [isSubmitting, setIsSubmitting] = React.useState(false)
  const [activeTab, setActiveTab] = React.useState("youtube")
  const { toast } = useToast()

  const youtubeForm = useForm<z.infer<typeof youtubeUrlSchema>>({
    resolver: zodResolver(youtubeUrlSchema),
    defaultValues: {
      youtubeUrl: "",
    },
  })

  const fileForm = useForm<z.infer<typeof fileUploadSchema>>({
    resolver: zodResolver(fileUploadSchema),
  })

  async function onYoutubeSubmit(values: z.infer<typeof youtubeUrlSchema>) {
    setIsSubmitting(true)

    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 2000))

      console.log(values)
      toast({
        title: "Processing started",
        description: "We're generating shorts from your YouTube video",
      })

      setIsSubmitting(false)

      window.dispatchEvent(
        new CustomEvent("reelsGenerated", {
          detail: {
            source: values.youtubeUrl,
            count: 5,
          },
        }),
      )
    } catch (error) {
      console.error(error)
      toast({
        title: "Something went wrong",
        description: "Please try again later",
        variant: "destructive",
      })
      setIsSubmitting(false)
    }
  }

  async function onFileSubmit(values: z.infer<typeof fileUploadSchema>) {
    setIsSubmitting(true)

    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 2000))

      console.log(values.file[0])
      toast({
        title: "Processing started",
        description: `We're generating shorts from "${values.file[0].name}"`,
      })

      setIsSubmitting(false)

      window.dispatchEvent(
        new CustomEvent("reelsGenerated", {
          detail: {
            source: values.file[0].name,
            count: 3,
          },
        }),
      )
    } catch (error) {
      console.error(error)
      toast({
        title: "Something went wrong",
        description: "Please try again later",
        variant: "destructive",
      })
      setIsSubmitting(false)
    }
  }

  return (
    <div className="rounded-lg border bg-card p-6 shadow-sm">
      <Tabs defaultValue="youtube" value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="youtube">YouTube URL</TabsTrigger>
          <TabsTrigger value="upload">Upload File</TabsTrigger>
        </TabsList>
        <TabsContent value="youtube" className="mt-6">
          <Form {...youtubeForm}>
            <form onSubmit={youtubeForm.handleSubmit(onYoutubeSubmit)} className="space-y-6">
              <FormField
                control={youtubeForm.control}
                name="youtubeUrl"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>YouTube URL</FormLabel>
                    <FormControl>
                      <div className="flex gap-2">
                        <Input placeholder="https://youtube.com/watch?v=..." {...field} />
                        <Button type="submit" disabled={isSubmitting}>
                          {isSubmitting ? (
                            <>
                              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                              Processing
                            </>
                          ) : (
                            <>
                              <Youtube className="mr-2 h-4 w-4" />
                              Generate
                            </>
                          )}
                        </Button>
                      </div>
                    </FormControl>
                    <FormDescription>Enter the URL of a YouTube podcast video</FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </form>
          </Form>
        </TabsContent>
        <TabsContent value="upload" className="mt-6">
          <Form {...fileForm}>
            <form onSubmit={fileForm.handleSubmit(onFileSubmit)} className="space-y-6">
              <FormField
                control={fileForm.control}
                name="file"
                render={({ field: { onChange, value, ...rest } }) => (
                  <FormItem>
                    <FormLabel>Upload Podcast</FormLabel>
                    <FormControl>
                      <div className="grid gap-4">
                        <Input
                          type="file"
                          accept=".mp4,.avi,.mov"
                          onChange={(e) => onChange(e.target.files)}
                          {...rest}
                        />
                        <Button type="submit" disabled={isSubmitting}>
                          {isSubmitting ? (
                            <>
                              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                              Processing
                            </>
                          ) : (
                            <>
                              <Upload className="mr-2 h-4 w-4" />
                              Upload & Generate
                            </>
                          )}
                        </Button>
                      </div>
                    </FormControl>
                    <FormDescription>Upload a video file (MP4, AVI, MOV, max 20MB)</FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
                
              />
            </form>
          </Form>
        </TabsContent>
      </Tabs>
    </div>
  )
}
  
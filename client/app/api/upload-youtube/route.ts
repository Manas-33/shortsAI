// import ytdl from 'ytdl-core';
// import { v2 as cloudinary } from 'cloudinary';
// import { NextResponse } from 'next/server';

// cloudinary.config({
//   cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
//   api_key: process.env.CLOUDINARY_API_KEY,
//   api_secret: process.env.CLOUDINARY_API_SECRET,
// });

// const MAX_RETRIES = 3;
// const RETRY_DELAY = 2000; // milliseconds

// async function uploadToCloudinaryWithRetry(videoStream, retryCount = 0) {
//   return new Promise((resolve, reject) => {
//     const uploadStream = cloudinary.uploader.upload_stream(
//       { resource_type: 'video', upload_preset: process.env.CLOUDINARY_UPLOAD_PRESET },
//       async (error, result) => {
//         if (error) {
//           console.error('Cloudinary upload error:', error);
//           if (error.http_code === 499 && retryCount < MAX_RETRIES) {
//             console.log(`Retrying upload (attempt ${retryCount + 1})...`);
//             setTimeout(async () => {
//               try {
//                 const retryResult = await uploadToCloudinaryWithRetry(videoStream, retryCount + 1);
//                 resolve(retryResult);
//               } catch (retryError) {
//                 reject(NextResponse.json({ error: 'Cloudinary upload failed after retries' }, { status: 500 }));
//               }
//             }, RETRY_DELAY);
//           } else {
//             reject(NextResponse.json({ error: 'Cloudinary upload failed' }, { status: 500 }));
//           }
//         } else {
//           console.log('Cloudinary upload successful:', result);
//           resolve(NextResponse.json({ cloudinaryUrl: result.secure_url }, { status: 200 }));
//         }
//       }
//     );
//     videoStream.pipe(uploadStream);
//   });
// }

// function isValidYouTubeUrl(url) {
//   const youtubeRegex = /^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
//   return youtubeRegex.test(url);
// }

// export async function POST(req) {
//   try {
//     const { youtubeUrl } = await req.json();
//     console.log(`Received YouTube URL: ${youtubeUrl}`);

//     if (!isValidYouTubeUrl(youtubeUrl)) {
//       console.error('Invalid YouTube URL');
//       return NextResponse.json({ error: 'Invalid YouTube URL' }, { status: 400 });
//     }

//     console.log("Starting ytdl download...");
//     const videoStream = ytdl(youtubeUrl, { quality: 'highestaudio' });
//     console.log("ytdl download started.");

//     // Check for ytdl errors.
//     videoStream.on('error', (err) => {
//       console.error('ytdl error:', err);
//       return NextResponse.json({ error: 'ytdl download error' }, { status: 500 });
//     });

//     const cloudinaryUploadResult = await uploadToCloudinaryWithRetry(videoStream);
//     return cloudinaryUploadResult;

//   } catch (error) {
//     console.error('Error processing YouTube video:', error);
//     return NextResponse.json({ error: 'Failed to process YouTube video' }, { status: 500 });
//   }
// }

// ------------------------------------------------------------------------------------------------------

// import ytdl from 'ytdl-core';
// import { v2 as cloudinary } from 'cloudinary';
// import { NextResponse } from 'next/server';

// cloudinary.config({
//   cloud_name: process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME,
//   api_key: process.env.NEXT_PUBLIC_CLOUDINARY_API_KEY,
//   api_secret: process.env.NEXT_PUBLIC_CLOUDINARY_API_SECRET,
// });

// const MAX_RETRIES = 3;
// const RETRY_DELAY = 2000; // milliseconds

// async function uploadToCloudinaryWithRetry(videoStream, retryCount = 0) {
//   return new Promise((resolve, reject) => {
//     const uploadStream = cloudinary.uploader.upload_stream(
//       { resource_type: 'video', upload_preset: process.env.NEXT_PUBLIC_CLOUDINARY_UPLOAD_PRESET },
//       async (error, result) => {
//         if (error) {
//           console.error('Cloudinary upload error:', error);
//           if (error.http_code === 499 && retryCount < MAX_RETRIES) {
//             console.log(`Retrying upload (attempt ${retryCount + 1})...`);
//             setTimeout(async () => {
//               try {
//                 const retryResult = await uploadToCloudinaryWithRetry(videoStream, retryCount + 1);
//                 resolve(retryResult);
//               } catch (retryError) {
//                 reject(NextResponse.json({ error: 'Cloudinary upload failed after retries' }, { status: 500 }));
//               }
//             }, RETRY_DELAY);
//           } else {
//             reject(NextResponse.json({ error: 'Cloudinary upload failed' }, { status: 500 }));
//           }
//         } else {
//           console.log('Cloudinary upload successful:', result);
//           resolve(NextResponse.json({ cloudinaryUrl: result.secure_url }, { status: 200 }));
//           //send result.
//         }
//       }
//     );
//     videoStream.pipe(uploadStream);
//   });
// }

// function isValidYouTubeUrl(url) {
//   const youtubeRegex = /^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
//   return youtubeRegex.test(url);
// }

// export async function POST(req) {
//   try {
//     const { youtubeUrl } = await req.json();
//     console.log(`Received YouTube URL: ${youtubeUrl}`);

//     if (!isValidYouTubeUrl(youtubeUrl)) {
//       console.error('Invalid YouTube URL');
//       return NextResponse.json({ error: 'Invalid YouTube URL' }, { status: 400 });
//     }

//     console.log("Starting ytdl download...");
//     const videoStream = ytdl(youtubeUrl, { quality: 'highestaudio' });
//     console.log("ytdl download started.");

//     // Check for ytdl errors.
//     let ytdlError = false;
//     videoStream.on('error', (err) => {
//       console.error('ytdl error:', err);
//       ytdlError = true;
//     });

//     // Wait for the 'finish' or 'error' event before proceeding.
//     await new Promise((resolve) => {
//       videoStream.on('finish', resolve);
//       videoStream.on('error', resolve);
//     });

//     if (ytdlError) {
//       return NextResponse.json({ error: 'ytdl download error' }, { status: 500 });
//     }

//     const cloudinaryUploadResult = await uploadToCloudinaryWithRetry(videoStream);
//     return cloudinaryUploadResult;

//   } catch (error) {
//     console.error('Error processing YouTube video:', error);
//     return NextResponse.json({ error: 'Failed to process YouTube video' }, { status: 500 });
//   }
// }

//=====================================================================================================

import ytdl from 'ytdl-core';
import { v2 as cloudinary, UploadApiResponse, UploadApiErrorResponse } from 'cloudinary';
import { NextResponse } from 'next/server';
import { Readable } from 'stream';

cloudinary.config({
  cloud_name: process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME!,
  api_key: process.env.NEXT_PUBLIC_CLOUDINARY_API_KEY!,
  api_secret: process.env.NEXT_PUBLIC_CLOUDINARY_API_SECRET!,
});

const MAX_RETRIES = 3;
const RETRY_DELAY = 2000; // milliseconds

// Define type for the retry function's parameters
async function uploadToCloudinaryWithRetry(
  videoStream: Readable,
  retryCount: number = 0
): Promise<any> {
  return new Promise((resolve, reject) => {
    const uploadStream = cloudinary.uploader.upload_stream(
      {
        resource_type: 'video',
        upload_preset: process.env.NEXT_PUBLIC_CLOUDINARY_UPLOAD_PRESET!,
      },
      async (error: UploadApiErrorResponse | undefined, result: UploadApiResponse | undefined) => {
        if (error) {
          console.error('Cloudinary upload error:', error);
          if (error.http_code === 499 && retryCount < MAX_RETRIES) {
            console.log(`Retrying upload (attempt ${retryCount + 1})...`);
            setTimeout(async () => {
              try {
                const retryResult = await uploadToCloudinaryWithRetry(videoStream, retryCount + 1);
                resolve(retryResult);
              } catch (retryError) {
                reject(NextResponse.json({ error: 'Cloudinary upload failed after retries' }, { status: 500 }));
              }
            }, RETRY_DELAY);
          } else {
            reject(NextResponse.json({ error: 'Cloudinary upload failed' }, { status: 500 }));
          }
        } else if (result) {
          console.log('Cloudinary upload successful:', result);
          resolve(NextResponse.json({ cloudinaryUrl: result.secure_url }, { status: 200 }));
        } else {
          reject(NextResponse.json({ error: 'Cloudinary upload failed' }, { status: 500 }));
        }
      }
    );
    videoStream.pipe(uploadStream);
  });
}

// Type for the YouTube URL validation function
function isValidYouTubeUrl(url: string): boolean {
  const youtubeRegex = /^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
  return youtubeRegex.test(url);
}

// Define the POST function and its request parameter type
export async function POST(req: Request): Promise<NextResponse> {
  try {
    const { youtubeUrl }: { youtubeUrl: string } = await req.json();
    console.log(`Received YouTube URL: ${youtubeUrl}`);

    if (!isValidYouTubeUrl(youtubeUrl)) {
      console.error('Invalid YouTube URL');
      return NextResponse.json({ error: 'Invalid YouTube URL' }, { status: 400 });
    }

    console.log("Starting ytdl download...");
    const videoStream: Readable = ytdl(youtubeUrl, { quality: 'highestaudio' });
    console.log("ytdl download started.");

    // Check for ytdl errors.
    let ytdlError = false;
    videoStream.on('error', (err: Error) => {
      console.error('ytdl error:', err);
      ytdlError = true;
    });

    // Wait for the 'finish' or 'error' event before proceeding.
    await new Promise<void>((resolve) => {
      videoStream.on('finish', resolve);
      videoStream.on('error', resolve);
    });

    if (ytdlError) {
      return NextResponse.json({ error: 'ytdl download error' }, { status: 500 });
    }

    const cloudinaryUploadResult = await uploadToCloudinaryWithRetry(videoStream);
    return cloudinaryUploadResult;

  } catch (error: unknown) {
    console.error('Error processing YouTube video:', error);
    return NextResponse.json({ error: 'Failed to process YouTube video' }, { status: 500 });
  }
}

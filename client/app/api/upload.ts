import { v2 as cloudinary, UploadApiResponse } from 'cloudinary';
import fs from 'fs';
import { NextApiRequest, NextApiResponse } from 'next';
import { IncomingMessage, ServerResponse } from 'http';
import multer from 'multer';

// Configure Cloudinary
cloudinary.config({
  cloud_name: process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME!,
  api_key: process.env.NEXT_PUBLIC_CLOUDINARY_API_KEY!,
  api_secret: process.env.NEXT_PUBLIC_CLOUDINARY_API_SECRET!,
});

export async function uploadToCloudinary(filePath: string): Promise<string> {
  try {
    const result: UploadApiResponse = await cloudinary.uploader.upload(filePath, {
      resource_type: 'video',
      folder: 'podcasts',
    });

    // Delete the temporary file after upload
    fs.unlinkSync(filePath);

    return result.secure_url;
  } catch (error: unknown) {
    // Type assertion to 'Error' to access error.message
    if (error instanceof Error) {
      console.error('Error uploading to Cloudinary:', error.message);
      throw error;
    }
    // In case error is not an instance of Error (though unlikely), we handle it safely
    console.error('An unknown error occurred');
    throw new Error('An unknown error occurred');
  }
}

export async function handleUpload(
  req: NextApiRequest & { file: Express.Multer.File }, 
  res: NextApiResponse
): Promise<void> {
  if (req.method === 'POST') {
    try {
      const file = req.file;
      if (!file) {
        return res.status(400).json({ error: 'No file uploaded' });
      }

      const uploadedUrl = await uploadToCloudinary(file.path);

      return res.status(200).json({ url: uploadedUrl });
    } catch (error: unknown) {
      // Type assertion to 'Error' to access error.message
      if (error instanceof Error) {
        return res.status(500).json({ error: error.message });
      }
      return res.status(500).json({ error: 'An unknown error occurred' });
    }
  }

  return res.status(405).json({ error: 'Method not allowed' });
}


'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function ResumeUploadPage() {
  const [file, setFile] = useState<File | null>(null)
  const [resumeText, setResumeText] = useState('')
  const [isUploading, setIsUploading] = useState(false)
  const [uploadMethod, setUploadMethod] = useState<'file' | 'text'>('file')
  const [uploadResult, setUploadResult] = useState<any>(null)
  const [error, setError] = useState('')
  const router = useRouter()

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      // Validate file type
      const allowedTypes = ['.docx', '.pdf', '.txt']
      const fileExtension = selectedFile.name.toLowerCase().substring(selectedFile.name.lastIndexOf('.'))
      
      if (!allowedTypes.includes(fileExtension)) {
        setError('Please upload a .docx, .pdf, or .txt file')
        return
      }
      
      // Validate file size (10MB max)
      if (selectedFile.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB')
        return
      }
      
      setFile(selectedFile)
      setError('')
    }
  }

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setResumeText(e.target.value)
    setError('')
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setUploadResult(null)
    setIsUploading(true)

    try {
      const formData = new FormData()
      
      if (uploadMethod === 'file' && file) {
        formData.append('file', file)
      } else if (uploadMethod === 'text' && resumeText.trim()) {
        formData.append('text', resumeText)
      } else {
        setError('Please provide a file or paste your resume text')
        setIsUploading(false)
        return
      }

      const response = await fetch('/api/v1/resumes', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Upload failed')
      }

      const result = await response.json()
      setUploadResult(result)
      
      // Redirect to dashboard after successful upload
      setTimeout(() => {
        router.push('/dashboard')
      }, 2000)
      
    } catch (err: any) {
      setError(err.message || 'An error occurred during upload')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-bold tracking-tight text-foreground mb-4">
          Upload Your Resume
        </h1>
        <p className="text-lg text-muted-foreground">
          Get started by uploading your resume or pasting the text
        </p>
      </div>

      <div className="bg-card p-8 rounded-lg border">
        <div className="mb-6">
          <div className="flex space-x-4 mb-6">
            <button
              type="button"
              onClick={() => setUploadMethod('file')}
              className={`px-4 py-2 rounded-md font-medium transition-colors ${
                uploadMethod === 'file'
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
              }`}
            >
              Upload File
            </button>
            <button
              type="button"
              onClick={() => setUploadMethod('text')}
              className={`px-4 py-2 rounded-md font-medium transition-colors ${
                uploadMethod === 'text'
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
              }`}
            >
              Paste Text
            </button>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {uploadMethod === 'file' ? (
            <div>
              <label htmlFor="resume-file" className="block text-sm font-medium text-foreground mb-2">
                Resume File (.docx, .pdf, .txt)
              </label>
              <input
                id="resume-file"
                type="file"
                accept=".docx,.pdf,.txt"
                onChange={handleFileChange}
                className="block w-full text-sm text-border border rounded-md p-3 file:mr-4 file:mt-0 file:py-2 file:px-4 file:py-1 file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-primary-foreground hover:file:bg-primary/90 cursor-pointer"
              />
              {file && (
                <div className="mt-2 p-3 bg-muted rounded-md">
                  <p className="text-sm text-muted-foreground">
                    <strong>Selected:</strong> {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div>
              <label htmlFor="resume-text" className="block text-sm font-medium text-foreground mb-2">
                Resume Text
              </label>
              <textarea
                id="resume-text"
                rows={12}
                value={resumeText}
                onChange={handleTextChange}
                placeholder="Paste your resume text here..."
                className="block w-full text-sm text-border border rounded-md p-3 focus:ring-2 focus:ring-ring focus:ring-offset-2"
              />
              <p className="mt-2 text-sm text-muted-foreground">
                {resumeText.length} characters
              </p>
            </div>
          )}

          {error && (
            <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-md">
              <p className="text-sm text-destructive">{error}</p>
            </div>
          )}

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={isUploading || (!file && uploadMethod === 'file') || (!resumeText.trim() && uploadMethod === 'text')}
              className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-12 px-8"
            >
              {isUploading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-r-2 border-t-2 border-l-2 border-primary-foreground mr-2"></div>
                  Uploading...
                </>
              ) : (
                'Upload Resume'
              )}
            </button>
          </div>
        </form>

        {uploadResult && (
          <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
            <h3 className="text-lg font-semibold text-green-800 mb-2">Upload Successful!</h3>
            <div className="text-sm text-green-700">
              <p><strong>Resume ID:</strong> {uploadResult.id}</p>
              <p><strong>Title:</strong> {uploadResult.title}</p>
              <p><strong>Status:</strong> {uploadResult.is_active}</p>
            </div>
            <p className="mt-3 text-sm text-muted-foreground">
              Redirecting to dashboard...
            </p>
          </div>
        )}
      </div>

      <div className="mt-8 text-center">
        <p className="text-sm text-muted-foreground">
          Your resume will be securely stored and used to generate personalized job application materials.
        </p>
      </div>
    </div>
  )
}

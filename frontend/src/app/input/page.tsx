"use client"

import { useState } from 'react'
import { AppLayout } from '@/components/layout/app-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { 
  Upload, 
  FileText, 
  Target,
  Plus,
  X,
  Check,
  Sparkles,
  Briefcase,
  Zap,
  ArrowRight,
  Info,
  CheckCircle2,
  AlertCircle,
  Calendar,
  Clock
} from 'lucide-react'

// Mock data
const mockResumes = [
  {
    id: 1,
    title: "Senior Frontend Developer Resume",
    fileName: "john_doe_frontend_dev.pdf",
    uploadedDate: "2024-01-15",
    status: "active",
    lastUsed: "2 days ago",
    fitScore: 85
  },
  {
    id: 2,
    title: "Full Stack Developer Resume",
    fileName: "john_doe_full_stack.pdf",
    uploadedDate: "2024-01-10",
    status: "active",
    lastUsed: "1 week ago",
    fitScore: 72
  },
  {
    id: 3,
    title: "Software Engineer Resume",
    fileName: "john_doe_software_eng.pdf",
    uploadedDate: "2024-01-05",
    status: "archived",
    lastUsed: "2 weeks ago",
    fitScore: 68
  }
]

export default function InputPage() {
  const [selectedResume, setSelectedResume] = useState<number | null>(null)
  const [jobDescription, setJobDescription] = useState('')
  const [analysisName, setAnalysisName] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setUploadedFile(file)
    }
  }

  const handleAnalyze = async () => {
    if (!selectedResume && !uploadedFile) {
      alert('Please select or upload a resume')
      return
    }
    if (!jobDescription.trim()) {
      alert('Please enter a job description')
      return
    }

    setIsAnalyzing(true)
    // Mock analysis process
    setTimeout(() => {
      setIsAnalyzing(false)
      // Redirect to fit analysis page
      window.location.href = '/fit-analysis'
    }, 2000)
  }

  const removeUploadedFile = () => {
    setUploadedFile(null)
  }

  const getStatusBadge = (status: string) => {
    const variants = {
      active: { variant: "default" as const, color: "bg-green-500" },
      archived: { variant: "secondary" as const, color: "bg-gray-500" }
    }
    return variants[status as keyof typeof variants] || variants.archived
  }

  const getFitScoreColor = (score: number) => {
    if (score >= 80) return "text-green-600 bg-green-50"
    if (score >= 60) return "text-yellow-600 bg-yellow-50"
    return "text-red-600 bg-red-50"
  }

  return (
    <AppLayout>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20">
        <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
          {/* Enhanced Header */}
          <div className="text-center space-y-4">
            <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-full text-sm font-medium">
              <Sparkles className="mr-2 h-4 w-4" />
              AI-Powered Job Matching
            </div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-indigo-900 bg-clip-text text-transparent">
              Find Your Perfect Match
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
              Upload your resume and paste the job description to get instant AI-powered compatibility analysis with personalized recommendations.
            </p>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white/80 backdrop-blur-sm rounded-xl p-4 border border-white/20 shadow-lg">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <FileText className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Resumes</p>
                  <p className="text-2xl font-bold text-gray-900">12</p>
                </div>
              </div>
            </div>
            <div className="bg-white/80 backdrop-blur-sm rounded-xl p-4 border border-white/20 shadow-lg">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Target className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Analyses Completed</p>
                  <p className="text-2xl font-bold text-gray-900">48</p>
                </div>
              </div>
            </div>
            <div className="bg-white/80 backdrop-blur-sm rounded-xl p-4 border border-white/20 shadow-lg">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Zap className="h-5 w-5 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Avg. Fit Score</p>
                  <p className="text-2xl font-bold text-gray-900">78%</p>
                </div>
              </div>
            </div>
          </div>

          <div className="grid gap-8 lg:grid-cols-2">
            {/* Enhanced Resume Selection */}
            <Card className="bg-white/90 backdrop-blur-sm border-0 shadow-2xl">
              <CardHeader className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-t-xl">
                <CardTitle className="flex items-center text-xl">
                  <FileText className="mr-3 h-6 w-6" />
                  Select Your Resume
                </CardTitle>
                <CardDescription className="text-blue-100">
                  Choose from existing resumes or upload a new one
                </CardDescription>
              </CardHeader>
              <CardContent className="p-6 space-y-6">
                {/* Existing Resumes */}
                <div>
                  <h4 className="font-bold text-gray-900 mb-6 flex items-center text-lg">
                    <div className="p-2 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg mr-3">
                      <Briefcase className="h-5 w-5 text-white" />
                    </div>
                    Your Resumes
                  </h4>
                  <div className="space-y-4">
                    {mockResumes.map((resume) => (
                      <div
                        key={resume.id}
                        className={`group relative p-6 rounded-2xl border-2 cursor-pointer transition-all duration-300 transform hover:scale-[1.02] ${
                          selectedResume === resume.id
                            ? 'border-blue-500 bg-gradient-to-r from-blue-50 via-indigo-50 to-purple-50 shadow-2xl ring-4 ring-blue-200 ring-opacity-50'
                            : 'border-gray-200 hover:border-blue-300 hover:shadow-xl bg-white hover:bg-gradient-to-r hover:from-gray-50 hover:to-blue-50'
                        }`}
                        onClick={() => setSelectedResume(resume.id)}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center mb-3">
                              <h5 className="font-bold text-gray-900 text-lg">{resume.title}</h5>
                              {selectedResume === resume.id && (
                                <div className="ml-3 flex items-center px-3 py-1 bg-blue-500 text-white rounded-full text-sm font-medium">
                                  <CheckCircle2 className="mr-1 h-4 w-4" />
                                  Selected
                                </div>
                              )}
                            </div>
                            <div className="flex items-center mb-4 text-gray-600">
                              <FileText className="mr-2 h-4 w-4 text-gray-400" />
                              <span className="text-sm">{resume.fileName}</span>
                              <span className="mx-2 text-gray-300">•</span>
                              <Calendar className="mr-2 h-4 w-4 text-gray-400" />
                              <span className="text-sm">Uploaded {resume.uploadedDate}</span>
                            </div>
                            <div className="flex flex-wrap items-center gap-3">
                              <Badge 
                                variant={getStatusBadge(resume.status).variant} 
                                className={`text-xs font-medium px-3 py-1 rounded-full ${
                                  resume.status === 'active' 
                                    ? 'bg-green-100 text-green-800 hover:bg-green-200' 
                                    : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                                } transition-colors duration-200`}
                              >
                                {resume.status}
                              </Badge>
                              <div className="flex items-center text-xs text-gray-500 bg-gray-50 px-3 py-1 rounded-full">
                                <Clock className="mr-1 h-3 w-3" />
                                Used {resume.lastUsed}
                              </div>
                              <div className={`px-3 py-1 rounded-full text-xs font-bold border ${
                                resume.fitScore >= 80 
                                  ? 'bg-green-100 text-green-800 border-green-300' 
                                  : resume.fitScore >= 60 
                                  ? 'bg-yellow-100 text-yellow-800 border-yellow-300'
                                  : 'bg-red-100 text-red-800 border-red-300'
                              }`}>
                                <div className="flex items-center">
                                  <Target className="mr-1 h-3 w-3" />
                                  {resume.fitScore}% match
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        {selectedResume === resume.id && (
                          <div className="absolute top-2 right-2">
                            <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Enhanced Upload Section */}
                <div className="border-t pt-6">
                  <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
                    <Plus className="mr-2 h-4 w-4" />
                    Upload New Resume
                  </h4>
                  {uploadedFile ? (
                    <div className="p-4 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-xl">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <div className="p-2 bg-green-100 rounded-lg mr-3">
                            <FileText className="h-5 w-5 text-green-600" />
                          </div>
                          <div>
                            <span className="font-medium text-gray-900">{uploadedFile.name}</span>
                            <span className="text-sm text-gray-600 ml-2">
                              ({(uploadedFile.size / 1024).toFixed(1)} KB)
                            </span>
                          </div>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={removeUploadedFile}
                          className="text-red-600 hover:text-red-700 hover:bg-red-50"
                        >
                          <X className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-blue-400 hover:bg-blue-50/30 transition-all duration-200">
                      <div className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-100 to-indigo-100 rounded-full flex items-center justify-center mb-4">
                        <Upload className="h-8 w-8 text-blue-600" />
                      </div>
                      <p className="text-gray-700 font-medium mb-2">Drop your resume here</p>
                      <p className="text-sm text-gray-500 mb-4">or click to browse files</p>
                      <p className="text-xs text-gray-400 mb-4">PDF, DOC, DOCX (Max 10MB)</p>
                      <input
                        type="file"
                        accept=".pdf,.doc,.docx"
                        onChange={handleFileUpload}
                        className="hidden"
                        id="resume-upload"
                      />
                      <Button asChild className="bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700">
                        <label htmlFor="resume-upload" className="cursor-pointer">
                          Choose File
                        </label>
                      </Button>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Enhanced Job Description Input */}
            <Card className="bg-white/90 backdrop-blur-sm border-0 shadow-2xl">
              <CardHeader className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-t-xl">
                <CardTitle className="flex items-center text-xl">
                  <Target className="mr-3 h-6 w-6" />
                  Job Description
                </CardTitle>
                <CardDescription className="text-indigo-100">
                  Paste the complete job description for accurate analysis
                </CardDescription>
              </CardHeader>
              <CardContent className="p-6 space-y-6">
                {/* Analysis Name */}
                <div>
                  <label htmlFor="analysis-name" className="block text-sm font-semibold text-gray-900 mb-2">
                    Analysis Name <span className="text-gray-400 font-normal">(Optional)</span>
                  </label>
                  <Input
                    id="analysis-name"
                    placeholder="e.g., Senior Frontend Developer at TechCorp"
                    value={analysisName}
                    onChange={(e) => setAnalysisName(e.target.value)}
                    className="border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>

                {/* Job Description Text */}
                <div>
                  <label htmlFor="job-description" className="block text-sm font-semibold text-gray-900 mb-2">
                    Job Description <span className="text-red-500">*</span>
                  </label>
                  <Textarea
                    id="job-description"
                    placeholder="Paste the complete job description here... Include requirements, responsibilities, and qualifications for the best analysis results."
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    rows={12}
                    className="resize-none border-gray-200 focus:border-blue-500 focus:ring-blue-500"
                  />
                  <div className="flex items-center justify-between mt-2">
                    <p className="text-xs text-gray-500">
                      {jobDescription.length} characters
                    </p>
                    {jobDescription.length > 0 && (
                      <div className="flex items-center text-xs text-green-600">
                        <CheckCircle2 className="h-3 w-3 mr-1" />
                        Ready for analysis
                      </div>
                    )}
                  </div>
                </div>

                {/* Enhanced Tips Section */}
                <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-4">
                  <div className="flex items-start">
                    <Info className="h-5 w-5 text-blue-600 mr-3 mt-0.5 flex-shrink-0" />
                    <div>
                      <h5 className="font-semibold text-blue-900 mb-2">Pro Tips for Best Results:</h5>
                      <ul className="text-sm text-blue-800 space-y-2">
                        <li className="flex items-start">
                          <CheckCircle2 className="h-4 w-4 mr-2 mt-0.5 text-blue-600 flex-shrink-0" />
                          Include the complete job description with all requirements
                        </li>
                        <li className="flex items-start">
                          <CheckCircle2 className="h-4 w-4 mr-2 mt-0.5 text-blue-600 flex-shrink-0" />
                          Ensure your resume is up-to-date with recent experience
                        </li>
                        <li className="flex items-start">
                          <CheckCircle2 className="h-4 w-4 mr-2 mt-0.5 text-blue-600 flex-shrink-0" />
                          The AI will identify skill gaps and provide tailored recommendations
                        </li>
                        <li className="flex items-start">
                          <CheckCircle2 className="h-4 w-4 mr-2 mt-0.5 text-blue-600 flex-shrink-0" />
                          Results include compatibility score and improvement suggestions
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Enhanced Analysis Button */}
          <Card className="bg-gradient-to-r from-purple-500 to-pink-500 text-white border-0 shadow-2xl">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-xl font-bold mb-2">Ready to Analyze?</h4>
                  <div className="flex items-center space-x-4 text-purple-100">
                    <div className="flex items-center">
                      {selectedResume || uploadedFile ? (
                        <>
                          <CheckCircle2 className="mr-2 h-4 w-4" />
                          Resume selected
                        </>
                      ) : (
                        <>
                          <AlertCircle className="mr-2 h-4 w-4" />
                          No resume selected
                        </>
                      )}
                    </div>
                    <span>•</span>
                    <div className="flex items-center">
                      {jobDescription.trim() ? (
                        <>
                          <CheckCircle2 className="mr-2 h-4 w-4" />
                          Job description provided
                        </>
                      ) : (
                        <>
                          <AlertCircle className="mr-2 h-4 w-4" />
                          No job description
                        </>
                      )}
                    </div>
                  </div>
                </div>
                <Button
                  onClick={handleAnalyze}
                  disabled={isAnalyzing || (!selectedResume && !uploadedFile) || !jobDescription.trim()}
                  size="lg"
                  className="bg-white text-purple-600 hover:bg-purple-50 font-semibold px-8"
                >
                  {isAnalyzing ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-purple-600 mr-3" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Target className="mr-2 h-5 w-5" />
                      Start Analysis
                      <ArrowRight className="ml-2 h-5 w-5" />
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppLayout>
  )
}

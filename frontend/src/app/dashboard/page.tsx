"use client"

import { AppLayout } from '@/components/layout/app-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  FileText, 
  Target, 
  TrendingUp, 
  Calendar,
  Plus,
  ArrowRight,
  Sparkles,
  Briefcase,
  Zap,
  Users,
  BarChart3,
  Clock,
  CheckCircle2,
  AlertCircle,
  Star
} from 'lucide-react'

// Mock data
const recentAnalyses = [
  {
    id: 1,
    name: "Senior Frontend Developer at TechCorp",
    type: "Fit Analysis",
    score: 85,
    date: "2024-01-15",
    status: "completed",
    company: "TechCorp",
    location: "San Francisco, CA"
  },
  {
    id: 2,
    name: "Full Stack Engineer at StartupXYZ",
    type: "Fit Analysis", 
    score: 72,
    date: "2024-01-14",
    status: "completed",
    company: "StartupXYZ",
    location: "Remote"
  },
  {
    id: 3,
    name: "React Developer at DigitalAgency",
    type: "Tailoring Review",
    score: null,
    date: "2024-01-13",
    status: "in_progress",
    company: "DigitalAgency",
    location: "New York, NY"
  },
  {
    id: 4,
    name: "UI/UX Designer at CreativeStudio",
    type: "Fit Analysis",
    score: 91,
    date: "2024-01-12",
    status: "completed",
    company: "CreativeStudio",
    location: "Los Angeles, CA"
  }
]

const quickStats = [
  {
    title: "Total Analyses",
    value: "24",
    change: "+3 this week",
    icon: Target,
    color: "from-blue-500 to-blue-600",
    bgColor: "from-blue-50 to-blue-100",
    iconColor: "text-blue-600"
  },
  {
    title: "Avg. Fit Score",
    value: "78%",
    change: "+5% improvement",
    icon: TrendingUp,
    color: "from-green-500 to-green-600",
    bgColor: "from-green-50 to-green-100",
    iconColor: "text-green-600"
  },
  {
    title: "Resumes Uploaded",
    value: "12",
    change: "+2 this month",
    icon: FileText,
    color: "from-purple-500 to-purple-600",
    bgColor: "from-purple-50 to-purple-100",
    iconColor: "text-purple-600"
  },
  {
    title: "Applications Sent",
    value: "8",
    change: "+1 this week",
    icon: Briefcase,
    color: "from-orange-500 to-orange-600",
    bgColor: "from-orange-50 to-orange-100",
    iconColor: "text-orange-600"
  }
]

const quickActions = [
  {
    title: "Upload New Resume",
    description: "Add a new resume to analyze",
    icon: FileText,
    href: "/input",
    color: "from-blue-500 to-indigo-600"
  },
  {
    title: "Analyze Job Description",
    description: "Check compatibility with your resume",
    icon: Target,
    href: "/input",
    color: "from-green-500 to-emerald-600"
  },
  {
    title: "Track Applications",
    description: "Monitor your job application status",
    icon: Briefcase,
    href: "#",
    color: "from-purple-500 to-pink-600"
  },
  {
    title: "Skill Gap Analysis",
    description: "Identify areas for improvement",
    icon: TrendingUp,
    href: "#",
    color: "from-orange-500 to-red-600"
  }
]

const getScoreColor = (score: number) => {
  if (score >= 80) return "bg-green-500"
  if (score >= 60) return "bg-yellow-500"
  return "bg-red-500"
}

const getScoreBadgeColor = (score: number) => {
  if (score >= 80) return "bg-green-100 text-green-800"
  if (score >= 60) return "bg-yellow-100 text-yellow-800"
  return "bg-red-100 text-red-800"
}

const getStatusBadge = (status: string) => {
  const variants = {
    completed: { variant: "default" as const, text: "Completed", color: "bg-green-100 text-green-800" },
    in_progress: { variant: "secondary" as const, text: "In Progress", color: "bg-yellow-100 text-yellow-800" },
    pending: { variant: "outline" as const, text: "Pending", color: "bg-gray-100 text-gray-800" }
  }
  return variants[status as keyof typeof variants] || variants.pending
}

export default function DashboardPage() {
  return (
    <AppLayout>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50/20">
        <div className="max-w-7xl mx-auto px-6 py-8 space-y-8">
          {/* Enhanced Header */}
          <div className="text-center space-y-4">
            <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-full text-sm font-medium">
              <Sparkles className="mr-2 h-4 w-4" />
              Welcome Back!
            </div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-indigo-900 bg-clip-text text-transparent">
              Your Job Search Dashboard
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
              Track your job applications, analyze fit scores, and get AI-powered recommendations to land your dream job.
            </p>
          </div>

          {/* Enhanced Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {quickStats.map((stat, index) => {
              const Icon = stat.icon
              return (
                <Card key={index} className="bg-white/90 backdrop-blur-sm border-0 shadow-xl hover:shadow-2xl transition-all duration-300">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div className={`p-3 bg-gradient-to-r ${stat.bgColor} rounded-xl`}>
                        <Icon className={`h-6 w-6 ${stat.iconColor}`} />
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-green-600 font-medium">{stat.change}</p>
                      </div>
                    </div>
                    <div>
                      <p className="text-3xl font-bold text-gray-900 mb-1">{stat.value}</p>
                      <p className="text-sm text-gray-600">{stat.title}</p>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>

          {/* Quick Actions */}
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <Zap className="mr-3 h-6 w-6 text-yellow-500" />
              Quick Actions
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {quickActions.map((action, index) => {
                const Icon = action.icon
                return (
                  <Card key={index} className="group hover:shadow-2xl transition-all duration-300 cursor-pointer border-0 bg-white/90 backdrop-blur-sm">
                    <CardContent className="p-6 text-center">
                      <div className={`inline-flex p-4 bg-gradient-to-r ${action.color} rounded-xl mb-4 group-hover:scale-110 transition-transform duration-300`}>
                        <Icon className="h-8 w-8 text-white" />
                      </div>
                      <h3 className="font-semibold text-gray-900 mb-2">{action.title}</h3>
                      <p className="text-sm text-gray-600 mb-4">{action.description}</p>
                      <Button className={`bg-gradient-to-r ${action.color} hover:opacity-90 text-white border-0 w-full`}>
                        Get Started
                        <ArrowRight className="ml-2 h-4 w-4" />
                      </Button>
                    </CardContent>
                  </Card>
                )
              })}
            </div>
          </div>

          {/* Recent Analyses */}
          <div>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                <BarChart3 className="mr-3 h-6 w-6 text-blue-500" />
                Recent Analyses
              </h2>
              <Button variant="outline" className="border-gray-200 hover:border-blue-500">
                View All
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
            <div className="grid gap-4">
              {recentAnalyses.map((analysis) => (
                <Card key={analysis.id} className="bg-white/90 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-all duration-300">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center mb-2">
                          <h3 className="text-lg font-semibold text-gray-900">{analysis.name}</h3>
                          <Badge className={`ml-3 ${getStatusBadge(analysis.status).color}`}>
                            {getStatusBadge(analysis.status).text}
                          </Badge>
                        </div>
                        <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                          <div className="flex items-center">
                            <Briefcase className="mr-1 h-4 w-4" />
                            {analysis.company}
                          </div>
                          <div className="flex items-center">
                            <Calendar className="mr-1 h-4 w-4" />
                            {analysis.date}
                          </div>
                          <div className="flex items-center">
                            <Users className="mr-1 h-4 w-4" />
                            {analysis.location}
                          </div>
                        </div>
                        <div className="flex items-center space-x-4">
                          <Badge variant="outline" className="border-gray-200">
                            {analysis.type}
                          </Badge>
                          {analysis.score && (
                            <div className="flex items-center space-x-2">
                              <span className="text-sm text-gray-600">Fit Score:</span>
                              <div className="flex items-center">
                                <div className={`w-2 h-2 rounded-full ${getScoreColor(analysis.score)} mr-2`}></div>
                                <span className="font-semibold text-gray-900">{analysis.score}%</span>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center space-x-3">
                        {analysis.status === "completed" && (
                          <Button className="bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700">
                            View Results
                            <ArrowRight className="ml-2 h-4 w-4" />
                          </Button>
                        )}
                        {analysis.status === "in_progress" && (
                          <Button variant="outline" className="border-yellow-300 text-yellow-600 hover:bg-yellow-50">
                            <Clock className="mr-2 h-4 w-4" />
                            In Progress
                          </Button>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Achievement Section */}
          <Card className="bg-gradient-to-r from-purple-500 to-pink-500 text-white border-0 shadow-2xl">
            <CardContent className="p-8">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold mb-2 flex items-center">
                    <Star className="mr-3 h-6 w-6" />
                    You're Doing Great!
                  </h2>
                  <p className="text-purple-100 text-lg mb-4">
                    Your average fit score of 78% puts you in the top 25% of candidates. Keep up the excellent work!
                  </p>
                  <div className="flex items-center space-x-6">
                    <div className="flex items-center">
                      <CheckCircle2 className="mr-2 h-5 w-5" />
                      <span>24 Analyses Completed</span>
                    </div>
                    <div className="flex items-center">
                      <TrendingUp className="mr-2 h-5 w-5" />
                      <span>5% Score Improvement</span>
                    </div>
                  </div>
                </div>
                <div className="text-center">
                  <div className="text-5xl font-bold mb-2">78%</div>
                  <p className="text-purple-100">Avg. Fit Score</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppLayout>
  )
}

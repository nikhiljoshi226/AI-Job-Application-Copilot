import Link from 'next/link'
import { AppLayout } from '@/components/layout/app-layout'

export default function Home() {
  return (
    <AppLayout>
      <main className="container mx-auto px-4 py-8">
        {/* Debug section to verify Tailwind is working */}
        <div className="mb-8 p-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg">
          <h2 className="text-xl font-bold mb-2">🎨 Tailwind CSS Debug Test</h2>
          <p>If you see this with a blue-purple gradient background, Tailwind CSS is working correctly!</p>
        </div>

        <div className="text-center">
          <h1 className="text-4xl font-bold tracking-tight text-foreground mb-4">
            AI Job Application Copilot
          </h1>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Your intelligent companion for job applications. Analyze resumes, parse job descriptions, 
            generate tailored content, and prepare for interviews.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto mb-12">
            <div className="bg-card p-6 rounded-lg border shadow-lg hover:shadow-xl transition-shadow">
              <h2 className="text-2xl font-semibold mb-3">Resume Analysis</h2>
              <p className="text-muted-foreground mb-4">
                Parse and analyze your resume to extract skills, experience, and achievements.
              </p>
              <Link 
                href="/dashboard" 
                className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
              >
                Get Started
              </Link>
            </div>
            
            <div className="bg-card p-6 rounded-lg border shadow-lg hover:shadow-xl transition-shadow">
              <h2 className="text-2xl font-semibold mb-3">Job Analysis</h2>
              <p className="text-muted-foreground mb-4">
                Extract requirements and insights from job descriptions to match your profile.
              </p>
              <Link 
                href="/input" 
                className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
              >
                Analyze Jobs
              </Link>
            </div>
            
            <div className="bg-card p-6 rounded-lg border shadow-lg hover:shadow-xl transition-shadow">
              <h2 className="text-2xl font-semibold mb-3">Application Tracker</h2>
              <p className="text-muted-foreground mb-4">
                Track your applications throughout the entire hiring process.
              </p>
              <Link 
                href="/dashboard" 
                className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
              >
                Track Applications
              </Link>
            </div>
          </div>
          
          <div className="text-center">
            <p className="text-muted-foreground">
              Ready to optimize your job search?{' '}
              <Link href="/dashboard" className="text-primary hover:underline">
                Go to Dashboard
              </Link>
            </p>
          </div>
        </div>
      </main>
    </AppLayout>
  )
}

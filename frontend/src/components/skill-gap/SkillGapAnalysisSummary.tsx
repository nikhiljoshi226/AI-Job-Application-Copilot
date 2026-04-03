import React, { useState, useEffect } from 'react';
import { TrendingUp, AlertCircle, CheckCircle, AlertTriangle, BookOpen, Target, BarChart3, Download, RefreshCw, Eye, Brain, Lightbulb, Calendar, Users } from 'lucide-react';

interface SkillGapAnalysisData {
  id: number;
  analysis_name: string;
  resume_id: number;
  job_description_ids: number[];
  job_count: number;
  analysis_summary: {
    overall_assessment: string;
    assessment_message: string;
    skill_coverage_score: number;
    total_missing_skills: number;
    high_frequency_gaps: number;
    critical_gaps: number;
    key_findings: string[];
    recommendations_summary: string[];
  };
  missing_skills: {
    missing_technical: Array<{
      skill: string;
      frequency: number;
      importance: number;
      jobs: string[];
      companies: string[];
      priority_score: number;
    }>;
    missing_soft_skills: Array<{
      skill: string;
      frequency: number;
      importance: number;
      jobs: string[];
      companies: string[];
      priority_score: number;
    }>;
    gap_summary: {
      total_missing_skills: number;
      categories: Record<string, number>;
    };
  };
  repeated_gaps: {
    high_frequency_gaps: Array<{
      skill: string;
      category: string;
      frequency: number;
      importance: number;
      jobs: string[];
      companies: string[];
      priority_score: number;
    }>;
    critical_gaps: Array<{
      skill: string;
      category: string;
      frequency: number;
      importance: number;
      jobs: string[];
      companies: string[];
      priority_score: number;
    }>;
    category_gaps: Record<string, Array<{
      skill: string;
      category: string;
      frequency: number;
      importance: number;
      jobs: string[];
      companies: string[];
      priority_score: number;
    }>>;
    gap_analysis: {
      total_repeated_gaps: number;
      most_common_gap: {
        skill: string;
        frequency: number;
      };
      critical_gaps_count: number;
      categories_with_gaps: number;
      average_gap_frequency: number;
    };
  learning_recommendations: Array<{
    type: string;
    skill?: string;
    category?: string;
    title: string;
    description: string;
    priority: string;
    time_estimate: string;
    resources: string[];
    learning_path: string[];
    prerequisites: string[];
  }>;
  project_suggestions: Array<{
    title: string;
    description: string;
    skills_covered: string[];
    difficulty: string;
    time_estimate: string;
    tech_stack: string[];
    learning_outcomes: string[];
    portfolio_value: string;
  }>;
  action_items: Array<{
    type: string;
    priority: string;
    title: string;
    description: string;
    timeline: string;
    resources: string[];
    success_metrics: string[];
  }>;
  skill_coverage_score: number;
  created_at: string;
  updated_at: string;
  last_accessed_at: string;
}

interface SkillGapAnalysisSummaryProps {
  analysisId: number;
  className?: string;
}

export const SkillGapAnalysisSummary: React.FC<SkillGapAnalysisSummaryProps> = ({
  analysisId,
  className = ""
}) => {
  const [analysis, setAnalysis] = useState<SkillAnalysisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'missing-skills' | 'repeated-gaps' | 'recommendations'>('overview');
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());

  // Fetch analysis data
  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/v1/skill-gap-analysis/${analysisId}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch skill gap analysis');
        }
        
        const data = await response.json();
        setAnalysis(data);
      } catch (error) {
        console.error('Error fetching skill gap analysis:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [analysisId]);

  const toggleExpansion = (itemId: string) => {
    setExpandedItems(prev => {
      const newSet = new Set(prev);
      if (newSet.has(itemId)) {
        newSet.delete(itemId);
      } else {
        newSet.add(itemId);
      }
      return newSet;
    });
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 0.8) return 'Excellent';
    if (score >= 0.6) return 'Good';
    if (score >= 0.4) return 'Fair';
    return 'Needs Improvement';
  };

  const getAssessmentColor = (assessment: string) => {
    switch (assessment) {
      case 'excellent': return 'text-green-600';
      case 'good': return 'text-blue-600';
      case 'fair': return 'text-yellow-600';
      case 'needs_improvement': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getAssessmentIcon = (assessment: string) => {
    switch (assessment) {
      case 'excellent': return <CheckCircle className="w-5 h-5" />;
      case 'good': return <CheckCircle className="w-5 h-5" />;
      case 'fair': return <AlertCircle className="w-5 h-5" />;
      case 'needs_improvement': return <AlertTriangle className="w-5 h-5" />;
      default: return <AlertCircle className="w-5 h-5" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-700';
      case 'medium': return 'bg-yellow-100 text-yellow-700';
      case 'low': return 'bg-green-100 text-green-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const toggleItemExpansion = (itemId: string) => {
    setExpandedItems(prev => {
      const newSet = new Set(prev);
      if (newSet.has(itemId)) {
        newSet.delete(itemId);
      } else {
        newSet.add(itemId);
      }
      return newSet;
    });
  };

  if (loading) {
    return (
      <div className={`flex items-center justify-center p-8 ${className}`}>
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mr-3"></div>
        <span>Loading skill gap analysis...</span>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className={`flex items-center justify-center p-8 ${className}`}>
        <div className="text-center">
          <Brain className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">Skill Gap Analysis Not Found</h2>
          <p className="text-gray-600">The skill gap analysis you're looking for doesn't exist.</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`max-w-6xl mx-auto px-4 py-8 ${className}`}>
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{analysis.analysis_name}</h1>
            <p className="text-gray-600 mt-1">
              Analysis of {analysis.job_count} job descriptions • {analysis.job_count} companies
            </p>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => window.print()}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              <Download className="w-4 h-4" />
              <span>Export</span>
            </button>
            <button
              onClick={() => window.location.reload()}
              className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {/* Overall Assessment */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="text-center">
            <div className="flex items-center justify-center mb-2">
              {getAssessmentIcon(analysis.analysis_summary.overall_assessment)}
              <span className={`ml-2 text-lg font-semibold ${getAssessmentColor(analysis.analysis_summary.overall_assessment)}`}>
                {analysis.analysis_summary.overall_assessment.charAt(0).toUpperCase() + analysis.analysis_summary.overall_assessment.slice(1)}
              </span>
            </div>
            <p className="text-sm text-gray-600">{analysis.analysis_summary.assessment_message}</p>
          </div>
          
          <div className="text-center">
            <div className={`text-2xl font-bold ${getScoreColor(analysis.skill_coverage_score)}`}>
              {(analysis.skill_coverage_score * 100).toFixed(1)}%
            </div>
            <p className="text-sm text-gray-600">Skill Coverage</p>
            <p className="text-xs text-gray-500">{getScoreLabel(analysis.skill_coverage_score)}</p>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {analysis.analysis_summary.total_missing_skills}
            </div>
            <p className="text-sm text-gray-600">Missing Skills</p>
          </div>
        </div>

        {/* Key Findings */}
        <div className="bg-blue-50 p-4 rounded-lg mb-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-3">Key Findings</h3>
          <ul className="list-disc list-inside space-y-2 text-sm text-blue-700">
            {analysis.analysis_summary.key_findings.map((finding, index) => (
              <li key={index}>{finding}</li>
            ))}
          </ul>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            <button
              onClick={() => setActiveTab('overview')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'overview'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <div className="flex items-center gap-2">
                <BarChart3 className="w-4 h-4" />
                <span>Overview</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('missing-skills')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'missing-skills'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                <span>Missing Skills</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('repeated-gaps')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'repeated-gaps'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4" />
                <span>Repeated Gaps</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('recommendations')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'recommendations'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <div className="flex items-center gap-2">
                <Lightbulb className="w-4 h-4" />
                <span>Recommendations</span>
              </div>
            </button>
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Statistics */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900">{analysis.analysis_summary.total_missing_skills}</div>
                  <p className="text-sm text-gray-600">Total Missing Skills</p>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">{analysis.analysis_summary.high_frequency_gaps}</div>
                  <p className="text-sm text-gray-600">High-Frequency Gaps</p>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-600">{analysis.analysis_summary.critical_gaps}</div>
                  <p className="text-sm text-gray-600">Critical Gaps</p>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{analysis.analysis_recommendations_count || 0}</div>
                  <p className="text-sm text-gray-600">Learning Recommendations</p>
                </div>
              </div>

              {/* Recommendations Summary */}
              <div className="bg-green-50 p-4 rounded-lg">
                <h3 className="text-lg font-semibold text-green-900 mb-3">Recommendations Summary</h3>
                <ul className="list-disc list-inside space-y-2 text-sm text-green-700">
                  {analysis.analysis_summary.recommendations_summary.map((rec, index) => (
                    <li key={index}>{rec}</li>
                  ))}
                </ul>
              </div>

              {/* Action Items Preview */}
              <div className="bg-purple-50 p-4 rounded-lg">
                <h3 className="text-lg font-semibold text-purple-900 mb-3">Action Items</h3>
                <div className="space-y-2">
                  {(analysis.action_items || []).slice(0, 3).map((item, index) => (
                    <div key={index} className="flex items-center justify-between p-2 bg-white rounded">
                      <div className="flex-1">
                        <span className={`px-2 py-1 text-xs font-medium rounded ${getPriorityColor(item.priority)}`}>
                          {item.priority}
                        </span>
                        <span className="ml-2 text-sm font-medium">{item.title}</span>
                      </div>
                      <span className="text-xs text-gray-500">{item.timeline}</span>
                    </div>
                  ))}
                </div>
                {(analysis.action_items || []).length > 3 && (
                  <div className="text-center">
                    <button className="text-blue-600 text-sm hover:text-blue-800">
                      View all {analysis.action_items.length} action items
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'missing-skills' && (
            <div className="space-y-6">
              {/* Missing Skills Summary */}
              <div className="bg-red-50 p-4 rounded-lg mb-6">
                <h3 className="text-lg font-semibold text-red-900 mb-3">Missing Skills Summary</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-red-600">{analysis.missing_skills.gap_summary.total_missing_skills}</div>
                    <p className="text-sm text-red-700">Total Missing</p>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600">{analysis.missing_skills.gap_summary.categories.technical || 0}</div>
                    <p className="text-sm text-orange-700">Technical</p>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{analysis.missing_skills.gap_categories.soft_skills || 0}</div>
                    <p className="text-sm text-blue-700">Soft Skills</p>
                  </div>
                </div>
              </div>

              {/* Missing Technical Skills */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Missing Technical Skills</h3>
                <div className="space-y-3">
                  {analysis.missing_skills.missing_technical.slice(0, 10).map((skill, index) => (
                    <div
                      key={index}
                      className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h4 className="text-md font-medium text-gray-900">{skill.skill}</h4>
                          <div className="flex items-center gap-2 mt-1">
                            <span className={`px-2 py-1 text-xs font-medium rounded ${getPriorityColor('medium')}`}>
                              Priority: {skill.priority_score.toFixed(2)}
                            </span>
                            <span className="px-2 py-1 text-xs font-medium rounded bg-gray-100 text-gray-700">
                              Frequency: {skill.frequency}
                            </span>
                          </div>
                        </div>
                        <button
                          onClick={() => toggleItemExpansion(`tech-${index}`)}
                          className="text-gray-400 hover:text-gray-600"
                        >
                          {expandedItems.has(`tech-${index}`) ? '▲' : '▼'}
                        </button>
                      </div>
                      
                      {expandedItems.has(`tech-${index}`) && (
                        <div className="mt-4 space-y-3">
                          <div className="bg-gray-50 p-3 rounded">
                            <h5 className="text-sm font-medium text-gray-700 mb-2">Appears in:</h5>
                            <div className="flex flex-wrap gap-2">
                              {skill.jobs.map((job, jobIndex) => (
                                <span key={jobIndex} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                                  {job}
                                </span>
                              ))}
                            </div>
                          </div>
                          <div className="bg-gray-50 p-3 rounded">
                            <h5 className="text-sm font-medium text-gray-700 mb-2">Companies:</h5>
                            <div className="flex flex-wrap gap-2">
                              {skill.companies.map((company, companyIndex) => (
                                <span key={companyIndex} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                                  {company}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
                
                {analysis.missing_skills.missing_technical.length > 10 && (
                  <div className="text-center mt-6">
                    <button className="text-blue-600 text-sm hover:text-blue-800">
                      View all {analysis.missing_skills.missing_technical.length} technical skills
                    </button>
                  </div>
                )}

                {/* Missing Soft Skills */}
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Missing Soft Skills</h3>
                <div className="space-y-3">
                  {analysis.missing_skills.missing_soft_skills.slice(0, 5).map((skill, index) => (
                    <div
                      key={index}
                      className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h4 className="text-md font-medium text-gray-900">{skill.skill}</h4>
                          <div className="flex items-center gap-2 mt-1">
                            <span className={`px-2 py-1 text-xs font-medium rounded ${getPriorityColor('medium')}`}>
                              Priority: {skill.priority_score.toFixed(2)}
                            </span>
                            <span className="px-2 py-1 text-xs font-medium rounded bg-gray-100 text-gray-700">
                              Frequency: {skill.frequency}
                            </span>
                          </div>
                        </div>
                        <button
                          onClick={() => toggleItemExpansion(`soft-${index}`)}
                          className="text-gray-400 hover:text-gray-600"
                        >
                          {expandedItems.has(`soft-${index}`) ? '▲' : '▼'}
                        </button>
                      </div>
                      
                      {expandedItems.has(`soft-${index}`) && (
                        <div className="mt-4 space-y-3">
                          <div className="bg-gray-50 p-3 rounded">
                            <h5 className="text-sm font-medium text-gray-700 mb-2">Appears in:</h5>
                            <div className="flex flex-wrap gap-2">
                              {skill.jobs.map((job, jobIndex) => (
                                <span key={jobIndex} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                                  {job}
                                </span>
                              ))}
                            </div>
                          </div>
                          <div className="bg-gray-50 p-3 rounded">
                            <h5 className="text-sm font-medium text-gray-700 mb-2">Companies:</h5>
                            <div className="flex flex-wrap gap-2">
                              {skill.companies.map((company, companyIndex) => (
                                <span key={companyIndex} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                                  {company}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
                
                {analysis.missing_skills.missing_soft_skills.length > 5 && (
                  <div className="text-center mt-6">
                    <button className="text-blue-600 text-sm hover:text-blue-800">
                      View all {analysis.missing_skills.missing_soft_skills.length} soft skills
                    </button>
                  </div>
                )}
              </div>
          )}

          {activeTab === 'repeated-gaps' && (
            <div className="space-y-6">
              {/* Repeated Gaps Summary */}
              <div className="bg-orange-50 p-4 rounded-lg mb-6">
                <h3 className="text-lg font-semibold text-orange-900 mb-3">Repeated Gaps Summary</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-orange-600">{analysis.repeated_gaps.gap_analysis.total_repeated_gaps}</div>
                    <p className="text-sm text-orange-700">Total Repeated Gaps</p>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-red-600">{analysis.repeated_gaps.gap_analysis.critical_gaps_count}</div>
                    <div className="text-sm text-red-700">Critical Gaps</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">{analysis.repeated_gaps.gap_analysis.categories_with_gaps}</div>
                    <div className="text-sm text-blue-700">Categories with Gaps</div>
                  </div>
                </div>
              </div>

              {/* Most Common Gap */}
              {analysis.repeated_gaps.gap_analysis.most_common_gap && (
                <div className="bg-yellow-50 p-4 rounded-lg mb-6">
                  <h3 className="text-lg font-semibold text-yellow-900 mb-3">Most Common Gap</h3>
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="text-md font-medium text-gray-900">
                        {analysis.repeated_gaps.gap_analysis.most_common_gap.skill.title()}
                      </h4>
                      <p className="text-sm text-gray-600">
                        Appears in {analysis.repeated_gaps.gap_analysis.most_common_gap.frequency} job postings
                      </p>
                    </div>
                    <div className="text-right">
                      <span className="px-3 py-1 bg-yellow-100 text-yellow-700 text-sm rounded">
                        Priority: {(analysis.repeated_gaps.gap_analysis.most_common_gap.priority_score * 100).toFixed(1)}
                      </span>
                    </div>
                  </div>
                </div>
              )}

              {/* High Frequency Gaps */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">High-Frequency Gaps</h3>
                <div className="space-y-3">
                  {analysis.repeated_gaps.high_frequency_gaps.slice(0, 10).map((gap, index) => (
                    <div
                      key={index}
                      className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h4 className="text-md font-medium text-gray-900">{gap.skill.title()}</h4>
                          <span className="text-sm text-gray-600">({gap.category})</span>
                          <div className="flex items-center gap-2 mt-1">
                            <span className={`px-2 py-1 text-xs font-medium rounded ${getPriorityColor('high')}`}>
                              High Priority
                            </span>
                            <span className="px-2 py-1 text-xs font-medium rounded bg-gray-100 text-gray-700">
                              {gap.frequency} occurrences
                            </span>
                          </div>
                        </div>
                        <button
                          onClick={() => toggleItemExpansion(`gap-${index}`)}
                          className="text-gray-400 hover:text-gray-600"
                        >
                          {expandedItems.has(`gap-${index}`) ? '▲' : '▼'}
                        </button>
                      </div>
                      
                      {expandedItems.has(`gap-${index}`) && (
                        <div className="mt-4 space-y-3">
                          <div className="bg-gray-50 p-3 rounded">
                            <h5 className="text-sm font-medium text-gray-700 mb-2">Appears in:</h5>
                            <div className="flex flex-wrap gap-2">
                              {gap.jobs.map((job, jobIndex) => (
                                <span key={jobIndex} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                                  {job}
                                </span>
                              ))}
                            </div>
                          </div>
                          <div className="bg-gray-50 p-3 rounded">
                            <h5 className="text-sm font-medium text-gray-700 mb-2">Companies:</h5>
                            <div className="flex flex-wrap gap-2">
                              {gap.companies.map((company, companyIndex) => (
                                <span key={companyIndex} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                                  {company}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
                
                {analysis.repeated_gaps.high_frequency_gaps.length > 10 && (
                  <div className="text-center mt-6">
                    <button className="text-blue-600 text-sm hover:text-blue-800">
                      View all {analysis.repeated_gaps.high_frequency_gaps.length} repeated gaps
                    </button>
                  </div>
                )}
              </div>

              {/* Critical Gaps */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-red-900 mb-4">Critical Gaps</h3>
                <div className="space-y-3">
                  {analysis.repeated_gaps.critical_gaps.slice(0, 5).map((gap, index) => (
                    <div
                      key={index}
                      className="border border-red-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h4 className="text-md font-medium text-gray-900">{gap.skill.title()}</h4>
                          <span className="text-sm text-gray-600">({gap.category})</span>
                          <div className="flex items-center gap-2 mt-1">
                            <span className={`px-2 py-1 text-xs font-medium rounded bg-red-100 text-red-700`}>
                              Critical
                            </span>
                            <span className="px-2 py-1 text-xs font-medium rounded bg-gray-100 text-gray-700">
                              {gap.frequency} occurrences
                            </span>
                          </div>
                        </div>
                        <button
                          onClick={() => toggleItemExpansion(`critical-${index}`)}
                          className="text-gray-400 hover:text-gray-600"
                        >
                          {expandedItems.has(`critical-${index}`) ? '▲' : '▼'}
                        </button>
                      </div>
                      
                      {expandedItems.has(`critical-${index}`) && (
                        <div className="mt-4 space-y-3">
                          <div className="bg-red-50 p-3 rounded">
                            <h5 className="text-sm font-medium text-red-700 mb-2">Appears in:</h5>
                            <div className="flex flex-wrap gap-2">
                              {gap.jobs.map((job, jobIndex) => (
                                <span key={jobIndex} className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded">
                                  {job}
                                </span>
                              ))}
                            </div>
                          </div>
                          <div className="bg-red-50 p-3 rounded">
                            <h5 className="text-sm font-medium text-red-700 mb-2">Companies:</h5>
                            <div className="flex flex-wrap gap-2">
                              {gap.companies.map((company, companyIndex) => (
                                <span key={companyIndex} className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded">
                                  {company}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
                
                {analysis.repeated_gaps.critical_gaps.length > 5 && (
                  <div className="text-center mt-6">
                    <button className="text-blue-600 text-sm hover:text-blue-800">
                      View all {analysis.repeated_gaps.critical_gaps.length} critical gaps
                    </button>
                  </div>
                )}
              </div>

              {/* Category Gaps */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Gaps by Category</h3>
                <div className="space-y-4">
                  {Object.entries(analysis.repeated_gaps.category_gaps).map(([category, skills], categoryIndex) => (
                    <div key={categoryIndex} className="border border-gray-200 rounded-lg p-4">
                      <h4 className="text-md font-medium text-gray-900 capitalize">{category}</h4>
                      <div className="text-sm text-gray-600">{len(skills)} skills missing</div>
                      <div className="space-y-2">
                        {skills.slice(0, 3).map((skill, skillIndex) => (
                          <div key={skillIndex} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                            <span className="text-sm font-medium text-gray-900">{skill.skill.title()}</span>
                            <span className="text-xs text-gray-500">
                              {skill.frequency} occurrences
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'recommendations' && (
            <div className="space-y-6">
              {/* Learning Recommendations */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Learning Recommendations</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {analysis.learning_recommendations.slice(0, 6).map((rec, index) => (
                    <div
                      key={index}
                      className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <h4 className="text-md font-medium text-gray-900">{rec.title}</h4>
                          <span className={`px-2 py-1 text-xs font-medium rounded ${getPriorityColor(rec.priority)}`}>
                            {rec.priority}
                          </span>
                          <span className="text-xs text-gray-500 ml-2">({rec.time_estimate})</span>
                        </div>
                        <span className={`px-2 py-1 text-xs font-medium rounded ${
                          rec.type === 'skill_specific' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700'
                        }`}>
                          {rec.type}
                        </span>
                      </div>
                      
                      <p className="text-sm text-gray-700 mb-3">{rec.description}</p>
                      
                      <div className="space-y-2">
                        <div className="bg-blue-50 p-3 rounded">
                          <h5 className="text-sm font-medium text-blue-700 mb-2">Learning Path:</h5>
                          <ol className="list-decimal list-inside space-y-1 text-sm text-blue-700">
                            {rec.learning_path.map((step, stepIndex) => (
                              <li key={stepIndex}>{step}</li>
                            ))}
                          </ol>
                        </div>
                        
                        {rec.prerequisites && rec.prerequisites.length > 0 && (
                          <div className="bg-yellow-50 p-3 rounded">
                            <h5 className="text-sm font-medium text-yellow-700 mb-2">Prerequisites:</h5>
                            <ul className="list-disc list-inside space-y-1 text-sm text-yellow-700">
                              {rec.prerequisites.map((prereq, prereqIndex) => (
                                <li key={prereqIndex}>{prereq}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                        
                        <div className="bg-green-50 p-3 rounded">
                          <h5 className="text-sm font-medium text-green-700 mb-2">Resources:</h5>
                          <ul className="list-disc list-inside space-y-1 text-sm text-green-700">
                            {rec.resources.map((resource, resourceIndex) => (
                              <li key={resourceIndex}>{resource}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                
                {analysis.learning_recommendations.length > 6 && (
                  <div className="text-center mt-6">
                    <button className="text-blue-600 text-sm hover:text-blue-800">
                      View all {analysis.learning_recommendations.length} recommendations
                    </button>
                  </div>
                )}
              </div>

              {/* Project Suggestions */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Project Suggestions</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {analysis.project_suggestions.slice(0, 6).map((project, index) => (
                    <div
                      key={index}
                      className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <h4 className="text-md font-medium text-gray-900">{project.title}</h4>
                          <span className={`px-2 py-1 text-xs font-medium rounded ${
                            project.difficulty === 'easy' ? 'bg-green-100 text-green-700' :
                            project.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-red-100 text-red-700'
                          }`}>
                            {project.difficulty}
                          </span>
                          <span className="text-xs text-gray-500 ml-2">({project.time_estimate})</span>
                        </div>
                        <span className={`px-2 py-1 text-xs font-medium rounded ${
                          project.portfolio_value === 'very_high' ? 'bg-purple-100 text-purple-700' :
                          project.portfolio_value === 'high' ? 'bg-blue-100 text-blue-700' :
                          'bg-gray-100 text-gray-700'
                        }`}>
                          {project.portfolio_value}
                        </span>
                      </div>
                      
                      <p className="text-sm text-gray-700 mb-3">{project.description}</p>
                      
                      <div className="space-y-2">
                        <div className="bg-gray-50 p-3 rounded">
                          <h5 className="text-sm font-medium text-gray-700 mb-2">Skills Covered:</h5>
                          <div className="flex flex-wrap gap-2">
                            {project.skills_covered.map((skill, skillIndex) => (
                              <span key={skillIndex} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                        
                        <div className="bg-gray-50 p-3 rounded">
                          <h5 className="text-sm font-medium text-gray-700 mb-2">Tech Stack:</h5>
                          <div className="flex flex-wrap gap-2">
                            {project.tech_stack.map((tech, techIndex) => (
                              <span key={techIndex} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                                {tech}
                              </span>
                            ))}
                          </div>
                        </div>
                        
                        <div className="bg-gray-50 p-3 rounded">
                          <h5 className="text-sm font-medium text-gray-700 mb-2">Learning Outcomes:</h5>
                          <ul className="list-disc list-inside space-y-1 text-sm text-gray-700">
                            {project.learning_outcomes.map((outcome, outcomeIndex) => (
                              <li key={outcomeIndex}>{outcome}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                </div>
                
                {analysis.project_suggestions.length > 6 && (
                  <div className="text-center mt-6">
                    <button className="text-blue-600 text-sm hover:text-blue-800">
                      View all {analysis.project_suggestions.length} project suggestions
                    </button>
                  </div>
                )}
              </div>

              {/* Action Items */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Action Items</h3>
                <div className="space-y-3">
                  {(analysis.action_items || []).slice(0, 5).map((item, index) => (
                    <div
                      key={index}
                      className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h4 className="text-md font-medium text-gray-900">{item.title}</h4>
                          <span className={`px-2 py-1 text-xs font-medium rounded ${getPriorityColor(item.priority)}`}>
                            {item.priority}
                          </span>
                          <span className="text-xs text-gray-500 ml-2">{item.timeline}</span>
                        </div>
                        <span className="text-xs text-gray-500">
                          Type: {item.type}
                        </span>
                      </div>
                      
                      <p className="text-sm text-gray-700 mb-3">{item.description}</p>
                      
                      <div className="space-y-2">
                        <div className="bg-gray-50 p-3 rounded">
                          <h5 className="text-sm font-medium text-gray-700 mb-2">Resources:</h5>
                          <ul className="list-disc list-inside space-y-1 text-sm text-gray-700">
                            {item.resources.map((resource, resourceIndex) => (
                              <li key={resourceIndex}>{resource}</li>
                            ))}
                          </ul>
                        </div>
                        
                        <div className="bg-gray-50 p-3 rounded">
                          <h5 className="text-sm font-medium text-gray-700 mb-2">Success Metrics:</h5>
                          <ul className="list-disc list-inside space-y-1 text-sm text-gray-700">
                            {item.success_metrics.map((metric, metricIndex) => (
                              <li key={metricIndex}>{metric}</li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                
                {(analysis.action_items || []).length > 5 && (
                  <div className="text-center mt-6">
                    <button className="text-blue-600 text-sm hover:text-blue-800">
                      View all {analysis.action_items.length} action items
                    </button>
                  </div>
                )}
              </div>
            </div>
        </div>

        {/* Footer */}
        <div className="bg-gray-50 rounded-lg p-4 text-center text-sm text-gray-600">
          <p>
            Created on {new Date(analysis.created_at).toLocaleDateString()} • 
            Last accessed {new Date(analysis.last_accessed_at).toLocaleDateString()}
          </p>
        </div>
      </div>
    );
};

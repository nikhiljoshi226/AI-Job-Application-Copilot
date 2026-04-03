'use client';

import React, { useState, useEffect } from 'react';
import { FileText, Users, Clock, Target, CheckCircle, AlertCircle, Download, RefreshCw, Play, BookOpen, Brain } from 'lucide-react';

interface InterviewPrepData {
  id: number;
  application_id?: number;
  job_description_id: number;
  interview_context: {
    interview_type: string;
    question_count: number;
    star_story_count: number;
    difficulty_level: string;
    estimated_duration: string;
  };
  questions: Array<{
    id: string;
    type: string;
    category: string;
    question: string;
    focus_area: string;
    difficulty: string;
    answer_draft: string;
    answer_length: number;
    key_points: string[];
  }>;
  star_stories: Array<{
    id: string;
    title: string;
    situation: string;
    task: string;
    action: string;
    result: string;
    skills_used: string[];
    context: {
      company: string;
      title: string;
      dates: string;
    };
    focus_areas: string[];
  }>;
  preparation_guide: {
    focus_areas: Array<{
      area: string;
      priority: string;
      description: string;
      preparation_time: string;
    }>;
    tips: string[];
    recommendations: string[];
    research_points: string[];
    day_of_preparation: {
      morning: string[];
      before_interview: string[];
      during_interview: string[];
    };
    common_mistakes: string[];
  };
  content_summary: {
    total_questions: number;
    behavioral_questions: number;
    technical_questions: number;
    situational_questions: number;
    star_stories: number;
    estimated_prep_time: string;
    difficulty_level: string;
    interview_type: string;
  };
  scores: {
    truthfulness_score: number;
    content_quality_score: number;
    personalization_score: number;
  };
  created_at: string;
  updated_at: string;
  last_accessed_at: string;
}

interface InterviewPrepPageProps {
  params: {
    id: string;
  };
}

export default function InterviewPrepPage({ params }: InterviewPrepPageProps) {
  const [interviewPrep, setInterviewPrep] = useState<InterviewPrepData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('questions');
  const [expandedQuestions, setExpandedQuestions] = useState<Set<string>>(new Set());
  const [expandedStories, setExpandedStories] = useState<Set<string>>(new Set());

  // Fetch interview prep data
  useEffect(() => {
    const fetchInterviewPrep = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/v1/interview-prep/${params.id}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch interview prep');
        }
        
        const data = await response.json();
        setInterviewPrep(data);
      } catch (error) {
        console.error('Error fetching interview prep:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchInterviewPrep();
  }, [params.id]);

  const toggleQuestionExpansion = (questionId: string) => {
    setExpandedQuestions(prev => {
      const newSet = new Set(prev);
      if (newSet.has(questionId)) {
        newSet.delete(questionId);
      } else {
        newSet.add(questionId);
      }
      return newSet;
    });
  };

  const toggleStoryExpansion = (storyId: string) => {
    setExpandedStories(prev => {
      const newSet = new Set(prev);
      if (newSet.has(storyId)) {
        newSet.delete(storyId);
      } else {
        newSet.add(storyId);
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
    return 'Needs Improvement';
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-700';
      case 'medium': return 'bg-yellow-100 text-yellow-700';
      case 'hard': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const getQuestionTypeColor = (type: string) => {
    switch (type) {
      case 'behavioral': return 'bg-blue-100 text-blue-700';
      case 'technical': return 'bg-purple-100 text-purple-700';
      case 'situational': return 'bg-orange-100 text-orange-700';
      case 'company': return 'bg-teal-100 text-teal-700';
      case 'role': return 'bg-indigo-100 text-indigo-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mr-3"></div>
        <span>Loading interview preparation...</span>
      </div>
    );
  }

  if (!interviewPrep) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <FileText className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">Interview Preparation Not Found</h2>
          <p className="text-gray-600">The interview preparation you're looking for doesn't exist.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Interview Preparation</h1>
            <p className="text-gray-600 mt-1">
              {interviewPrep.interview_context.company || 'Company'} - {interviewPrep.interview_context.job_title || 'Position'}
            </p>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => window.print()}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              <Download className="w-4 h-4" />
              <span>Print</span>
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

        {/* Scores */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="text-center">
            <div className={`text-2xl font-bold ${getScoreColor(interviewPrep.scores.truthfulness_score)}`}>
              {(interviewPrep.scores.truthfulness_score * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-gray-600">Truthfulness</div>
            <div className="text-xs text-gray-500">{getScoreLabel(interviewPrep.scores.truthfulness_score)}</div>
          </div>
          <div className="text-center">
            <div className={`text-2xl font-bold ${getScoreColor(interviewPrep.scores.content_quality_score)}`}>
              {(interviewPrep.scores.content_quality_score * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-gray-600">Content Quality</div>
            <div className="text-xs text-gray-500">{getScoreLabel(interviewPrep.scores.content_quality_score)}</div>
          </div>
          <div className="text-center">
            <div className={`text-2xl font-bold ${getScoreColor(interviewPrep.scores.personalization_score)}`}>
              {(interviewPrep.scores.personalization_score * 100).toFixed(0)}%
            </div>
            <div className="text-sm text-gray-600">Personalization</div>
            <div className="text-xs text-gray-500">{getScoreLabel(interviewPrep.scores.personalization_score)}</div>
          </div>
        </div>

        {/* Interview Context */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span className="text-gray-500">Interview Type:</span>
            <span className="font-medium capitalize">{interviewPrep.interview_context.interview_type}</span>
          </div>
          <div>
            <span className="text-gray-500">Difficulty:</span>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(interviewPrep.interview_context.difficulty_level)}`}>
              {interviewPrep.interview_context.difficulty_level}
            </span>
          </div>
          <div>
            <span className="text-gray-500">Questions:</span>
            <span className="font-medium">{interviewPrep.interview_context.question_count}</span>
          </div>
          <div>
            <span className="text-gray-500">Duration:</span>
            <span className="font-medium">{interviewPrep.interview_context.estimated_duration}</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            <button
              onClick={() => setActiveTab('questions')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'questions'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <div className="flex items-center gap-2">
                <Users className="w-4 h-4" />
                <span>Questions ({interviewPrep.content_summary.total_questions})</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('stories')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'stories'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <div className="flex items-center gap-2">
                <BookOpen className="w-4 h-4" />
                <span>STAR Stories ({interviewPrep.content_summary.star_stories})</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('guide')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'guide'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <div className="flex items-center gap-2">
                <Target className="w-4 h-4" />
                <span>Preparation Guide</span>
              </div>
            </button>
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {activeTab === 'questions' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Interview Questions</h3>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <span>Total: {interviewPrep.content_summary.total_questions}</span>
                  <span>•</span>
                  <span>Behavioral: {interviewPrep.content_summary.behavioral_questions}</span>
                  <span>•</span>
                  <span>Technical: {interviewPrep.content_summary.technical_questions}</span>
                  <span>•</span>
                  <span>Situational: {interviewPrep.content_summary.situational_questions}</span>
                </div>
              </div>

              <div className="space-y-4">
                {interviewPrep.questions.map((question) => (
                  <div
                    key={question.id}
                    className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <span className={`px-2 py-1 text-xs font-medium rounded-full ${getQuestionTypeColor(question.type)}`}>
                            {question.type}
                          </span>
                          <span className={`px-2 py-1 text-xs font-medium rounded-full ${getDifficultyColor(question.difficulty)}`}>
                            {question.difficulty}
                          </span>
                        </div>
                        <h4 className="text-lg font-medium text-gray-900">{question.question}</h4>
                        <p className="text-sm text-gray-600">Focus: {question.focus_area}</p>
                      </div>
                      <button
                        onClick={() => toggleQuestionExpansion(question.id)}
                        className="text-gray-400 hover:text-gray-600"
                      >
                        {expandedQuestions.has(question.id) ? '▲' : '▼'}
                      </button>
                    </div>

                    {expandedQuestions.has(question.id) && (
                      <div className="mt-4 space-y-3">
                        <div className="bg-gray-50 p-3 rounded">
                          <h5 className="text-sm font-medium text-gray-700 mb-2">Answer Draft:</h5>
                          <p className="text-sm text-gray-700 whitespace-pre-wrap">{question.answer_draft}</p>
                        </div>
                        {question.key_points.length > 0 && (
                          <div className="bg-blue-50 p-3 rounded">
                            <h5 className="text-sm font-medium text-blue-700 mb-2">Key Points:</h5>
                            <ul className="list-disc list-inside space-y-1 text-sm text-blue-700">
                              {question.key_points.map((point, index) => (
                                <li key={index}>{point}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'stories' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">STAR Stories</h3>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <span>Total: {interviewPrep.content_summary.star_stories}</span>
                  <span>•</span>
                  <span>Prepared from your resume experience</span>
                </div>
              </div>

              <div className="space-y-4">
                {interviewPrep.star_stories.map((story) => (
                  <div
                    key={story.id}
                    className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex-1">
                        <h4 className="text-lg font-medium text-gray-900">{story.title}</h4>
                        <p className="text-sm text-gray-600">{story.context.company} • {story.context.title}</p>
                      </div>
                      <button
                        onClick={() => toggleStoryExpansion(story.id)}
                        className="text-gray-400 hover:text-gray-600"
                      >
                        {expandedStories.has(story.id) ? '▲' : '▼'}
                      </button>
                    </div>

                    {expandedStories.has(story.id) && (
                      <div className="mt-4 space-y-4">
                        <div className="bg-gray-50 p-3 rounded">
                          <h5 className="text-sm font-medium text-gray-700 mb-2">Situation:</h5>
                          <p className="text-sm text-gray-700">{story.situation}</p>
                        </div>
                        <div className="bg-gray-50 p-3 rounded">
                          <h5 className="text-sm font-medium text-gray-700 mb-2">Task:</h5>
                          <p className="text-sm text-gray-700">{story.task}</p>
                        </div>
                        <div className="bg-gray-50 p-3 rounded">
                          <h5 className="text-sm font-medium text-gray-700 mb-2">Action:</h5>
                          <p className="text-sm text-gray-700">{story.action}</p>
                        </div>
                        <div className="bg-gray-50 p-3 rounded">
                          <h5 className="text-sm font-medium text-gray-700 mb-2">Result:</h5>
                          <p className="text-sm text-gray-700">{story.result}</p>
                        </div>
                        {story.skills_used.length > 0 && (
                          <div className="bg-blue-50 p-3 rounded">
                            <h5 className="text-sm font-medium text-blue-700 mb-2">Skills Used:</h5>
                            <div className="flex flex-wrap gap-2">
                              {story.skills_used.map((skill, index) => (
                                <span
                                  key={index}
                                  className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded"
                                >
                                  {skill}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                        {story.focus_areas.length > 0 && (
                          <div className="bg-green-50 p-3 rounded">
                            <h5 className="text-sm font-medium text-green-700 mb-2">Focus Areas:</h5>
                            <div className="flex flex-wrap gap-2">
                              {story.focus_areas.map((area, index) => (
                                <span
                                  key={index}
                                  className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded"
                                >
                                  {area}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'guide' && (
            <div className="space-y-6">
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Focus Areas</h3>
                <div className="space-y-3">
                  {interviewPrep.preparation_guide.focus_areas.map((area, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="text-md font-medium text-gray-900">{area.area}</h4>
                        <span className={`px-2 py-1 text-xs font-medium rounded ${
                          area.priority === 'high' ? 'bg-red-100 text-red-700' :
                          area.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'
                        }`}>
                          {area.priority}
                        </span>
                      </div>
                      <p className="text-sm text-gray-700">{area.description}</p>
                      <div className="text-xs text-gray-500 mt-2">
                        Preparation time: {area.preparation_time}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Preparation Tips</h3>
                <div className="bg-blue-50 p-4 rounded-lg">
                  <ul className="list-disc list-inside space-y-2 text-sm text-blue-700">
                    {interviewPrep.preparation_guide.tips.map((tip, index) => (
                      <li key={index}>{tip}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommendations</h3>
                <div className="bg-green-50 p-4 rounded-lg">
                  <ul className="list-disc list-inside space-y-2 text-sm text-green-700">
                    {interviewPrep.preparation_guide.recommendations.map((rec, index) => (
                      <li key={index}>{rec}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Research Points</h3>
                <div className="bg-orange-50 p-4 rounded-lg">
                  <ul className="list-disc list-inside space-y-2 text-sm text-orange-700">
                    {interviewPrep.preparation_guide.research_points.map((point, index) => (
                      <li key={index}>{point}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <h3 className="text-md font-semibold text-gray-900 mb-3">Day Before Interview</h3>
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <h4 className="text-sm font-medium text-purple-700 mb-2">Morning</h4>
                    <ul className="list-disc list-inside space-y-1 text-sm text-purple-700">
                      {interviewPrep.preparation_guide.day_of_preparation.morning.map((item, index) => (
                        <li key={index}>{item}</li>
                      ))}
                    </ul>
                    <h4 className="text-sm font-medium text-purple-700 mb-2 mt-4">Before Interview</h4>
                    <ul className="list-disc list-inside space-y-1 text-sm text-purple-700">
                      {interviewPrep.preparation_guide.day_of_preparation.before_interview.map((item, index) => (
                        <li key={index}>{item}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div>
                  <h3 className="text-md font-semibold text-gray-900 mb-3">During Interview</h3>
                  <div className="bg-teal-50 p-4 rounded-lg">
                    <ul className="list-disc list-inside space-y-1 text-sm text-teal-700">
                      {interviewPrep.preparation_guide.day_of_preparation.during_interview.map((item, index) => (
                        <li key={index}>{item}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div>
                  <h3 className="text-md font-semibold text-gray-900 mb-3">Common Mistakes</h3>
                  <div className="bg-red-50 p-4 rounded-lg">
                    <ul className="list-disc list-inside space-y-1 text-sm text-red-700">
                      {interviewPrep.preparation_guide.common_mistakes.map((mistake, index) => (
                        <li key={index}>{mistake}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="bg-gray-50 rounded-lg p-4 text-center text-sm text-gray-600">
        <p>
          Created on {new Date(interviewPrep.created_at).toLocaleDateString()} • 
          Last accessed {new Date(interviewPrep.last_accessed_at).toLocaleDateString()}
        </p>
      </div>
    </div>
  );
}

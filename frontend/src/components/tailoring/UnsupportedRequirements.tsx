import React from 'react';
import { AlertTriangle, Info, Target, Lightbulb } from 'lucide-react';
import { UnsupportedRequirementCardProps } from '@/types/tailoring';

export const UnsupportedRequirements: React.FC<{
  requirements: UnsupportedRequirementCardProps['requirement'][];
}> = ({ requirements }) => {
  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high': return 'text-red-600 bg-red-50 border-red-200';
      case 'medium': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'low': return 'text-blue-600 bg-blue-50 border-blue-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getImpactIcon = (impact: string) => {
    switch (impact) {
      case 'high': return <AlertTriangle className="w-5 h-5" />;
      case 'medium': return <Info className="w-5 h-5" />;
      case 'low': return <Target className="w-5 h-5" />;
      default: return <Info className="w-5 h-5" />;
    }
  };

  const getSectionIcon = (section: string) => {
    switch (section) {
      case 'required_skills': return '🛠️';
      case 'preferred_skills': return '⭐';
      case 'responsibilities': return '📋';
      case 'qualifications': return '🎓';
      case 'role_type': return '👔';
      case 'experience_level': return '📊';
      default: return '📄';
    }
  };

  const groupBySection = (requirements: any[]) => {
    return requirements.reduce((groups, req) => {
      const section = req.jd_section;
      if (!groups[section]) {
        groups[section] = [];
      }
      groups[section].push(req);
      return groups;
    }, {} as Record<string, any[]>);
  };

  const groupedRequirements = groupBySection(requirements);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-3 bg-amber-100 rounded-full">
            <AlertTriangle className="w-6 h-6 text-amber-600" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">Unsupported Requirements</h2>
            <p className="text-gray-600 mt-1">
              These job requirements cannot be supported by your current resume. 
              Consider addressing these gaps or highlighting related experience.
            </p>
          </div>
        </div>

        {/* Summary Stats */}
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-3 bg-red-50 rounded-lg">
            <div className="text-2xl font-bold text-red-600">
              {requirements.filter(r => r.impact === 'high').length}
            </div>
            <div className="text-sm text-gray-600">High Impact</div>
          </div>
          <div className="text-center p-3 bg-yellow-50 rounded-lg">
            <div className="text-2xl font-bold text-yellow-600">
              {requirements.filter(r => r.impact === 'medium').length}
            </div>
            <div className="text-sm text-gray-600">Medium Impact</div>
          </div>
          <div className="text-center p-3 bg-blue-50 rounded-lg">
            <div className="text-2xl font-bold text-blue-600">
              {requirements.filter(r => r.impact === 'low').length}
            </div>
            <div className="text-sm text-gray-600">Low Impact</div>
          </div>
        </div>
      </div>

      {/* Requirements by Section */}
      {Object.entries(groupedRequirements).map(([section, sectionReqs]) => (
        <div key={section} className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center gap-3">
              <span className="text-xl">{getSectionIcon(section)}</span>
              <h3 className="text-lg font-semibold text-gray-900">
                {section.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </h3>
              <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                {sectionReqs.length} requirement{sectionReqs.length !== 1 ? 's' : ''}
              </span>
            </div>
          </div>

          <div className="p-4 space-y-4">
            {sectionReqs.map((req, index) => (
              <div key={index} className={`border rounded-lg p-4 ${getImpactColor(req.impact)}`}>
                <div className="flex items-start gap-3">
                  <div className="mt-1">
                    {getImpactIcon(req.impact)}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium text-gray-900">{req.requirement}</h4>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full border ${
                        req.impact === 'high' ? 'bg-red-100 text-red-700 border-red-200' :
                        req.impact === 'medium' ? 'bg-yellow-100 text-yellow-700 border-yellow-200' :
                        'bg-blue-100 text-blue-700 border-blue-200'
                      }`}>
                        {req.impact} impact
                      </span>
                    </div>

                    <div className="space-y-3">
                      {/* Suggestion */}
                      <div className="flex items-start gap-2">
                        <Lightbulb className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" />
                        <div>
                          <p className="text-sm font-medium text-gray-700">Recommendation</p>
                          <p className="text-sm text-gray-600">{req.suggestion}</p>
                        </div>
                      </div>

                      {/* Additional Guidance based on impact */}
                      {req.impact === 'high' && (
                        <div className="bg-red-50 border border-red-200 rounded p-3">
                          <p className="text-sm text-red-800">
                            <strong>High Priority:</strong> This requirement significantly impacts your candidacy. 
                            Consider gaining this experience or finding roles where it's not essential.
                          </p>
                        </div>
                      )}

                      {req.impact === 'medium' && (
                        <div className="bg-yellow-50 border border-yellow-200 rounded p-3">
                          <p className="text-sm text-yellow-800">
                            <strong>Medium Priority:</strong> While important, this may not be a dealbreaker. 
                            Highlight related skills and transferable experience.
                          </p>
                        </div>
                      )}

                      {req.impact === 'low' && (
                        <div className="bg-blue-50 border border-blue-200 rounded p-3">
                          <p className="text-sm text-blue-800">
                            <strong>Low Priority:</strong> Nice to have but not critical. 
                            Focus on your core strengths and relevant experience.
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}

      {/* No Requirements */}
      {requirements.length === 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
          <div className="flex justify-center mb-4">
            <div className="p-3 bg-green-100 rounded-full">
              <Target className="w-8 h-8 text-green-600" />
            </div>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">All Requirements Supported!</h3>
          <p className="text-gray-600">
            Your resume supports all the key requirements for this position. 
            You're well-aligned with what they're looking for.
          </p>
        </div>
      )}

      {/* Actionable Tips */}
      {requirements.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-4">How to Address These Gaps</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <h4 className="font-medium text-blue-800">Short-term Strategies</h4>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• Highlight transferable skills in related areas</li>
                <li>• Emphasize rapid learning ability</li>
                <li>• Showcase relevant projects or coursework</li>
                <li>• Consider certifications for missing skills</li>
              </ul>
            </div>
            <div className="space-y-2">
              <h4 className="font-medium text-blue-800">Long-term Development</h4>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• Plan skill development for high-impact gaps</li>
                <li>• Seek projects that build missing experience</li>
                <li>• Network with professionals in target areas</li>
                <li>• Consider roles that bridge to your target position</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

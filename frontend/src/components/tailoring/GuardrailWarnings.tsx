import React from 'react';
import { Shield, AlertTriangle, CheckCircle, Info, XCircle } from 'lucide-react';
import { GuardrailViolation } from '@/types/tailoring';

export const GuardrailWarnings: React.FC<{
  violations: GuardrailViolation[];
}> = ({ violations }) => {
  const getViolationIcon = (type: string) => {
    switch (type) {
      case 'fabrication_detected':
        return <XCircle className="w-5 h-5 text-red-600" />;
      case 'excessive_claims':
        return <AlertTriangle className="w-5 h-5 text-yellow-600" />;
      case 'unsupported_experience':
        return <AlertTriangle className="w-5 h-5 text-orange-600" />;
      default:
        return <Info className="w-5 h-5 text-blue-600" />;
    }
  };

  const getViolationColor = (type: string) => {
    switch (type) {
      case 'fabrication_detected':
        return 'border-red-200 bg-red-50';
      case 'excessive_claims':
        return 'border-yellow-200 bg-yellow-50';
      case 'unsupported_experience':
        return 'border-orange-200 bg-orange-50';
      default:
        return 'border-blue-200 bg-blue-50';
    }
  };

  const getViolationTitle = (type: string) => {
    switch (type) {
      case 'fabrication_detected':
        return 'Fabrication Detected';
      case 'excessive_claims':
        return 'Excessive Claims';
      case 'unsupported_experience':
        return 'Unsupported Experience';
      default:
        return 'Guardrail Warning';
    }
  };

  const getViolationDescription = (type: string) => {
    switch (type) {
      case 'fabrication_detected':
        return 'This suggestion contains indicators of fabricated information that cannot be verified from your resume.';
      case 'excessive_claims':
        return 'This suggestion makes multiple quantifiable claims that may be exaggerated or unsupported.';
      case 'unsupported_experience':
        return 'This suggestion claims experience or skills not supported by your resume history.';
      default:
        return 'This suggestion may not be fully supported by your resume content.';
    }
  };

  const groupByType = (violations: GuardrailViolation[]) => {
    return violations.reduce((groups, violation) => {
      const type = violation.type;
      if (!groups[type]) {
        groups[type] = [];
      }
      groups[type].push(violation);
      return groups;
    }, {} as Record<string, GuardrailViolation[]>);
  };

  const groupedViolations = groupByType(violations);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-3 bg-amber-100 rounded-full">
            <Shield className="w-6 h-6 text-amber-600" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-gray-900">Guardrail Warnings</h2>
            <p className="text-gray-600 mt-1">
              These suggestions triggered our truthfulness safeguards. 
              Review carefully before approving.
            </p>
          </div>
        </div>

        {/* Summary Stats */}
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center p-3 bg-red-50 rounded-lg">
            <div className="text-2xl font-bold text-red-600">
              {violations.filter(v => v.type === 'fabrication_detected').length}
            </div>
            <div className="text-sm text-gray-600">Fabrication Risks</div>
          </div>
          <div className="text-center p-3 bg-yellow-50 rounded-lg">
            <div className="text-2xl font-bold text-yellow-600">
              {violations.filter(v => v.type !== 'fabrication_detected').length}
            </div>
            <div className="text-sm text-gray-600">Other Warnings</div>
          </div>
        </div>
      </div>

      {/* Violations by Type */}
      {Object.entries(groupedViolations).map(([type, typeViolations]) => (
        <div key={type} className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className={`p-4 border-b border-gray-200 ${getViolationColor(type)}`}>
            <div className="flex items-center gap-3">
              {getViolationIcon(type)}
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {getViolationTitle(type)}
                </h3>
                <p className="text-sm text-gray-600 mt-1">
                  {getViolationDescription(type)}
                </p>
              </div>
              <span className="ml-auto px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                {typeViolations.length} violation{typeViolations.length !== 1 ? 's' : ''}
              </span>
            </div>
          </div>

          <div className="p-4 space-y-4">
            {typeViolations.map((violation, index) => (
              <div key={index} className={`border rounded-lg p-4 ${getViolationColor(violation.type)}`}>
                <div className="flex items-start gap-3">
                  <div className="mt-1">
                    {getViolationIcon(violation.type)}
                  </div>
                  <div className="flex-1">
                    {/* Violation Reason */}
                    <div className="mb-3">
                      <h4 className="font-medium text-gray-900 mb-1">Issue Detected</h4>
                      <p className="text-sm text-gray-700">{violation.reason}</p>
                    </div>

                    {/* Problematic Suggestion */}
                    <div className="mb-3">
                      <h4 className="font-medium text-gray-900 mb-2">Problematic Content</h4>
                      <div className="bg-white border border-gray-300 rounded p-3">
                        <div className="space-y-2">
                          {violation.suggestion.current_text && (
                            <div>
                              <span className="text-xs font-medium text-gray-500">Original:</span>
                              <p className="text-sm text-gray-800 italic">
                                "{violation.suggestion.current_text}"
                              </p>
                            </div>
                          )}
                          {violation.suggestion.suggested_text && (
                            <div>
                              <span className="text-xs font-medium text-gray-500">Suggested:</span>
                              <p className="text-sm text-red-800 font-medium">
                                "{violation.suggestion.suggested_text}"
                              </p>
                            </div>
                          )}
                          {violation.suggestion.suggested_addition && (
                            <div>
                              <span className="text-xs font-medium text-gray-500">Addition:</span>
                              <p className="text-sm text-red-800 font-medium">
                                "{violation.suggestion.suggested_addition}"
                              </p>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Truthfulness Score */}
                    <div className="mb-3">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-700">Truthfulness Score</span>
                        <span className={`px-2 py-1 text-xs font-medium rounded ${
                          violation.suggestion.truthfulness_score < 0.5 ? 'bg-red-100 text-red-700' :
                          violation.suggestion.truthfulness_score < 0.7 ? 'bg-yellow-100 text-yellow-700' :
                          'bg-green-100 text-green-700'
                        }`}>
                          {(violation.suggestion.truthfulness_score * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>

                    {/* Evidence Source */}
                    <div className="mb-3">
                      <h4 className="font-medium text-gray-900 mb-1">Evidence Analysis</h4>
                      <div className="bg-gray-50 border border-gray-200 rounded p-3">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs font-medium text-gray-700">Source</span>
                          <span className={`px-2 py-1 text-xs rounded ${
                            violation.suggestion.evidence.confidence === 'high' ? 'bg-green-100 text-green-700' :
                            violation.suggestion.evidence.confidence === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-red-100 text-red-700'
                          }`}>
                            {violation.suggestion.evidence.confidence} confidence
                          </span>
                        </div>
                        <p className="text-sm text-gray-600">{violation.suggestion.evidence.reference}</p>
                      </div>
                    </div>

                    {/* Recommended Action */}
                    <div className={`p-3 rounded border ${
                      violation.type === 'fabrication_detected' ? 'bg-red-50 border-red-200' :
                      'bg-yellow-50 border-yellow-200'
                    }`}>
                      <h4 className="font-medium text-gray-900 mb-1">Recommended Action</h4>
                      {violation.type === 'fabrication_detected' ? (
                        <p className="text-sm text-red-800">
                          <strong>Reject this suggestion.</strong> Fabricated information can damage your credibility 
                          and may be discovered during background checks.
                        </p>
                      ) : (
                        <p className="text-sm text-yellow-800">
                          <strong>Edit or reject this suggestion.</strong> Consider modifying the claim to be 
                          more conservative and accurately reflect your actual experience.
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}

      {/* No Violations */}
      {violations.length === 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
          <div className="flex justify-center mb-4">
            <div className="p-3 bg-green-100 rounded-full">
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No Guardrail Violations!</h3>
          <p className="text-gray-600">
            All suggestions passed our truthfulness validation. 
            You can proceed with confidence that the recommendations are based on your actual experience.
          </p>
        </div>
      )}

      {/* Best Practices */}
      {violations.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-4">Best Practices for Resume Writing</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <h4 className="font-medium text-blue-800">Truthfulness Guidelines</h4>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• Only claim experience you can verify</li>
                <li>• Be conservative with metrics and achievements</li>
                <li>• Focus on actual accomplishments over claims</li>
                <li>• Use honest language that reflects reality</li>
              </ul>
            </div>
            <div className="space-y-2">
              <h4 className="font-medium text-blue-800">Red Flags to Avoid</h4>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• "Expert" or "Master" without evidence</li>
                <li>• Multiple exact percentage improvements</li>
                <li>• Claims of "revolutionizing" or "pioneering"</li>
                <li>• Experience levels not supported by timeline</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

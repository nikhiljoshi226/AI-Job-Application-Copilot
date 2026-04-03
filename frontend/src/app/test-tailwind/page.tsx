export default function TestTailwind() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-8">Tailwind CSS Test</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl shadow-xl p-6 transform hover:scale-105 transition-all duration-300">
            <div className="w-16 h-16 bg-blue-500 rounded-full mx-auto mb-4"></div>
            <h2 className="text-xl font-bold text-gray-800 mb-2">Card 1</h2>
            <p className="text-gray-600">If you see this styled properly, Tailwind is working!</p>
          </div>
          
          <div className="bg-white rounded-xl shadow-xl p-6 transform hover:scale-105 transition-all duration-300">
            <div className="w-16 h-16 bg-green-500 rounded-full mx-auto mb-4"></div>
            <h2 className="text-xl font-bold text-gray-800 mb-2">Card 2</h2>
            <p className="text-gray-600">This should have a green circle and hover effects.</p>
          </div>
          
          <div className="bg-white rounded-xl shadow-xl p-6 transform hover:scale-105 transition-all duration-300">
            <div className="w-16 h-16 bg-purple-500 rounded-full mx-auto mb-4"></div>
            <h2 className="text-xl font-bold text-gray-800 mb-2">Card 3</h2>
            <p className="text-gray-600">All cards should be responsive and interactive.</p>
          </div>
        </div>
        
        <div className="mt-12 text-center">
          <button className="bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-8 rounded-full transform hover:scale-110 transition-all duration-300">
            Test Button
          </button>
        </div>
      </div>
    </div>
  )
}

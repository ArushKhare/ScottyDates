import React, { useState } from 'react';
import { Heart, X, Camera, MessageCircle, Send, ArrowLeft } from 'lucide-react';

const CMUDatingApp = () => {
  const [currentView, setCurrentView] = useState('discover');
  const [profileData, setProfileData] = useState({
    name: 'You',
    age: '',
    height: '',
    major: '',
    photo: null,
    hobby: '',
    class: ''
  });

  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [likedProfiles, setLikedProfiles] = useState([]);
  const [matches, setMatches] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);
  const [chatMessages, setChatMessages] = useState({});
  const [messageInput, setMessageInput] = useState('');

  const sampleProfiles = [
    {
      id: 1,
      name: "Alex Chen",
      age: 21,
      height: "5'9\"",
      major: "Computer Science",
      hobby: "Rock climbing, photography",
      class: "Junior",
      photo: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=500&fit=crop",
      likesYou: true
    },
    {
      id: 2,
      name: "Sarah Miller",
      age: 20,
      height: "5'6\"",
      major: "Mechanical Engineering",
      hobby: "Running, reading sci-fi",
      class: "Sophomore",
      photo: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=500&fit=crop",
      likesYou: false
    },
    {
      id: 3,
      name: "Jordan Lee",
      age: 22,
      height: "6'1\"",
      major: "Business Administration",
      hobby: "Basketball, cooking",
      class: "Senior",
      photo: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=500&fit=crop",
      likesYou: true
    },
    {
      id: 4,
      name: "Emily Zhang",
      age: 21,
      height: "5'5\"",
      major: "Architecture",
      hobby: "Sketching, hiking",
      class: "Junior",
      photo: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=500&fit=crop",
      likesYou: true
    }
  ];

  const handleInputChange = (field, value) => {
    setProfileData(prev => ({ ...prev, [field]: value }));
  };

  const handleSwipe = (direction) => {
    const currentProfile = sampleProfiles[currentCardIndex];
    
    if (direction === 'right') {
      setLikedProfiles(prev => [...prev, currentProfile.id]);
      
      if (currentProfile.likesYou) {
        setMatches(prev => [...prev, currentProfile]);
        alert(`It's a match! You and ${currentProfile.name} liked each other! 💕`);
      }
    }
    
    if (currentCardIndex < sampleProfiles.length - 1) {
      setCurrentCardIndex(prev => prev + 1);
    } else {
      setCurrentCardIndex(0);
    }
  };

  const sendMessage = () => {
    if (!messageInput.trim() || !selectedChat) return;

    const newMessage = {
      text: messageInput,
      sender: 'you',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setChatMessages(prev => ({
      ...prev,
      [selectedChat.id]: [...(prev[selectedChat.id] || []), newMessage]
    }));

    setMessageInput('');

    setTimeout(() => {
      const autoReply = {
        text: getAutoReply(),
        sender: 'them',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setChatMessages(prev => ({
        ...prev,
        [selectedChat.id]: [...(prev[selectedChat.id] || []), autoReply]
      }));
    }, 1500);
  };

  const getAutoReply = () => {
    const replies = [
      "That sounds great! Tell me more 😊",
      "I'd love to! When are you free?",
      "Haha that's awesome!",
      "Yeah, I'm really into that too!",
      "Want to meet up at the UC sometime?"
    ];
    return replies[Math.floor(Math.random() * replies.length)];
  };

  const ProfileView = () => (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 p-6">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800">Create Your Profile</h1>
            <div className="flex gap-2">
              <button
                onClick={() => setCurrentView('profile')}
                className={`px-4 py-2 rounded-lg font-semibold transition ${
                  currentView === 'profile' 
                    ? 'bg-red-500 text-white' 
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                Profile
              </button>
              <button
                onClick={() => setCurrentView('discover')}
                className={`px-4 py-2 rounded-lg font-semibold transition ${
                  currentView === 'discover' 
                    ? 'bg-red-500 text-white' 
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                Discover
              </button>
              <button
                onClick={() => setCurrentView('matches')}
                className={`px-4 py-2 rounded-lg font-semibold transition relative ${
                  currentView === 'matches' 
                    ? 'bg-red-500 text-white' 
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                Matches
                {matches.length > 0 && (
                  <span className="absolute -top-2 -right-2 bg-pink-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {matches.length}
                  </span>
                )}
              </button>
            </div>
          </div>

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Name</label>
              <input
                type="text"
                value={profileData.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-red-400 focus:outline-none transition"
                placeholder="Your full name"
              />
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Age</label>
                <input
                  type="number"
                  value={profileData.age}
                  onChange={(e) => handleInputChange('age', e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-red-400 focus:outline-none transition"
                  placeholder="21"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Height</label>
                <input
                  type="text"
                  value={profileData.height}
                  onChange={(e) => handleInputChange('height', e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-red-400 focus:outline-none transition"
                  placeholder="5'10&quot;"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Class</label>
                <select
                  value={profileData.class}
                  onChange={(e) => handleInputChange('class', e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-red-400 focus:outline-none transition"
                >
                  <option value="">Select</option>
                  <option value="Freshman">Freshman</option>
                  <option value="Sophomore">Sophomore</option>
                  <option value="Junior">Junior</option>
                  <option value="Senior">Senior</option>
                  <option value="Graduate">Graduate</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Major</label>
              <input
                type="text"
                value={profileData.major}
                onChange={(e) => handleInputChange('major', e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-red-400 focus:outline-none transition"
                placeholder="e.g., Computer Science, Engineering"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Photo</label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-red-400 transition cursor-pointer">
                <Camera className="mx-auto mb-4 text-gray-400" size={48} />
                <p className="text-gray-600 font-medium">Click to upload photo</p>
                <p className="text-sm text-gray-400 mt-2">JPG, PNG up to 10MB</p>
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Hobbies</label>
              <textarea
                value={profileData.hobby}
                onChange={(e) => handleInputChange('hobby', e.target.value)}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-red-400 focus:outline-none transition"
                rows="3"
                placeholder="Tell us about your interests and hobbies..."
              />
            </div>

            <button className="w-full bg-gradient-to-r from-red-500 to-orange-500 text-white font-bold py-4 rounded-lg hover:from-red-600 hover:to-orange-600 transition transform hover:scale-105 shadow-lg">
              Save Profile
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  const DiscoverView = () => {
    const currentProfile = sampleProfiles[currentCardIndex];
    const peopleWhoLikeYou = sampleProfiles.filter(p => p.likesYou && !likedProfiles.includes(p.id));

    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 p-6">
        <div className="max-w-md mx-auto">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-800">Discover</h1>
            <div className="flex gap-2">
              <button
                onClick={() => setCurrentView('profile')}
                className={`px-4 py-2 rounded-lg font-semibold transition ${
                  currentView === 'profile' 
                    ? 'bg-red-500 text-white' 
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                Profile
              </button>
              <button
                onClick={() => setCurrentView('discover')}
                className={`px-4 py-2 rounded-lg font-semibold transition ${
                  currentView === 'discover' 
                    ? 'bg-red-500 text-white' 
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                Discover
              </button>
              <button
                onClick={() => setCurrentView('matches')}
                className={`px-4 py-2 rounded-lg font-semibold transition relative ${
                  currentView === 'matches' 
                    ? 'bg-red-500 text-white' 
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                Matches
                {matches.length > 0 && (
                  <span className="absolute -top-2 -right-2 bg-pink-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {matches.length}
                  </span>
                )}
              </button>
            </div>
          </div>

          {peopleWhoLikeYou.length > 0 && (
            <div className="bg-gradient-to-r from-pink-500 to-red-500 text-white rounded-2xl p-4 mb-6 shadow-lg">
              <h3 className="font-bold text-lg mb-2">💕 {peopleWhoLikeYou.length} {peopleWhoLikeYou.length === 1 ? 'person likes' : 'people like'} you!</h3>
              <p className="text-sm opacity-90">Keep swiping to find your matches</p>
            </div>
          )}

          <div className="bg-white rounded-3xl shadow-2xl overflow-hidden">
            <div className="relative">
              <img 
                src={currentProfile.photo} 
                alt={currentProfile.name}
                className="w-full h-96 object-cover"
              />
              <div className="absolute top-4 right-4 bg-red-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                Active Today
              </div>
              {currentProfile.likesYou && (
                <div className="absolute top-4 left-4 bg-pink-500 text-white px-3 py-1 rounded-full text-sm font-semibold flex items-center gap-1">
                  <Heart size={16} fill="white" />
                  Likes You
                </div>
              )}
            </div>

            <div className="p-6">
              <h2 className="text-3xl font-bold text-gray-800 mb-2">
                {currentProfile.name}, {currentProfile.age}
              </h2>
              
              <div className="space-y-3 mb-6">
                <div className="flex items-center gap-2 text-gray-600">
                  <span className="font-semibold">Height:</span>
                  <span>{currentProfile.height}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-600">
                  <span className="font-semibold">Major:</span>
                  <span>{currentProfile.major}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-600">
                  <span className="font-semibold">Class:</span>
                  <span>{currentProfile.class}</span>
                </div>
                <div className="flex items-start gap-2 text-gray-600">
                  <span className="font-semibold">Hobbies:</span>
                  <span>{currentProfile.hobby}</span>
                </div>
              </div>

              <div className="flex justify-center gap-6 mt-8">
                <button
                  onClick={() => handleSwipe('left')}
                  className="bg-white border-4 border-gray-300 rounded-full p-5 hover:border-gray-400 transition transform hover:scale-110 shadow-lg"
                >
                  <X size={32} className="text-gray-600" />
                </button>
                <button
                  onClick={() => handleSwipe('right')}
                  className="bg-gradient-to-br from-red-500 to-pink-500 rounded-full p-5 hover:from-red-600 hover:to-pink-600 transition transform hover:scale-110 shadow-xl"
                >
                  <Heart size={32} className="text-white" />
                </button>
              </div>

              <div className="text-center mt-6 text-sm text-gray-500">
                {currentCardIndex + 1} of {sampleProfiles.length}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const MatchesView = () => {
    if (selectedChat) {
      const messages = chatMessages[selectedChat.id] || [];
      
      return (
        <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 flex flex-col">
          <div className="bg-white shadow-md p-4 flex items-center gap-4">
            <button
              onClick={() => setSelectedChat(null)}
              className="p-2 hover:bg-gray-100 rounded-full transition"
            >
              <ArrowLeft size={24} className="text-gray-700" />
            </button>
            <img 
              src={selectedChat.photo} 
              alt={selectedChat.name}
              className="w-12 h-12 rounded-full object-cover"
            />
            <div>
              <h2 className="font-bold text-lg text-gray-800">{selectedChat.name}</h2>
              <p className="text-sm text-green-500">Active now</p>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            <div className="text-center">
              <div className="inline-block bg-pink-100 text-pink-600 px-4 py-2 rounded-full text-sm font-semibold mb-4">
                💕 You matched with {selectedChat.name}!
              </div>
            </div>

            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.sender === 'you' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs px-4 py-2 rounded-2xl ${
                    msg.sender === 'you'
                      ? 'bg-red-500 text-white'
                      : 'bg-gray-200 text-gray-800'
                  }`}
                >
                  <p>{msg.text}</p>
                  <p className={`text-xs mt-1 ${
                    msg.sender === 'you' ? 'text-red-100' : 'text-gray-500'
                  }`}>
                    {msg.timestamp}
                  </p>
                </div>
              </div>
            ))}
          </div>

          <div className="bg-white border-t p-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={messageInput}
                onChange={(e) => setMessageInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Type a message..."
                className="flex-1 px-4 py-3 border-2 border-gray-200 rounded-full focus:border-red-400 focus:outline-none transition"
              />
              <button
                onClick={sendMessage}
                className="bg-red-500 text-white p-3 rounded-full hover:bg-red-600 transition"
              >
                <Send size={24} />
              </button>
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800">Your Matches</h1>
            <div className="flex gap-2">
              <button
                onClick={() => setCurrentView('profile')}
                className={`px-4 py-2 rounded-lg font-semibold transition ${
                  currentView === 'profile' 
                    ? 'bg-red-500 text-white' 
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                Profile
              </button>
              <button
                onClick={() => setCurrentView('discover')}
                className={`px-4 py-2 rounded-lg font-semibold transition ${
                  currentView === 'discover' 
                    ? 'bg-red-500 text-white' 
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                Discover
              </button>
              <button
                onClick={() => setCurrentView('matches')}
                className={`px-4 py-2 rounded-lg font-semibold transition relative ${
                  currentView === 'matches' 
                    ? 'bg-red-500 text-white' 
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                Matches
                {matches.length > 0 && (
                  <span className="absolute -top-2 -right-2 bg-pink-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {matches.length}
                  </span>
                )}
              </button>
            </div>
          </div>

          {matches.length === 0 ? (
            <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
              <Heart size={64} className="mx-auto mb-4 text-gray-300" />
              <h2 className="text-2xl font-bold text-gray-800 mb-2">No matches yet</h2>
              <p className="text-gray-600 mb-6">Start swiping to find your perfect match!</p>
              <button
                onClick={() => setCurrentView('discover')}
                className="bg-gradient-to-r from-red-500 to-orange-500 text-white font-bold px-8 py-3 rounded-lg hover:from-red-600 hover:to-orange-600 transition"
              >
                Start Discovering
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {matches.map((match) => (
                <div
                  key={match.id}
                  className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition cursor-pointer"
                  onClick={() => setSelectedChat(match)}
                >
                  <div className="flex">
                    <img 
                      src={match.photo} 
                      alt={match.name}
                      className="w-32 h-32 object-cover"
                    />
                    <div className="p-4 flex-1">
                      <h3 className="text-xl font-bold text-gray-800 mb-1">
                        {match.name}, {match.age}
                      </h3>
                      <p className="text-sm text-gray-600 mb-2">{match.major}</p>
                      <p className="text-sm text-gray-500 mb-3">{match.hobby}</p>
                      <button className="flex items-center gap-2 bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition">
                        <MessageCircle size={18} />
                        Chat Now
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <>
      {currentView === 'profile' && <ProfileView />}
      {currentView === 'discover' && <DiscoverView />}
      {currentView === 'matches' && <MatchesView />}
    </>
  );
};

export default CMUDatingApp;
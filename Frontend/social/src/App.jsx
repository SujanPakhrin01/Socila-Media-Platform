import React, { useState, useEffect } from 'react';
import { User, Home, MessageSquare, Heart, LogOut, Search, Plus, Trash2 } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';
const MEDIA_URL = 'http://localhost:8000';

const App = () => {
  const [currentPage, setCurrentPage] = useState('login');
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [profiles, setProfiles] = useState([]);
  const [comments, setComments] = useState({});
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setUser({ token });
      loadPosts();
    }
  }, []);

  const apiCall = async (endpoint, options = {}) => {
    const token = localStorage.getItem('access_token');
    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
      setCurrentPage('login');
      throw new Error('Authentication failed');
    }

    return response;
  };

  const handleSignup = async (username, email, password) => {
    try {
      const response = await fetch(`${API_BASE}/SignUp/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
      });

      const result = await response.json();
      if (response.ok) {
        localStorage.setItem('access_token', result.access);
        localStorage.setItem('refresh_token', result.refresh);
        setUser({ token: result.access });
        setCurrentPage('home');
        loadPosts();
      } else {
        alert('Signup failed: ' + JSON.stringify(result));
      }
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };

  const handleLogin = async (username, password) => {
    try {
      const response = await fetch(`${API_BASE}/Login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      const result = await response.json();
      if (response.ok) {
        localStorage.setItem('access_token', result.access);
        localStorage.setItem('refresh_token', result.refresh);
        setUser({ token: result.access });
        setCurrentPage('home');
        loadPosts();
      } else {
        alert('Login failed: ' + JSON.stringify(result));
      }
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    setCurrentPage('login');
    setPosts([]);
  };

  const loadPosts = async () => {
    try {
      const response = await apiCall('/Home/');
      const data = await response.json();
      setPosts(data);
    } catch (error) {
      console.error('Error loading posts:', error);
    }
  };

  const loadProfiles = async () => {
    try {
      const response = await apiCall('/Profile/');
      const data = await response.json();
      setProfiles(data);
    } catch (error) {
      console.error('Error loading profiles:', error);
    }
  };

  const createPost = async (content, imageFile) => {
    const formData = new FormData();
    formData.append('content', content);
    if (imageFile) {
      formData.append('image', imageFile);
    }

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_BASE}/Home/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        loadPosts();
        alert('Post created successfully!');
        return true;
      } else {
        const error = await response.json();
        alert('Error: ' + JSON.stringify(error));
      }
    } catch (error) {
      alert('Error creating post: ' + error.message);
    }
    return false;
  };

  const deletePost = async (postId) => {
    if (!window.confirm('Are you sure you want to delete this post?')) return;

    try {
      const response = await apiCall(`/Home/${postId}/`, {
        method: 'DELETE',
      });

      if (response.ok) {
        loadPosts();
        alert('Post deleted successfully!');
      }
    } catch (error) {
      alert('Error deleting post: ' + error.message);
    }
  };

  const toggleLike = async (postId) => {
    try {
      const response = await apiCall('/Like/', {
        method: 'POST',
        body: JSON.stringify({ post: postId }),
      });

      if (response.ok) {
        const result = await response.json();
        setPosts(prevPosts => 
          prevPosts.map(post => 
            post.id === postId 
              ? { ...post, likes_count: result.likes_count, is_liked: result.liked }
              : post
          )
        );
      }
    } catch (error) {
      console.error('Error toggling like:', error);
    }
  };

  const addComment = async (postId, content) => {
    if (!content || !content.trim()) {
      alert('Please enter a comment');
      return;
    }

    try {
      const response = await apiCall('/Comments/', {
        method: 'POST',
        body: JSON.stringify({ post: postId, content }),
      });

      if (response.ok) {
        loadPosts();
        setComments({ ...comments, [postId]: '' });
      }
    } catch (error) {
      alert('Error adding comment: ' + error.message);
    }
  };

  const searchPosts = async () => {
    try {
      const response = await apiCall(`/Home/?search=${searchTerm}`);
      const data = await response.json();
      setPosts(data);
    } catch (error) {
      console.error('Error searching posts:', error);
    }
  };

  if (!user) {
    return <LoginSignup 
      currentPage={currentPage}
      setCurrentPage={setCurrentPage}
      handleLogin={handleLogin}
      handleSignup={handleSignup}
    />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation 
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
        handleLogout={handleLogout}
        loadPosts={loadPosts}
        loadProfiles={loadProfiles}
      />

      <div className="max-w-6xl mx-auto px-4 py-8">
        {currentPage === 'home' && (
          <HomePage
            searchTerm={searchTerm}
            setSearchTerm={setSearchTerm}
            searchPosts={searchPosts}
            createPost={createPost}
            posts={posts}
            deletePost={deletePost}
            toggleLike={toggleLike}
            comments={comments}
            setComments={setComments}
            addComment={addComment}
          />
        )}

        {currentPage === 'profile' && (
          <ProfilePage profiles={profiles} />
        )}
      </div>
    </div>
  );
};

const LoginSignup = ({ currentPage, setCurrentPage, handleLogin, handleSignup }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = () => {
    if (currentPage === 'login') {
      handleLogin(username, password);
    } else {
      handleSignup(username, email, password);
    }
  };

  return (
    <div className="min-h-screen from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            {currentPage === 'login' ? 'Welcome Back' : 'Join Us'}
          </h1>
          <p className="text-gray-600">
            {currentPage === 'login' ? 'Sign in to continue' : 'Create your account'}
          </p>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          {currentPage === 'signup' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          )}
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <button
            onClick={handleSubmit}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition"
          >
            {currentPage === 'login' ? 'Sign In' : 'Create Account'}
          </button>
          
          <p className="text-center text-sm text-gray-600">
            {currentPage === 'login' ? "Don't have an account? " : "Already have an account? "}
            <button
              onClick={() => setCurrentPage(currentPage === 'login' ? 'signup' : 'login')}
              className="text-blue-600 hover:underline"
            >
              {currentPage === 'login' ? 'Sign Up' : 'Sign In'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

const Navigation = ({ currentPage, setCurrentPage, handleLogout, loadPosts, loadProfiles }) => {
  return (
    <nav className="bg-white shadow-sm border-b sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-blue-600">SocialApp</h1>
        <div className="flex items-center gap-4">
          <button
            onClick={() => { setCurrentPage('home'); loadPosts(); }}
            className={`p-2 rounded-lg ${currentPage === 'home' ? 'bg-blue-100 text-blue-600' : 'text-gray-600 hover:bg-gray-100'}`}
          >
            <Home size={20} />
          </button>
          <button
            onClick={() => { setCurrentPage('profile'); loadProfiles(); }}
            className={`p-2 rounded-lg ${currentPage === 'profile' ? 'bg-blue-100 text-blue-600' : 'text-gray-600 hover:bg-gray-100'}`}
          >
            <User size={20} />
          </button>
          <button
            onClick={handleLogout}
            className="p-2 rounded-lg text-red-600 hover:bg-red-50"
          >
            <LogOut size={20} />
          </button>
        </div>
      </div>
    </nav>
  );
};

const HomePage = ({ searchTerm, setSearchTerm, searchPosts, createPost, posts, deletePost, toggleLike, comments, setComments, addComment }) => {
  const [postContent, setPostContent] = useState('');
  const [postImage, setPostImage] = useState(null);

  const handleCreatePost = async () => {
    if (!postContent.trim()) {
      alert('Please enter some content');
      return;
    }
    
    const success = await createPost(postContent, postImage);
    if (success) {
      setPostContent('');
      setPostImage(null);
      // Reset file input
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) fileInput.value = '';
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Search posts by username or ID..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && searchPosts()}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={searchPosts}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
          >
            <Search size={18} />
            Search
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
          <Plus size={20} />
          Create Post
        </h2>
        <div className="space-y-4">
          <textarea
            placeholder="What's on your mind?"
            value={postContent}
            onChange={(e) => setPostContent(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            rows="3"
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Upload Image (optional)</label>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setPostImage(e.target.files[0])}
              className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
          </div>
          <button
            onClick={handleCreatePost}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Post
          </button>
        </div>
      </div>

      {posts.length === 0 && (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <p className="text-gray-500 text-lg">No posts yet. Create the first one!</p>
        </div>
      )}

      <div className="space-y-4">
        {posts.map((post) => (
          <PostCard
            key={post.id}
            post={post}
            deletePost={deletePost}
            toggleLike={toggleLike}
            comments={comments}
            setComments={setComments}
            addComment={addComment}
          />
        ))}
      </div>
    </div>
  );
};

const PostCard = ({ post, deletePost, toggleLike, comments, setComments, addComment }) => {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
            {post.user?.username?.[0]?.toUpperCase() || 'U'}
          </div>
          <div>
            <p className="font-semibold">{post.user?.username || 'Anonymous'}</p>
            <p className="text-sm text-gray-500">
              {new Date(post.created_at).toLocaleDateString()} at {new Date(post.created_at).toLocaleTimeString()}
            </p>
          </div>
        </div>
        <button
          onClick={() => deletePost(post.id)}
          className="text-red-600 hover:bg-red-50 p-2 rounded transition"
        >
          <Trash2 size={18} />
        </button>
      </div>

      <p className="text-gray-800 mb-4 whitespace-pre-wrap">{post.content}</p>

      {post.image && (
        <img
          src={post.image.startsWith('http') ? post.image : `${MEDIA_URL}${post.image}`}
          alt="Post"
          className="w-full rounded-lg mb-4 max-h-96 object-cover"
          onError={(e) => {
            console.error('Image failed to load:', post.image);
            e.target.style.display = 'none';
          }}
        />
      )}

      <div className="flex items-center gap-6 pt-4 border-t">
        <button
          onClick={() => toggleLike(post.id)}
          className={`flex items-center gap-2 transition ${
            post.is_liked ? 'text-red-600' : 'text-gray-600 hover:text-red-600'
          }`}
        >
          <Heart size={20} fill={post.is_liked ? 'currentColor' : 'none'} />
          <span className="font-medium">{post.likes_count || 0}</span>
        </button>
        <div className="flex items-center gap-2 text-gray-600">
          <MessageSquare size={20} />
          <span className="font-medium">{post.comments?.length || 0}</span>
        </div>
      </div>

      <div className="mt-4 space-y-3">
        {post.comments && post.comments.length > 0 && (
          <div className="space-y-2">
            {post.comments.map((comment, idx) => (
              <div key={idx} className="bg-gray-50 rounded-lg p-3">
                <p className="font-semibold text-sm text-blue-600">{comment.user?.username}</p>
                <p className="text-gray-700 text-sm mt-1">{comment.content}</p>
                <p className="text-xs text-gray-400 mt-1">
                  {new Date(comment.created_at).toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        )}

        <div className="flex gap-2 mt-3">
          <input
            type="text"
            placeholder="Add a comment..."
            value={comments[post.id] || ''}
            onChange={(e) => setComments({ ...comments, [post.id]: e.target.value })}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                addComment(post.id, comments[post.id]);
              }
            }}
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={() => addComment(post.id, comments[post.id])}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 text-sm transition"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

const ProfilePage = ({ profiles }) => {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-6">All Users</h2>
      {profiles.length === 0 && (
        <p className="text-gray-500 text-center py-8">No profiles found</p>
      )}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {profiles.map((profile) => (
          <div key={profile.id} className="border rounded-lg p-6 hover:shadow-lg transition">
            <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-4">
              {profile.username?.[0]?.toUpperCase()}
            </div>
            <h3 className="text-center font-bold text-lg">{profile.username}</h3>
            <p className="text-center text-sm text-gray-600 mt-1">{profile.email}</p>
            {profile.first_name && (
              <p className="text-center text-sm text-gray-500 mt-2">
                {profile.first_name} {profile.last_name}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
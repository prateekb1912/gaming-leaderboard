// frontend/src/App.jsx
import { useEffect, useState } from "react";
import axios from "axios";

const BASE_URL = "https://gaming-leaderboard-9euy.onrender.com";
interface UserRank {
  user_id: number;
  username: string;
  total_score: number;
  rank: number;
}

function App() {
  const [leaderboard, setLeaderboard] = useState<UserRank[]>([]);
  const [userId, setUserId] = useState("");
  const [userRank, setUserRank] = useState<UserRank | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchLeaderboard = async () => {
    try {
      const res = await axios.get(BASE_URL + "/api/leaderboard/top");
      setLeaderboard(res.data);
    } catch (err) {
      console.error("Error fetching leaderboard:", err);
    }
  };

  const fetchUserRank = async () => {
    try {
      if (!userId) return;
      setLoading(true);
      const res = await axios.get(`${BASE_URL}/api/leaderboard/rank/${userId}`);
      setUserRank(res.data);
    } catch (err) {
      console.error("Error fetching user rank:", err);
      setUserRank(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeaderboard();
    const interval = setInterval(fetchLeaderboard, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white p-4 font-sans">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-extrabold text-center mb-8">
          🎮 Gaming Leaderboard
        </h1>

        <div className="bg-gray-800 rounded-xl shadow-md p-6 mb-10">
          <h2 className="text-2xl font-semibold mb-4">🏆 Top 10 Players</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full table-auto text-sm">
              <thead>
                <tr className="bg-gray-700 text-left">
                  <th className="px-4 py-2">Rank</th>
                  <th className="px-4 py-2">User</th>
                  <th className="px-4 py-2">Total Score</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map((entry) => (
                  <tr
                    key={entry.user_id}
                    className="border-b border-gray-600 hover:bg-gray-700"
                  >
                    <td className="px-4 py-2 font-medium">{entry.rank}</td>
                    <td className="px-4 py-2">{entry.username}</td>
                    <td className="px-4 py-2 text-green-400">
                      {entry.total_score}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-gray-800 rounded-xl shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-4">🔍 Check Your Rank</h2>
          <div className="flex items-center space-x-4 mb-4">
            <input
              type="number"
              className="text-black p-2 rounded w-full max-w-xs"
              placeholder="Enter User ID"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
            />
            <button
              onClick={fetchUserRank}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded transition"
            >
              Check
            </button>
          </div>

          {loading && <p className="text-yellow-400">⏳ Loading...</p>}
          {userRank && (
            <div className="mt-2 text-green-400 space-y-1">
              <p>
                ✅ <strong>User:</strong> {userRank.username}
              </p>
              <p>
                🏅 <strong>Rank:</strong> {userRank.rank}
              </p>
              <p>
                🎮 <strong>Total Score:</strong> {userRank.total_score}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;

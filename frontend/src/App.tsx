// frontend/src/App.jsx
import { useEffect, useState } from "react";
import axios from "axios";

interface Leaderboard {
  user_id: number;
  username: string;
  total_score: number;
  rank: number;
}

function App() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [userId, setUserId] = useState("");
  const [userRank, setUserRank] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchLeaderboard = async () => {
    try {
      const res = await axios.get("/api/leaderboard/top");
      setLeaderboard(res.data);
    } catch (err) {
      console.error("Error fetching leaderboard:", err);
    }
  };

  const fetchUserRank = async () => {
    try {
      if (!userId) return;
      setLoading(true);
      const res = await axios.get(`/api/leaderboard/rank/${userId}`);
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
    <div className="min-h-screen bg-gray-900 text-white p-4">
      <h1 className="text-3xl font-bold mb-6">🎮 Live Leaderboard</h1>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Top 10 Players</h2>
        <table className="w-full table-auto border-collapse">
          <thead>
            <tr className="bg-gray-700">
              <th className="px-4 py-2">Rank</th>
              <th className="px-4 py-2">User</th>
              <th className="px-4 py-2">Total Score</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((entry: Leaderboard) => (
              <tr key={entry.user_id} className="border-b border-gray-700">
                <td className="px-4 py-2">{entry.rank}</td>
                <td className="px-4 py-2">{entry.username}</td>
                <td className="px-4 py-2">{entry.total_score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mb-4">
        <h2 className="text-xl font-semibold mb-2">Check Your Rank</h2>
        <input
          type="number"
          className="text-black p-2 mr-2 rounded"
          placeholder="Enter User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        />
        <button
          onClick={fetchUserRank}
          className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded"
        >
          Check
        </button>
      </div>

      {loading && <p className="text-yellow-400">Loading...</p>}
      {userRank && (
        <div className="mt-2 text-green-400">
          <p>User ID: {userRank.user_id}</p>
          <p>Rank: {userRank.rank}</p>
        </div>
      )}
    </div>
  );
}

export default App;

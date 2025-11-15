// frontend/app.js
const API_BASE = "http://localhost:8000";
let accessToken = null;

// swipe state
let matches = [];
let currentMatchIndex = 0;

// chat state
let currentChatUserId = null;

function authHeader() {
  return accessToken ? { Authorization: `Bearer ${accessToken}` } : {};
}

// ------------ AUTH ------------

async function register() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const full_name = document.getElementById("full_name").value;

  const resp = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, full_name }),
  });
  const data = await resp.json();
  console.log("register", data);
  if (resp.ok) {
    alert("Registered! Now log in.");
  } else {
    alert(data.detail || "Registration failed");
  }
}

async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const body = new URLSearchParams();
  body.append("username", email);
  body.append("password", password);

  const resp = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  const data = await resp.json();
  console.log("login", data);
  if (data.access_token) {
    accessToken = data.access_token;
    alert("Logged in!");
  } else {
    alert(data.detail || "Login failed");
  }
}

// ------------ PROFILE ------------

async function saveProfile() {
  const age = parseInt(document.getElementById("age").value);
  const gender = document.getElementById("gender").value;
  const major = document.getElementById("major").value;
  const class_year = parseInt(document.getElementById("class_year").value);
  const campus = document.getElementById("campus").value;
  const interests = document
    .getElementById("interests")
    .value.split(",")
    .map((s) => s.trim())
    .filter((s) => s.length > 0);
  const bio = document.getElementById("bio").value;

  const resp = await fetch(`${API_BASE}/profile`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeader(),
    },
    body: JSON.stringify({
      age,
      gender,
      major,
      class_year,
      campus,
      interests,
      bio,
    }),
  });
  const data = await resp.json();
  console.log("profile", data);
  if (resp.ok) {
    alert("Profile saved");
  } else {
    alert(data.detail || "Error saving profile");
  }
}

// ------------ SWIPING ------------

async function loadMatches() {
  const resp = await fetch(`${API_BASE}/matches`, {
    headers: {
      ...authHeader(),
    },
  });
  const data = await resp.json();
  console.log("matches", data);
  if (!resp.ok) {
    alert(data.detail || "Error loading matches");
    return;
  }
  matches = data;
  currentMatchIndex = 0;
  renderCurrentMatch();
}

function renderCurrentMatch() {
  const container = document.getElementById("swipe_container");
  container.innerHTML = "";

  if (!matches || matches.length === 0) {
    container.innerHTML = "<p>No matches yet. Try again later.</p>";
    return;
  }

  const m = matches[currentMatchIndex];
  const card = document.createElement("div");
  card.className = "match-card";

  const name = document.createElement("h3");
  name.textContent = `User #${m.profile.user_id} (score: ${m.score.toFixed(1)})`;

  const details = document.createElement("p");
  details.textContent = `${m.profile.age || "?"} • ${m.profile.gender || ""} • ${
    m.profile.major
  } • Class of ${m.profile.class_year}`;

  const interests = document.createElement("p");
  interests.textContent = `Interests: ${m.profile.interests.join(", ")}`;

  const bio = document.createElement("p");
  bio.textContent = `Bio: ${m.profile.bio}`;

  const actions = document.createElement("div");
  actions.className = "match-actions";

  const prevBtn = document.createElement("button");
  prevBtn.textContent = "⬅ Prev";
  prevBtn.onclick = () => {
    currentMatchIndex =
      (currentMatchIndex - 1 + matches.length) % matches.length;
    renderCurrentMatch();
  };

  const passBtn = document.createElement("button");
  passBtn.textContent = "Pass";
  passBtn.onclick = () => {
    // For now we just go to next; you could call a /swipe endpoint later
    currentMatchIndex = (currentMatchIndex + 1) % matches.length;
    renderCurrentMatch();
  };

  const likeBtn = document.createElement("button");
  likeBtn.textContent = "Like";
  likeBtn.onclick = () => {
    // In a real app, POST a "like" to backend; for now just advance
    alert(`You liked user #${m.profile.user_id}`);
    currentMatchIndex = (currentMatchIndex + 1) % matches.length;
    renderCurrentMatch();
  };

  const chatBtn = document.createElement("button");
  chatBtn.textContent = "Chat";
  chatBtn.onclick = () => {
    openChat(m.profile.user_id);
  };

  actions.appendChild(prevBtn);
  actions.appendChild(passBtn);
  actions.appendChild(likeBtn);
  actions.appendChild(chatBtn);

  card.appendChild(name);
  card.appendChild(details);
  card.appendChild(interests);
  card.appendChild(bio);
  card.appendChild(actions);

  container.appendChild(card);
}

// ------------ CHAT ------------

function openChat(otherUserId) {
  currentChatUserId = otherUserId;
  document.getElementById(
    "chat_with_user_label"
  ).textContent = `User #${otherUserId}`;
  loadChatThread();
  // optionally scroll chat into view
  document.getElementById("chat").scrollIntoView({ behavior: "smooth" });
}

async function loadChatThread() {
  if (!currentChatUserId) return;

  const resp = await fetch(
    `${API_BASE}/messages/thread/${currentChatUserId}`,
    {
      headers: {
        ...authHeader(),
      },
    }
  );
  const data = await resp.json();
  console.log("thread", data);

  const container = document.getElementById("chat_messages");
  container.innerHTML = "";

  if (!resp.ok) {
    container.textContent = data.detail || "Error loading messages";
    return;
  }

  if (!Array.isArray(data) || data.length === 0) {
    container.textContent = "No messages yet. Say hi!";
    return;
  }

  data.forEach((m) => {
    const div = document.createElement("div");
    const fromMe = m.from_user_id !== undefined && m.from_user_id === getMyUserIdFromToken();
    div.className = fromMe ? "msg-me" : "msg-them";
    const who = fromMe ? "You" : `User #${m.from_user_id}`;
    div.textContent = `${who}: ${m.text}`;
    container.appendChild(div);
  });

  container.scrollTop = container.scrollHeight;
}

// quick hack: decode JWT payload to get 'sub' (user id)
function getMyUserIdFromToken() {
  if (!accessToken) return null;
  const parts = accessToken.split(".");
  if (parts.length !== 3) return null;
  try {
    const payload = JSON.parse(atob(parts[1]));
    return payload.sub || null;
  } catch (e) {
    return null;
  }
}

async function sendChatMessage() {
  if (!currentChatUserId) {
    alert("Select a chat first (from the Swipe card).");
    return;
  }

  const textArea = document.getElementById("chat_input");
  const text = textArea.value.trim();
  if (!text) return;

  const resp = await fetch(`${API_BASE}/messages`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeader(),
    },
    body: JSON.stringify({
      to_user_id: currentChatUserId,
      text,
    }),
  });
  const data = await resp.json();
  console.log("send message", data);
  if (!resp.ok) {
    alert(data.detail || "Error sending message");
    return;
  }

  textArea.value = "";
  loadChatThread();
}

async function getChatHelperForCurrent() {
  if (!currentChatUserId) {
    alert("Select a chat first.");
    return;
  }

  const resp = await fetch(
    `${API_BASE}/ai/chat-helper/${currentChatUserId}`,
    {
      headers: {
        ...authHeader(),
      },
    }
  );
  const data = await resp.json();
  console.log("chat helper", data);

  if (!resp.ok) {
    alert(data.detail || "Error getting AI suggestions");
    return;
  }

  document.getElementById("ai_summary").textContent = data.summary || "";

  const ul = document.getElementById("ai_openers");
  ul.innerHTML = "";
  (data.openers || []).forEach((line) => {
    const li = document.createElement("li");
    li.textContent = line;
    li.className = "ai-suggestion";
    li.onclick = () => {
      const input = document.getElementById("chat_input");
      input.value = line;
      input.focus();
    };
    ul.appendChild(li);
  });
}
